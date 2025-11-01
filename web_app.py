
import os
import cv2
from flask import Flask, request, render_template, send_from_directory
from blind_watermark import WaterMark

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/embed', methods=['POST'])
def embed():
    if 'file' not in request.files or not request.files['file'].filename:
        return render_template('index.html', error="请选择一个图片文件。")

    file = request.files['file']
    password = request.form.get('password', '123456')
    wm_type = request.form.get('wm_type', 'text')

    password_int = abs(hash(password)) % (2**32)

    # Save the cover image
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    bwm = WaterMark(password_img=password_int, password_wm=password_int)
    bwm.read_img(filename)

    wm_shape_str = ""

    try:
        if wm_type == 'text':
            wm_content = request.form.get('wm_content')
            if not wm_content:
                return render_template('index.html', error="请输入水印文字。")
            bwm.read_wm(wm_content, mode='str')
            wm_shape_str = str(len(bwm.wm_bit))
        elif wm_type == 'image':
            if 'wm_file' not in request.files or not request.files['wm_file'].filename:
                return render_template('index.html', error="请选择一个水印图片。")
            wm_file = request.files['wm_file']
            wm_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'wm_' + wm_file.filename)
            wm_file.save(wm_filename)
            bwm.read_wm(wm_filename, mode='img')
            # Get shape from the actual watermark image
            wm_img = cv2.imread(wm_filename, cv2.IMREAD_GRAYSCALE)
            if wm_img is None:
                 return render_template('index.html', error="无法读取水印图片文件。")
            wm_shape_str = f"{wm_img.shape[0]},{wm_img.shape[1]}"

        # Embed the watermark
        embedded_filename = 'embedded_' + file.filename
        embedded_filepath = os.path.join(app.config['UPLOAD_FOLDER'], embedded_filename)
        bwm.embed(embedded_filepath)

    except AssertionError as e:
        return render_template('index.html', error=f"嵌入失败：{e}")
    except Exception as e:
        return render_template('index.html', error=f"发生未知错误: {e}")

    return render_template('index.html',
                           result='embedded',
                           wm_shape=wm_shape_str,
                           download_url=f'/uploads/{embedded_filename}')

@app.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files or not request.files['file'].filename:
        return render_template('index.html', error="请选择一个带水印的图片文件。")

    file = request.files['file']
    password = request.form.get('password', '123456')
    wm_shape_str = request.form.get('wm_shape', '')

    if not wm_shape_str:
        return render_template('index.html', error="请输入水印形状。")

    password_int = abs(hash(password)) % (2**32)
    bwm = WaterMark(password_img=password_int, password_wm=password_int)

    # Save the watermarked image
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    wm_content = None
    wm_is_image = False
    try:
        if ',' in wm_shape_str:
            # Image watermark
            shape = tuple(map(int, wm_shape_str.split(',')))
            mode = 'img'
            wm_is_image = True
            out_wm_name = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_' + file.filename)
            bwm.extract(filename, wm_shape=shape, mode=mode, out_wm_name=out_wm_name)
            wm_content = f'/uploads/{os.path.basename(out_wm_name)}'
        else:
            # Text watermark
            shape = int(wm_shape_str)
            mode = 'str'
            wm_is_image = False
            wm_content = bwm.extract(filename, wm_shape=shape, mode=mode)

    except Exception as e:
        return render_template('index.html', error=f"提取失败，请检查密码或水印形状是否正确。错误信息: {e}")

    return render_template('index.html',
                           result='extracted',
                           wm_content=wm_content,
                           wm_is_image=wm_is_image)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5891)
