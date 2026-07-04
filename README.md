# blind-watermark

Blind watermark by frequency in Python

[![PyPI](https://img.shields.io/pypi/v/blind_watermark)](https://pypi.org/project/blind_watermark/)
[![Build Status](https://travis-ci.com/guofei9987/blind_watermark.svg?branch=master)](https://travis-ci.com/guofei9987/blind_watermark)
[![codecov](https://codecov.io/gh/guofei9987/blind_watermark/branch/master/graph/badge.svg)](https://codecov.io/gh/guofei9987/blind_watermark)
[![License](https://img.shields.io/pypi/l/blind_watermark.svg)](https://github.com/guofei9987/blind_watermark/blob/master/LICENSE)
![Python](https://img.shields.io/badge/python->=3.5-green.svg)
![Platform](https://img.shields.io/badge/platform-windows%20|%20linux%20|%20macos-green.svg)
[![stars](https://img.shields.io/github/stars/guofei9987/blind_watermark.svg?style=social)](https://github.com/guofei9987/blind_watermark/)
[![fork](https://img.shields.io/github/forks/guofei9987/blind_watermark?style=social)](https://github.com/guofei9987/blind_watermark/fork)
[![Downloads](https://pepy.tech/badge/blind-watermark)](https://pepy.tech/project/blind-watermark)
[![Discussions](https://img.shields.io/badge/discussions-green.svg)](https://github.com/guofei9987/blind_watermark/discussions)


- **Documentation:** [https://BlindWatermark.github.io/blind_watermark/#/en/](https://BlindWatermark.github.io/blind_watermark/#/en/)
- **中文文档：** [https://BlindWatermark.github.io/blind_watermark/#/zh/](https://BlindWatermark.github.io/blind_watermark/#/zh/)
- **中文 readme：** [README_cn.md](README_cn.md)
- **Source code:** [https://github.com/guofei9987/blind_watermark](https://github.com/guofei9987/blind_watermark)


# install
```bash
pip install blind-watermark
```

or install the latest version:
```bach
git clone git@github.com:guofei9987/blind_watermark.git
cd blind_watermark
pip install .
```

# How to use


## Use in bash

The CLI tool now supports subcommands and features automatic password generation alongside automatic metadata file (.json) extraction.

```bash
# embed watermark into image:
bwm embed examples/pic/ori_img.jpeg "watermark text" examples/output/embedded.png
# A .json metadata file will be automatically generated alongside your output_image holding your password and wm_shape.

# extract watermark from image:
bwm extract examples/output/embedded.png
# It automatically fetches the password and wm_shape from the corresponding .json file!
```

*If you prefer to assign passwords and paths manually, use the `-p` and `-m` flags:*
```bash
# Embed with manual password and custom metadata path:
bwm embed examples/pic/ori_img.jpeg "watermark text" examples/output/embedded.png -p 1234 -m meta/my_metadata.json

# Extract by specifying the metadata path:
bwm extract examples/output/embedded.png -m meta/my_metadata.json
```

## Use in python
see [examples](/examples/example_str.py)


original image + watermark = embedded image

![origin_image](docs/原图.jpeg) + '@guofei9987 开源万岁！' = ![打上水印的图](docs/打上水印的图.jpg)

embed:
```python
from blind_watermark import WaterMark

bwm1 = WaterMark(password_img=1, password_wm=1)
bwm1.read_img('pic/ori_img.jpg')
wm = '@guofei9987 开源万岁！'
bwm1.read_wm(wm, mode='str')
bwm1.embed('output/embedded.png')
len_wm = len(bwm1.wm_bit)
print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))
```

extract
```python
bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract('output/embedded.png', wm_shape=len_wm, mode='str')
print(wm_extract)
```
Output:
>@guofei9987 开源万岁！


## Attack robust
|Attack Type|Attacked image|Extracted watermark|
|--|--|--|
|Rotate attack 45 degree|![旋转攻击](docs/旋转攻击.jpg)|'@guofei9987 开源万岁！'|
|Random crop attack|![截屏攻击](docs/截屏攻击2_还原.jpg)|'@guofei9987 开源万岁！'|
|Mask attack| ![多遮挡攻击](docs/多遮挡攻击.jpg) |'@guofei9987 开源万岁！'|
|Horizontal crop attack|![横向裁剪攻击](docs/横向裁剪攻击_填补.jpg)|'@guofei9987 开源万岁！'|
|Vertical crop attack|![纵向裁剪攻击](docs/纵向裁剪攻击_填补.jpg)|'@guofei9987 开源万岁！'|
|Resize attack|![缩放攻击](docs/缩放攻击.jpg)|'@guofei9987 开源万岁！'|
|Salt-and-pepper noise attack|![椒盐攻击](docs/椒盐攻击.jpg)|'@guofei9987 开源万岁！'|
|Brightness attack|![亮度攻击](docs/亮度攻击.jpg)|'@guofei9987 开源万岁！'|


## Embed images

see [examples](/examples/example_str.py)

embed
```python
from blind_watermark import WaterMark

bwm1 = WaterMark(password_wm=1, password_img=1)
# read original image
bwm1.read_img('pic/ori_img.jpg')
# read watermark
bwm1.read_wm('pic/watermark.png')
# embed
bwm1.embed('output/embedded.png')
```

extract
```python
bwm1 = WaterMark(password_wm=1, password_img=1)
# notice that wm_shape is necessary
bwm1.extract(filename='output/embedded.png', wm_shape=(128, 128), out_wm_name='output/extracted.png', )
```

|Attack Type|Attacked image|Extracted watermark|
|--|--|--|
|Rotate attack 45 degree|![旋转攻击](docs/旋转攻击.jpg)|![](docs/旋转攻击_提取水印.png)|
|Random crop attack|![截屏攻击](docs/截屏攻击2_还原.jpg)|![](docs/旋转攻击_提取水印.png)|
|Mask attack| ![多遮挡攻击](docs/多遮挡攻击.jpg) |![多遮挡_提取水印](docs/多遮挡攻击_提取水印.png)|

## Embed bits

see [examples](/examples/example_bit.py)

```python
from blind_watermark import WaterMark

bwm1 = WaterMark(password_img=1, password_wm=1)
bwm1.read_img('pic/ori_img.jpg')
bwm1.read_wm([True, False, True, True, True, False], mode='bit')
bwm1.embed('output/embedded.png')
```
extract:
```python
bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract('output/embedded.png', wm_shape=6, mode='bit')
print(wm_extract)
```


# Multiple processes
```python
WaterMark(..., processes=None)
```
- `processes`: An integer to specify the number of threads. The default is `None`, which means using all threads


# Related project
- text_blind_watermark: [https://github.com/guofei9987/text_blind_watermark](https://github.com/guofei9987/text_blind_watermark)
- HideInfo：[https://github.com/guofei9987/HideInfo](https://github.com/guofei9987/HideInfo)
