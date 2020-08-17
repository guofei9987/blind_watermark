from setuptools import setup, find_packages
from os import path as os_path
import blind_watermark

this_directory = os_path.abspath(os_path.dirname(__file__))


# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(name='blind_watermark',
      python_requires='>=3.5',
      version=blind_watermark.__version__,
      description='Blind Watermark in Python',
      long_description=read_file('docs/en/README.md'),
      long_description_content_type="text/markdown",
      url='https://github.com/guofei9987/blind_watermark',
      author='Guo Fei',
      author_email='guofei9987@foxmail.com',
      license='MIT',
      packages=find_packages(),
      platforms=['linux', 'windows', 'macos'],
      install_requires=['numpy', 'opencv-python'],
      zip_safe=False)
