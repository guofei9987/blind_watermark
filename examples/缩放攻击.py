# -*- coding: utf-8 -*-
# run origin.py to generate the embedded image

from blind_watermark import att

# 缩放攻击
att.resize_att('output/embedded.png', 'output/缩放攻击.png', out_shape=(800, 600))
att.resize_att('output/缩放攻击.png', 'output/缩放攻击_还原.png', out_shape=(1920, 1200))
# out_shape 是分辨率，需要颠倒一下
# %%提取水印
from blind_watermark import WaterMark

bwm1 = WaterMark(password_wm=1, password_img=1)
bwm1.extract(filename="output/缩放攻击_还原.png", wm_shape=(128, 128), out_wm_name="output/缩放攻击_提取水印.png")
