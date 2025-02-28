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
                        log.debug(f"{projectname2}项目招投标及合同文件提交稽核成功")
                        break
                    else:
                        log.debug(f"第{i+1}个项目已处于项目招投标及合同文件流程中，跳过")
                else:
                    # 如果循环没有通过break退出，则执行else子句
                    log.debug("没有可研完成且尚未提交稽核的项目")
            else:
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
                plan_date = response_data2[j]['planDate']
                actual_date = plan_date + timedelta(days=7)
                # actual_date = datetime.strftime(actual_date, '%Y-%m-%d')
                print(actual_date)
                num1 = len(response_data2)
                count_num = 0 # 记录未提交稽核的节点数，由于提交稽核不需要所有节点都填写完，所以需要逐一判断节点是否已提交稽核
                for j in range(num1):
                    if not response_data2[j]['implProgressStatus'] or response_data2[j]['implProgressStatus'] == 'tb':
                        count_num += 1
                        j += 1
                else:
                    if count_num == num1:
                        # 3.保存项目建设实施进度

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
                        response_data3 = response3.json()['data']
                        projectname2 = response_data3['projectName']
                        # 4.提交稽核
                        api4 = Api('api')['项目建设实施进度提交稽核']
                        url5 = f"https://{host}{api4}"
                        data2 = json.dumps({
                            "processId": "1889599825780019200",
                            "businessId": f"{projectid}",
                            "nodeUserList": [
                                {
                                    "nodeId": "1889599825780019201",
                                    "userId": 70557
                                },
                                {
                                    "nodeId": "1889599825780019202",
                                    "userId": 71048
                                }
                            ],
                            "businessType": 6,
                            "businessData": {
                                "data": {
                                    "projectName": f"{projectname2}",
                                    "projectId": f"{projectid}"
                                }
                            }
                        })
                        headers2 = {
                            "Authorization": f"Bearer {authorization}",
                            "Content-Type": "application/json"
                        }
                        response4 = requests.post(url5, data=data2, headers=headers2)
                        print(response4.json())
                        assert response4.json()['code'] == 200
                        log.debug(f'{projectname2}项目建设实施进度提交稽核成功')
                        break
                    else:
                        log.debug(f"第{i + 1}个项目已处于项目建设实施进度流程中，跳过")
                        continue
            else:
                log.debug("没有可研完成且尚未提交稽核的项目")
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
                # 2.查询项目合规性手续详情详情
                list_info = data_list1[i]
                projectid = list_info['projectId']
                api2 = Api('api')['项目合规性手续详情']
                url3 = f"https://{host}{api2}"
                url_ss = '?'.join([url3, f'projectId={projectid}'])
                response2 = requests.get(url_ss, headers=headers)
                response_json = response2.json()
                response_data2 = response_json['data']
                if not response_data2[0]['implComplianceStatus'] or response_data2[0]['implComplianceStatus'] == 'tb':
                    # 3.保存项目合规性手续
                    plan_date = response_data2[0]['planDate']
                    actual_date = plan_date + timedelta(days=3)
                    #actual_date = datetime.strftime(actual_date, '%Y-%m-%d')
                    print(actual_date)
                    api3 = Api('api')['保存项目合规性手续']
                    url4 = f"https://{host}{api3}"
                    uri, filename = self.ss_upload()
                    data1 = json.dumps({
                        "projectId": f"{projectid}",
                        "detailList": [
                            {
                                "dictId": 76,
                                "dictName": "立项备案登记",
                                "feasibleComplianceId": "1892829138416406529",
                                "planDate": f"{plan_date}",
                                "remake": "手续备注测试1",
                                "implComplianceStatus": "tb",
                                "actualProgressDate": f"{actual_date}",
                                "fileName": f"{filename}",
                                "fileUrl": f"{uri}"
                            },
                            {
                                "dictId": 88,
                                "dictName": "生产资质",
                                "feasibleComplianceId": "1892829138416406530",
                                "planDate": f"{plan_date}",
                                "remake": "手续备注测试2",
                                "actualProgressDate": f"{actual_date}"
                            }
                        ]
                    })
                    headers1 = {
                        "Authorization": f"Bearer {authorization}",
                        "Content-Type": "application/json"
                    }
                    response3 = requests.post(url4, data=data1, headers=headers1)
                    print(response3.json())
                    response_data2 = response3.json()['data']
                    projectname2 = response_data2['projectName']
                    # 4.项目合规性手续提交稽核
                    api4 = Api('api')['项目合规性手续提交稽核']
                    url5 = f"https://{host}{api4}"
                    data2 = json.dumps({
                        "processId": "1889950321795534848",
                        "businessId": f"{projectid}",
                        "nodeUserList": [
                            {
                                "nodeId": "1889950321795534849",
                                "userId": 70557
                            },
                            {
                                "nodeId": "1889950321795534850",
                                "userId": 71048
                            }
                        ],
                        "businessType": 7,
                        "businessData": {
                            "data": {
                                "projectName": f"{projectname2}",
                                "projectId": f"{projectid}"
                            }
                        }
                    })
                    headers2 = {
                        "Authorization": f"Bearer {authorization}",
                        "Content-Type": "application/json"
                    }
                    response4 = requests.post(url5, data=data2, headers=headers2)
                    response_data3 = response4.json()
                    assert response_data3['code'] == 200
                    log.debug(f"{projectname2}项目合规性手续提交稽核成功")
                    break
                else:
                    log.debug(f"第{i + 1}个项目已处于合规性手续办理流程中，跳过")
                    continue
            else:
                log.debug("没有可研完成且尚未提交合规性手续稽核的项目")
        else:
            log.debug("没有可研完成的项目")

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
                # 2.查询项目投资预算实施进度详情
                list_info = data_list1[i]
                projectid = list_info['projectId']
                api2 = Api('api')['项目投资预算实施进度详情']
                url3 = f"https://{host}{api2}"
                url_ss = '?'.join([url3, f'projectId={projectid}'])
                response2 = requests.get(url_ss, headers=headers)
                response_json = response2.json()
                response_data2 = response_json['data']
                if not response_data2[0]['implAssetStatus'] or response_data2[0]['implAssetStatus'] == 'tb':
                    # 3.更新项目投资预算实施进度
                    api3 = Api('api')['保存项目投资预算实施进度']
                    url4 = f"https://{host}{api3}"
                    data1 = json.dumps({
                        "projectId": f"{projectid}",
                        "detailList": [
                            {
                                "budgetAmount": 30,
                                "fieldCname": "1.基建概算",
                                "fieldName": "flatProAmount",
                                "projectId": f"{projectid}",
                                "sorted": 10,
                                "type": "count",
                                "implAssetStatus": "tb",
                                "actualAmount": 31
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "1.1 总平工程",
                                "fieldName": "totalFlatProAmount",
                                "projectId": f"{projectid}",
                                "sorted": 11,
                                "type": "edit",
                                "actualAmount": "10"
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "1.2 单体工程",
                                "fieldName": "synthFlatProAmount",
                                "projectId": f"{projectid}",
                                "sorted": 12,
                                "type": "edit",
                                "actualAmount": "9"
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "1.3 封装工程",
                                "fieldName": "warapFlatProAmount",
                                "projectId": f"{projectid}",
                                "sorted": 13,
                                "type": "edit",
                                "actualAmount": "11"
                            },
                            {
                                "budgetAmount": 0,
                                "fieldCname": "1.4 其他基建工程",
                                "fieldName": "otherFlatProAmount",
                                "projectId": f"{projectid}",
                                "sorted": 14,
                                "type": "edit",
                                "actualAmount": "1"
                            },
                            {
                                "budgetAmount": 30,
                                "fieldCname": "2.设备概算",
                                "fieldName": "equipmentAmount",
                                "projectId": f"{projectid}",
                                "sorted": 20,
                                "type": "count",
                                "actualAmount": 18
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "2.1 生产设备",
                                "fieldName": "produceEquipmentAmount",
                                "projectId": f"{projectid}",
                                "sorted": 21,
                                "type": "edit",
                                "actualAmount": "10"
                            },
                            {
                                "budgetAmount": 0,
                                "fieldCname": "2.2 环保设备",
                                "fieldName": "environmentEquipmentAmount",
                                "projectId": f"{projectid}",
                                "sorted": 22,
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "2.3 实验设备",
                                "fieldName": "experimentEquipmentAmount",
                                "projectId": f"{projectid}",
                                "sorted": 23,
                                "type": "edit",
                                "actualAmount": "8"
                            },
                            {
                                "budgetAmount": 0,
                                "fieldCname": "2.4 办公及后勤设备",
                                "fieldName": "rearEquipmentAmount",
                                "projectId": f"{projectid}",
                                "sorted": 24,
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "2.5 其他设备",
                                "fieldName": "otherEquipmentAmount",
                                "projectId": f"{projectid}",
                                "sorted": 25,
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "3.工程建设服务费",
                                "fieldName": "proServerAmount",
                                "projectId": f"{projectid}",
                                "sorted": 30,
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "4.土地购置费",
                                "fieldName": "landPurAmount",
                                "projectId": f"{projectid}",
                                "sorted": 40,
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 20,
                                "fieldCname": "5.不可预见费",
                                "fieldName": "preparAmount",
                                "projectId": f"{projectid}",
                                "sorted": 50,
                                "type": "count",
                                "actualAmount": 0
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "5.1 基本预备费",
                                "fieldName": "basicPreparAmount",
                                "projectId": f"{projectid}",
                                "sorted": 51,
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 10,
                                "fieldCname": "5.2 涨价预备费",
                                "fieldName": "increasePreparAmount",
                                "projectId": f"{projectid}",
                                "sorted": 52,
                                "type": "edit"
                            },
                            {
                                "budgetAmount": 100,
                                "fieldCname": "6.总投资额",
                                "fieldName": "totalAmount",
                                "projectId": f"{projectid}",
                                "sorted": 60,
                                "type": "count",
                                "actualAmount": 49
                            }
                        ]
                    }
                    )
                    headers1 = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {authorization}"
                    }
                    response3 = requests.post(url1, headers=headers1, json=data1)
                    print(response1.json())
                    response_data3 = response3.json()['data']
                    projectname2 = response_data3['projectName']
                    # 4.项目投资预算实施进度提交稽核
                    api4 = Api('api')['项目投资预算实施进度提交稽核']
                    url5 = f"https://{host}{api4}"
                    data2 = json.dumps({
                        "processId": "1889935646890528768",
                        "businessId": f"{projectid}",
                        "nodeUserList": [
                            {
                                "nodeId": "1889935646890528769",
                                "userId": 70557
                            },
                            {
                                "nodeId": "1889935646890528770",
                                "userId": 71048
                            }
                        ],
                        "businessType": 8,
                        "businessData": {
                            "data": {
                                "projectName": f"{projectname2}",
                                "projectId": f"{projectid}"
                            }
                        }
                    })
                    headers2 = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {authorization}"
                    }
                    response4 = requests.post(url5, headers=headers2, json=data2)
                    print(response4.json())
                    assert response4.json()['code'] == 200
                    log.debug(f'{projectname2}项目投资预算实施进度提交稽核成功')
                    break
                else:
                    log.debug(f"第{i + 1}个项目已处于合规性手续办理流程中，跳过")
                    # continue
            else:
                log.debug("没有可研完成且尚未提交投资预算实施进度稽核的项目")
        else:
            log.debug("没有可研完成的项目")







Ss = Ssgl()
if __name__ == '__main__':
    Ss.ss_add_permit('测试')