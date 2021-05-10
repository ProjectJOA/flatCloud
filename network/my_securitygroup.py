import utils.exec_aws_cmd_util as cmdUtil
import utils.go_main as goMain
import network.my_vpcs as myVpcs
import json

selected_first_menu = "5" # 1 단계 선택 메뉴 번호

def sg_startMain(selected_second_menu):
	json_res = ""
	if selected_second_menu == "1":
		json_res = search_all_sg_arr()
	elif selected_second_menu == "2":
		json_res = create_sg()
	elif selected_second_menu == "5":
		json_res = search_inoutBound("inout")
	elif selected_second_menu == "6":
		json_res = add_inoutBound("in")			
	elif selected_second_menu == "7":
		json_res = add_inoutBound("out")
	elif selected_second_menu == "8":
		json_res = del_inoutBound()
	else:				
		print("준비중입니다.")
	return json_res

def create_sg():
	print("Security Group 을 생성합니다.")
	print("Security Group 생성시 이름을 입력하세요 (예 test_sg): ")
	sgNm=input()	#생성될 object 이름.
	print("Security Group 을 생성할 Vpc를 선택합니다.")
	# 등록된 vpc 목록을 가져옵니다.
	selectedVpcInfoArr = myVpcs.select_vpc()
	print("Security Group 생성중입니다.")	
	command = 'aws ec2 create-security-group --group-name '+sgNm+' --description "'+sgNm+'" --vpc-id '+selectedVpcInfoArr[2]+' --query GroupId --output text'
	credGwId = cmdUtil.create_resource(command, sgNm)
	print("Security Group 이 생성되었습니다.")
	retStr = {"SecurityGroupId":credGwId, "SecurityGroupNm":sgNm}
	return retStr

def add_inoutBound(doType):
	doComment = "Inbound"
	awsCmd = "authorize-security-group-ingress"
	if doType == "out":
		doComment = "Outbound"
		awsCmd = "authorize-security-group-egress"

	print("Security Group 에 "+doComment+" 를 추가합니다.")
	print("먼저 추가할 Security Group을 선택합니다.")
	selectedSGInfoArr = select_sg("","")
	print("TCP Protocol 만 등록 가능합니다.")
	print("허용할 Port 를 입력해주세요 (예: 80)")
	inPort=input()
	print("허용할 IP 대역을 입력해주세요 (예: 192.168.10.23/32")
	inipRange=input()
	if cmdUtil.ipValidate(inipRange):
		print(doComment+" 정책 추가 중입니다.")
		command = 'aws ec2 '+awsCmd+' --group-id '+selectedSGInfoArr[1]+' --ip-permissions IpProtocol=tcp,FromPort='+inPort+',ToPort='+inPort+',IpRanges="[{CidrIp='+inipRange+'}]"'
		cmdUtil.exec_commd(command)
	
	return "success"

def del_inoutBound():
	awsCmd = ""
	selectedObj = select_inoutBound()
	selectedInOutBoundArr = (selectedObj).split(' | ')
	print("선택하신 ("+selectedObj+") 삭제하시겠습니까?(y/n)")
	nextStep2_YN=input()
	if nextStep2_YN.lower() == 'y':
		if selectedInOutBoundArr[0] == "in":
			awsCmd = "revoke-security-group-ingress"
		else:
			awsCmd = " revoke-security-group-egress"
		#revoke-security-group-ingress
	command = 'aws ec2 '+awsCmd+' --group-id '+selectedInOutBoundArr[5]+' --ip-permissions IpProtocol='+selectedInOutBoundArr[4]
	if selectedInOutBoundArr[4] != "-1":
		command = command+',FromPort='+selectedInOutBoundArr[2]+',ToPort='+selectedInOutBoundArr[3]
	command = command+',IpRanges="[{CidrIp='+selectedInOutBoundArr[1]+'}]"'
	cmdUtil.exec_commd(command)
	print("선택하신 ("+selectedObj+") 삭제되었습니다.")
	return "success"

def search_sg(srcKey,srcStr):
	search_wd=""
	if srcKey == "vpc-id":
		search_wd = " Name=vpc-id,Values="+srcStr
	if search_wd != "":
		search_wd = "--filter"+search_wd
	command = 'aws ec2 describe-security-groups '+search_wd+' --query SecurityGroups[*]'
	json_res = cmdUtil.getJson_exec_commd(command)
	return json_res

def search_all_sg_arr():
	ret_obj = search_sg("","")
	objArr=[]
	if len(ret_obj) < 1:
		print("먼저 Security group을 생성해 주세요.")
		goMain.go_main()
	else:
		i=0
		for oneObj in ret_obj:
			i+=1
			objInfo = get_simple_sg_info(oneObj)
			objArr.append(objInfo)
			print(str(i)+"."+objInfo)
	return objArr

def get_simple_sg_info(jsonObj):
	GroupId = jsonObj.get("GroupId")
	vpcId = jsonObj.get("VpcId")
	tagValue = "noname"
	tagKey = "Name"
	if cmdUtil.is_json_key_present(jsonObj,"Tags"):
		tagValue = cmdUtil.getString_tagValue(jsonObj.get("Tags"),tagKey)
	retVpcInfo = tagValue+" : "+GroupId+" : "+vpcId
	return retVpcInfo

def get_simple_inoutBound_info(inoutType, sgId, jsonObj):
	try:
		inoutBoundArr = []
		for inoutB in jsonObj:
			ipProtocol = inoutB.get("IpProtocol")
			if ipProtocol == "-1":
				fromPort = "All"
				toPort = "All"
			else:
				fromPort = str(inoutB.get("FromPort"))
				toPort = str(inoutB.get("ToPort"))
			for cidrIps in inoutB.get("IpRanges"):
				cidrIpsStr = cidrIps.get("CidrIp")
				inoutObj = inoutType+" | "+cidrIpsStr+" | "+fromPort+" | "+toPort+" | "+ipProtocol+" | "+sgId
				inoutBoundArr.append(inoutObj)
			for cidrIps in inoutB.get("Ipv6Ranges"):
				cidrIpsStr = cidrIps.get("CidrIpv6")
				inoutObj = inoutType+" | "+cidrIpsStr+" | "+fromPort+" | "+toPort+" | "+ipProtocol+" | "+sgId
				inoutBoundArr.append(inoutObj)
		return inoutBoundArr
	except Exception as e:
		print(e)		

def select_sg(srcKey,srcStr):
	ret_obj = search_sg(srcKey,srcStr)
	objArr=[]	
	if len(ret_obj) < 1:
		print("먼저 Security group 을 생성해 주세요.")
		goMain.go_main()
	else:
		i=0
		for oneObj in ret_obj:
			i+=1
			objInfo = get_simple_sg_info(oneObj)
			objArr.append(objInfo)
			print(str(i)+"."+objInfo)
	selectedNo=input()
	# 사용자가 입력한 번호가 rr 보다 많으면 처음부터 다시 시작.
	if int(selectedNo) > len(objArr):
		print("잘못 선택하셨습니다. 처음부터 다시 시작합니다.")
		goMain.go_main()
	# 선택한 번호에 맞는 obj를 변수에 저장합니다.
	selectedObjInfoArr=[]
	for index in range(len(objArr)):
		if selectedNo == str(index+1):
			selectedObjInfoArr = (objArr[index]).split(' : ')
			break

	return selectedObjInfoArr		

def search_inoutBound(searchtype):
	print("먼저 Security Group을 선택합니다.")
	selectedSGInfoArr = select_sg("","")
	command = 'aws ec2 describe-security-groups --group-ids '+selectedSGInfoArr[1]+' --query SecurityGroups[0]'
	json_res = cmdUtil.getJson_exec_commd(command)
	retArr = []
	if len(json_res.get("IpPermissions")) > 0:
		retArr = retArr + get_simple_inoutBound_info("in",selectedSGInfoArr[1], json_res.get("IpPermissions"))
	if len(json_res.get("IpPermissionsEgress")) > 0:
		retArr = retArr + get_simple_inoutBound_info("out",selectedSGInfoArr[1], json_res.get("IpPermissionsEgress"))
	i=0
	for retObj in retArr:
		i+=1
		print(str(i)+"."+retObj)
	return retArr	

def select_inoutBound():
	retArr = search_inoutBound("inout")
	print("p.처음으로 가기")
	selectNo="0"
	while 1>0:
		print("삭제할 IN/OUT 정책을 선택합니다.")
		selectNo=input()
		if selectNo.lower() == "p":
			goMain.go_main()
		elif int(selectNo) > len(retArr):
			print("잘못 선택하셨습니다.")
		else:
			break
	return retArr[int(selectNo)-1]
