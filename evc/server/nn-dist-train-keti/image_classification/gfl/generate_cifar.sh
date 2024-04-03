mkdir data

cd data

mkdir cifar10
mkdir cifar100

cd cifar10

wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
tar -xzf cifar-10-python.tar.gz

cd ../cifar100

wget https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz
tar -xzf cifar-100-python.tar.gz
