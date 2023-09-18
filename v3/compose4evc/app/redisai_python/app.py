import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from ml2rt import save_sklearn, load_model
from redisai import Client

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List

## FastAPI & CORS (Cross-Origin Resource Sharing)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RedisAI Client
redisai_client = Client(host='0.0.0.0', port=6379)
#redisai_client = redis.Redis(host='0.0.0.0', port=6379)

# model output path
MODEL_OUTPUT_PATH = './_output/iris.onnx'

@app.get('/train')
async def train():
    # 1. Prepare the train and test data
    iris = load_iris()
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    # 2. Train the model - using logistic regression classifier
    model = LogisticRegression(max_iter=5000)
    model.fit(X_train, y_train)

    # 3. Convert sklearn model to ONNX model
    dummy = X_train[0].astype(np.float32)
    save_sklearn(model, MODEL_OUTPUT_PATH, prototype=dummy) # save model to MODEL_OUTPUT_PATH
    
    # 4. Set ONNX model to RedisAI
    model_name = 'iris-clf'
    model = load_model(MODEL_OUTPUT_PATH)
    redisai_client.modelset('iris-clf', 'onnx', 'cpu', model)
    print(f">> '{model_name}'' model is saved to RedisAI 🟢.")


@app.get('/inference') 
async def inference(model: str, sepal_length: float, sepal_width: float, petal_length: float, petal_width: float):
    # 1. Check Model in RedisAI
    try:
        model_meta = redisai_client.modelget(f'{model}', meta_only=True)
        print(f">> '{model}'' model is active on RedisAI 🟢.")
        print(model_meta)
    except:
        model_meta = None
        print(f">>{model}' model is not active on RedisAI. 🔴")
        return JSONResponse({'status':'fail', 'class':None})

    if model_meta:
        # 2. Set input tensor
        input_value = [sepal_length, sepal_width, petal_length, petal_width]
        intput_tensor = np.array(input_value).astype(np.float32)
        redisai_client.tensorset(f'{model}:in', intput_tensor)

        # 3. Predict
        redisai_client.modelexecute(model, inputs=[f'{model}:in'], outputs=[f'{model}:out1', f'{model}:out2'])

        # 4. Get result
        out = redisai_client.tensorget(f'{model}:out1')[0]
        labels = ['setosa', 'versicolor', 'virginica']
        print(labels[out])

        return JSONResponse({'status':'success', 'pred':labels[out]})


#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port="8011")
