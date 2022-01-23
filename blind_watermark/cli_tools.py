from optparse import OptionParser
from .blind_watermark import WaterMark

usage1 = 'blind_watermark --embed --pwd 1234 image.jpg "watermark text" embed.png'
usage2 = 'blind_watermark --extract --pwd 1234 --wm_shape 111 embed.png'
optParser = OptionParser(usage=usage1 + '\n' + usage2)

optParser.add_option('--embed', dest='work_mode', action='store_const', const='embed'
                     , help='Embed watermark into images')
optParser.add_option('--extract', dest='work_mode', action='store_const', const='extract'
                     , help='Extract watermark from images')

optParser.add_option('-p', '--pwd', dest='password', help='password, like 1234')
optParser.add_option('--wm_shape', dest='wm_shape', help='Watermark shape, like 120')

(opts, args) = optParser.parse_args()


def main():
    bwm1 = WaterMark(password_img=int(opts.password))
    if opts.work_mode == 'embed':
        if not len(args) == 3:
            print('Error! Usage: ')
            print(usage1)
            return
        else:
            bwm1.read_img(args[0])
            bwm1.read_wm(args[1], mode='str')
            bwm1.embed(args[2])
            print('Embed succeed! to file ', args[2])
            print('Put down watermark size:', len(bwm1.wm_bit))

    if opts.work_mode == 'extract':
        if not len(args) == 1:
            print('Error! Usage: ')
            print(usage2)
            return

        else:
            wm_str = bwm1.extract(filename=args[0], wm_shape=int(opts.wm_shape), mode='str')
            print('Extract succeed! watermark is:')
            print(wm_str)


'''
python -m blind_watermark.cli_tools --embed --pwd 1234 examples/pic/ori_img.jpeg "watermark text" examples/output/embedded.png
python -m blind_watermark.cli_tools --extract --pwd 1234 --wm_shape 111 examples/output/embedded.png


cd examples
blind_watermark --embed --pwd 1234 examples/pic/ori_img.jpeg "watermark text" examples/output/embedded.png
blind_watermark --extract --pwd 1234 --wm_shape 111 examples/output/embedded.png
'''
