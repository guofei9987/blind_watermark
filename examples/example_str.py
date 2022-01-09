#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# embed string
import numpy as np
from blind_watermark import WaterMark
from blind_watermark import att
from blind_watermark.recover import estimate_crop_parameters, recover_crop

import cv2

bwm1 = WaterMark(password_img=1, password_wm=1)
bwm1.read_img('pic/ori_img.jpeg')
wm = '@guofei9987 开源万岁！'
bwm1.read_wm(wm, mode='str')
bwm1.embed('output/embedded.png')

len_wm = len(bwm1.wm_bit)  # 解水印需要用到长度
print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))

ori_img_shape = cv2.imread('pic/ori_img.jpeg').shape[:2]  # 抗攻击需要知道原图的shape

# %% 解水印
bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract('output/embedded.png', wm_shape=len_wm, mode='str')
print("不攻击的提取结果：", wm_extract)

assert wm == wm_extract, '提取水印和原水印不一致'

# %%截屏攻击 = 裁剪攻击 + 缩放攻击 + 知道攻击参数（按照参数还原）

loc = ((0.1, 0.1), (0.5, 0.5))
resize = 0.7
att.cut_att('output/embedded.png', 'output/截屏攻击.png', loc=loc, resize=resize)

bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/截屏攻击.png', wm_shape=len_wm, mode='str')
print("截屏攻击={loc}，缩放攻击={resize}，并且知道攻击参数。提取结果：".format(loc=loc, resize=resize), wm_extract)
assert wm == wm_extract, '提取水印和原水印不一致'

# %% 截屏攻击 = 剪切攻击 + 缩放攻击 + 不知道攻击参数
import importlib

importlib.reload(att)

loc_r = ((0.1, 0.1), (0.7, 0.6))
scale = 0.7
_, (x1, y1, x2, y2) = att.cut_att2('output/embedded.png', 'output/截屏攻击2.png', loc_r=loc_r, scale=scale)
print(f'Crop attack\'s real parameters: x1={x1},y1={y1},x2={x2},y2={y2}')

# estimate crop attack parameters:
(x1, y1, x2, y2), image_o_shape, score, scale_infer = estimate_crop_parameters(original_file='output/embedded.png',
                                                                               template_file='output/截屏攻击2.png',
                                                                               scale=(0.5, 2), search_num=200)

print(f'Crop attack\'s estimate parameters: x1={x1},y1={y1},x2={x2},y2={y2}. score={score}')

# recover from attack:
recover_crop('output/截屏攻击2.png', 'output/截屏攻击2_还原.png', (x1, y1, x2, y2), image_o_shape)

bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/截屏攻击2_还原.png', wm_shape=len_wm, mode='str')
print("截屏攻击，不知道攻击参数。提取结果：", wm_extract)
assert wm == wm_extract, '提取水印和原水印不一致'

# %% Vertical cut
r = 0.3
att.cut_att_width('output/embedded.png', 'output/横向裁剪攻击.png', ratio=r)
att.anti_cut_att('output/横向裁剪攻击.png', 'output/横向裁剪攻击_填补.png', origin_shape=ori_img_shape)

# 提取水印
bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/横向裁剪攻击_填补.png', wm_shape=len_wm, mode='str')
print(f"横向裁剪攻击r={r}后的提取结果：", wm_extract)

assert wm == wm_extract, '提取水印和原水印不一致'

# %% horizontal cut
r = 0.4
att.cut_att_height('output/embedded.png', 'output/纵向裁剪攻击.png', ratio=r)
att.anti_cut_att('output/纵向裁剪攻击.png', 'output/纵向裁剪攻击_填补.png', origin_shape=ori_img_shape)

# extract:
bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/纵向裁剪攻击_填补.png', wm_shape=len_wm, mode='str')
print(f"纵向裁剪攻击r={r}后的提取结果：", wm_extract)

assert wm == wm_extract, '提取水印和原水印不一致'
# %%椒盐攻击
ratio = 0.05
att.salt_pepper_att('output/embedded.png', 'output/椒盐攻击.png', ratio=ratio)
# ratio是椒盐概率

# 提取
wm_extract = bwm1.extract('output/椒盐攻击.png', wm_shape=len_wm, mode='str')
print(f"椒盐攻击ratio={ratio}后的提取结果：", wm_extract)
assert np.all(wm == wm_extract), '提取水印和原水印不一致'

# %%旋转攻击
angle = 60
att.rot_att('output/embedded.png', 'output/旋转攻击.png', angle=angle)
att.rot_att('output/旋转攻击.png', 'output/旋转攻击_还原.png', angle=-angle)

# 提取水印
bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/旋转攻击_还原.png', wm_shape=len_wm, mode='str')
print(f"旋转攻击angle={angle}后的提取结果：", wm_extract)
assert wm == wm_extract, '提取水印和原水印不一致'

# %%遮挡攻击
n = 60
att.shelter_att('output/embedded.png', 'output/多遮挡攻击.png', ratio=0.1, n=n)

# 提取
bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/多遮挡攻击.png', wm_shape=len_wm, mode='str')
print(f"遮挡攻击{n}次后的提取结果：", wm_extract)
assert wm == wm_extract, '提取水印和原水印不一致'

# %%缩放攻击
att.resize_att('output/embedded.png', 'output/缩放攻击.png', out_shape=(400, 300))
att.resize_att('output/缩放攻击.png', 'output/缩放攻击_还原.png', out_shape=ori_img_shape[::-1])
# out_shape 是分辨率，需要颠倒一下

bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/缩放攻击_还原.png', wm_shape=len_wm, mode='str')
print("缩放攻击后的提取结果：", wm_extract)
assert np.all(wm == wm_extract), '提取水印和原水印不一致'
# %%

att.bright_att('output/embedded.png', 'output/亮度攻击.png', ratio=0.9)
att.bright_att('output/亮度攻击.png', 'output/亮度攻击_还原.png', ratio=1.1)
wm_extract = bwm1.extract('output/亮度攻击_还原.png', wm_shape=len_wm, mode='str')

print("亮度攻击后的提取结果：", wm_extract)
assert np.all(wm == wm_extract), '提取水印和原水印不一致'
