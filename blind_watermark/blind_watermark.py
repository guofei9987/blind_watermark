#!/usr/bin/env python3
# coding=utf-8
# @Time    : 2020/8/13
# @Author  : github.com/guofei9987

import numpy as np
import cv2

from .bwm_core import WaterMarkCore


class WaterMark:
    def __init__(self, password_wm=1, password_img=1, block_shape=(4, 4), mode='common', processes=None):

        self.bwm_core = WaterMarkCore(password_img=password_img, mode=mode, processes=processes)

        self.password_wm = password_wm

    def read_img(self, filename):
        self.bwm_core.read_img(filename=filename)

    def read_img_wm(self, filename):
        wm = cv2.imread(filename)
        if wm is None:
            raise IOError("file '{filename}' not read".format(filename=filename))

        # 读入图片格式的水印，并转为一维 bit 格式
        self.wm = wm[:, :, 0]
        # 加密信息只用bit类，抛弃灰度级别
        self.wm_bit = self.wm.flatten() > 128

    def read_wm(self, wm_content, mode='img'):
        if mode == 'img':
            self.read_img_wm(filename=wm_content)
        elif mode == 'str':
            byte = bin(int(wm_content.encode('utf-8').hex(), base=16))[2:]
            self.wm_bit = (np.array(list(byte)) == '1')
        else:
            self.wm_bit = np.array(wm_content)

        self.wm_size = self.wm_bit.size

        # 水印加密:
        np.random.RandomState(self.password_wm).shuffle(self.wm_bit)

        self.bwm_core.read_wm(self.wm_bit)

    def embed(self, filename):
        self.bwm_core.embed(filename=filename)

    def extract_decrypt(self, wm_avg):
        wm_index = np.arange(self.wm_size)
        np.random.RandomState(self.password_wm).shuffle(wm_index)
        wm_avg[wm_index] = wm_avg.copy()
        return wm_avg

    def extract(self, filename, wm_shape, out_wm_name=None, mode='img'):
        self.wm_size = np.array(wm_shape).prod()

        if mode in ('str', 'bit'):
            wm_avg = self.bwm_core.extract_with_kmeans(filename=filename, wm_shape=wm_shape)
        else:
            wm_avg = self.bwm_core.extract(filename=filename, wm_shape=wm_shape)

        # 解密：
        wm = self.extract_decrypt(wm_avg=wm_avg)

        # 转化为指定格式：
        if mode == 'img':
            cv2.imwrite(out_wm_name, 255 * wm.reshape(wm_shape[0], wm_shape[1]))
        elif mode == 'str':
            byte = ''.join((np.round(wm)).astype(np.int).astype(np.str))
            wm = bytes.fromhex(hex(int(byte, base=2))[2:]).decode('utf-8')

        return wm
