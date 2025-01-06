from flask import Flask, request, render_template, redirect, url_for
import subprocess
import os
import tempfile

app = Flask(__name__)
# Change the upload folder to a temporary directory
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'scanfiletemp')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            # 使用capa分析文件
            result = subprocess.run(['capa', file_path], capture_output=True, text=True)
            return render_template('result.html', result=result.stdout)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
