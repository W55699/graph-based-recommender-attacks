#! /bin/bash
pushd "$(dirname "$0")"
wget http://files.grouplens.org/datasets/movielens/ml-1m.zip
unzip ml-1m.zip
rm ml-1m.zip

echo 'parsing movielens data'
python parse_movielens.py 1m
mv movielens_1m.dat* ../
rm -r ml-1m

echo 'Finished loading movielens 1m!'
popd
