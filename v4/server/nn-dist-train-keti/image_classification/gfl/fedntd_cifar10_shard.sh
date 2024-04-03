#shard new

python main.py --config_path ./config/cifar10/fedntd.json --partition_method sharding_new --partition_s 2 --device cuda:3 --local_epochs 5 

python main.py --config_path ./config/cifar10/fedntd.json --partition_method sharding_new --partition_s 2 --device cuda:3 --local_epochs 10 

python main.py --config_path ./config/cifar10/fedntd.json --partition_method sharding_new --partition_s 2 --device cuda:3 --local_epochs 15 



#shard 2

python main.py --config_path ./config/cifar10/fedntd.json --partition_method sharding --partition_s 2 --device cuda:3 --local_epochs 5 

python main.py --config_path ./config/cifar10/fedntd.json --partition_method sharding --partition_s 2 --device cuda:3 --local_epochs 10 

python main.py --config_path ./config/cifar10/fedntd.json --partition_method sharding --partition_s 2 --device cuda:3 --local_epochs 15 



#shard 3

python main.py --config_path ./config/cifar10/fedntd.json --partition_method sharding --partition_s 3 --device cuda:3 --local_epochs 5 

python main.py --config_path ./config/cifar10/fedntd.json --partition_method sharding --partition_s 3 --device cuda:3 --local_epochs 10 

python main.py --config_path ./config/cifar10/fedntd.json --partition_method sharding --partition_s 3 --device cuda:3 --local_epochs 15 


#shard 5

python main.py --config_path ./config/cifar10/fedntd.json --partition_method sharding --partition_s 5 --device cuda:3 --local_epochs 5 

python main.py --config_path ./config/cifar10/fedntd.json --partition_method sharding --partition_s 5 --device cuda:3 --local_epochs 10 

python main.py --config_path ./config/cifar10/fedntd.json --partition_method sharding --partition_s 5 --device cuda:3 --local_epochs 15 


#shard 10

python main.py --config_path ./config/cifar10/fedntd.json --partition_method sharding --partition_s 10 --device cuda:3 --local_epochs 5 

python main.py --config_path ./config/cifar10/fedntd.json --partition_method sharding --partition_s 10 --device cuda:3 --local_epochs 10 

python main.py --config_path ./config/cifar10/fedntd.json --partition_method sharding --partition_s 10 --device cuda:3 --local_epochs 15 



#i.i.d

python main.py --config_path ./config/cifar10/fedntd.json --partition_method iid --device cuda:3 --local_epochs 5 

python main.py --config_path ./config/cifar10/fedntd.json --partition_method iid --device cuda:3 --local_epochs 10 

python main.py --config_path ./config/cifar10/fedntd.json --partition_method iid --device cuda:3 --local_epochs 15 
