#!/usr/bin/env python3
# coding=utf-8
# @Time    : 2020/8/13
# @Author  : github.com/guofei9987
import warnings

import numpy as np
import cv2

from .bwm_core import WaterMarkCore
from .version import bw_notes


class WaterMark:
    def __init__(self, password_wm=1, password_img=1, block_shape=(4, 4), mode='common', processes=None):
        bw_notes.print_notes()

        self.bwm_core = WaterMarkCore(password_img=password_img, mode=mode, processes=processes)

        self.password_wm = password_wm

        self.wm_bit = None
        self.wm_size = 0

    def read_img(self, filename=None, img=None):
        if img is None:
            # 从文件读入图片
            img = cv2.imread(filename, flags=cv2.IMREAD_UNCHANGED)
            assert img is not None, "image file '{filename}' not read".format(filename=filename)

        self.bwm_core.read_img_arr(img=img)
        return img

    def read_wm(self, wm_content, mode='img'):
        assert mode in ('img', 'str', 'bit'), "mode in ('img','str','bit')"
        if mode == 'img':
            wm = cv2.imread(filename=wm_content, flags=cv2.IMREAD_GRAYSCALE)
            assert wm is not None, 'file "{filename}" not read'.format(filename=wm_content)

            # 读入图片格式的水印，并转为一维 bit 格式，抛弃灰度级别
            self.wm_bit = wm.flatten() > 128

        elif mode == 'str':
            byte = bin(int(wm_content.encode('utf-8').hex(), base=16))[2:]
            self.wm_bit = (np.array(list(byte)) == '1')
        else:
            self.wm_bit = np.array(wm_content)

        self.wm_size = self.wm_bit.size

        # 水印加密:
        np.random.RandomState(self.password_wm).shuffle(self.wm_bit)

        self.bwm_core.read_wm(self.wm_bit)

    def embed(self, filename=None, compression_ratio=None):
        '''
        :param filename: string
            Save the image file as filename
        :param compression_ratio: int or None
            If compression_ratio = None, do not compression,
            If compression_ratio is integer between 0 and 100, the smaller, the output file is smaller.
        :return:
        '''
        embed_img = self.bwm_core.embed()
        if filename is not None:
            if compression_ratio is None:
                cv2.imwrite(filename=filename, img=embed_img)
            elif filename.endswith('.jpg'):
                cv2.imwrite(filename=filename, img=embed_img, params=[cv2.IMWRITE_JPEG_QUALITY, compression_ratio])
            elif filename.endswith('.png'):
                cv2.imwrite(filename=filename, img=embed_img, params=[cv2.IMWRITE_PNG_COMPRESSION, compression_ratio])
            else:
                cv2.imwrite(filename=filename, img=embed_img)
        return embed_img

    def extract_decrypt(self, wm_avg):
        wm_index = np.arange(self.wm_size)
        np.random.RandomState(self.password_wm).shuffle(wm_index)
        wm_avg[wm_index] = wm_avg.copy()
        return wm_avg

    def extract(self, filename=None, embed_img=None, wm_shape=None, out_wm_name=None, mode='img'):
        assert wm_shape is not None, 'wm_shape needed'

        if filename is not None:
            embed_img = cv2.imread(filename, flags=cv2.IMREAD_COLOR)
            assert embed_img is not None, "{filename} not read".format(filename=filename)

        self.wm_size = np.array(wm_shape).prod()

        if mode in ('str', 'bit'):
            wm_avg = self.bwm_core.extract_with_kmeans(img=embed_img, wm_shape=wm_shape)
        else:
            wm_avg = self.bwm_core.extract(img=embed_img, wm_shape=wm_shape)

        # 解密：
        wm = self.extract_decrypt(wm_avg=wm_avg)

        # 转化为指定格式：
        if mode == 'img':
            wm = 255 * wm.reshape(wm_shape[0], wm_shape[1])
            cv2.imwrite(out_wm_name, wm)
        elif mode == 'str':
            byte = ''.join(str((i >= 0.5) * 1) for i in wm)
            wm = bytes.fromhex(hex(int(byte, base=2))[2:]).decode('utf-8', errors='replace')

        return wm
