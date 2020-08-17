#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from blind_watermark import WaterMark

bwm1 = WaterMark(password_wm=1, password_img=1)
# 读取原图
bwm1.read_img('pic/ori_img.jpg')
# 读取水印
bwm1.read_wm('pic/watermark.png')
# 打上盲水印
bwm1.embed('output/打上水印的图.png')

# %% 解水印


bwm1 = WaterMark(password_wm=1, password_img=1)
# 注意需要设定水印的长宽wm_shape
bwm1.extract(filename='output/打上水印的图.png', wm_shape=(128, 128), out_wm_name='output/解出的水印.png', )
