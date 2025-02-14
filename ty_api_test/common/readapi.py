# coding=utf-8

import os
import yaml

#项目目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#api接口目录
API_PATH = os.path.join(BASE_DIR, 'data')

class Api:
    """获取api接口路径"""

    def __init__(self, name):
        self.file_name = '%s.yaml' % name
        self.api_path = os.path.join(API_PATH, self.file_name)
        if not os.path.exists(self.api_path):
            raise FileNotFoundError("%s 文件不存在！" % self.api_path)
        with open(self.api_path,encoding='utf-8') as f:
            self.data = yaml.safe_load(f)   #将yaml格式文件转换为python值；而yaml.saft_dump()将python值转换为yaml格式文件

    def __getitem__(self, item):
        """获取属性"""
        data = self.data.get(item)
        #print(self.data)
        if data:
            name, value = data.split('==')
            return value
        raise ArithmeticError("{}中不存在关键字：{}".format(self.file_name, item))

if __name__ == '__main__':
    search = Api('api')
    print(search['登录'])