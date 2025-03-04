#待办稽核相关操作
from time import sleep

import requests
from ty_api_test.common.logger import *
from ty_api_test.page.login_api import login
from ty_api_test.common.readconfig import *
from ty_api_test.common.readapi import *
import json


class Dbjh:
    """待办任务相关操作封装"""
    def __init__(self,user,password):
        self.authorization,self.userid = login(u=user, p=password)
    def get_task(self, businesstype= ''):
        """获取待办任务"""
        authorization = self.authorization
        userid = self.userid
        # print(authorization)
        # print(userid)
        host = Readconfig('HOST-TZB').host
        api = Api('api')['待办任务']
        # print(api)
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}",
            'Content-Type': 'application/json'
        }
        data = json.dumps({
            "pageNum": 1,
            "pageSize": 10,
            "userId": userid,
            "status": "PENDING",
            "businessType": businesstype,
            "sord": "desc",
            "jsonQueryFields": [
            ]
        })
        # print(data)
        response = requests.post(url, data, headers=headers)
        # print(response.json())
        assert response.status_code == 200

        data1 = response.json()['data']
        datalist = data1['list']
        #print(datalist)
        # print(len(datalist))
        num = len(datalist)
        businessid_list =[]
        taskid_list = []
        for i in range(num):
            a = datalist[i]
            businessid_list.append(a['businessId'])
            taskid_list.append(a['taskId'])
            i+=1
        print(businessid_list)
        print(taskid_list)
        print(num)
        return businessid_list,taskid_list,num
    def lx_jude_pass(self,excuted_num=1):
        """立项待办任务稽核通过"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['立项稽核']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}",
            'Content-Type': 'application/json'
        }
        businessId_list, taskId_list, num = self.get_task("1")
        # businessType=1,立项项目；2,可研项目；3，实施许可令；97，项目中止恢复；98，项目中止；99，项目终止
        if num>=excuted_num:
            for i in range(excuted_num):
                data = json.dumps({
                    "status": "APPROVE",
                    "result": "通过",
                    "establishId": f"{businessId_list[i]}",
                    "taskId": f"{taskId_list[i]}",
                    "comments": "稽核测试通过"
                })
                response = requests.post(url, headers=headers, data=data)
                assert response.status_code == 200
                #print(response.json())
                log.debug(f'第{i+1}条立项待办任务审核通过成功')
                i+=1
        else:
            log.debug(f"暂时没有{excuted_num}条待办任务")


    def ky_jude_pass(self,excuted_num=1):
        """可研待办任务稽核通过"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['可研稽核']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}",
            'Content-Type': 'application/json'
        }
        businessId_list,taskId_list,num = self.get_task("2")
        # businessType=1,立项项目；2,可研项目；3，实施许可令；97，项目中止恢复；98，项目中止；99，项目终止
        if num>=excuted_num:
            for i in range(excuted_num):
                # businessId = businessId_list[i]
                # taskId = taskId_list[i]
                data = json.dumps({
                    "status": "APPROVE",
                    "result": "通过",
                    "businessId": f"{businessId_list[i]}",
                    "taskId": f"{taskId_list[i]}",
                    "comments": "稽核测试通过"
                })
                response = requests.post(url, headers=headers, data=data)
                assert response.status_code == 200
                #print(response.json())
                log.debug(f'第{i+1}条可研待办任务审核通过成功')
                i+=1
        else:
            log.debug(f"暂时没有{excuted_num}条待办任务")
    def lx_jude_reject(self,excuted_num=1):
        """立项待办任务稽核驳回"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['立项稽核']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}",
            'Content-Type': 'application/json'
        }
        businessId_list, taskId_list, num = self.get_task("1")
        # businessType=1,立项项目；2,可研项目；3，实施许可令；97，项目中止恢复；98，项目中止；99，项目终止
        if num>=excuted_num:
            for i in range(excuted_num):
                data = json.dumps({
                    "status": "REJECTED",
                    "result": "拒绝",
                    "establishId": f"{businessId_list[i]}",
                    "taskId": f"{taskId_list[i]}",
                    "comments": "稽核测试驳回"
                })
                response = requests.post(url, headers=headers, data=data)
                assert response.status_code == 200
                #print(response.json())
                log.debug(f'第{i+1}条立项待办任务审核驳回成功')
                i+=1
        else:
            log.debug(f"暂时没有{excuted_num}条待办任务")
    def ky_jude_reject(self,excuted_num=1):
        """可研待办任务稽核驳回"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['可研稽核']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}",
            'Content-Type': 'application/json'
        }
        businessId_list, taskId_list, num = self.get_task("2")
        # businessType=1,立项项目；2,可研项目；3，实施许可令；97，项目中止恢复；98，项目中止；99，项目终止
        if num>=excuted_num:
            for i in range(excuted_num):
                data = json.dumps({
                    "status": "REJECTED",
                    "result": "拒绝",
                    "businessId": f"{businessId_list[i]}",
                    "taskId": f"{taskId_list[i]}",
                    "comments": "稽核测试驳回"
                })
                response1 = requests.post(url, headers=headers, data=data)
                print(response1.json())
                assert response1.status_code == 200
              #print(response.json())
                log.debug(f'第{i+1}条可研待办任务审核驳回成功')
                i+=1
        else:
            log.debug(f"暂时没有{excuted_num}条待办任务")

# db1 = Dbjh('User3','Password3')
#db2 = Dbjh('User2','Password2')
#User3 = wangyong6     #二级单位稽核人
#User2 = kangle1        #总部审定人
#User1 = caomeng
if __name__ == '__main__':

    # #1.1二级单位稽核人立项稽核
    # db1 = Dbjh('User3', 'Password3')
    # db1.lx_jude_pass(1)
    # db1.get_task("1")
    # sleep(1)
    # #1.2总部审定人立项审定
    # db2 = Dbjh('User2','Password2')
    # db2.lx_jude_pass(1)
    # db2.get_task("1")
    # db2.lx_jude_reject(1)
    #
    # 2.1可研稽核:
    db1 = Dbjh('User3', 'Password3')
    db1.ky_jude_pass(1)
    db1.get_task("2")
    # 2.2可研审定:
    db2 = Dbjh('User2','Password2')
    db2.ky_jude_pass(1)
    db2.get_task("2")