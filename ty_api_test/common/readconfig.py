#conding=utf-8
import os
import configparser

#HOST = 'HOST'
# 项目目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   #os.path.abspath（）返回绝对路径；os.path.dirname()返回目录路径
                                                                       #__file__ 查看模块的源文件路径
# 配置文件
INI_PATH = os.path.join(BASE_DIR, 'config', 'config.ini')

class Readconfig:
    """配置文件"""

    def __init__(self,host):
        if not os.path.exists(INI_PATH):     #os.path.exists() 如果路径存在，返回ture；反之，返回false
            raise FileNotFoundError("配置文件%s不存在！" % INI_PATH)
        self.config = configparser.RawConfigParser()   #配置文件解析器,当有%的符号时请使用Raw读取,一般用ConfigParser()就可以
        self.config.read(INI_PATH, encoding='utf-8')
        #print(self.config.sections()) #返回的section，当前config.ini有2个section,即[HOST]、[HOST-TZB]
        self.HOST = host
    def _get(self, section, option):
        """获取"""
        return self.config.get(section, option)

    def _set(self, section, option, value):
        """更新"""
        self.config.set(section, option, value)
        with open(INI_PATH, 'w') as f:
            self.config.write(f)

    @property
    def host(self):
        return self._get(self.HOST, self.HOST)  #第一个HOST是section,第二个HOST 是[HOST]下的键值对的value值


if __name__ == '__main__':
    ini = Readconfig('User1')
    print(ini.host)