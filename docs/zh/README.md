# blind-watermark
基于傅里叶变换的数字盲水印  


[![PyPI](https://img.shields.io/pypi/v/blind_watermark)](https://pypi.org/project/blind_watermark/)
[![Build Status](https://travis-ci.com/guofei9987/blind_watermark.svg?branch=master)](https://travis-ci.com/guofei9987/blind_watermark)
[![codecov](https://codecov.io/gh/guofei9987/blind_watermark/branch/master/graph/badge.svg)](https://codecov.io/gh/guofei9987/blind_watermark)
[![License](https://img.shields.io/pypi/l/blind_watermark.svg)](https://github.com/guofei9987/blind_watermark/blob/master/LICENSE)
![Python](https://img.shields.io/badge/python->=3.5-green.svg)
![Platform](https://img.shields.io/badge/platform-windows%20|%20linux%20|%20macos-green.svg)
[![PyPI_downloads](https://img.shields.io/pypi/dm/blind_watermark)](https://pypi.org/project/blind_watermark/)
[![Join the chat at https://gitter.im/guofei9987/blind_watermark](https://badges.gitter.im/guofei9987/blind_watermark.svg)](https://gitter.im/guofei9987/blind_watermark?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


- **Documentation:** [https://BlindWatermark.github.io/blind_watermark/#/en/](https://blind_watermark.github.io/blind_watermark/#/en/)
- **文档：** [https://BlindWatermark.github.io/blind_watermark/#/zh/](https://blind_watermark.github.io/blind_watermark/#/zh/)  
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

## 如何使用

嵌入水印
```python
from blind_watermark import WaterMark

bwm1 = WaterMark(password_wm=1, password_img=1)
# 读取原图
bwm1.read_img('pic/ori_img.jpg')
# 读取水印
bwm1.read_wm('pic/watermark.png')
# 打上盲水印
bwm1.embed('output/打上水印的图.png')
```


提取水印
```python
bwm1 = WaterMark(password_wm=1, password_img=1)
# 注意需要设定水印的长宽wm_shape
bwm1.extract(filename='output/打上水印的图.png', wm_shape=(128, 128), out_wm_name='output/解出的水印.png', )
```

## 效果展示

|原图|水印|
|--|--|
|![原图](../原图.jpg)|![水印](../水印.png)|

|打上水印的图|提取的水印|
|--|--|
|![打上水印的图](../打上水印的图.jpg)|![提取的水印](../解出的水印.png)|


### 各种攻击后的效果

|攻击方式|攻击后的图片|提取的水印|
|--|--|--|
|旋转攻击45度<br>[旋转攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/旋转攻击.py)|![旋转攻击](../旋转攻击.jpg)|![](../旋转攻击_提取水印.png)|
|多遮挡<br>[多遮挡攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/多遮挡攻击.py)| ![多遮挡攻击](../多遮挡攻击.jpg)|![多遮挡_提取水印](../多遮挡攻击_提取水印.png)|
|横向裁剪50%<br>[横向裁剪攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/横向裁剪攻击.py)|![横向裁剪攻击](../横向裁剪攻击.jpg)|![](../横向裁剪攻击_提取水印.png)|
|纵向裁剪50%<br>[纵向裁剪攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/纵向裁剪攻击.py)|![纵向裁剪攻击](../纵向裁剪攻击.jpg)|![纵向裁剪](../纵向裁剪攻击_提取水印.png)|
|缩放攻击（1200X1920->600X800）<br>[缩放攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/缩放攻击.py)|![缩放攻击](../缩放攻击.jpg)|![](../缩放攻击_提取水印.png)|
|椒盐攻击<br>[椒盐击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/椒盐攻击.py)|![椒盐攻击](../椒盐攻击.jpg)|![](../椒盐攻击_提取水印.png)|
|亮度提高10%<br>[亮度调高攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/亮度调高攻击.py)|![亮度调高攻击](../亮度调高攻击.jpg)|![](../亮度调高攻击_提取水印.png)|
|亮度调低10%<br>[亮度调暗攻击.py](https://github.com/guofei9987/blind_watermark/blob/master/examples/亮度调低攻击.py)|![亮度调低攻击](../亮度调低攻击.jpg)|![](../亮度调低攻击_提取水印.png)|


### 隐水印还可以是二进制数据

作为 demo， 如果要嵌入是如下长度为6的二进制数据
```python
wm = [True, False, True, True, True, False]
```

嵌入水印

```python
# 除了嵌入图片，也可以嵌入比特类数据
from blind_watermark import WaterMark

bwm1 = WaterMark(password_img=1, password_wm=1)
bwm1.read_ori_img('pic/ori_img.jpg')
bwm1.read_wm([True, False, True, True, True, False], mode='bit')
bwm1.embed('output/打上水印的图.png')
```

解水印：（注意设定水印形状 `wm_shape`）
```python
bwm1 = WaterMark(password_img=1, password_wm=1, wm_shape=6)
wm_extract = bwm1.extract('output/打上水印的图.png', mode='bit')
print(wm_extract)
```

解出的水印是一个0～1之间的实数，方便用户自行卡阈值。如果水印信息量远小于图片可容纳量，实测偏差极小。

