DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR

wget "www.columbia.edu/~yg2482/static/tFinal.csv.gz"
gunzip tFinal.csv.gz

cd -

