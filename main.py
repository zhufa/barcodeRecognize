# -*- coding:utf-8 -*-
# 不加上条语句中文注释会报错

from flask import Flask, render_template, request
from os import path, mkdir
from werkzeug.utils import secure_filename
import recognize, shutil

app = Flask(__name__)

MAX_FILE_LENGTH = 5*1024*1024  # 最大文件大小
ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'jpg', 'gif', 'bmp'])  # 允许的文件类型


def allowed_file(filename):  # 判断文件类型是否允许
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def homepage():  # 首页
    # 删除上一次的识别文件方法：删除用来存储上传文件的文件夹，在新建该文件夹
    shutil.rmtree('static/upload/')
    mkdir('static/upload/')
    return render_template('homepage.html')


@app.route('/result',methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        f = request.files["upload_file"]
        f_len = request.content_length  # 获取文件大小
        if not f:
            return render_template('result.html', errortype=u'错误：文件不存在')
        elif not allowed_file(f.filename):
            return render_template('result.html', errortype=u'错误：文件类型不允许，仅支持png/jpeg/gif/bmp/jpg')
        elif f_len>MAX_FILE_LENGTH:
            return render_template('result.html', errortype=u'错误：文件大于5M')
        else:
            base_path = path.abspath(path.dirname(__file__))
            upload_path = path.join(base_path,'static/upload/')
            file_name = upload_path + f.filename
            f.save(file_name)
            r = recognize.recon(file_name)  # 识别结果传回给r
            # if path.exists(file_name): # 识别完立即删除文件
                # remove(file_name)
            if not r:
                return render_template('result.html',errortype=u'无法识别或条码二维码类型不支持')
            return render_template('result.html', title=u'识别结果', img_src=f.filename, codetype=r[0][1],
                                   result=unicode(r[0][0], "utf-8"))  # 中文转unicode
    return render_template('homepage.html')


if __name__ == '__main__':
    app.run(host='172.28.31.149', debug=True)
