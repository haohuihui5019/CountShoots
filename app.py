import argparse
import json
import os
import shutil

import imageio
from PIL import Image
from flask import render_template, jsonify, url_for
from flask import request, Flask
import model
import time
import predict
from yolo import YOLO
from gevent import pywsgi

app = Flask(__name__)


@app.route('/get_drawedImage', methods=['POST'])
def anyname_you_like():
    startTime = time.time()
    received_file = request.files['input_image']
    imageFileName = received_file.filename
    if received_file:
        # 保存接收的图片到指定文件夹
        received_dirPath = 'static'
        if not os.path.isdir(received_dirPath):
            os.makedirs(received_dirPath)
        imageFilePath = os.path.join(received_dirPath, imageFileName)
        received_file.save(imageFilePath)
        print('接收图片文件保存到此路径：%s' % imageFilePath)
        usedTime = time.time() - startTime
        print('接收图片并保存，总共耗时%.2f秒' % usedTime)
        cut_path = 'static/cut'
        path = 'static/cut'
        # for file in os.listdir(path):
        # os.remove(os.path.join(path, file))
        shutil.rmtree('static/cut')
        os.mkdir('static/cut')
        drawed_image = predict.predict(imageFilePath, cut_path)
        # 把目标检测结果图保存在服务端指定路径，返回指定路径对应的图片经过base64编码后的字符串
        drawed_imageFileName = 'drawed_' + os.path.splitext(imageFileName)[0] + '.jpg'
        drawed_imageFilePath = os.path.join(received_dirPath, drawed_imageFileName)
        drawed_image.save(drawed_imageFilePath)
        image_source_url = url_for('static', filename=drawed_imageFileName)
        return jsonify(src=image_source_url)


@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return environ


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/images', methods=['POST'])
def get_images():
    path = 'static/cut'  # 文件夹路径
    count = 0
    an = []
    an.clear()
    bn = []
    for file in os.listdir(path):  # file 表示的是文件名
        print(file)
        an.append(file)
        bn.append(model.vis(path + '/' + file))
        count = count + 1
    print(count)
    images = []
    temp = 0
    for i in range(count):
        c = {}
        a = '/static/cut/' + an[temp]
        b = "New Shoots: " + bn[temp]
        c['img'] = a
        c['description'] = b
        print(c)
        images.append(c)
        # images[temp] = {'img': a, 'description': b}
        temp = temp + 1
    response = jsonify({'data': {'list': images}})
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Expires'] = '-1'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Etag'] = '0'
    return response


@app.route('/about')
def aa():
    return render_template('about.html')


@app.route('/album')
def bb():
    return render_template('album.html')


@app.route('/blog')
def cc():
    return render_template('blog.html')


@app.route('/home')
def dd():
    return render_template('home.html')


@app.route('/join')
def ee():
    return render_template('join.html')


if __name__ == '__main__':
    app.run()
