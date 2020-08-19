# blind-watermark

Blind watermark based on wavelet transform.


[![PyPI](https://img.shields.io/pypi/v/blind_watermark)](https://pypi.org/project/blind_watermark/)
[![Build Status](https://travis-ci.com/guofei9987/blind_watermark.svg?branch=master)](https://travis-ci.com/guofei9987/blind_watermark)
[![codecov](https://codecov.io/gh/guofei9987/blind_watermark/branch/master/graph/badge.svg)](https://codecov.io/gh/guofei9987/blind_watermark)
[![License](https://img.shields.io/pypi/l/blind_watermark.svg)](https://github.com/guofei9987/blind_watermark/blob/master/LICENSE)
![Python](https://img.shields.io/badge/python->=3.5-green.svg)
![Platform](https://img.shields.io/badge/platform-windows%20|%20linux%20|%20macos-green.svg)
[![Downloads](https://pepy.tech/badge/blind-watermark)](https://pepy.tech/project/blind-watermark)
[![Join the chat at https://gitter.im/guofei9987/blind_watermark](https://badges.gitter.im/guofei9987/blind_watermark.svg)](https://gitter.im/guofei9987/blind_watermark?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


- **Documentation:** [https://BlindWatermark.github.io/blind_watermark/#/en/](https://BlindWatermark.github.io/blind_watermark/#/en/)
- **文档：** [https://BlindWatermark.github.io/blind_watermark/#/zh/](https://BlindWatermark.github.io/blind_watermark/#/zh/)  
- **Source code:** [https://github.com/guofei9987/blind_watermark](https://github.com/guofei9987/blind_watermark)


# install
```bash
pip install blind-watermark
```

For the current developer version:
```bach
git clone git@github.com:guofei9987/blind_watermark.git
cd blind_watermark
pip install .
```

## How to use

How to embed watermark:
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


How to extract watermark
```python
bwm1 = WaterMark(password_wm=1, password_img=1)
# notice that wm_shape is necessary
bwm1.extract(filename='output/embedded.png', wm_shape=(128, 128), out_wm_name='output/extracted.png', )
```

## demos:

|origin image|watermark|
|--|--|
|![origin_image](https://blindwatermark.github.io/blind_watermark/原图.jpg)|![watermark](https://blindwatermark.github.io/blind_watermark/水印.png)|

|image embedded with watermark|extracted watermark|
|--|--|
|![origin_image](https://blindwatermark.github.io/blind_watermark/打上水印的图.jpg)|![watermark](https://blindwatermark.github.io/blind_watermark/解出的水印.png)|


### Attack on the embedded image


|attack method|image after attack|extracted watermark|
|--|--|--|
|Rotate 45 Degrees<br>[旋转攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/旋转攻击.py)|![旋转攻击](https://blindwatermark.github.io/blind_watermark/旋转攻击.jpg)|![](https://blindwatermark.github.io/blind_watermark/旋转攻击_提取水印.png)|
|Many Coverage<br>[多遮挡攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/多遮挡攻击.py)| ![多遮挡攻击](https://blindwatermark.github.io/blind_watermark/多遮挡攻击.jpg) |![多遮挡_提取水印](https://blindwatermark.github.io/blind_watermark/多遮挡攻击_提取水印.png)|
|50% Horizontal Crop<br>[横向裁剪攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/横向裁剪攻击.py)|![横向裁剪攻击](https://blindwatermark.github.io/blind_watermark/横向裁剪攻击.jpg)|![](https://blindwatermark.github.io/blind_watermark/横向裁剪攻击_提取水印.png)|
|50% Vertical Crop<br>[纵向裁剪攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/纵向裁剪攻击.py)|![纵向裁剪攻击](https://blindwatermark.github.io/blind_watermark/纵向裁剪攻击.jpg)|![纵向裁剪](https://blindwatermark.github.io/blind_watermark/纵向裁剪攻击_提取水印.png)|
|Resize（1200X1920->600X800）<br>[缩放攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/缩放攻击.py)|![缩放攻击](https://blindwatermark.github.io/blind_watermark/缩放攻击.jpg)|![](https://blindwatermark.github.io/blind_watermark/缩放攻击_提取水印.png)|
|Pepper Noise<br>[椒盐击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/椒盐攻击.py)|![椒盐攻击](https://blindwatermark.github.io/blind_watermark/椒盐攻击.jpg)|![](https://blindwatermark.github.io/blind_watermark/椒盐攻击_提取水印.png)|
|Brightness 10% Up<br>[亮度调高攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/亮度调高攻击.py)|![亮度调高攻击](https://blindwatermark.github.io/blind_watermark/亮度调高攻击.jpg)|![](https://blindwatermark.github.io/blind_watermark/亮度调高攻击_提取水印.png)|
|Brightness 10% Down<br>[亮度调暗攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/亮度调低攻击.py)|![亮度调低攻击](https://blindwatermark.github.io/blind_watermark/亮度调低攻击.jpg)|![](https://blindwatermark.github.io/blind_watermark/亮度调低攻击_提取水印.png)|


### embed string
Embed:
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

Extract:
```python
bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract('output/embedded.png', wm_shape=len_wm, mode='str')
print(wm_extract)
```

### embed array of bits

As demo, we embed 6 bytes data:
```python
wm = [True, False, True, True, True, False]
```

Embed:
```python
from blind_watermark import WaterMark

bwm1 = WaterMark(password_img=1, password_wm=1)
bwm1.read_ori_img('pic/ori_img.jpg')
bwm1.read_wm([True, False, True, True, True, False], mode='bit')
bwm1.embed('output/embedded.png')
```

Extract:
```python
bwm1 = WaterMark(password_img=1, password_wm=1, wm_shape=6)
wm_extract = bwm1.extract('output/打上水印的图.png', mode='bit')
print(wm_extract)
```
Notice that `wm_shape` (shape of watermark) is necessary

The output `wm_extract` is an array of float. set a threshold such as 0.5.
