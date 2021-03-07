# -*- coding: utf-8 -*-

from blind_watermark import WaterMark
import os
import cv2


def batch_embed():
    password_wm = int(input('算法采用双密码系统，请设定密码1：(必须是数字)'))
    password_img = int(input('算法采用双密码系统，请设定密码2：(必须是数字)'))
    bwm1 = WaterMark(password_wm=password_wm, password_img=password_img)

    _, _, files = list(os.walk("watermark"))[0]
    if len(files) == 0:
        print('wartermark 文件夹中没有图片！，即将退出！')
        return
    else:
        watermark = files[0]
        print('水印是 {}'.format(watermark))

    # read watermark
    bwm1.read_wm('watermark/{watermark}'.format(watermark=watermark))
    watermark_shape = cv2.imread('watermark/{watermark}'.format(watermark=watermark)).shape[:]
    print('请记下水印大小，解密的时候需要输入: {}x{}'.format(*watermark_shape))

    # read images
    _, _, images = list(os.walk("images"))[0]
    if len(images) == 0:
        print('images 文件夹中没有图片！，即将退出！')
        return
    else:
        print('已经读取原图：{}个，分别是 {}'.format(len(images), ', '.join(images)))

    for image in images:
        bwm1.read_img('images/{image}'.format(image=image))
        bwm1.embed('output/{image}'.format(image=image))
        print('images/{image} 已经被打上水印，并放入 output/{image}'.format(image=image))


def batch_extract():
    password_wm = int(input('算法采用双密码系统，请设定密码1：(必须是数字)'))
    password_img = int(input('算法采用双密码系统，请设定密码2：(必须是数字)'))
    bwm1 = WaterMark(password_wm=password_wm, password_img=password_img)

    watermark_shape = input('请输入水印大小，例如 128x128')
    watermark_shape = tuple(int(i) for i in watermark_shape.split('x'))

    # read images
    _, _, images = list(os.walk("images"))[0]
    if len(images) == 0:
        print('images 文件夹中没有图片！，即将退出！')
        return
    else:
        print('已经读取打上水印的图：{}个，分别是 {}'.format(len(images), ', '.join(images)))

    for image in images:
        bwm1.extract(filename='images/{image}'.format(image=image)
                     , wm_shape=watermark_shape
                     , out_wm_name='output/{image}'.format(image=image))

        print('images/{image} 已解出水印，水印放入 output/{image}'.format(image=image))


def main():
    print('''开源代码地址：https://github.com/guofei9987/blind_watermark ，欢迎star
    本程序免费提供使用！
    程序功能：
        功能1: 把盲水印嵌入原图
        功能2: 水印解密模式（需要输入密码）
    程序开始运行：
    请注意，本程序需要和其下文件夹配合工作，他们分别是:
        /images: 存放待打上盲水印原图（功能1），或者待解出盲水印的图片（功能2）。如果有多张图片，则会批量运行。
        /watermark：存放水印，只有第一张生效（只在功能1下生效）
        /output：程序的输出。打上盲水印的图（功能1），或者解出的水印（功能2）
    复制此程序时，请直接打包本程序所在文件夹
    ''')
    print('''请选择程序工作模式：
        0：安装所需包
        1: 把盲水印嵌入原图
        2: 水印解密模式（需要输入密码）
    ''')
    work_mode = int(input("请选输入工作模式序号"))

    if work_mode == 0:
        print('正在检查并安装所需包...')
        os.system('pip install blind-watermark')
    if work_mode == 1:
        batch_embed()
        print('盲水印已经批量打入原图，放到了文件夹 /output 下')
    elif work_mode == 2:
        batch_extract()
        print('盲水印已经批量解出，放到了文件夹 /output 下')

    else:
        print('模式选择错误')

    input('按任意键退出')


if __name__ == '__main__':
    main()
