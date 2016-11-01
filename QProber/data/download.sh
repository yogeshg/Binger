#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR
wget http://www.cs.columbia.edu/~gravano/cs6111/Proj2/data/root.txt
wget http://www.cs.columbia.edu/~gravano/cs6111/Proj2/data/health.txt
wget http://www.cs.columbia.edu/~gravano/cs6111/Proj2/data/computers.txt
wget http://www.cs.columbia.edu/~gravano/cs6111/Proj2/data/sports.txt
cd -
