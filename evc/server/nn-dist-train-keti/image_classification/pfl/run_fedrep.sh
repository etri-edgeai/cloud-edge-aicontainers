#LDA
python main_fedrep.py --fl_alg fedrep --dataset cifar100 --lr_decay 0.1 --model mobile --num_classes 100 --hetero_option lda --alpha 0.1 --epochs 320 --lr 0.1 --num_users 100 --frac 0.1 --local_ep 5 --local_bs 50 --gpu 2

python main_fedrep.py --fl_alg fedrep --dataset cifar100 --lr_decay 0.1 --model mobile --num_classes 100 --hetero_option lda --alpha 0.5 --epochs 320 --lr 0.1 --num_users 100 --frac 0.1 --local_ep 5 --local_bs 50 --gpu 2

python main_fedrep.py --fl_alg fedrep --dataset cifar100 --lr_decay 0.1 --model mobile --num_classes 100 --hetero_option lda --alpha 1.0 --epochs 320 --lr 0.1 --num_users 100 --frac 0.1 --local_ep 5 --local_bs 50 --gpu 2


#Shard

python main_fedrep.py --fl_alg fedrep --dataset cifar100 --lr_decay 0.1 --model mobile --num_classes 100 --hetero_option shard --shard_per_user 10 --epochs 320 --lr 0.1 --num_users 100 --frac 0.1 --local_ep 5 --local_bs 50 --gpu 3

python main_fedrep.py --fl_alg fedrep --dataset cifar100 --lr_decay 0.1 --model mobile --num_classes 100 --hetero_option shard --shard_per_user 50 --epochs 320 --lr 0.1 --num_users 100 --frac 0.1 --local_ep 5 --local_bs 50 --gpu 3

python main_fedrep.py --fl_alg fedrep --dataset cifar100 --lr_decay 0.1 --model mobile --num_classes 100 --hetero_option shard --shard_per_user 100 --epochs 320 --lr 0.1 --num_users 100 --frac 0.1 --local_ep 5 --local_bs 50 --gpu 3