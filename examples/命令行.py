# encoding:utf-8


from blind_watermark import WaterMark


def get_value(value_get, str_info):
    attempts = 0
    success = False
    while attempts < 30000 and not success:
        try:

            value = int(input(str_info + "\n"))
            success = True
        except:
            print("输入错误请重新输入")
            attempts += 1
            if attempts == 3000:
                break
    return value


def get_str(str_get, str_info):
    attempts = 0
    success = False
    while attempts < 3000 and not success:
        try:

            str_get = str(input(str_info + "\n"))
            success = True
        except:
            print("输入错误请重新输入" + str_info)
            attempts += 1
            if attempts == 3000:
                break
    return str_get


def mod_1():
    attempts = 0
    success = False
    while attempts < 3000 and not success:
        try:
            print("默认工作模式：")
            password_wm = 123
            password_img = 123
            password_wm = get_value(password_wm, "请输入水印加密密码，只能是数字组合")
            password_img = get_value(password_img, "请输入原图加密密码，只能是数字组合")
            bwm1 = WaterMark(password_wm, password_img)
            print("请将你的原图放置于yuantu文件夹下")
            yuantu_name_head = "abc"
            yuantu_name_head = get_str(yuantu_name_head, "输入你的原图文件名,要带后缀,例如：abc.png/abc.jpg|不支持带汉字文件名")
            yuantu_name = 'yuantu/' + yuantu_name_head
            print("正在寻找" + yuantu_name + "文件")
            bwm1.read_img(yuantu_name)
            print("图片已经被读取")
            shu_liang = 50
            shu_liang = get_value(shu_liang, "输入你想生成的图片数量，目前最大支持60张，\n 你可以自行放入wm_61/wm_62...，然后输入数量即可")
            i = 1
            int(i)
            int(shu_liang)
            while i < shu_liang + 1:
                ge_shi = str('.png')
                shuiyin_tu = str('shuiyin/wm_')
                shuiyin_name = shuiyin_tu + str(i) + ge_shi
                shuchu_tu = str('shuchu/img_')
                shuchu_name = shuchu_tu + str(i) + "_" + yuantu_name_head
                str(shuiyin_name)
                str(shuchu_name)
                print(shuiyin_name + "水印读取中")
                print(shuchu_name + "输出图生成中")

                bwm1.read_wm(shuiyin_name)

                bwm1.embed(shuchu_name)
                print(str(i / shu_liang * 100) + "%已经完成")
                i = i + 1


        except:
            print("程序出错，可能是你输入的图片过小，没有足够空间添加水印，或输入文件名称错误,,请从头开始")
            attempts += 1
            if attempts == 3000:
                break
    return 0


def mod_2():
    attempts = 0
    success = False
    while attempts < 3000 and not success:
        try:
            print("自定义工作模式：")
            print(
                "提示：此模式可以添加任意水印到任意图中，请注意本程序限制了水印的大小\n 以防止过大水印造成的画质损失，水印推荐使用透明底黑色标记符号或高反差图像，\n 原图越大，你可以写入的水印就越大，对于更大的图片，建议放置白底黑色二维码，\n 如果程序窗口出错，请注意出错内容中，可容纳大小提示")
            password_wm = 123
            password_img = 123
            password_wm = get_value(password_wm, "请输入水印加密密码，只能是数字组合")
            password_img = get_value(password_img, "请输入原图加密密码，只能是数字组合")
            bwm1 = WaterMark(password_wm, password_img)
            print("请将你的原图放置于yuantu文件夹下")
            yuantu_name = "abc"
            yuantu_name = get_str(yuantu_name, "输入你的原图文件名,要带后缀,例如：abc.png/abc.jpg|不支持带汉字文件名")
            yuantu_name = 'yuantu/' + yuantu_name
            print("正在寻找" + yuantu_name + "原图文件")
            bwm1.read_img(yuantu_name)
            shuiyin_name = "abc"
            shuiyin_name = get_str(shuiyin_name, "输入你的水印文件名,要带后缀,例如：abc.png/abc.jpg|不支持带汉字文件名")
            shuiyin_name = 'shuiyin/' + shuiyin_name
            print("正在寻找" + shuiyin_name + "水印文件")
            bwm1.read_wm(shuiyin_name)
            shuchu_name = "abc"
            shuchu_name = get_str(shuchu_name, "输入你想要的输出文件名,要带后缀,例如：abc.png/abc.jpg|不支持带汉字文件名")
            shuchu_name = 'shuchu/' + shuchu_name
            print("正在输出" + shuchu_name + "已加水印文件,请等待结束提示")
            bwm1.embed(shuchu_name)
            print("输出完毕\n\n\n\n")


        except:
            print("程序出错，可能是你输入的图片过小，没有足够空间添加水印，或输入文件名称错误,请从头开始")
            attempts += 1
            if attempts == 3000:
                break
    return 0


def mod_3():
    attempts = 0
    success = False
    while attempts < 3000 and not success:
        try:
            print("图片水印解密模式：")
            print("请将你需要解密文件放置于jiemi文件夹下")
            jiemi_name = "abc"
            jiemi_name = get_str(jiemi_name, "输入你想要解密的文件名,要带后缀,例如：abc.png/abc.jpg|不支持带汉字文件名")
            jiemi_name = 'jiemi/' + jiemi_name
            print("正在寻找" + jiemi_name + "待解密文件")
            password_wm = 123
            password_img = 123
            password_wm = get_value(password_wm, "请输入水印加密密码，只能是数字组合")
            password_img = get_value(password_img, "请输入原图加密密码，只能是数字组合")
            bwm1 = WaterMark(password_wm, password_img)
            print("请输入你曾经对这张图加的水印尺寸：例如如果你的水印是640 x 480的，则它的长是640，宽是480，如果是使用默认水印，请两次输入100 \n")
            x = 0
            y = 0
            x = get_value(x, "请输入长:")
            y = get_value(y, "请输入宽:")
            print("你输入的长宽是%dx%d" % (x, y))
            print("正在运行。请等待结束提示")

            bwm1.extract(filename=jiemi_name, wm_shape=(x, y), out_wm_name='shuchu/jiemi.png', )
            print("解密数据已经输出到shuichu文件夹下，名称为jiemi.png\n\n\n\n")


        except:
            print("程序出错，可能是输入文件名称或水印参数错误,,请从头开始")
            attempts += 1
            if attempts == 3000:
                break
    return 0


def batch_embed():
    pass


def batch_extract():
    pass

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
        /res：程序的输出。打上盲水印的图（功能1），或者解出的水印（功能2）
    复制此程序时，请直接打包本程序所在文件夹
    
    请选择程序工作模式：
        1: 把盲水印嵌入原图
        2: 水印解密模式（需要输入密码）
    ''')

    work_mode = int(input("请选输入工作模式序号"))

    if work_mode == 1:
        batch_embed()
        print('盲水印已经批量打入，放到了文件夹 /res 下')
    elif work_mode == 2:
        batch_extract()
        print('盲水印已经批量解出，放到了文件夹 /res 下')

    else:
        print('模式选择错误')

    input('按任意键退出')

if __name__=='__main__':
    # main()
    print('本功能正在优化，近期完成（一周内）')