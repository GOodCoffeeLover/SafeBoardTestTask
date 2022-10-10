#!/usr/bin/env python
import json
import os
import re
import shutil
import time

import yaml
import datetime
# import cerberus

# def validate(obj):
#     v = cerberus.Validator(schema)
#     res =  v.validate(obj)
#     # print(json.dumps(v.document_error_tree['type'], indent=2))
#     print(v.errors)
#     return

# split rules into two rule groups
def split_rules(rules):
    dir_rules, file_rules = [], []
    for rule in rules:
        if rule['type'] == 'dir':
            dir_rules.append(rule)
        elif rule['type'] == 'file':
            file_rules.append(rule)

    return dir_rules, file_rules

# check what type of assembly dir
def is_release(dir_name):
    versions = dir_name.split('.')
    if len(versions) != 4:
        return None
    if int(versions[2]) / 10 > 0:
        return False
    else:
        return True

#check if assembly_type is target
def check_assembly(assembly_type, file_name):
    return (assembly_type == 'release') == is_release(file_name)

#check if file_path file older then days days
def older(days, file_path):
    if days is None:
        return True
    now = datetime.datetime.fromtimestamp(time.time())
    then = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
    delta = datetime.timedelta(days=days)
    return then + delta < now

def match_regex(regexp, file_path):
    res = re.match(regexp, file_name)
    return res is not None


# function of iterating over files and applying deleting rules
def iterate_over_files(path, rules):
    if path[-1] != '/':
        path += "/"

    files = os.listdir(path)

    for file in files:
        if os.path.isdir(path + file):
            iterate_over_files(path+file, rules)
        else:
            for rule in rules:
                if match_regex(rule['mask'], path+file) and older(rule.get('older_in_days'), path+file):
                    print(f'delete {path + file}')
                    # os.remove(path+file)
                    break

# function of iterating over dirs and applying deleting rules
def iterate_over_dirs(path, rules):
    if path[-1] != '/':
        path += "/"

    files = os.listdir(path)

    for file in files:
        if os.path.isdir(path + file):
            for rule in rules:

                if (
                        check_assembly(rule["assembly_type"], file)         # check assembly type
                        and older(rule.get("older_in_days"), path + file)   # check if file is old enough
                ):
                    print(f'delete {path+file}')
                    # shutil.rmtree(path+file)
                    break




def main():
    path = ''
    rules = []

    with open("config.yaml") as file:
        yml = yaml.load(file, Loader=yaml.Loader)
        # print(json.dumps(yml, indent=2) )
        path = yml['path']
        rules = yml['rules']

    dir_rules, file_rules = split_rules(rules)
    iterate_over_dirs(path, dir_rules)
    iterate_over_files(path, file_rules)


if __name__ == '__main__':
    main()
