#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
How to embed and extract without writing files to local file system.
The format of images is numpy.array.
This is useful if you want to use blind-watermark in another project.
"""

from blind_watermark import WaterMark

import cv2

# %%
img = cv2.imread('pic/ori_img.jpeg', flags=cv2.IMREAD_UNCHANGED)
wm = '@guofei9987 开源万岁！'

# %% embed string into image whose format is numpy.array
bwm = WaterMark(password_img=1, password_wm=1)
bwm.read_img(img=img)

bwm.read_wm(wm, mode='str')
embed_img = bwm.embed()

len_wm = len(bwm.wm_bit)  # 解水印需要用到长度
print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))

# %% extract from image whose format is numpy.array
bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract(embed_img=embed_img, wm_shape=len_wm, mode='str')
print("不攻击的提取结果：", wm_extract)

assert wm == wm_extract, '提取水印和原水印不一致'
