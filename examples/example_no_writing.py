#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This demonstrates how to embed and extract without writing files to local file system.
The format of images is numpy.array.
This may be useful if you want to use blind-watermark in another project.
"""
import blind_watermark
from blind_watermark import WaterMark
from blind_watermark import att
from blind_watermark.recover import estimate_crop_parameters, recover_crop
import cv2
import numpy as np
import os

blind_watermark.bw_notes.close()

os.chdir(os.path.dirname(__file__))
ori_img = cv2.imread('pic/ori_img.jpeg', flags=cv2.IMREAD_UNCHANGED)
wm = '@guofei9987 开源万岁！'
ori_img_shape = ori_img.shape[:2]  # 抗攻击有时需要知道原图的shape
h, w = ori_img_shape

# %% embed string into image whose format is numpy.array
bwm = WaterMark(password_img=1, password_wm=1)
bwm.read_img(img=ori_img)

bwm.read_wm(wm, mode='str')
embed_img = bwm.embed()

len_wm = len(bwm.wm_bit)  # 解水印需要用到长度
print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))

# %% extract from image whose format is numpy.array
bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract(embed_img=embed_img, wm_shape=len_wm, mode='str')
print("不攻击的提取结果：", wm_extract)

assert wm == wm_extract, '提取水印和原水印不一致'

# %%截屏攻击1 = 裁剪攻击 + 缩放攻击 + 知道攻击参数（按照参数还原）

loc_r = ((0.1, 0.1), (0.5, 0.5))
scale = 0.7

x1, y1, x2, y2 = int(w * loc_r[0][0]), int(h * loc_r[0][1]), int(w * loc_r[1][0]), int(h * loc_r[1][1])

img_attacked = att.cut_att3(input_img=embed_img, output_file_name=None, loc=(x1, y1, x2, y2), scale=scale)

# 还原攻击
img_recover = recover_crop(tem_img=img_attacked, loc=(x1, y1, x2, y2), image_o_shape=ori_img_shape)
bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract(embed_img=img_recover, wm_shape=len_wm, mode='str')
print("截屏攻击={loc}，缩放攻击={resize}，并且知道攻击参数。提取结果：".format(loc=(x1, y1, x2, y2), resize=scale), wm_extract)
assert wm == wm_extract, '提取水印和原水印不一致'

# %% 截屏攻击2 = 剪切攻击 + 缩放攻击 + 不知道攻击参数（因此需要 estimate_crop_parameters 来推测攻击参数）

loc_r = ((0.1, 0.1), (0.7, 0.6))
scale = 0.7
x1, y1, x2, y2 = int(w * loc_r[0][0]), int(h * loc_r[0][1]), int(w * loc_r[1][0]), int(h * loc_r[1][1])
print(f'Crop attack\'s real parameters: x1={x1},y1={y1},x2={x2},y2={y2}')
img_attacked = att.cut_att3(input_img=embed_img, loc=(x1, y1, x2, y2), scale=scale)

# estimate crop attack parameters:
(x1, y1, x2, y2), image_o_shape, score, scale_infer = estimate_crop_parameters(ori_img=embed_img,
                                                                               tem_img=img_attacked,
                                                                               scale=(0.5, 2), search_num=200)

print(f'Crop att estimate parameters: x1={x1},y1={y1},x2={x2},y2={y2}, scale_infer = {scale_infer}. score={score}')

# recover from attack:
img_recover = recover_crop(tem_img=img_attacked, loc=(x1, y1, x2, y2), image_o_shape=image_o_shape)

bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract(embed_img=img_recover, wm_shape=len_wm, mode='str')
print("截屏攻击，不知道攻击参数。提取结果：", wm_extract)
assert wm == wm_extract, '提取水印和原水印不一致'

# %%裁剪攻击1 = 裁剪 + 不做缩放 + 知道攻击参数
loc_r = ((0.1, 0.2), (0.5, 0.5))
x1, y1, x2, y2 = int(w * loc_r[0][0]), int(h * loc_r[0][1]), int(w * loc_r[1][0]), int(h * loc_r[1][1])

img_attacked = att.cut_att3(input_img=embed_img, loc=(x1, y1, x2, y2), scale=None)

# recover from attack:
img_recover = recover_crop(tem_img=img_attacked,
                           loc=(x1, y1, x2, y2), image_o_shape=image_o_shape)

bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract(embed_img=img_recover, wm_shape=len_wm, mode='str')
print("裁剪攻击，知道攻击参数。提取结果：", wm_extract)
assert wm == wm_extract, '提取水印和原水印不一致'

# %% 裁剪攻击2 = 裁剪 + 不做缩放 + 不知道攻击参数
loc_r = ((0.1, 0.1), (0.5, 0.4))
x1, y1, x2, y2 = int(w * loc_r[0][0]), int(h * loc_r[0][1]), int(w * loc_r[1][0]), int(h * loc_r[1][1])

img_attacked = att.cut_att3(input_img=embed_img, loc=(x1, y1, x2, y2), scale=None)

print(f'Cut attack\'s real parameters: x1={x1},y1={y1},x2={x2},y2={y2}')

# estimate crop attack parameters:
(x1, y1, x2, y2), image_o_shape, score, scale_infer = estimate_crop_parameters(ori_img=embed_img,
                                                                               tem_img=img_attacked,
                                                                               scale=(1, 1), search_num=None)

print(f'Cut attack\'s estimate parameters: x1={x1},y1={y1},x2={x2},y2={y2}. score={score}')

# recover from attack:
img_recover = recover_crop(tem_img=img_attacked,
                           loc=(x1, y1, x2, y2), image_o_shape=image_o_shape)

bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract(embed_img=img_recover, wm_shape=len_wm, mode='str')
print("裁剪攻击，不知道攻击参数。提取结果：", wm_extract)
assert wm == wm_extract, '提取水印和原水印不一致'

# %%椒盐攻击
ratio = 0.05
img_attacked = att.salt_pepper_att(input_img=embed_img, ratio=ratio)
# ratio是椒盐概率

# 提取
wm_extract = bwm1.extract(embed_img=img_attacked, wm_shape=len_wm, mode='str')
print(f"椒盐攻击ratio={ratio}后的提取结果：", wm_extract)
assert np.all(wm == wm_extract), '提取水印和原水印不一致'

# %%旋转攻击
angle = 60
img_attacked = att.rot_att(input_img=embed_img, angle=angle)
img_recover = att.rot_att(input_img=img_attacked, angle=-angle)

# 提取水印
bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract(embed_img=img_recover, wm_shape=len_wm, mode='str')
print(f"旋转攻击angle={angle}后的提取结果：", wm_extract)
assert wm == wm_extract, '提取水印和原水印不一致'

# %%遮挡攻击
n = 60
img_attacked = att.shelter_att(input_img=embed_img, ratio=0.1, n=n)

# 提取
bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract(embed_img=img_attacked, wm_shape=len_wm, mode='str')
print(f"遮挡攻击{n}次后的提取结果：", wm_extract)
assert wm == wm_extract, '提取水印和原水印不一致'

# %%缩放攻击
img_attacked = att.resize_att(input_img=embed_img, out_shape=(400, 300))
img_recover = att.resize_att(input_img=img_attacked, out_shape=ori_img_shape[::-1])
# out_shape 是分辨率，需要颠倒一下

bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract(embed_img=img_recover, wm_shape=len_wm, mode='str')
print("缩放攻击后的提取结果：", wm_extract)
assert np.all(wm == wm_extract), '提取水印和原水印不一致'
# %%

img_attacked = att.bright_att(input_img=embed_img, ratio=0.9)
img_recover = att.bright_att(input_img=img_attacked, ratio=1.1)
wm_extract = bwm1.extract(embed_img=img_recover, wm_shape=len_wm, mode='str')

print("亮度攻击后的提取结果：", wm_extract)
assert np.all(wm == wm_extract), '提取水印和原水印不一致'
