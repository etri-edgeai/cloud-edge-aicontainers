import os

UPLOAD_FOLDER = "./upload_folder"
MODEL_FOLDER = "./model_folder"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(MODEL_FOLDER):
    os.makedirs(MODEL_FOLDER)
