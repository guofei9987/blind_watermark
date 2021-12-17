# -*- coding: utf-8 -*-
# run origin.py to generate the embedded image

from blind_watermark import att
from blind_watermark import WaterMarkCore
import numpy as np

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# 除了嵌入图片，也可以嵌入比特类数据
import numpy as np
from blind_watermark import WaterMark

bwm1 = WaterMark(password_img=1, password_wm=1)

# 读取原图
bwm1.read_img('pic/ori_img.jpg')

# 读取水印
wm = [True, False, True, False, True, False, True, False, True, False]
bwm1.read_wm(wm, mode='bit')

# 打上盲水印
bwm1.embed('output/embedded.png')

# %% 解水印

# 注意设定水印的长宽wm_shape
bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract('output/embedded.png', wm_shape=10, mode='bit')
print("不攻击的提取结果：", wm_extract)

assert np.all(wm == wm_extract), '提取水印和原水印不一致'

# %%
# 一次横向裁剪打击
att.cut_att_width('output/embedded.png', 'output/横向裁剪攻击.png', ratio=0.2)
att.anti_cut_att('output/横向裁剪攻击.png', 'output/横向裁剪攻击_填补.png', origin_shape=(1200, 1920))

# 提取水印
bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/横向裁剪攻击_填补.png', wm_shape=10, mode='bit')
print("横向裁剪攻击后的提取结果：", wm_extract)

assert np.all(wm == wm_extract), '提取水印和原水印不一致'

# %%一次纵向裁剪攻击
att.cut_att_height('output/embedded.png', 'output/纵向裁剪攻击.png', ratio=0.5)
att.anti_cut_att('output/纵向裁剪攻击.png', 'output/纵向裁剪攻击_填补.png', origin_shape=(1200, 1920))

# 提取
bwm1 = WaterMark(password_wm=1, password_img=1)
bwm1.extract(filename="output/纵向裁剪攻击_填补.png", wm_shape=(128, 128), out_wm_name="output/纵向裁剪攻击_提取水印.png")
wm_extract = bwm1.extract('output/纵向裁剪攻击_填补.png', wm_shape=10, mode='bit')
print("纵向裁剪攻击后的提取结果：", wm_extract)

assert np.all(wm == wm_extract), '提取水印和原水印不一致'
# %%椒盐攻击
att.salt_pepper_att('output/embedded.png', 'output/椒盐攻击.png', ratio=0.05)
# ratio是椒盐概率

# 提取
wm_extract = bwm1.extract('output/椒盐攻击.png', wm_shape=10, mode='bit')
print("纵向裁剪攻击后的提取结果：", wm_extract)
assert np.all(wm == wm_extract), '提取水印和原水印不一致'

# %%旋转攻击
att.rot_att('output/embedded.png', 'output/旋转攻击.png', angle=45)
att.rot_att('output/旋转攻击.png', 'output/旋转攻击_还原.png', angle=-45)

# 提取水印
bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/旋转攻击_还原.png', wm_shape=10, mode='bit')
print("纵向裁剪攻击后的提取结果：", wm_extract)
assert np.all(wm == wm_extract), '提取水印和原水印不一致'

# %%多遮挡攻击

att.shelter_att('output/embedded.png', 'output/多遮挡攻击.png', ratio=0.1, n=10)

# 提取
bwm1 = WaterMark(password_wm=1, password_img=1)
wm_extract = bwm1.extract('output/多遮挡攻击.png', wm_shape=10, mode='bit')
print("纵向裁剪攻击后的提取结果：", wm_extract)
assert np.all(wm == wm_extract), '提取水印和原水印不一致'
