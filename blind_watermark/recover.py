import cv2
import numpy as np


def match_template(image, template, scale):
    w, h = int(template.shape[1] * scale), int(template.shape[0] * scale)
    resized = cv2.resize(template, dsize=(w, h))
    res = cv2.matchTemplate(image, resized, cv2.TM_CCOEFF_NORMED)
    ind = np.unravel_index(np.argmax(res, axis=None), res.shape)
    return ind, res[ind], scale


def search_template(image, template, scale=(0.5, 2), search_num=200):
    # 局部暴力搜索算法，寻找最优的scale
    tmp = []
    min_scale, max_scale = scale

    max_scale = min(max_scale, image.shape[0] / template.shape[0], image.shape[1] / template.shape[1])

    max_idx = 0

    for i in range(2):
        for scale in np.linspace(min_scale, max_scale, search_num):
            ind, score, scale = match_template(image, template, scale)
            tmp.append([ind, score, scale])

        # 寻找最佳
        max_idx = 0
        max_score = 0
        for idx, (ind, score, scale) in enumerate(tmp):
            if score > max_score:
                max_idx, max_score = idx, score

        min_scale, max_scale = tmp[max(0, max_idx - 1)][2], tmp[max(0, max_idx + 1)][2]

        # search_num = (max_scale - min_scale) * max(template.shape[1], template.shape[0])
        # search_num = int(search_num+1)
        search_num = 6

    return tmp[max_idx]


def estimate_crop_parameters(original_file, template_file, scale=(0.5, 2), search_num=200):
    # 推测攻击后的图片，在原图片中的位置、大小
    template = cv2.imread(template_file, cv2.IMREAD_GRAYSCALE)  # template image
    image = cv2.imread(original_file, cv2.IMREAD_GRAYSCALE)  # image

    ind, score, scale_infer = search_template(image, template, scale=scale, search_num=search_num)
    w, h = int(template.shape[1] * scale_infer), int(template.shape[0] * scale_infer)
    x1, y1, x2, y2 = ind[0], ind[1], ind[0] + h, ind[1] + w
    return (x1, y1, x2, y2), image.shape, score, scale


def recover_crop(template_file, output_file_name, loc, image_o_shape):
    (x1, y1, x2, y2) = loc
    template_o = cv2.imread(template_file)  # template image

    img_recovery = np.zeros((image_o_shape[0], image_o_shape[1], 3))

    img_recovery[x1:x2, y1:y2, :] = cv2.resize(template_o, dsize=(y2 - y1, x2 - x1))

    cv2.imwrite(output_file_name, img_recovery)


def recover_crop2(original_file, template_file, output_file_name, scale=(0.5, 2), search_num=200):
    template_o = cv2.imread(template_file)  # template image

    (x1, y1, x2, y2), image_o_shape, score, scale_infer = estimate_crop_parameters(original_file, template_file,
                                                                                   scale=scale,
                                                                                   search_num=search_num)

    img_recovery = np.zeros((image_o_shape[0], image_o_shape[1], 3))

    img_recovery[x1:x2, y1:y2, :] = cv2.resize(template_o, dsize=(y2 - y1, x2 - x1))

    cv2.imwrite(output_file_name, img_recovery)


def recover_crop1(original_file, template_file, output_file_name, scale=(0.5, 2), search_num=200):
    template_o = cv2.imread(template_file)  # template image
    image_o = cv2.imread(original_file)  # image

    # 推测位置、大小
    template = cv2.cvtColor(template_o, cv2.COLOR_BGR2GRAY)
    image = cv2.cvtColor(image_o, cv2.COLOR_BGR2GRAY)
    ind, score, scale_infer = search_template(image, template, scale=(0.5, 2), search_num=200)

    w, h = int(template.shape[1] * scale_infer), int(template.shape[0] * scale_infer)

    img_recovery = np.zeros_like(image_o)

    img_recovery[ind[0]:ind[0] + h, ind[1]:ind[1] + w, :] = cv2.resize(template_o, dsize=(w, h))

    cv2.imwrite(output_file_name, img_recovery)
    return ind, score, scale_infer
