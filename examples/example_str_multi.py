#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
demonstrate multiprocessing and multithreading
'''
# embed string
from blind_watermark import WaterMark
import cv2
import os

os.chdir(os.path.dirname(__file__))

mode = 'multiprocessing'
bwm = WaterMark(password_img=1, password_wm=1, processes=mode)
bwm.read_img('pic/ori_img.jpeg')
wm = '@guofei9987 开源万岁！'
bwm.read_wm(wm, mode='str')
bwm.embed('output/embedded.png')

len_wm = len(bwm.wm_bit)  # 解水印需要用到长度
print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))

ori_img_shape = cv2.imread('pic/ori_img.jpeg').shape[:2]  # 抗攻击有时需要知道原图的shape
h, w = ori_img_shape

# %% 解水印
bwm1 = WaterMark(password_img=1, password_wm=1, processes=mode)
wm_extract = bwm1.extract('output/embedded.png', wm_shape=len_wm, mode='str')
print("不攻击的提取结果：", wm_extract)

assert wm == wm_extract, '提取水印和原水印不一致'

mode = 'multithreading'

bwm = WaterMark(password_img=1, password_wm=1, processes=mode)
bwm.read_img('pic/ori_img.jpeg')
wm = '@guofei9987 开源万岁！'
bwm.read_wm(wm, mode='str')
bwm.embed('output/embedded.png')

len_wm = len(bwm.wm_bit)  # 解水印需要用到长度
print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))

ori_img_shape = cv2.imread('pic/ori_img.jpeg').shape[:2]  # 抗攻击有时需要知道原图的shape
h, w = ori_img_shape

# %% 解水印
bwm1 = WaterMark(password_img=1, password_wm=1, processes=mode)
wm_extract = bwm1.extract('output/embedded.png', wm_shape=len_wm, mode='str')
print("不攻击的提取结果：", wm_extract)

assert wm == wm_extract, '提取水印和原水印不一致'
