#alpha 0.1

python main.py --config_path ./config/cifar100/fedexp.json --partition_method lda --partition_alpha 0.1  --device cuda:6 --local_epochs 5

python main.py --config_path ./config/cifar100/fedexp.json --partition_method lda --partition_alpha 0.1  --device cuda:6 --local_epochs 1

python main.py --config_path ./config/cifar100/fedexp.json --partition_method lda --partition_alpha 0.1  --device cuda:6 --local_epochs 10



#alpha 0.3

python main.py --config_path ./config/cifar100/fedexp.json --partition_method lda --partition_alpha 0.3  --device cuda:6 --local_epochs 5

python main.py --config_path ./config/cifar100/fedexp.json --partition_method lda --partition_alpha 0.3  --device cuda:6 --local_epochs 1

python main.py --config_path ./config/cifar100/fedexp.json --partition_method lda --partition_alpha 0.3  --device cuda:6 --local_epochs 10


#alpha 0.5

python main.py --config_path ./config/cifar100/fedexp.json --partition_method lda --partition_alpha 0.5  --device cuda:6 --local_epochs 5

python main.py --config_path ./config/cifar100/fedexp.json --partition_method lda --partition_alpha 0.5  --device cuda:6 --local_epochs 1

python main.py --config_path ./config/cifar100/fedexp.json --partition_method lda --partition_alpha 0.5  --device cuda:6 --local_epochs 10


#alpha 1.0

python main.py --config_path ./config/cifar100/fedexp.json --partition_method lda --partition_alpha 1.0  --device cuda:6 --local_epochs 5

python main.py --config_path ./config/cifar100/fedexp.json --partition_method lda --partition_alpha 1.0  --device cuda:6 --local_epochs 1

python main.py --config_path ./config/cifar100/fedexp.json --partition_method lda --partition_alpha 1.0  --device cuda:6 --local_epochs 10



