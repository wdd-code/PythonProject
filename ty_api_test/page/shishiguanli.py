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
                    log.debug("实施许可令稽核提交成功")
                    break
                else:
                    log.debug(f"第{i+1}个项目已处于实施稽核流程中，跳过")
            else:
                # 如果循环没有通过break退出，则执行else子句
                log.debug("没有可研完成且尚未提交实施稽核的项目")
        else:
            log.debug("没有可研完成的项目")
    def ss_project_company(self, queryname):
            """更新项目公司，提交稽核"""
            # 1.查询项目名称，模糊查询
            authorization = self.authorization
            host = Readconfig('HOST-TZB').host
            headers = {
                "Authorization": f"Bearer {authorization}"
            }
            api1 = Api('api')['可研完成的项目']
            url1 = f"https://{host}{api1}"
            projectname = urllib.parse.quote(queryname)
            projectname1 = f"projectName={projectname}"
            url2 = '&'.join([url1, projectname1])
            response1 = requests.get(url2, headers=headers)
            print(response1.json())
            response_data1 = response1.json()['data']
            data_list1 = response_data1['list']
            num = response_data1['endRow']
            if num > 0:
                """可研完成的项目可能有多个，有些可能已经是提交稽核，用for循环来遍历尝试，直到添加成功break"""
                for i in range(num):
                    # 2.查询项目详情
                    list_info = data_list1[i]
                    projectid = list_info['projectId']
                    api2 = Api('api')['项目详情']
                    url3 = f"https://{host}{api2}"
                    url_ss = '?'.join([url3, f'projectId={projectid}'])
                    response2 = requests.get(url_ss, headers=headers)
                    response_json = response2.json()
                    response_data2 = response_json['data']

                    if response_data2['implCompanyStatus'] == 'tb':
                        # 3.添加项目公司/暂存
                        api3 = Api('api')['添加项目公司']
                        url4 = f"https://{host}{api3}"
                        uri, filename = self.ss_upload()
                        data1 = json.dumps({
                            "projectCompanyName": "测试项目公司",
                            "projectId": f"{projectid}",
                            "implCompanyStatus": "tb",
                            "companyFiles": [
                                {
                                    "dictId": "105",
                                    "file": [
                                    ],
                                    "fileName": f"{filename}",
                                    "fileUrl": f"{uri}"
                                }
                            ]
                        })
                        headers1 = {
                            "Authorization": f"Bearer {authorization}",
                            "Content-Type": "application/json"
                        }
                        response3 = requests.post(url4, data=data1, headers=headers1)
                        print(response3.json())
                        response_data3 = response3.json()['data']
                        projectname2 = response_data3['projectName']
                        # 4.提交稽核
                        api4 = Api('api')['项目公司提交稽核']
                        url5 = f"https://{host}{api4}"
                        data2 = json.dumps({
                            "processId": "1889227480372482048",
                            "nodeUserList": [
                                {
                                    "nodeId": "1889118550821777409",
                                    "userId": 70557
                                },
                                {
                                    "nodeId": "1889228550821777409",
                                    "userId": 71048
                                }
                            ],
                            "businessType": 4,
                            "businessData": {
                                "data": {
                                    "projectName": f"{projectname2}",
                                    "projectId": f"{projectid}"
                                }
                            }
                        })
                        response4 = requests.post(url5, data=data1, headers=headers1)
                        print(response4.json())
                        assert response4.json()['code'] == 200
                        log.debug("项目公司稽核提交成功")
                        break
                    else:
                        log.debug(f"第{i+1}个项目已处于项目公司稽核流程中，跳过")
                else:
                    # 如果循环没有通过break退出，则执行else子句
                    log.debug("没有可研完成的项目")


    def ss_project_contract(self, queryname):
            """更新项目招投标及合同文件，提交稽核"""
            # 1.查询项目名称，模糊查询
            authorization = self.authorization
            host = Readconfig('HOST-TZB').host
            headers = {
                "Authorization": f"Bearer {authorization}"
            }
            api1 = Api('api')['可研完成的项目']
            url1 = f"https://{host}{api1}"
            projectname = urllib.parse.quote(queryname)
            projectname1 = f"projectName={projectname}"
            url2 = '&'.join([url1, projectname1])
            response1 = requests.get(url2, headers=headers)
            print(response1.json())
            response_data1 = response1.json()['data']
            data_list1 = response_data1['list']
            num = response_data1['endRow']
            if num > 0:
                """可研完成的项目可能有多个，有些可能已经是提交稽核，用for循环来遍历尝试，直到添加成功break"""
                for i in range(num):
                    # 2.查询项目招投标及合同文件详情
                    list_info = data_list1[i]
                    projectid = list_info['projectId']
                    api2 = Api('api')['项目招投标及合同文件详情']
                    url3 = f"https://{host}{api2}"
                    url_ss = '?'.join([url3, f'projectId={projectid}'])
                    response2 = requests.get(url_ss, headers=headers)
                    response_json = response2.json()
                    response_data2 = response_json['data']
                    if not response_data2 or response_data2[0]['implContractStatus'] == 'tb':
                        # 3.添加项目招投标及合同文件
                        api3 = Api('api')['添加项目招投标及合同文件']
                        url4 = f"https://{host}{api3}"
                        uri, filename = self.ss_upload()
                        data1 = json.dumps({
                            "projectId": f"{projectid}",
                            "contractInfos": [
                                {
                                    "businessType": "121",
                                    "budgetAmount": "100",
                                    "actualAmount": "100",
                                    "fileUrl": f"{uri}",
                                    "fileName": f"{filename}",
                                    "implContractStatus": "tb"
                                }
                            ]
                        })
                        headers1 = {
                            "Authorization": f"Bearer {authorization}",
                            "Content-Type": "application/json"
                        }
                        response3 = requests.post(url4, data=data1, headers=headers1)
                        print(response3.json())
                        response_data3 = response3.json()['data']
                        projectname2 = response_data3['projectName']
                        # 4.提交稽核
                        api4 = Api('api')['项目招投标及合同文件提交稽核']
                        url5 = f"https://{host}{api4}"
                        data2 = json.dumps({
                            "processId": "1889488130877296640",
                            "businessId": f"{projectid}",
                            "nodeUserList": [
                                {
                                    "nodeId": "1889488577105104896",
                                    "userId": 70557
                                },
                                {
                                    "nodeId": "1889488577105104897",
                                    "userId": 71048
                                }
                            ],
                            "businessType": 5,
                            "businessData": {
                                "data": {
                                    "projectName": f"{projectname2}",
                                    "projectId": f"{projectid}"
                                }
                            }
                        })
                        response4 = requests.post(url5, data=data2, headers=headers1)
                        print(response4.json())
                        assert response4.json()['code'] == 200
                        log.debug("项目招投标及合同文件提交稽核成功")
                        break
                    else:
                        log.debug(f"第{i+1}个项目已处于项目招投标及合同文件流程中，跳过")
                else:
                    # 如果循环没有通过break退出，则执行else子句
                    log.debug("没有可研完成的项目")

    def ss_project_built(self, queryname):
        """更新项目建设（实施）进度，提交稽核"""
        # 1.查询项目名称，模糊查询
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        headers = {
            "Authorization": f"Bearer {authorization}"
        }
        api1 = Api('api')['可研完成的项目']
        url1 = f"https://{host}{api1}"
        projectname = urllib.parse.quote(queryname)
        projectname1 = f"projectName={projectname}"
        url2 = '&'.join([url1, projectname1])
        response1 = requests.get(url2, headers=headers)
        print(response1.json())
        response_data1 = response1.json()['data']
        data_list1 = response_data1['list']
        num = response_data1['endRow']
        if num > 0:
            """可研完成的项目可能有多个，有些可能已经是提交稽核，用for循环来遍历尝试，直到添加成功break"""
            for i in range(num):
                # 2.查询项目建设实施进度详情
                list_info = data_list1[i]
                projectid = list_info['projectId']
                api2 = Api('api')['项目建设实施进度详情']
                url3 = f"https://{host}{api2}"
                url_ss = '?'.join([url3, f'projectId={projectid}'])
                response2 = requests.get(url_ss, headers=headers)
                response_json = response2.json()
                response_data2 = response_json['data']
                num1 = len(response_data2)
                for j in range(num1):
                    if not response_data2[j]['implProgressStatus'] or response_data2[j]['implProgressStatus'] == 'tb':
                        # 3.保存项目建设实施进度
                        plan_date = response_data2[j]['planDate']
                        actual_date = plan_date + timedelta(days=7)
                        #actual_date = datetime.strftime(actual_date, '%Y-%m-%d')
                        print(actual_date)
                        api3 = Api('api')['保存项目建设实施进度']
                        url4 = f"https://{host}{api3}"
                        uri, filename = self.ss_upload()
                        data1 = json.dumps({
                            "projectId": f"{projectid}",
                            "detailList": [
                                {
                                    "dictId": 63,
                                    "dictName": "施工许可",
                                    "feasiblePlanId": "1892829138106028034",
                                    "planDate": f"{plan_date}",
                                    "implProgressStatus": "tb",
                                    "actualProgressDate": f"{actual_date}",
                                    "actualProgressDesc": "测试建设实施进度"
                                },
                                {
                                    "dictId": 70,
                                    "dictName": "正式投产",
                                    "feasiblePlanId": "1892829138106028035",
                                    "planDate": f"{plan_date}",
                                    "actualProgressDate": f"{actual_date}",
                                    "actualProgressDesc": "测试"
                                }
                            ]
                        })
                        headers1 = {
                            "Authorization": f"Bearer {authorization}",
                            "Content-Type": "application/json"
                        }
                        response3 = requests.post(url4, data=data1, headers=headers1)
                        print(response3.json())
                        break
                    else:
                        continue
                else:
                    log.debug(f"第{i + 1}个项目已处于项目建设实施进度流程中，跳过")
            else:
                log.debug("没有可研完成的项目")

    def ss_project_procedure(self, queryname):
        """更新项目合规性手续办理，提交稽核"""
        # 1.查询项目名称，模糊查询
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        headers = {
            "Authorization": f"Bearer {authorization}"
        }
        api1 = Api('api')['可研完成的项目']
        url1 = f"https://{host}{api1}"
        projectname = urllib.parse.quote(queryname)
        projectname1 = f"projectName={projectname}"
        url2 = '&'.join([url1, projectname1])
        response1 = requests.get(url2, headers=headers)
        print(response1.json())
        response_data1 = response1.json()['data']
        data_list1 = response_data1['list']
        num = response_data1['endRow']
        if num > 0:
            """可研完成的项目可能有多个，有些可能已经是提交稽核，用for循环来遍历尝试，直到添加成功break"""
            for i in range(num):
                # 2.查询项目招投标及合同文件详情
                list_info = data_list1[i]
                projectid = list_info['projectId']
                api2 = Api('api')['项目招投标及合同文件详情']
                url3 = f"https://{host}{api2}"
                url_ss = '?'.join([url3, f'projectId={projectid}'])
                response2 = requests.get(url_ss, headers=headers)
                response_json = response2.json()
                response_data2 = response_json['data']

    def ss_project_investment(self, queryname):
        """更新项目投资预算实施进度，提交稽核"""
        # 1.查询项目名称，模糊查询
        authorization = self.authorization
        host = Readconfig('HOST-TZB').host
        headers = {
            "Authorization": f"Bearer {authorization}"
        }
        api1 = Api('api')['可研完成的项目']
        url1 = f"https://{host}{api1}"
        projectname = urllib.parse.quote(queryname)
        projectname1 = f"projectName={projectname}"
        url2 = '&'.join([url1, projectname1])
        response1 = requests.get(url2, headers=headers)
        print(response1.json())
        response_data1 = response1.json()['data']
        data_list1 = response_data1['list']
        num = response_data1['endRow']
        if num > 0:
            """可研完成的项目可能有多个，有些可能已经是提交稽核，用for循环来遍历尝试，直到添加成功break"""
            for i in range(num):
                # 2.查询项目招投标及合同文件详情
                list_info = data_list1[i]
                projectid = list_info['projectId']
                api2 = Api('api')['项目招投标及合同文件详情']
                url3 = f"https://{host}{api2}"
                url_ss = '?'.join([url3, f'projectId={projectid}'])
                response2 = requests.get(url_ss, headers=headers)
                response_json = response2.json()
                response_data2 = response_json['data']




Ss = Ssgl()
if __name__ == '__main__':
    Ss.ss_add_permit('测试')