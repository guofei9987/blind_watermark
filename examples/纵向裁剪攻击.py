from blind_watermark import att
import numpy as np

# 一次纵向裁剪打击
att.cut_att_height('output/打上水印的图.png', 'output/纵向裁剪打击.png', ratio=0.5)

att.anti_cut_att('output/纵向裁剪打击.png', 'output/纵向裁剪打击_填补.png', origin_shape=(1200, 1920))

# %%纵向裁剪打击.png
from blind_watermark import WaterMark

bwm1 = WaterMark(password_wm=1, password_img=1)
bwm1.extract(filename="output/纵向裁剪打击_填补.png", wm_shape=(128, 128), out_wm_name="output/纵向裁剪打击_提取水印.png")
