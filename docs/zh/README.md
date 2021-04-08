# blind-watermark

基于小波变换的数字盲水印  


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


![demonstration](https://blindwatermark.github.io/demonstration/demonstration.jpg)


### 嵌入字符串
嵌入：
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

提取：
```python
bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract('output/embedded.png', wm_shape=len_wm, mode='str')
print(wm_extract)
```
Output:
>@guofei9987 开源万岁！


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

解出的水印是一个0～1之间的实数，方便用户自行卡阈值。如果水印信息量远小于图片可容纳量，偏差极小。

# 并行计算

```python
WaterMark(..., processes=None)
```
- `processes`: 整数，指定线程数。默认为 `None`, 表示使用全部线程。
