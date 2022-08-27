# by JPark @ 2022

query=$1
if [ x$1 == x ]; then
    query="wandb" 
fi

echo ----------------------------------------
echo e.g. sh run_query.sh \"wandb\"
echo ----------------------------------------
echo ". Query = " $query
echo ----------------------------------------
echo ". Results = " 

grep -R "$query" --include="*.py" ./v2

echo ----------------------------------------

