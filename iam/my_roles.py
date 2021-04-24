import utils.exec_aws_cmd_util as cmdUtil
import json

# aws iam list-instance-profiles

def search_instance_profiles():
	command = 'aws iam list-instance-profiles --query InstanceProfiles[*]'
	json_res = cmdUtil.getJson_exec_commd(command)
	return json_res

def get_simple_instance_profile_info(jsonObj):
	InstanceProfileName = jsonObj.get("InstanceProfileName")
	InstanceProfileId = jsonObj.get("InstanceProfileId")
	retObjInfo = InstanceProfileName+" : "+InstanceProfileId
	return retObjInfo

def select_instance_profiles():
	ret_obj = search_instance_profiles()
	if len(ret_obj) < 1:
		print("먼저 instance profiles 를 생성해 주세요.")
		exit()
	else:
		objArr=[]
		i=0
		for oneObj in ret_obj:
			i+=1
			objInfo = get_simple_instance_profile_info(oneObj)
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