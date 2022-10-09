set -e
mkdir   -p  ./assembles

cd ./assembles

mkdir -p ./4.0.0.16/install ./4.0.0.16/tests ./4.0.0.16/debug ./4.0.0.16/report
touch ./4.0.0.16/install/file.rpm ./4.0.0.16/tests/tests.tar.gz ./4.0.0.16/debug/debug.rpm  ./4.0.0.16/report/report.xml

cp  -r ./4.0.0.16  ./4.0.0.15
cp  -r ./4.0.0.16  ./4.0.55555.3832952
cp  -r ./4.0.0.16  ./4.0.0.167
cp  -r ./4.0.0.16  ./4.0.55555.3832954

cd ..
