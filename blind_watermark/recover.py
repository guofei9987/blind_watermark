import cv2
import numpy as np

import functools


# 一个帮助缓存化加速的类，引入事实上的全局变量
class MyValues:
    def __init__(self):
        self.idx = 0
        self.image, self.template = None, None

    def set_val(self, image, template):
        self.idx += 1
        self.image, self.template = image, template


my_value = MyValues()


@functools.lru_cache(maxsize=None, typed=False)
def match_template(w, h, idx):
    image, template = my_value.image, my_value.template
    resized = cv2.resize(template, dsize=(w, h))
    scores = cv2.matchTemplate(image, resized, cv2.TM_CCOEFF_NORMED)
    ind = np.unravel_index(np.argmax(scores, axis=None), scores.shape)
    return ind, scores[ind]


def match_template_by_scale(scale):
    image, template = my_value.image, my_value.template
    w, h = round(template.shape[1] * scale), round(template.shape[0] * scale)
    ind, score = match_template(w, h, idx=my_value.idx)
    return ind, score, scale


def search_template(scale=(0.5, 2), search_num=200):
    image, template = my_value.image, my_value.template
    # 局部暴力搜索算法，寻找最优的scale
    tmp = []
    min_scale, max_scale = scale

    max_scale = min(max_scale, image.shape[0] / template.shape[0], image.shape[1] / template.shape[1])

    max_idx = 0

    for i in range(2):
        for scale in np.linspace(min_scale, max_scale, search_num):
            ind, score, scale = match_template_by_scale(scale)
            tmp.append([ind, score, scale])

        # 寻找最佳
        max_idx = 0
        max_score = 0
        for idx, (ind, score, scale) in enumerate(tmp):
            if score > max_score:
                max_idx, max_score = idx, score

        min_scale, max_scale = tmp[max(0, max_idx - 1)][2], tmp[min(len(tmp) - 1, max_idx + 1)][2]

        search_num = 2 * int((max_scale - min_scale) * max(template.shape[1], template.shape[0])) + 1

    return tmp[max_idx]


def estimate_crop_parameters(original_file=None, template_file=None, ori_img=None, tem_img=None
                             , scale=(0.5, 2), search_num=200):
    # 推测攻击后的图片，在原图片中的位置、大小
    if template_file:
        tem_img = cv2.imread(template_file, cv2.IMREAD_GRAYSCALE)  # template image
    if original_file:
        ori_img = cv2.imread(original_file, cv2.IMREAD_GRAYSCALE)  # image

    if scale[0] == scale[1] == 1:
        # 不缩放
        scale_infer = 1
        scores = cv2.matchTemplate(ori_img, tem_img, cv2.TM_CCOEFF_NORMED)
        ind = np.unravel_index(np.argmax(scores, axis=None), scores.shape)
        ind, score = ind, scores[ind]
    else:
        my_value.set_val(image=ori_img, template=tem_img)
        ind, score, scale_infer = search_template(scale=scale, search_num=search_num)
    w, h = int(tem_img.shape[1] * scale_infer), int(tem_img.shape[0] * scale_infer)
    x1, y1, x2, y2 = ind[1], ind[0], ind[1] + w, ind[0] + h
    return (x1, y1, x2, y2), ori_img.shape, score, scale_infer


def recover_crop(template_file=None, tem_img=None, output_file_name=None, loc=None, image_o_shape=None):
    if template_file:
        tem_img = cv2.imread(template_file)  # template image

    (x1, y1, x2, y2) = loc

    img_recovered = np.zeros((image_o_shape[0], image_o_shape[1], 3))

    img_recovered[y1:y2, x1:x2, :] = cv2.resize(tem_img, dsize=(x2 - x1, y2 - y1))

    if output_file_name:
        cv2.imwrite(output_file_name, img_recovered)
    return img_recovered
