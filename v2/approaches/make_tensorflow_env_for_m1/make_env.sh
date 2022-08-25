conda create --prefix ./env python=3.8
conda activate ./env
conda install -c apple tensorflow-deps
python -m pip install tensorflow-macos
python -m pip install tensorflow-metal
python -m pip install tensorflow-datasets
conda install jupyter pandas numpy matplotlib scikit-learn
jupyter notebook
