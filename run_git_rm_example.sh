 find . -name .ipynb_checkpoints -print0 | xargs -0 git rm -rf --ignore-unmatch
