from optparse import OptionParser
from .blind_watermark import WaterMark

usage1 = 'blind_watermark --embed -p [pwd1]x[pwd2] image.jpg watermark.png embed.png'
usage2 = 'blind_watermark --extract -p [pwd1]x[pwd2] --wm_shape 128x128 embed.png wm_extract.png'
optParser = OptionParser(usage=usage1 + '\n' + usage2)

optParser.add_option('--embed', dest='work_mode', action='store_const', const='embed'
                     , help='Embed watermark into images')
optParser.add_option('--extract', dest='work_mode', action='store_const', const='extract'
                     , help='Extract watermark from images')

optParser.add_option('-p', '--pwd', dest='password', help='2 passwords, like 1x1')
optParser.add_option('--wm_shape', dest='wm_shape', help='Watermark shape, like 128x128')

(opts, args) = optParser.parse_args()


def main():
    print(opts)
    print(args)
    p1, p2 = opts.password.split('x')
    bwm1 = WaterMark(password_wm=int(p1), password_img=int(p2))
    if opts.work_mode == 'embed':
        if not len(args) == 3:
            print('Error! Usage: ')
            print(usage1)
            return
        else:
            bwm1.read_img(args[0])
            bwm1.read_wm(args[1])
            bwm1.embed(args[2])
            print('Embed succeed! to file ', args[2])

    if opts.work_mode == 'extract':
        if not len(args) == 2:
            print('Error! Usage: ')
            print(usage2)
            return

        else:
            shape1, shape2 = opts.wm_shape.split('x')
            bwm1.extract(filename=args[0], wm_shape=(int(shape1), int(shape2)), out_wm_name=args[1])
            print('Extract succeed! to file ', args[1])


'''
python -m blind_watermark.cli_tools --embed -p 1x1 examples/pic/ori_img.jpg examples/pic/watermark.png examples/output/embedded.png
python -m blind_watermark.cli_tools --extract -p 1x1 --wm_shape 128x128 examples/output/embedded.png examples/output/wm_extract.png


cd examples
blind_watermark --embed -p 1x1 pic/ori_img.jpg pic/watermark.png output/embedded.png
blind_watermark --extract -p 1x1 --wm_shape 128x128 output/embedded.png output/wm_extract.png
'''
