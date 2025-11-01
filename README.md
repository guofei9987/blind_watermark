# blind-watermark
Blind watermark based on DWT-DCT-SVD.

[![PyPI](https://img.shields.io/pypi/v/blind_watermark)](https://pypi.org/project/blind_watermark/)
[![Build Status](https://travis-ci.com/guofei9987/blind_watermark.svg?branch=master)](https://travis-ci.com/guofei9987/blind_watermark)
[![codecov](https://codecov.io/gh/guofei9987/blind_watermark/branch/master/graph/badge.svg)](https://codecov.io/gh/guofei9987/blind_watermark)
[![License](https://img.shields.io/pypi/l/blind_watermark.svg)](https://github.com/guofei9987/blind_watermark/blob/master/LICENSE)
![Python](https://img.shields.io/badge/python->=3.5-green.svg)
![Platform](https://img.shields.io/badge/platform-windows%20|%20linux%20|%20macos-green.svg)

- **Documentation:** [https://BlindWatermark.github.io/blind_watermark/#/en/](https://BlindWatermark.github.io/blind_watermark/#/en/)
- **中文文档:** [https://BlindWatermark.github.io/blind_watermark/#/zh/](https://BlindWatermark.github.io/blind_watermark/#/zh/)

# Quick Start: Web App

For ease of use, this project includes a modern web interface.

## How to Run

### Option 1: Run with Docker (Recommended)
This is the simplest and recommended method to avoid local environment issues.

1.  **Start the Application:**
    In the project root directory, run the following command:
    ```bash
    docker-compose up -d
    ```

2.  **Access the Application:**
    Open your browser and navigate to `http://localhost:5891`.

3.  **Stop the Application:**
    In the terminal, press `Ctrl+C`, then run the following command to clean up the containers:
    ```bash
    docker-compose down
    ```

### Option 2: Run Natively

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Start the Server:**
    ```bash
    python web_app.py
    ```

3.  **Access the Application:**
    Open your browser and navigate to `http://localhost:5891`.


# Advanced Usage (CLI & Library)

## Installation
```bash
pip install blind-watermark
```

## Usage as a CLI Tool
```bash
# Embed watermark into an image:
blind_watermark --embed --pwd 1234 examples/pic/ori_img.jpeg "watermark text" examples/output/embedded.png

# Extract watermark from an image:
blind_watermark --extract --pwd 1234 --wm_shape 111 examples/output/embedded.png
```

## Usage as a Python Library
See the [examples directory](/examples/) for more details.

**Example: Text Watermark**
```python
from blind_watermark import WaterMark

bwm = WaterMark(password_img=1, password_wm=1)
bwm.read_img('pic/ori_img.jpg')
bwm.read_wm('Hello World', mode='str')
bwm.embed('output/embedded.png')

# To extract, you need the length of the watermark bit string
len_wm = len(bwm.wm_bit)
print(f"Watermark length to use for extraction: {len_wm}")

wm_extract = bwm.extract('output/embedded.png', wm_shape=len_wm, mode='str')
print(f"Extracted watermark: {wm_extract}")
```

**Example: Image Watermark**
```python
from blind_watermark import WaterMark

bwm = WaterMark(password_img=1, password_wm=1)
bwm.read_img('pic/ori_img.jpg')
bwm.read_wm('pic/watermark.png', mode='img') # Use a watermark image
bwm.embed('output/embedded_with_img_wm.png')

# To extract, you need the shape of the watermark image (height, width)
wm_shape = (128, 128) # Example shape
bwm.extract('output/embedded_with_img_wm.png', wm_shape=wm_shape, out_wm_name='output/extracted_wm.png', mode='img')
```
