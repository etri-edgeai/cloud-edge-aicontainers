#LDA

python main_local.py --fl_alg local --dataset cifar100 --lr_decay 0.1 --model mobile --num_classes 100 --hetero_option lda --alpha 0.1 --epochs 160 --lr 0.1 --num_users 100 --local_bs 50 --results_save local --gpu 4

python main_local.py --fl_alg local --dataset cifar100 --lr_decay 0.1 --model mobile --num_classes 100 --hetero_option lda --alpha 0.5 --epochs 160 --lr 0.1 --num_users 100 --local_bs 50 --results_save local --gpu 4

python main_local.py --fl_alg local --dataset cifar100 --lr_decay 0.1 --model mobile --num_classes 100 --hetero_option lda --alpha 1.0 --epochs 160 --lr 0.1 --num_users 100 --local_bs 50 --results_save local --gpu 4



#Shard

python main_local.py --fl_alg local --dataset cifar100 --lr_decay 0.1 --model mobile --num_classes 100 --hetero_option shard --shard_per_user 10 --epochs 160 --lr 0.1 --num_users 100 --local_bs 50 --results_save local --gpu 4

python main_local.py --fl_alg local --dataset cifar100 --lr_decay 0.1 --model mobile --num_classes 100 --hetero_option shard --shard_per_user 50 --epochs 160 --lr 0.1 --num_users 100 --local_bs 50 --results_save local --gpu 4

python main_local.py --fl_alg local --dataset cifar100 --lr_decay 0.1 --model mobile --num_classes 100 --hetero_option shard --shard_per_user 100 --epochs 160 --lr 0.1 --num_users 100 --local_bs 50 --results_save local --gpu 4


