# -*- coding: utf-8 -*-
# @Time    : 2021/11/17 14:38
# @Author  : wyw

import os
import platform
import shutil
import version_config

def get_desc():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # long_description_str = title
    # long_description_str += '\n\n'

    long_description_str = ''

    def load_file(demo_file):
        with open(demo_file, mode='r', encoding='utf-8') as f:
            data_string = str(f.read())
        return data_string

    data_string = load_file(os.path.join(current_dir, 'readme.py'))
    long_description_str += '```py' + '\n' + data_string + '\n' + '```' + '\n'

    data_string = load_file(os.path.join(current_dir, 'test_py.py'))
    long_description_str += '```py' + '\n' + data_string + '\n' + '```' + '\n'

    data_string = load_file(os.path.join(current_dir, 'nn_sdk.java'))
    long_description_str += 'nn-sdk.java java包demo,配置参考python \n\n' + '```java' + '\n' + data_string + '\n' + '```' + '\n'

    data_string = load_file(os.path.join(current_dir, 'nn_sdk.h'))
    data_string += '\n\n'
    data_string += load_file(os.path.join(current_dir, 'test.c'))
    long_description_str += 'nn-sdk c包 \n\n' + '```c' + '\n' + data_string + '\n' + '```' + '\n'

    data_string = load_file(os.path.join(current_dir, 'test_aes.py'))
    long_description_str += 'aes加密示例 \n\n' + '```py' + '\n' + data_string + '\n' + '```' + '\n'

    return long_description_str


def copy_dep_lib():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    if platform.system().lower() == 'windows':
        file_map = {
            'src': [
                os.path.join(current_dir, '../Release/engine_csdk.pyd'),
                os.path.join(current_dir, '../../cxx_module/Release/fasttext_inf.dll')
            ],
            'dst': [
                os.path.join(current_dir, 'engine_csdk.pyd'),
                os.path.join(current_dir, 'fasttext_inf.dll')
            ]
        }

    elif platform.system().lower() == 'linux':

        file_map = {
            'src': [
                os.path.join(current_dir, '../engine_csdk.so'),
                os.path.join(current_dir, '../../{}/engine_trt7.so'.format( 'cxx_module')),
                os.path.join(current_dir, '../../{}/engine_trt8.so'.format( 'cxx_module')),
                os.path.join(current_dir, '../../{}/fasttext_inf.so'.format( 'cxx_module_cross_compile' if version_config.NN_SDK_CROSSCOMPILING else 'cxx_module'))
            ],
            'dst': [
                os.path.join(current_dir, 'engine_csdk.so'),
                os.path.join(current_dir, 'engine_trt7.so'),
                os.path.join(current_dir, 'engine_trt8.so'),
                os.path.join(current_dir, 'fasttext_inf.so')
            ],
        }
    src_lst = file_map['src']
    dst_lst = file_map['dst']
    for i in range(len(src_lst)):
        src = src_lst[i]
        dst = dst_lst[i]
        if os.path.exists(src):
            shutil.copyfile(src, dst)

def get_package_version():

    package_version = str(version_config.NN_SDK_VERSION_MAJOR) + '.' + \
                      str(version_config.NN_SDK_VERSION_MINOR) + '.' + \
                      str(version_config.NN_SDK_VERSION_PATCH)
    return package_version

def get_is_cross_compile():
    return version_config.NN_SDK_CROSSCOMPILING