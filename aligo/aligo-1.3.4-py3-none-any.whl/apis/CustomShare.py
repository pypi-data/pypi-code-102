"""自定义分享"""
import base64
import json
from typing import List, Dict

from aligo.core import *
from aligo.request import *
from aligo.types import *
from aligo.types.Enum import *


class CustomShare(Core):
    """..."""

    _ALIGO_SHARE_SCHEMA = 'aligo://'

    @staticmethod
    def __share_files_by_aligo(files: List[BaseFile]) -> List:
        """..."""
        result = []
        for file in files:
            result.append({
                'name': file.name,
                'content_hash': file.content_hash,
                'size': file.size,
                'url': file.download_url
            })
        return result

    @staticmethod
    def share_files_by_aligo(files: List[BaseFile]) -> str:
        """..."""
        result = CustomShare.__share_files_by_aligo(files)
        return CustomShare._ALIGO_SHARE_SCHEMA + base64.b64encode(json.dumps(result).encode()).decode()

    def __share_folder_by_aligo(self, parent_file_id: str, drive_id: str = None) -> List:
        """..."""
        result = []
        files = []
        # 1. 获取 parent_file_id 目录下文件列表
        for file in self._core_get_file_list(GetFileListRequest(parent_file_id=parent_file_id, drive_id=drive_id)):
            if file.type == 'file':
                # 2. 如果是文件, 添加到 files
                files.append(file)
                continue
            # 3. 否则是文件夹, 递归
            result.append([file.name, self.__share_folder_by_aligo(parent_file_id=file.file_id, drive_id=drive_id)])
        result.append(self.__share_files_by_aligo(files))
        return result

    def share_folder_by_aligo(self, parent_file_id: str, drive_id: str = None) -> str:
        """..."""
        result = self.__share_folder_by_aligo(parent_file_id=parent_file_id, drive_id=drive_id)
        if parent_file_id != 'root':
            folder = self._core_get_file(GetFileRequest(file_id=parent_file_id))
            result = [[folder.name, result]]
        else:
            result = [['root', result]]
        return CustomShare._ALIGO_SHARE_SCHEMA + base64.b64encode(json.dumps(result).encode()).decode()

    def __save_files_by_aligo(self, data: str, parent_file_id: str = 'root',
                              check_name_mode: CheckNameMode = 'auto_rename',
                              drive_id: str = None):
        result = []

        # data 肯定是list, 内含 文件夹 list 或文件 dict
        for obj in data:

            if isinstance(obj, dict):
                x = self.create_by_hash(
                    name=obj['name'], content_hash=obj['content_hash'],
                    size=obj['size'], url=obj['url'], parent_file_id=parent_file_id,
                    check_name_mode=check_name_mode, drive_id=drive_id)
                result.append(x)
                continue

            if len(obj) > 0 and isinstance(obj[0], str):
                # 创建文件夹
                folder = self._core_create_folder(CreateFolderRequest(name=obj[0], parent_file_id=parent_file_id,
                                                                      drive_id=drive_id))
                x = self.__save_files_by_aligo(obj[1], parent_file_id=folder.file_id)
                result.append((folder, x))
                continue

            file: Dict
            for file in obj:
                x = self.create_by_hash(
                    name=file['name'], content_hash=file['content_hash'],
                    size=file['size'], url=file['url'], parent_file_id=parent_file_id,
                    check_name_mode=check_name_mode, drive_id=drive_id)
                result.append(x)

        return result

    def save_files_by_aligo(self, data: str, parent_file_id: str = 'root',
                            check_name_mode: CheckNameMode = 'auto_rename',
                            drive_id: str = None):
        """..."""
        if not data.startswith(self._ALIGO_SHARE_SCHEMA):
            self._auth.log.warning(f'这不是合法 aligo 分享协议: {data}')
            return

        data = data[8:]
        data = json.loads(base64.b64decode(data))

        result = self.__save_files_by_aligo(data, parent_file_id, check_name_mode, drive_id)
        return result
