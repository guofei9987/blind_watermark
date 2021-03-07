# coding=utf-8

# attack on the watermark
import cv2
import numpy as np


def cut_att_height(input_filename, output_file_name, ratio=0.8):
    # 纵向剪切攻击
    input_img = cv2.imread(input_filename)
    input_img_shape = input_img.shape
    height = int(input_img_shape[0] * ratio)

    cv2.imwrite(output_file_name, input_img[:height, :, :])


def cut_att_width(input_filename, output_file_name, ratio=0.8):
    # 横向裁剪攻击
    input_img = cv2.imread(input_filename)
    input_img_shape = input_img.shape
    width = int(input_img_shape[1] * ratio)

    cv2.imwrite(output_file_name, input_img[:, :width, :])


def anti_cut_att(input_filename, output_file_name, origin_shape):
    # 反裁剪攻击：复制一块范围，然后补全
    # origin_shape 分辨率与约定理解的是颠倒的，约定的是列数*行数
    input_img = cv2.imread(input_filename)
    output_img = input_img.copy()
    output_img_shape = output_img.shape
    if output_img_shape[0] > origin_shape[0] or output_img_shape[0] > origin_shape[0]:
        print('裁剪打击后的图片，不可能比原始图片大，检查一下')
        return

    # 还原纵向打击
    while output_img_shape[0] < origin_shape[0]:
        output_img = np.concatenate([output_img, output_img[:origin_shape[0] - output_img_shape[0], :, :]], axis=0)
        output_img_shape = output_img.shape
    while output_img_shape[1] < origin_shape[1]:
        output_img = np.concatenate([output_img, output_img[:, :origin_shape[1] - output_img_shape[1], :]], axis=1)
        output_img_shape = output_img.shape

    cv2.imwrite(output_file_name, output_img)


def resize_att(input_filename, output_file_name, out_shape=(500, 500)):
    # 缩放攻击：因为攻击和还原都是缩放，所以攻击和还原都调用这个函数
    input_img = cv2.imread(input_filename)
    output_img = cv2.resize(input_img, dsize=out_shape)
    cv2.imwrite(output_file_name, output_img)


def bright_att(input_filename, output_file_name, ratio=0.8):
    # 亮度调整攻击，ratio应当多于0
    # ratio>1是调得更亮，ratio<1是亮度更暗
    input_img = cv2.imread(input_filename)
    output_img = input_img * ratio
    output_img[output_img > 255] = 255
    cv2.imwrite(output_file_name, output_img)


def shelter_att(input_filename, output_file_name, ratio=0.1, n=3):
    # 遮挡攻击：遮挡图像中的一部分
    # n个遮挡块
    # 每个遮挡块所占比例为ratio
    input_img = cv2.imread(input_filename)
    input_img_shape = input_img.shape
    output_img = input_img.copy()
    for i in range(n):
        tmp = np.random.rand() * (1 - ratio)  # 随机选择一个地方，1-ratio是为了防止溢出
        start_height, end_height = int(tmp * input_img_shape[0]), int((tmp + ratio) * input_img_shape[0])
        tmp = np.random.rand() * (1 - ratio)
        start_width, end_width = int(tmp * input_img_shape[1]), int((tmp + ratio) * input_img_shape[1])

        output_img[start_height:end_height, start_width:end_width, :] = 0

    cv2.imwrite(output_file_name, output_img)


def salt_pepper_att(input_filename, output_file_name, ratio=0.01):
    # 椒盐攻击
    input_img = cv2.imread(input_filename)
    input_img_shape = input_img.shape
    output_img = input_img.copy()
    for i in range(input_img_shape[0]):
        for j in range(input_img_shape[1]):
            if np.random.rand() < ratio:
                output_img[i, j, :] = 255
    cv2.imwrite(output_file_name, output_img)


def rot_att(input_filename, output_file_name, angle=45):
    # 旋转攻击
    input_img = cv2.imread(input_filename)
    rows, cols, _ = input_img.shape
    M = cv2.getRotationMatrix2D(center=(cols / 2, rows / 2), angle=angle, scale=1)
    output_img = cv2.warpAffine(input_img, M, (cols, rows))
    cv2.imwrite(output_file_name, output_img)
