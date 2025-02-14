from ty_api_test.page.lixiangtaizhang import *
from ty_api_test.page.daibanjihe import *


class Test_tzb:

#1.立项管理
    def test_lx1(self):
        """验证查看详情"""
        lx = Lxtz()
        lx.lx_info()
    def test_lx2(self):
        """验证查询功能"""
        lx = Lxtz()
        lx.lx_search()
    def test_lx3(self):
        """验证创建立项项目成功/暂存立项资料"""
        lx = Lxtz()
        id = lx.lx_create_project()
        lx.lx_save1(id)
    def test_lx3(self):
        """验证项目评审和决策情况保存成功"""
        lx = Lxtz()
        id = lx.lx_create_project()
        lx.lx_save1(id)
        lx.lx_save2(id)
    def test_lx4(self):
        """验证立项项目提交稽核成功"""
        lx = Lxtz()
        id = lx.lx_create_project()
        lx.lx_save1(id)
        lx.lx_save2(id)
        lx.lx_submit(id)
    def test_lx5(self):
        """立项待办任务-二级单位稽核人稽核通过"""
        db1 = Dbjh('User3','Password3')
        db1.jude_pass(1,'立项待办任务')
    def test_lx6(self):
        """立项待办任务-二级单位稽核人稽核驳回"""
        db1 = Dbjh('User3','Password3')
        db1.jude_reject(1,'立项待办任务')
    def test_lx7(self):
        """立项待办任务-总部审定人稽核通过"""
        db1 = Dbjh('User2','Password2')
        db1.jude_pass(1,'立项待办任务')
    def test_lx8(self):
        """立项待办任务-总部审定人稽核驳回"""
        db1 = Dbjh('User3','Password3')
        db1.jude_reject(1,'立项待办任务')

#可研管理
    # def test_kytz(self):


#实施许可令管理


if __name__ == '__main__':
    pass