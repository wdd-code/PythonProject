from ty_api_test.common.logger import *
from ty_api_test.page.login_api import login
from ty_api_test.common.readconfig import *
from ty_api_test.common.readapi import *
import urllib.parse
import requests
import json

class Ssgl:
    """实施许可令管理模块用例，相关api方法封装"""
    def __init__(self):
        self.authorization,self.userid = login()
    def ss_upload(self):
        """上传文件"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        api = Api('api')['上传文件']
        url = f"https://{host}{api}"
        headers = {
            "Authorization": f"Bearer {authorization}"
        }
        # 要上传的文件路径
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(BASE_DIR, 'Template.csv')
        if not os.path.exists(file_path):
            raise FileNotFoundError("测试文件%s不存在！" % file_path)

        # 打开文件，以二进制模式读取
        with open(file_path, 'rb') as f:
            files = {'file': f}  # 创建一个包含文件数据的字典
        # 发送POST请求，带上文件数据
            response = requests.post(url, files=files, headers=headers)
            #print(response.json())
            data = response.json()['data']
            uri = data['uri']
            filename = data['relativePathAndFileName']
            # print(uri)
            # print(filename)
            assert response.status_code == 200
        log.debug("上传文件成功")
        # print(uri)
        # print(filename)
        return uri,filename
    def ss_add_permit(self, queryname):
        """新增实施许可令，提交稽核"""
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        headers = {
            "Authorization": f"Bearer {authorization}"
        }
        # 1.查询项目名称，模糊查询
        api1 = Api('api')['可研完成的项目']
        url1 = f"https://{host}{api1}"
        projectname = urllib.parse.quote(queryname)  # 对字符串进行url编码，解码用unquote()函数
        projectname1 = f"projectName={projectname}"
        url2 = '&'.join([url1, projectname1])
        print(url2)
        response1 = requests.get(url2, headers=headers)
        print(response1.json())
        data = response1.json()['data']
        datalist = data['list']
        num = data['endRow']
        if num > 0:
            """可研完成的项目可能有多个，有些可能已经是提交稽核，用for循环来遍历尝试，直到添加成功break"""
            for i in range(num):
                # 2.查询实施许可令详情
                list_info = datalist[i]
                projectid = list_info['projectId']
                api2 = Api('api')['实施许可令详情']
                url3 = f"https://{host}{api2}"
                url_ss = '?'.join([url3, f'projectId={projectid}'])
                # print(url_ss)

                response2 = requests.get(url_ss, headers=headers)
                response_json = response2.json()
                list_info1 = response_json['data']
                print(list_info1)
                if not list_info1 or list_info1['implStatus'] == 'tb':
                # print(response_json)
                #     if ss_status == 'jh' or ss_status == 'sd' or ss_status == 'wc':
                #         """如果data数据中implStatus字段值为jh、sd,表示处于稽核、审定状态，不可编辑，需要排除"""
                #         log.debug("当前项目处于稽核、审定、完成状态，不可编辑，需要排除")
                #         print("当前项目处于稽核、审定、完成状态，不可编辑，需要排除")
                #         continue
                # 3.添加实施许可令/暂存
                    api3 = Api('api')['添加实施许可令']
                    url4 = f"https://{host}{api3}"
                    uri, filename = self.ss_upload()
                    data = json.dumps({
                        "id": "",
                        "projectId": f"{projectid}",
                        "implStatus": "tb",
                        "files": [
                            {
                                "dictId": "100",
                                "fileUrl": f"{uri}",
                                "fileName": f"{filename}"
                            }
                        ]
                    })
                    headers1 = {
                        "Authorization": f"Bearer {authorization}",
                        "Content-Type": "application/json"
                    }
                    response3 = requests.post(url4, data=data, headers=headers1)
                    print(response3.json())
                    data2 = response3.json()['data']
                    impllicenseid = data2['implLicenseId']
                    projectname1 = data2['projectName']
                    #4.提交稽核
                    api4 = Api('api')['实施提交稽核']
                    url5 = f"https://{host}{api4}"
                    data = json.dumps({
                        "processId": "1871457740242022401",
                        "businessId": f"{impllicenseid}",
                        "nodeUserList": [
                            {
                                "nodeId": "1871458261166170114",
                                "userId": 70557
                            },
                            {
                                "nodeId": "1871458457493053441",
                                "userId": 71048
                            }
                        ],
                        "businessType": 3,
                        "businessData": {
                            "data": {
                                "projectName": f"{projectname1}",
                                "projectId": f"{projectid}"
                            }
                        }
                    })
                    response4 = requests.post(url5, data=data, headers=headers1)
                    print(response4.json())
                    assert response4.json()['code'] == 200
                    log.debug("添加实施许可令成功")
                    break
                else:
                    log.debug(f"第{i+1}个项目已处于实施稽核流程中，跳过")
            else:
                # 如果循环没有通过break退出，则执行else子句
                log.debug("没有可研完成且尚未提交实施稽核的项目")
        else:
            log.debug("没有可研完成的项目")

Ss = Ssgl()
if __name__ == '__main__':
    Ss.ss_add_permit('测试')