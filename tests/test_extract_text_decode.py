import unittest

import numpy as np

from blind_watermark.blind_watermark import WaterMark


class ExtractTextDecodeTest(unittest.TestCase):
    def test_extract_str_pads_odd_length_hex(self):
        bwm = WaterMark(password_img=1, password_wm=1)
        bwm.extract_decrypt = lambda wm_avg: wm_avg
        bwm.bwm_core.extract_with_kmeans = lambda img, wm_shape: np.array([1, 1, 1, 1])

        wm = bwm.extract(embed_img=np.zeros((4, 4, 3)), wm_shape=4, mode='str')

        self.assertEqual(wm, '\x0f')


if __name__ == '__main__':
    unittest.main()
