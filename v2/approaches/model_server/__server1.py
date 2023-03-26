from flask import Flask, request, jsonify
import os
import shutil
import uuid

app = Flask(__name__)

# 경로 설정
MODEL_DIR = "models/"

# 모델 업로드
@app.route('/models/upload', methods=['POST'])
def upload_model():
    model_file = request.files['model']
    model_name = request.form['name']
    model_version = request.form['version']

    # 모델 디렉토리 생성
    model_dir = os.path.join(MODEL_DIR, model_name, model_version)
    os.makedirs(model_dir, exist_ok=True)

    # 모델 저장
    model_file.save(os.path.join(model_dir, 'model.tar.gz'))

    return jsonify({'message': 'Model uploaded successfully.'})

# 모델 다운로드
@app.route('/models/download', methods=['POST'])
def download_model():
    model_name = request.form['name']
    model_version = request.form['version']

    # 모델 디렉토리 확인
    model_dir = os.path.join(MODEL_DIR, model_name, model_version)
    if not os.path.exists(model_dir):
        return jsonify({'message': 'Model not found.'}), 404

    # 모델 압축
    model_uuid = str(uuid.uuid4())
    shutil.make_archive(model_uuid, 'gztar', model_dir)

    return jsonify({'model': model_uuid + '.tar.gz'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
