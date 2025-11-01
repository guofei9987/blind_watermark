# blind-watermark

基于频域的数字盲水印。

[![PyPI](https://img.shields.io/pypi/v/blind_watermark)](https://pypi.org/project/blind_watermark/)
[![Build Status](https://travis-ci.com/guofei9987/blind_watermark.svg?branch=master)](https://travis-ci.com/guofei9987/blind_watermark)
[![codecov](https://codecov.io/gh/guofei9987/blind_watermark/branch/master/graph/badge.svg)](https://codecov.io/gh/guofei9987/blind_watermark)
[![License](https://img.shields.io/pypi/l/blind_watermark.svg)](https://github.com/guofei9987/blind_watermark/blob/master/LICENSE)
![Python](https://img.shields.io/badge/python->=3.5-green.svg)
![Platform](https://img.shields.io/badge/platform-windows%20|%20linux%20|%20macos-green.svg)

- **Documentation:** [https://BlindWatermark.github.io/blind_watermark/#/en/](https://BlindWatermark.github.io/blind_watermark/#/en/)
- **中文文档:** [https://BlindWatermark.github.io/blind_watermark/#/zh/](https://BlindWatermark.github.io/blind_watermark/#/zh/)

# 快速开始：Web应用

为了方便使用，本项目已集成了一个美观、简洁的Web操作界面。

## 运行方式

### 方式一：通过 Docker 运行 (推荐)
这是最简单、最推荐的运行方式，可以避免本机环境的各种问题。

1.  **启动应用:**
    在项目根目录下，运行以下命令：
    ```bash
    docker-compose up -d
    ```
    Docker将会自动构建镜像并启动服务。

2.  **访问应用:**
    打开浏览器，访问 `http://localhost:5891` 即可开始使用。

3.  **停止应用:**
    在终端中，按 `Ctrl+C`，然后运行以下命令来彻底清理容器：
    ```bash
    docker-compose down
    ```

### 方式二：在本地直接运行

1.  **安装依赖:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **启动服务:**
    ```bash
    python web_app.py
    ```
3.  **访问应用:**
    打开浏览器，访问 `http://localhost:5891`。


# 高级用法 (命令行与库)

## 安装
```bash
pip install blind-watermark
```

## 在命令行中使用
```bash
# 嵌入水印到图片:
blind_watermark --embed --pwd 1234 examples/pic/ori_img.jpeg "watermark text" examples/output/embedded.png

# 从图片中提取水印:
blind_watermark --extract --pwd 1234 --wm_shape 111 examples/output/embedded.png
```

## 在 Python 中作为库使用
更多用法请参考 [examples 目录](/examples/)。

**示例：文本水印**
```python
from blind_watermark import WaterMark

bwm = WaterMark(password_img=1, password_wm=1)
bwm.read_img('pic/ori_img.jpg')
bwm.read_wm('你好，世界', mode='str')
bwm.embed('output/embedded.png')

# 提取时，需要水印的比特长度
len_wm = len(bwm.wm_bit)
print(f"用于提取的水印长度: {len_wm}")

wm_extract = bwm.extract('output/embedded.png', wm_shape=len_wm, mode='str')
print(f"提取出的水印: {wm_extract}")
```

**示例：图片水印**
```python
from blind_watermark import WaterMark

bwm = WaterMark(password_img=1, password_wm=1)
bwm.read_img('pic/ori_img.jpg')
bwm.read_wm('pic/watermark.png', mode='img') # 使用图片作为水印
bwm.embed('output/embedded_with_img_wm.png')

# 提取时，需要水印图片的尺寸 (height, width)
wm_shape = (128, 128) # 示例尺寸
bwm.extract('output/embedded_with_img_wm.png', wm_shape=wm_shape, out_wm_name='output/extracted_wm.png', mode='img')
```
