#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# embed string
import numpy as np
from blind_watermark import WaterMark
from blind_watermark import att
import cv2

bwm1 = WaterMark(password_img=1, password_wm=1)
bwm1.read_img('pic/ori_img.jpeg')
wm = '@guofei9987 开源万岁！'
bwm1.read_wm(wm, mode='str')
bwm1.embed('output/embedded.png')

len_wm = len(bwm1.wm_bit)  # 解水印需要用到长度
print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))

ori_img_shape = cv2.imread('pic/ori_img.jpeg').shape[:2]  # 抗攻击需要知道原图的shape

# %%
# 截屏攻击
loc = ((0.1, 0.1), (0.5, 0.5))
scale = 1.3
att.cut_att2('output/embedded.png', 'output/截屏攻击2.png', loc=loc, scale=scale)

# %%

from blind_watermark.recover import recover_crop

recover_crop(original_file='output/embedded.png',
             template_file='output/截屏攻击2.png',
             output_file_name='output/截屏攻击2_还原.png')

# %%
bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/截屏攻击2_还原.png', wm_shape=len_wm, mode='str')
print("截屏攻击，不知道攻击参数。提取结果：".format(loc=loc, scale=scale), wm_extract)
assert wm == wm_extract, '提取水印和原水印不一致'
