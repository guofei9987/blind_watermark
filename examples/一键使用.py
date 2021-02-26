from blind_watermark import WaterMark
print("开发者：evenif/风栖木兮")
print("开源代码地址：https://github.com/guofei9987/blind_watermark")
print("程序开始运行：")
print("如程序出错，请检查你的输入内容，重新打开此程序即可")
print("请注意，本程序需要和其下文件夹配合工作他们分别是:\n yuantu:放置原图\n shuiyin；存放水印\n jiemi存放等待解密文件\n shuichu输出文件夹\n 复制此程序时，请直接打包本程序所在文件夹")
#选择工作模式
#选择引擎
print("请选择程序工作模式：\n 1: 默认工作模式（自动添加一定数量水印）\n 2: 自定义模式（请在文件夹添加你的自定义水印）\n 3: 水印解密模式（需要输入密码）")

work_mode = int(input("请输入序号"))

if work_mode == 1:
	print("默认工作模式：")
	password_wm = int(input("请输入水印加密密码，（请记住此密码，解密时需要）只可以任意长度数字即可：\n"))
	password_img = int(input("请输入原图加密密码，（请记住此密码，解密时需要）只可以任意长度数字即可：\n"))
	bwm1 = WaterMark(password_wm, password_img)
	print("请将你的原图放置于yuantu文件夹下")
	yuantu_name_head = str(input("输入你的原图文件名,要带后缀哦，比如：“测试图.png“：\n"))
	yuantu_name = 'yuantu/'+yuantu_name_head
	print("正在寻找"+yuantu_name+"文件")
	bwm1.read_img(yuantu_name)
	shu_liang = int(input("输入你想生成的图片数量，目前最大支持50张哦\n"))
	i = 1
	int(i)
	int(shu_liang)
	while i < shu_liang+1:
		ge_shi = str('.png') 
		shuiyin_tu = str('shuiyin/wm_')
		shuiyin_name = shuiyin_tu+str(i)+ge_shi
		shuchu_tu = str('shuchu/img_')
		shuchu_name = shuchu_tu+str(i)+"_"+yuantu_name_head
		str(shuiyin_name)
		str(shuchu_name)
		print(shuiyin_name+"水印读取中")
		print(shuchu_name+"输出图生成中")
		print(str(i/shu_liang*100)+"%已经完成")
		bwm1.read_wm(shuiyin_name)
		
		bwm1.embed(shuchu_name)
		i =i+ 1

if work_mode == 2:
	print("自定义工作模式：")
	print("提示：此模式可以添加任意水印到任意图中，请注意本程序限制了水印的大小\n 以防止过大水印造成的画质损失，水印推荐使用透明底黑色标记符号或高反差图像，\n 原图越大，你可以写入的水印就越大，对于更大的图片，建议放置白底黑色二维码，\n 如果程序窗口出错，请注意出错内容中，可容纳大小提示")
	password_wm = int(input("请输入水印加密密码，（请记住此密码，解密时需要）只可以任意长度数字即可：\n"))
	password_img = int(input("请输入原图加密密码，（请记住此密码，解密时需要）只可以任意长度数字即可：\n"))
	bwm1 = WaterMark(password_wm, password_img)
	print("请将你的原图放置于yuantu文件夹下")
	yuantu_name = str(input("输入你的原图文件名,要带后缀哦，比如：“测试图.png“：\n"))
	yuantu_name = 'yuantu/'+yuantu_name
	print("正在寻找"+yuantu_name+"原图文件")
	bwm1.read_img(yuantu_name)
	shuiyin_name = str(input("输入你的水印文件名,要带后缀哦，比如：“shuiyin.png“：\n"))
	shuiyin_name = 'shuiyin/'+shuiyin_name
	print("正在寻找"+shuiyin_name+"水印文件")	
	bwm1.read_wm(shuiyin_name)
	shuchu_name = str(input("输入你想要输出的文件名,要带后缀哦，比如：“img_1.png“：\n"))
	shuchu_name = 'shuchu/'+shuchu_name
	bwm1.embed(shuchu_name)
	print("正在输出"+shuchu_name+"已加水印文件")
if work_mode == 3:
	print("图片水印解密模式：")
	print("请将你需要解密文件放置于jiemi文件夹下")
	jiemi_name = str(input("输入你的原图文件名,要带后缀哦，比如：“测试图.png“：\n"))
	jiemi_name = 'jiemi/'+jiemi_name
	print("正在寻找"+jiemi_name+"待解密文件")
	password_wm = int(input("请输入水印加密密码：\n"))
	password_img = int(input("请输入原图加密密码：\n"))
	bwm1 = WaterMark(password_wm, password_img)
	print("请输入你曾经加的水印尺寸：例如如果你的水印是640 x 480的，则它的长是640，宽是480 \n")
	x=int(input("请输入长:"))
	y=int(input("\n请输入宽："))
	print("你输入的长宽是%dx%d"%(x,y))
	bwm1.extract(filename=jiemi_name, wm_shape=(x, y), out_wm_name='shuchu/jiemi.png', )	
	print("解密数据已经输出到shuichu文件夹下，名称为jiemi.png")

input("程序执行完成，请检查文件夹下已经生成文件，按回车退出")
