# -*- coding: utf-8 -*-

from blind_watermark import att

# 亮度调高攻击
att.bright_att('output/embedded.png', 'output/亮度调高攻击.png', ratio=1.1)

#%% 提取水印
from blind_watermark import WaterMark

bwm1 = WaterMark(password_wm=1, password_img=1)
bwm1.extract(filename='output/亮度调高攻击.png', wm_shape=(128, 128), out_wm_name='output/亮度调高攻击_提取水印.png')
