# -*- coding: utf-8 -*-

from blind_watermark import att

# 旋转攻击
att.rot_att('output/embedded.png', 'output/旋转攻击.png', angle=45)
att.rot_att('output/旋转攻击.png', 'output/旋转攻击_还原.png', angle=-45)

# %%提取水印
from blind_watermark import WaterMark

bwm1 = WaterMark(password_wm=1, password_img=1)
bwm1.extract(filename='output/旋转攻击_还原.png', wm_shape=(128, 128), out_wm_name='output/旋转攻击_提取水印.png')

