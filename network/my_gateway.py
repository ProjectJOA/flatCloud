import utils.exec_aws_cmd_util as cmdUtil
import network.my_vpcs as myVpcs
import json

def create_gateway():
	print("Gateway를 생성합니다.")
	print("Gateway 생성시 이름을 입력하세요 : ")
	gwNm=input()		#생성될 object들의 접두사.
	print("Gateway를 생성합니다.")		
	command = 'aws ec2 create-internet-gateway --query InternetGateway.InternetGatewayId --output text'
	credGwId = cmdUtil.create_resource(command, gwNm)
	print("Internet gateway가 생성되었습니다.")
	print("생성하신 Gateway와 Vpc를 연결하시겠습니까?(y/n)")
	nextStepYN=input()
	if nextStepYN == 'Y' or nextStepYN == 'y':
		print("연결할 vpc를 선택하세요.")
		# 등록된 vpc 목록을 가져옵니다.
		selectedVpcInfoArr = myVpcs.select_vpc()
		attach_gw_to_vpc(credGwId, selectedVpcInfoArr[2])
	else:
		print("프로그램을 종료합니다.")
		exit()
	retStr = {"GatewayId":credGwId,"vpcId":selectedVpcInfoArr[2]}
	return retStr

def attach_gw_to_vpc(gwId, vpcId):
	command = 'aws ec2 attach-internet-gateway --internet-gateway-id '+gwId+' --vpc-id '+vpcId
	json_res = cmdUtil.exec_commd(command)
	print("Internet Gateway와 Vpc가 연결되었습니다.")
	return "success"	

def search_gw():
	command = "aws ec2 describe-internet-gateways --query InternetGateways[*]"
	json_res = cmdUtil.getJson_exec_commd(command)
	return json_res

def search_all_gw_arr():
	ret_obj = search_gw()
	objArr=[]
	if len(ret_obj) < 1:
		print("먼저 Internet gateway를 생성해 주세요.")
		exit()
	else:
		i=0
		for oneObj in ret_obj:
			i+=1
			objInfo = get_simple_gw_info(oneObj)
			objArr.append(objInfo)
			print(objInfo)
	return objArr

def get_simple_gw_info(jsonObj):
	InternetGatewayId = jsonObj.get("InternetGatewayId")
	tagValue = ""
	tagKey = "Name"
	if cmdUtil.is_json_key_present(jsonObj,"Tags"):
		tagValue = cmdUtil.getString_tagValue(jsonObj.get("Tags"),tagKey)
	retGwInfo = cmdUtil.nullToNoname(tagValue,"noname")+" : "+InternetGatewayId
	return retGwInfo

def select_gw():
	ret_obj = search_gw()
	if len(ret_obj) < 1:
		print("먼저 Internet gateway를 생성해 주세요.")
		exit()
	else:
		objArr=[]
		i=0
		for oneObj in ret_obj:
			i+=1
			objInfo = get_simple_gw_info(oneObj)
			objArr.append(objInfo)
			print(str(i)+"."+objInfo)
	selectedNo=input()
	# 사용자가 입력한 번호가 vpc arr 보다 많으면 처음부터 다시 시작.
	if int(selectedNo) > len(objArr):
		print("잘못 선택하셨습니다. 처음부터 다시 시작합니다.")
		exit()
	# 선택한 번호에 맞는 vpcid를 변수에 저장합니다.
	selectedObjInfoArr=[]
	for index in range(len(objArr)):
		if selectedNo == str(index+1):
			selectedObjInfoArr = (objArr[index]).split(' : ')
			break

	return selectedObjInfoArr	