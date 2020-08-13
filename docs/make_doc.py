# 不想用 Sphinx，也不像弄一堆静态html文件，所以自己写个咯


'''
需要从readme中解析出：
1. "-> Demo code: [examples/demo_pso.py](examples/demo_pso.py)"
2. 三个```python为开头，三个 ``` 为结尾
3. 从py文件中读出文本，并替换
4. 前几行是求star，只在readme中出现


需要从py文件中解析出：
1. # %% 做断点后赋予index值，然后插入readme
'''
import os
import sys

import re


def search_code(py_file_name, section_idx):
    '''
    给定py文件名和section序号，返回一个list，内容是py文件中的code（markdown格式）
    :param py_file_name:
    :param section_idx:
    :return:
    '''
    with open('../' + py_file_name, encoding='utf-8', mode="r") as f:
        content = f.readlines()
    content_new, i, search_idx, idx_first_match = [], 0, 0, None
    while i < len(content) and search_idx <= section_idx:
        if content[i].startswith('# %%'):
            search_idx += 1
            i += 1  # 带井号百分号的那一行也跳过去，不要放到文档里面
        if search_idx < section_idx:
            pass
        elif search_idx == section_idx:
            idx_first_match = idx_first_match or i  # record first match line
            content_new.append(content[i])
        i += 1
    return [
               '-> Demo code: [{py_file_name}#s{section_idx}](https://github.com/guofei9987/scikit-opt/blob/master/{py_file_name}#L{idx_first_match})\n'.
                   format(py_file_name=py_file_name, section_idx=section_idx + 1, idx_first_match=idx_first_match),
               '```python\n'] \
           + content_new \
           + ['```\n']


# %%


def make_doc(origin_file):
    with open(origin_file, encoding='utf-8', mode="r") as f_readme:
        readme = f_readme.readlines()

    regex = re.compile('\[examples/[\w#.]+\]')
    readme_idx = 0
    readme_new = []
    while readme_idx < len(readme):
        readme_line = readme[readme_idx]
        if readme_line.startswith('-> Demo code: ['):
            # 找到中括号里面的内容，解析为文件名，section号
            py_file_name, section_idx = regex.findall(readme[readme_idx])[0][1:-1].split('#s')
            section_idx = int(section_idx) - 1

            print('插入代码: ', py_file_name, section_idx)
            content_new = search_code(py_file_name, section_idx)
            readme_new.extend(content_new)

            # 往下寻找第一个代码结束位置
            while readme[readme_idx] != '```\n':
                readme_idx += 1
        else:
            # 如果不需要插入代码，就用原本的内容
            readme_new.append(readme_line)

        readme_idx += 1
    return readme_new


# 主页 README 和 en/README
readme_new = make_doc(origin_file='../README.md')
with open('../README.md', encoding='utf-8', mode="w") as f_readme:
    f_readme.writelines(readme_new)

with open('en/README.md', encoding='utf-8', mode="w") as f_readme_en:
    f_readme_en.writelines(readme_new[20:])

docs = ['zh/README.md',
        'zh/more_ga.md', 'en/more_ga.md',
        'zh/more_pso.md', 'en/more_pso.md',
        'zh/more_sa.md', 'en/more_sa.md',
        ]
for i in docs:
    docs_new = make_doc(origin_file=i)
    with open(i, encoding='utf-8', mode="w") as f:
        f.writelines(docs_new)

sys.exit()
