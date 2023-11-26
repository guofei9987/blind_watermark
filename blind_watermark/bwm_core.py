#!/usr/bin/env python3
# coding=utf-8
# @Time    : 2021/12/17
# @Author  : github.com/guofei9987
import numpy as np
from numpy.linalg import svd
import cv2
from cv2 import dct, idct
from pywt import dwt2, idwt2


class WaterMarkCore:
    def __init__(self, password_img=1, block_shape=(4, 4), d=(36, 20)):
        self.block_shape = block_shape
        self.block_h, self.block_w = block_shape  # block 的大小

        self.password_img = password_img
        self.d1, self.d2 = d  # d1/d2 越大鲁棒性越强,但输出图片的失真越大

        self.img, self.img_YUV = None, None
        self.block_num_h, self.block_num_w = None, None  # 分块数量
        self.img_h_align, self.img_w_align = None, None  # 可整除部分的像素大小
        self.ca, self.hvd, = None, [None] * 3  # 每个通道 dct 的结果

        self.wm_size = 0  # 水印的长度，原图片可插入信息的个数

        self.fast_mode = False
        self.alpha = None  # 用于处理透明图

        self.idx_shuffle = None  # 用于加密

    def read_img_arr(self, img):
        # 处理透明图
        self.alpha = None
        if img.shape[2] == 4:
            if img[:, :, 3].min() < 255:
                self.alpha = img[:, :, 3]
                img = img[:, :, :3]

        # 读入图片 BGR -> YUV -> dwt
        self.img = img.astype(np.float32)
        img_h, img_w = self.img.shape[:2]

        # 分块的数量
        self.block_num_h, self.block_num_w = img_h // 2 // self.block_h, img_w // 2 // self.block_w

        # ca 水印作用的像素区域
        ca_h, ca_w = self.block_num_h * self.block_h, self.block_num_w * self.block_w
        # 像素区域
        self.img_h_align, self.img_w_align = ca_h * 2, ca_w * 2

        self.img_YUV = cv2.cvtColor(self.img[:self.img_h_align, :self.img_w_align, :], cv2.COLOR_BGR2YUV)
        self.ca = np.zeros(shape=(ca_h, ca_w, 3))
        for channel in range(3):
            self.ca[:, :, channel], self.hvd[channel] = dwt2(self.img_YUV[:, :, channel], 'haar')

        self.idx_shuffle = random_strategy1(
            seed=self.password_img, size=self.block_num_h * self.block_num_w, block_shape=self.block_h * self.block_w,
        )

    def embed(self) -> np.ndarray:
        assert self.block_num_h * self.block_num_w > self.wm_size, "水印大小超过图片容量"
        embed_ca = np.zeros_like(self.ca)
        embed_yuv = np.zeros_like(self.img_YUV)
        embed_img = self.img.copy()

        for channel in range(3):
            for idx1 in range(self.block_num_h):
                for idx2 in range(self.block_num_w):
                    i = idx1 * self.block_num_w + idx2
                    slice1 = slice(idx1 * self.block_h, idx1 * self.block_h + self.block_h)
                    slice2 = slice(idx2 * self.block_w, idx2 * self.block_w + self.block_w)
                    wm_1 = self.wm_bit[i % self.wm_size]
                    embed_ca[slice1, slice2, channel] = \
                        self.block_add_wm_1(self.ca[slice1, slice2, channel], self.idx_shuffle[i], wm_1)

            # 逆变换回去
            embed_yuv[:, :, channel] = idwt2((embed_ca[:, :, channel], self.hvd[channel]), "haar")

        embed_img[:self.img_h_align, :self.img_w_align, :] = \
            cv2.cvtColor(embed_yuv.astype(np.float32), cv2.COLOR_YUV2BGR).clip(min=0, max=255)

        # 透明通道原样加回去
        if self.alpha is not None:
            embed_img = cv2.merge([embed_img.astype(np.uint8), self.alpha])
        return embed_img

    def read_wm(self, wm_bit):
        self.wm_bit = wm_bit
        self.wm_size = wm_bit.size

    def block_add_wm_1(self, block, shuffler, wm_1) -> np.ndarray:
        # dct->(flatten->加密->逆flatten)->svd->打水印->逆svd->(flatten->解密->逆flatten)->逆dct
        block_dct = dct(block)

        # 加密（打乱顺序）
        block_dct_shuffled = block_dct.flatten()[shuffler].reshape(self.block_shape)
        u, s, v = svd(block_dct_shuffled)
        s[0] = (s[0] // self.d1 + 1 / 4 + 1 / 2 * wm_1) * self.d1
        if self.d2:
            s[1] = (s[1] // self.d2 + 1 / 4 + 1 / 2 * wm_1) * self.d2

        block_dct_flatten = (u @ np.diag(s) @ v).flatten()
        block_dct_flatten[shuffler] = block_dct_flatten.copy()
        return idct(block_dct_flatten.reshape(self.block_shape))

    def block_get_wm_1(self, block, shuffler):
        # dct->flatten->加密->逆flatten->svd->解水印
        block_dct_shuffled = dct(block).flatten()[shuffler].reshape(self.block_shape)
        u, s, v = svd(block_dct_shuffled)
        wm = (s[0] % self.d1 > self.d1 / 2) * 1
        if self.d2:
            tmp = (s[1] % self.d2 > self.d2 / 2) * 1
            wm = (wm * 3 + tmp * 1) / 4
        return wm

    def block_add_wm_fast(self, block, shuffler, wm_1) -> np.ndarray:
        # dct->svd->打水印->逆svd->逆dct
        u, s, v = svd(dct(block))
        s[0] = (s[0] // self.d1 + 1 / 4 + 1 / 2 * wm_1) * self.d1
        return idct(u @ np.diag(s) @ v)

    def block_get_wm_fast(self, block, shuffler):
        # dct->svd->解水印
        u, s, v = svd(dct(block))
        return (s[0] % self.d1 > self.d1 / 2) * 1

    def extract_raw(self, img):
        # 每个分块提取 1 bit 信息
        self.read_img_arr(img=img)

        wm_block_bit = np.zeros(shape=(3, self.block_num_h * self.block_num_w))  # 3个channel，length 个分块提取的水印，全都记录下来

        for channel in range(3):
            for idx1 in range(self.block_num_h):
                for idx2 in range(self.block_num_w):
                    i = idx1 * self.block_num_w + idx2
                    slice1 = slice(idx1 * self.block_h, idx1 * self.block_h + self.block_h)
                    slice2 = slice(idx2 * self.block_w, idx2 * self.block_w + self.block_w)
                    wm_block_bit[channel, i] \
                        = self.block_get_wm_1(self.ca[slice1, slice2, channel], self.idx_shuffle[i])

        return wm_block_bit

    def extract_avg(self, wm_block_bit):
        # 对循环嵌入+3个 channel 求平均
        wm_avg = np.zeros(shape=self.wm_size)
        for i in range(self.wm_size):
            wm_avg[i] = wm_block_bit[:, i::self.wm_size].mean()
        return wm_avg

    def extract(self, img, wm_shape):
        self.wm_size = np.array(wm_shape).prod()

        # 提取每个分块埋入的 bit：
        wm_block_bit = self.extract_raw(img=img)
        # 做平均：
        wm_avg = self.extract_avg(wm_block_bit)
        return wm_avg

    def extract_with_kmeans(self, img, wm_shape):
        wm_avg = self.extract(img=img, wm_shape=wm_shape)
        return one_dim_kmeans(wm_avg)


def one_dim_kmeans(inputs):
    threshold = 0
    e_tol = 10 ** (-6)
    center = [inputs.min(), inputs.max()]  # 1. 初始化中心点
    for i in range(300):
        threshold = (center[0] + center[1]) / 2
        is_class01 = inputs > threshold  # 2. 检查所有点与这k个点之间的距离，每个点归类到最近的中心
        center = [inputs[~is_class01].mean(), inputs[is_class01].mean()]  # 3. 重新找中心点
        if np.abs((center[0] + center[1]) / 2 - threshold) < e_tol:  # 4. 停止条件
            threshold = (center[0] + center[1]) / 2
            break

    is_class01 = inputs > threshold
    return is_class01


def random_strategy1(seed, size, block_shape):
    return np.random.RandomState(seed) \
        .random(size=(size, block_shape)) \
        .argsort(axis=1)


def random_strategy2(seed, size, block_shape):
    # same with all blocks
    one_line = np.random.RandomState(seed) \
        .random(size=(1, block_shape)) \
        .argsort(axis=1)

    return np.repeat(one_line, repeats=size, axis=0)
