import utils.exec_aws_cmd_util as cmdUtil
import network.my_vpcs as myVpcs
import json

def search_sg(srcKey,srcStr):
	search_wd=""
	if srcKey == "vpc-id":
		search_wd = " Name=vpc-id,Values="+srcStr
	if search_wd != "":
		search_wd = "--filter"+search_wd
	command = 'aws ec2 describe-security-groups '+search_wd+'--query SecurityGroups[*]'
	json_res = cmdUtil.getJson_exec_commd(command)
	return json_res

def get_simple_sg_info(jsonObj):
	GroupId = jsonObj.get("GroupId")
	vpcId = jsonObj.get("VpcId")
	tagValue = ""
	tagKey = "Name"
	if cmdUtil.is_json_key_present(jsonObj,"Tags"):
		tagValue = cmdUtil.getString_tagValue(jsonObj.get("Tags"),tagKey)
	retVpcInfo = tagValue+" : "+cidr+" : "+vpcId
	return retVpcInfo

def select_sg(searchVpcId):
	ret_obj = search_sg(searchVpcId)
	if len(ret_obj) < 1:
		print("먼저 Security group 을 생성해 주세요.")
		exit()
	else:
		objArr=[]
		i=0
		for oneObj in ret_obj:
			i+=1
			objInfo = get_simple_routeTable_info(oneObj)
			objArr.append(objInfo)
			print(str(i)+"."+objInfo)
	selectedNo=input()
	# 사용자가 입력한 번호가 rr 보다 많으면 처음부터 다시 시작.
	if int(selectedNo) > len(objArr):
		print("잘못 선택하셨습니다. 처음부터 다시 시작합니다.")
		exit()
	# 선택한 번호에 맞는 obj를 변수에 저장합니다.
	selectedObjInfoArr=[]
	for index in range(len(objArr)):
		if selectedNo == str(index+1):
			selectedObjInfoArr = (objArr[index]).split(' : ')
			break

	return selectedObjInfoArr		