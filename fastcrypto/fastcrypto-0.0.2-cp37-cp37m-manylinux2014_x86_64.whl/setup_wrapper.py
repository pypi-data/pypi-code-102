# @Time    : 2021/11/17 23:31
# @Author  : tk
# @FileName: setup_wrapper.py
import os
import shutil
import platform
import version_config

def get_desc():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    demo_file = os.path.join(current_dir, 'test_py.py')
    with open(demo_file, mode='r', encoding='utf-8') as f:
        data_string = str(f.read())

    long_description_str = 'fastcrypto aes加密解密库\n\n' + '```py' + '\n' + data_string + '\n' + '```' + '\n'

    return long_description_str


def copy_dep_lib():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    if platform.system().lower() == 'windows':
        file_map = {
            'src': [
                os.path.join(current_dir, '../Release/fastcrypto.pyd'),
            ],
            'dst': [
                os.path.join(current_dir, 'fastcrypto.pyd'),
            ]
        }

    elif platform.system().lower() == 'linux':

        file_map = {
            'src': [
                os.path.join(current_dir, '../fastcrypto.so'),
            ],
            'dst': [
                os.path.join(current_dir, 'fastcrypto.so'),
            ],
        }
    src_lst = file_map['src']
    dst_lst = file_map['dst']
    for i in range(len(src_lst)):
        src = src_lst[i]
        dst = dst_lst[i]
        if os.path.exists(src):
            shutil.copyfile(src, dst)


def get_is_cross_compile():
    return version_config.BUILD_CROSSCOMPILING