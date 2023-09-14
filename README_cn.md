# blind-watermark

基于频域的数字盲水印  


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
- **文档：** [https://BlindWatermark.github.io/blind_watermark/#/zh/](https://BlindWatermark.github.io/blind_watermark/#/zh/)  
- **English readme** [README.md](README.md)
- **Source code:** [https://github.com/guofei9987/blind_watermark](https://github.com/guofei9987/blind_watermark)

# 安装
```bash
pip install blind-watermark
```

或者安装最新开发版本
```bach
git clone git@github.com:guofei9987/blind_watermark.git
cd blind_watermark
pip install .
```

# 如何使用

## 命令行中使用

```bash
# 嵌入水印：
blind_watermark --embed --pwd 1234 examples/pic/ori_img.jpeg "watermark text" examples/output/embedded.png
# 提取水印：
blind_watermark --extract --pwd 1234 --wm_shape 111 examples/output/embedded.png
```



## Python 中使用

原图 + 水印 = 打上水印的图

![origin_image](docs/原图.jpeg) + '@guofei9987 开源万岁！' = ![打上水印的图](docs/打上水印的图.jpg)



参考 [代码](/examples/example_str.py)


嵌入水印
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


提取水印
```python
bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract('output/embedded.png', wm_shape=len_wm, mode='str')
print(wm_extract)
```
Output:
>@guofei9987 开源万岁！


### 各种攻击后的效果

|攻击方式|攻击后的图片|提取的水印|
|--|--|--|
|旋转攻击45度|![旋转攻击](docs/旋转攻击.jpg)|'@guofei9987 开源万岁！'|
|随机截图|![截屏攻击](docs/截屏攻击2_还原.jpg)|'@guofei9987 开源万岁！'|
|多遮挡| ![多遮挡攻击](docs/多遮挡攻击.jpg) |'@guofei9987 开源万岁！'|
|纵向裁剪|![横向裁剪攻击](docs/横向裁剪攻击_填补.jpg)|'@guofei9987 开源万岁！'|
|横向裁剪|![纵向裁剪攻击](docs/纵向裁剪攻击_填补.jpg)|'@guofei9987 开源万岁！'|
|缩放攻击|![缩放攻击](docs/缩放攻击.jpg)|'@guofei9987 开源万岁！'|
|椒盐攻击|![椒盐攻击](docs/椒盐攻击.jpg)|'@guofei9987 开源万岁！'|
|亮度攻击|![亮度攻击](docs/亮度攻击.jpg)|'@guofei9987 开源万岁！'|



### 嵌入图片

参考 [代码](/examples/example_str.py)


嵌入：
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

提取：
```python
bwm1 = WaterMark(password_wm=1, password_img=1)
# notice that wm_shape is necessary
bwm1.extract(filename='output/embedded.png', wm_shape=(128, 128), out_wm_name='output/extracted.png', )
```

|攻击方式|攻击后的图片|提取的水印|
|--|--|--|
|旋转攻击45度|![旋转攻击](docs/旋转攻击.jpg)|![](docs/旋转攻击_提取水印.png)|
|随机截图|![截屏攻击](docs/截屏攻击2_还原.jpg)|![](docs/旋转攻击_提取水印.png)|
|多遮挡| ![多遮挡攻击](docs/多遮挡攻击.jpg) |![多遮挡_提取水印](docs/多遮挡攻击_提取水印.png)|



### 隐水印还可以是二进制数据

参考 [代码](/examples/example_bit.py)


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

解出的水印是一个0～1之间的实数，方便用户自行卡阈值。如果水印信息量远小于图片可容纳量，偏差极小。

# 并行计算

```python
WaterMark(..., processes=None)
```
- `processes`: 整数，指定线程数。默认为 `None`, 表示使用全部线程。


## 相关项目

- text_blind_watermark (文本盲水印，把信息隐秘地打入文本): [https://github.com/guofei9987/text_blind_watermark](https://github.com/guofei9987/text_blind_watermark)  
- HideInfo（藏物于图、藏物于音、藏图于文）：[https://github.com/guofei9987/HideInfo](https://github.com/guofei9987/HideInfo)
