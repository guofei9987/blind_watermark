#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# embed string
import numpy as np
from blind_watermark import WaterMark
from blind_watermark import att
from blind_watermark.recover import estimate_crop_parameters, recover_crop
import cv2
import os

os.chdir(os.path.dirname(__file__))

bwm = WaterMark(password_img=1, password_wm=1)
bwm.read_img('pic/ori_img.jpeg')
wm = '@guofei9987 开源万岁！'
bwm.read_wm(wm, mode='str')
bwm.embed('output/embedded.png')

len_wm = len(bwm.wm_bit)  # 解水印需要用到长度
print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))

ori_img_shape = cv2.imread('pic/ori_img.jpeg').shape[:2]  # 抗攻击有时需要知道原图的shape
h, w = ori_img_shape

# %% 解水印
bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract('output/embedded.png', wm_shape=len_wm, mode='str')
print("不攻击的提取结果：", wm_extract)

assert wm == wm_extract, '提取水印和原水印不一致'

# %%截屏攻击1 = 裁剪攻击 + 缩放攻击 + 知道攻击参数（之后按照参数还原）

loc_r = ((0.1, 0.1), (0.5, 0.5))
scale = 0.7

x1, y1, x2, y2 = int(w * loc_r[0][0]), int(h * loc_r[0][1]), int(w * loc_r[1][0]), int(h * loc_r[1][1])

# 截屏攻击
att.cut_att3(input_filename='output/embedded.png', output_file_name='output/截屏攻击1.png',
             loc=(x1, y1, x2, y2), scale=scale)

recover_crop(template_file='output/截屏攻击1.png', output_file_name='output/截屏攻击1_还原.png',
             loc=(x1, y1, x2, y2), image_o_shape=ori_img_shape)

bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/截屏攻击1_还原.png', wm_shape=len_wm, mode='str')
print("截屏攻击，知道攻击参数。提取结果：", wm_extract)
assert wm == wm_extract, '提取水印和原水印不一致'

# %% 截屏攻击2 = 剪切攻击 + 缩放攻击 + 不知道攻击参数（因此需要 estimate_crop_parameters 来推测攻击参数）
loc_r = ((0.1, 0.1), (0.7, 0.6))
scale = 0.7

x1, y1, x2, y2 = int(w * loc_r[0][0]), int(h * loc_r[0][1]), int(w * loc_r[1][0]), int(h * loc_r[1][1])

print(f'Crop attack\'s real parameters: x1={x1},y1={y1},x2={x2},y2={y2}')
att.cut_att3(input_filename='output/embedded.png', output_file_name='output/截屏攻击2.png',
             loc=(x1, y1, x2, y2), scale=scale)

# estimate crop attack parameters:
(x1, y1, x2, y2), image_o_shape, score, scale_infer = estimate_crop_parameters(original_file='output/embedded.png',
                                                                               template_file='output/截屏攻击2.png',
                                                                               scale=(0.5, 2), search_num=200)

print(f'Crop att estimate parameters: x1={x1},y1={y1},x2={x2},y2={y2}, scale_infer = {scale_infer}. score={score}')

# recover from attack:
recover_crop(template_file='output/截屏攻击2.png', output_file_name='output/截屏攻击2_还原.png',
             loc=(x1, y1, x2, y2), image_o_shape=image_o_shape)

bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/截屏攻击2_还原.png', wm_shape=len_wm, mode='str')
print("截屏攻击，不知道攻击参数。提取结果：", wm_extract)
assert wm == wm_extract, '提取水印和原水印不一致'

# %%裁剪攻击1 = 裁剪 + 不做缩放 + 知道攻击参数
loc_r = ((0.1, 0.2), (0.5, 0.5))
x1, y1, x2, y2 = int(w * loc_r[0][0]), int(h * loc_r[0][1]), int(w * loc_r[1][0]), int(h * loc_r[1][1])

att.cut_att3(input_filename='output/embedded.png', output_file_name='output/随机裁剪攻击.png',
             loc=(x1, y1, x2, y2), scale=None)

# recover from attack:
recover_crop(template_file='output/随机裁剪攻击.png', output_file_name='output/随机裁剪攻击_还原.png',
             loc=(x1, y1, x2, y2), image_o_shape=image_o_shape)

bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/随机裁剪攻击_还原.png', wm_shape=len_wm, mode='str')
print("裁剪攻击，知道攻击参数。提取结果：", wm_extract)
assert wm == wm_extract, '提取水印和原水印不一致'

# %% 裁剪攻击2 = 裁剪 + 不做缩放 + 不知道攻击参数
loc_r = ((0.1, 0.1), (0.5, 0.4))
x1, y1, x2, y2 = int(w * loc_r[0][0]), int(h * loc_r[0][1]), int(w * loc_r[1][0]), int(h * loc_r[1][1])

att.cut_att3(input_filename='output/embedded.png', output_file_name='output/随机裁剪攻击2.png',
             loc=(x1, y1, x2, y2), scale=None)

print(f'Cut attack\'s real parameters: x1={x1},y1={y1},x2={x2},y2={y2}')

# estimate crop attack parameters:
(x1, y1, x2, y2), image_o_shape, score, scale_infer = estimate_crop_parameters(original_file='output/embedded.png',
                                                                               template_file='output/随机裁剪攻击2.png',
                                                                               scale=(1, 1), search_num=None)

print(f'Cut attack\'s estimate parameters: x1={x1},y1={y1},x2={x2},y2={y2}. score={score}')

# recover from attack:
recover_crop(template_file='output/随机裁剪攻击2.png', output_file_name='output/随机裁剪攻击2_还原.png',
             loc=(x1, y1, x2, y2), image_o_shape=image_o_shape)

bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/随机裁剪攻击2_还原.png', wm_shape=len_wm, mode='str')
print("裁剪攻击，不知道攻击参数。提取结果：", wm_extract)
assert wm == wm_extract, '提取水印和原水印不一致'

# %%椒盐攻击
ratio = 0.05
att.salt_pepper_att(input_filename='output/embedded.png', output_file_name='output/椒盐攻击.png', ratio=ratio)
# ratio是椒盐概率

# 提取
wm_extract = bwm1.extract('output/椒盐攻击.png', wm_shape=len_wm, mode='str')
print(f"椒盐攻击ratio={ratio}后的提取结果：", wm_extract)
assert np.all(wm == wm_extract), '提取水印和原水印不一致'

# %%旋转攻击
angle = 60
att.rot_att(input_filename='output/embedded.png', output_file_name='output/旋转攻击.png', angle=angle)
att.rot_att(input_filename='output/旋转攻击.png', output_file_name='output/旋转攻击_还原.png', angle=-angle)

# 提取水印
bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/旋转攻击_还原.png', wm_shape=len_wm, mode='str')
print(f"旋转攻击angle={angle}后的提取结果：", wm_extract)
assert wm == wm_extract, '提取水印和原水印不一致'

# %%遮挡攻击
n = 60
att.shelter_att(input_filename='output/embedded.png', output_file_name='output/多遮挡攻击.png', ratio=0.1, n=n)

# 提取
bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/多遮挡攻击.png', wm_shape=len_wm, mode='str')
print(f"遮挡攻击{n}次后的提取结果：", wm_extract)
assert wm == wm_extract, '提取水印和原水印不一致'

# %%缩放攻击
att.resize_att(input_filename='output/embedded.png', output_file_name='output/缩放攻击.png', out_shape=(400, 300))
att.resize_att(input_filename='output/缩放攻击.png', output_file_name='output/缩放攻击_还原.png',
               out_shape=ori_img_shape[::-1])
# out_shape 是分辨率，需要颠倒一下

bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/缩放攻击_还原.png', wm_shape=len_wm, mode='str')
print("缩放攻击后的提取结果：", wm_extract)
assert np.all(wm == wm_extract), '提取水印和原水印不一致'
# %%亮度攻击

att.bright_att(input_filename='output/embedded.png', output_file_name='output/亮度攻击.png', ratio=0.9)
att.bright_att(input_filename='output/亮度攻击.png', output_file_name='output/亮度攻击_还原.png', ratio=1.1)
wm_extract = bwm1.extract('output/亮度攻击_还原.png', wm_shape=len_wm, mode='str')

print("亮度攻击后的提取结果：", wm_extract)
assert np.all(wm == wm_extract), '提取水印和原水印不一致'
