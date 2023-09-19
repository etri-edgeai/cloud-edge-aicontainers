#shard 10

python main.py --config_path ./config/cifar100/fedavg.json --partition_s 10  --device cuda:7 --local_epochs 5

# python main.py --config_path ./config/cifar100/fedavg.json --partition_s 10  --device cuda:7 --local_epochs 1

# python main.py --config_path ./config/cifar100/fedavg.json --partition_s 10  --device cuda:7 --local_epochs 10

#shard 50

python main.py --config_path ./config/cifar100/fedavg.json --partition_s 50 --device cuda:7 --local_epochs 5

# python main.py --config_path ./config/cifar100/fedavg.json --partition_s 50 --device cuda:7 --local_epochs 1

# python main.py --config_path ./config/cifar100/fedavg.json --partition_s 50 --device cuda:7 --local_epochs 10


#shard 100

python main.py --config_path ./config/cifar100/fedavg.json --partition_s 100 --device cuda:7 --local_epochs 5

# python main.py --config_path ./config/cifar100/fedavg.json --partition_s 100 --device cuda:7 --local_epochs 1

# python main.py --config_path ./config/cifar100/fedavg.json --partition_s 100 --device cuda:7 --local_epochs 10

