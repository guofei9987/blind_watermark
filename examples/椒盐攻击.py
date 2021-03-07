# -*- coding: utf-8 -*-

from blind_watermark import att
import numpy as np
import cv2

# %%椒盐攻击
att.salt_pepper_att('output/embedded.png', 'output/椒盐攻击.png', ratio=0.05)
# ratio是椒盐概率

# %%纵向裁剪打击.png
from blind_watermark import WaterMark

bwm1 = WaterMark(password_wm=1, password_img=1)
bwm1.extract(filename='output/椒盐攻击.png', wm_shape=(128, 128), out_wm_name='output/椒盐攻击_提取水印.png')

