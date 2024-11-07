from flask import Flask, request, render_template
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = '/opt/capa/file_TEMP'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capa_analyic', methods=['GET', 'POST'])
def capa_analyic():
    if request.method == 'POST':
        if 'file' not in request.files:
            return '沒有檔案被上傳'
        file = request.files['file']
        if file.filename == '':
            return '沒有選擇檔案'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # 執行指令
        try:
            result = subprocess.check_output(['capa', file_path, '-v'], stderr=subprocess.STDOUT)
            result = result.decode('utf-8')
        except subprocess.CalledProcessError as e:
            result = f'執行指令時出錯: {e.output.decode("utf-8")}'

        return render_template('result.html', result=result)
    return '''
    <h1>上傳檔案以執行 CAPA 分析</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="上傳">
    </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
