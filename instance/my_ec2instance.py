import utils.exec_aws_cmd_util as cmdUtil
import network.my_vpcs as myVpcs
import network.my_subnet as mySubnet
import network.my_securitygroup as mysg
import network.my_keypairs as mykeys
import network.my_elb as myelb
import iam.my_roles as myroles
import utils.go_main as goMain
# import start_manage_myaws as startMain

selected_first_menu = "6" # 1 단계 선택 메뉴 번호

def ec2inst_startMain(selected_second_menu):
	json_res = ""
	if selected_second_menu == "1":
		json_res = search_all_ec2instance("","","")
	elif selected_second_menu == "2":
		json_res = create_instance()
	elif selected_second_menu == "4":
		json_res = remove_instance()						
	elif selected_second_menu == "5":
		json_res = start_instance()
	elif selected_second_menu == "6":
		json_res = stop_instance()
	elif selected_second_menu == "7":
		json_res = get_simple_instanceinfo()
	else:
		print("준비중입니다")	
	return json_res

def get_simple_instanceinfo():
	elbInstArr = myelb.get_elb_instances()

	ret_obj = search_ec2instance("", "", "", "")
	instArr=[]
	for idx, oneObj in enumerate(ret_obj):
		InstanceId = oneObj.get("InstanceId")
		objInfo = get_simple_ec2instance_info(oneObj)
		dnsYn="N"
		for idx, elbObj in enumerate(elbInstArr):
			elbInfoArr = elbObj.split(" : ")
			if InstanceId == elbInfoArr[2]:
				objInfo = objInfo+" : "+elbInfoArr[1]
				dnsYn="Y"
				break
		if dnsYn == "N":
			objInfo = objInfo+" : no elb"
		instArr = objInfo.split(" : ")
		print(instArr[0])
		print(instArr[2])
		print(instArr[4])
		print(instArr[7])
		print("")
	return "success"

def create_instance():
	print("ec2 instance 를 생성합니다.")
	print("instance 생성시 이름을 입력하세요 : ")
	instanceNm=goMain.goPage_inputValCheck(selected_first_menu) # 입력시 p, x 입력시 이전 메뉴 또는 프로그램 종료 진행
	instanceId=""
	print("instance 로 생성할 linux이미지를 선택합니다.")
	print("linux 이미지는 Default로 amazon Linux를 설치합니다.")
	while 1>0:
		print("1.Default로 설치합니다. 2.검색해서 설치합니다.")
		nextStep=goMain.goPage_inputValCheck(selected_first_menu) # 입력시 p, x 입력시 이전 메뉴 또는 프로그램 종료 진행
		selectedImageInfoArr = []
		searchImageKeyword = ""
		if nextStep == "2":
			while 0<1:
				print("이미지를 검색할 단어를 입력하세요.")
				searchImageKeyword=goMain.goPage_inputValCheck(selected_first_menu) # 입력시 p, x 입력시 이전 메뉴 또는 프로그램 종료 진행
				selectedImageInfoArr = search_instance_image(searchImageKeyword)
				if selectedImageInfoArr != "research":
					break
			break
		elif nextStep == "1":
			selectedImageInfoArr = search_instance_image("")
			break
		else:
			print("잘못 선택하셨습니다. 다시 선택해주세요.")
	#selectedImageInfoArr[3]
	print("Subnet을 선택합니다.")
	selectedSubnetInfoArr = mySubnet.select_subnet()
	#selectedSubnetInfoArr[3]
	print("Security Group을 선택합니다.")
	selectedSGInfoArr = mysg.select_sg("vpc-id",selectedSubnetInfoArr[4])
	print("instance 에 접속에 필요한 key-pairs 를 선택합니다.")
	selectedkeysInfoArr = mykeys.select_keypairs()
	print("instance 에 적용할 권한인 instance profile을 선택합니다.")
	selectedInstanceProfileInfoArr = myroles.select_instance_profiles()

	print("instance 를 생성하시겠습니까?(y/n)")
	netStepYN=goMain.goPage_inputValCheck(selected_first_menu) # 입력시 p, x 입력시 이전 메뉴 또는 프로그램 종료 진행
	if netStepYN.lower() == 'y':
		command = "aws ec2 run-instances --image-id "+selectedImageInfoArr[3]
		command = command+" --instance-type t2.micro --count 1"
		command = command+" --subnet-id "+selectedSubnetInfoArr[3]+" --associate-public-ip-address"
		command = command+" --security-group-ids "+selectedSGInfoArr[1]
		command = command+" --iam-instance-profile Name="+selectedInstanceProfileInfoArr[0]+" --key-name "+selectedkeysInfoArr[1]
		command = command+" --query Instances[*].InstanceId --output text"
		instanceId = cmdUtil.create_resource(command, instanceNm)
	print("Instance 생성 되었습니다.")
	print("instance OS 명을 입력하세요 (예: ubuntu): ")
	osNm=goMain.goPage_inputValCheck(selected_first_menu) # 입력시 p, x 입력시 이전 메뉴 또는 프로그램 종료 진행
	cmdUtil.create_anytag(instanceId,'OSType',osNm)	
	retStr = {"instanceNm":instanceNm, "instanceId":instanceId}
	return retStr

def search_ec2instance(search_vpc, search_subnet, search_tagname, instance_state):
	search_word = ""
	if search_vpc != "":
		search_word = search_word+" Name=vpc-id,Values="+search_vpc
	if search_subnet != "":
		search_word = search_word+" Name=subnet-id,Values="+search_subnet
	if search_tagname != "":
		search_word = search_word+" Name=tag-value,Values="+search_tagname
	if instance_state != "":
		search_word = search_word+" Name=instance-state-name,Values="+instance_state

	if search_word != "":
		search_word = "--filter"+search_word

	command = "aws ec2 describe-instances "+search_word+" --query Reservations[*].Instances[0]"
	json_res = cmdUtil.getJson_exec_commd(command)
	return json_res

def search_instance_image(searchStr):
	if searchStr == "":
		command = 'aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*-x86_64-gp2" "Name=state,Values=available" --query "reverse(sort_by(Images, &CreationDate))[:3]"'
	#elif (searchStr.lower()).contains("ubuntu"):
	elif "ubuntu" in searchStr.lower():
		command = 'aws ec2 describe-images --image-id ami-04876f29fd3a5e8ba ami-0ba5cd124d7a79612 ami-08508144e576d5b64 --query "reverse(sort_by(Images, &CreationDate))[:3]"'
	else:
		searchStr = "*"+searchStr+"*"
		command = 'aws ec2 describe-images --owners amazon --filters "Name=name,Values='+searchStr+'" "Name=state,Values=available" --query "reverse(sort_by(Images, &CreationDate))[:3]"'

	ret_obj = cmdUtil.getJson_exec_commd(command)
	selectedObjInfoArr=[]
	objArr=[]
	if len(ret_obj) < 1:
		print("해당 이미지가 없습니다.")
		goMain.go_second_menu(selected_first_menu)
	else:
		i=0
		for oneObj in ret_obj:
			i+=1
			objInfo = get_simple_image_info(oneObj)
			objArr.append(objInfo)
			print(str(i)+"."+objInfo)
	print("p.다시 검색해서 선택합니다.")			
	selectedNo=goMain.goPage_inputValCheck(selected_first_menu) # 입력시 p, x 입력시 이전 메뉴 또는 프로그램 종료 진행
	# 사용자가 입력한 번호가 vpc arr 보다 많으면 처음부터 다시 시작.
	if selectedNo == "p" or selectedNo == "P":
		selectedObjInfoArr = "research"
	elif int(selectedNo) > len(objArr):
		print("잘못 선택하셨습니다. 처음부터 다시 시작합니다.")
		goMain.go_second_menu(selected_first_menu)
	else:
		# 선택한 번호에 맞는 vpcid를 변수에 저장합니다.
		selectedObjInfoArr = (objArr[int(selectedNo)-1]).split(' : ')
	# for index in range(len(objArr)):
	# 	if selectedNo == str(index+1):
	# 		selectedObjInfoArr = (objArr[index]).split(' : ')
	# 		break

	return selectedObjInfoArr	

def get_simple_image_info(jsonObj):
	ImageId = jsonObj.get("ImageId")
	Architecture = jsonObj.get("Architecture")
	PlatformDetails = jsonObj.get("PlatformDetails")
	Name = jsonObj.get("Name")
	retInfo = Name+" : "+PlatformDetails+" : "+Architecture+" : "+ImageId
	return retInfo


def search_all_ec2instance(search_vpc, search_subnet, search_tagname):
	ret_obj = search_ec2instance(search_vpc, search_subnet, search_tagname, "")
	objArr=[]
	if len(ret_obj) < 1:
		print("먼저 ec2 Instance를 생성해 주세요.")
	else:
		i=0
		for oneObj in ret_obj:
			i+=1
			objInfo = get_simple_ec2instance_info(oneObj)
			print(str(i)+"."+objInfo)
			objArr.append(objInfo)
	return objArr

def get_simple_ec2instance_info(jsonObj):
	PublicIpAddress = cmdUtil.nullToNoname(jsonObj.get("PublicIpAddress"),"no public ip")
	PrivateIpAddress = cmdUtil.nullToNoname(jsonObj.get("PrivateIpAddress"),"no private ip")
	InstanceId = jsonObj.get("InstanceId")
	SubnetId = cmdUtil.nullToNoname(jsonObj.get("SubnetId"),"no subnet id")
	VpcId = cmdUtil.nullToNoname(jsonObj.get("VpcId"),"no vpc id")
	currentState = (jsonObj.get("State")).get("Name")
	tagValue = ""
	tagKey = "Name"
	if cmdUtil.is_json_key_present(jsonObj,"Tags"):
		tagValue = cmdUtil.getString_tagValue(jsonObj.get("Tags"),tagKey)
	else:
		tagValue = "noname"
	retInfo = cmdUtil.nullToNoname(tagValue,"noname")+" : "+currentState+" : "+PublicIpAddress+" : "+PrivateIpAddress+" : "+InstanceId+" : "+VpcId+" : "+SubnetId
	return retInfo

def select_ec2instance_byId(instanceId):
	command = "aws ec2 describe-instances --instance-ids "+instanceId+" --query Reservations[*].Instances[0]"
	json_res = cmdUtil.getJson_exec_commd(command)
	selectedObjInfoArr=[]
	for oneObj in json_res:
		objInfo = get_simple_ec2instance_info(oneObj)
		selectedObjInfoArr.append(objInfo)
	return selectedObjInfoArr

def select_ec2instance(search_vpc, search_subnet, search_tagname, instance_state):
	ret_obj = search_ec2instance(search_vpc, search_subnet, search_tagname, instance_state)
	objArr=[]	
	if len(ret_obj) < 1:
		print("먼저 ec2 Instance를 생성해 주세요.")
		goMain.go_second_menu(selected_first_menu)
	else:
		i=0
		for oneObj in ret_obj:
			i+=1
			objInfo = get_simple_ec2instance_info(oneObj)
			objArr.append(objInfo)
			print(str(i)+"."+objInfo)
	selectedNo=goMain.goPage_inputValCheck(selected_first_menu) # 입력시 p, x 입력시 이전 메뉴 또는 프로그램 종료 진행
	# 사용자가 입력한 번호가 vpc arr 보다 많으면 처음부터 다시 시작.
	if int(selectedNo) > len(objArr):
		print("잘못 선택하셨습니다.")
		goMain.go_second_menu(selected_first_menu)
	# 선택한 번호에 맞는 vpcid를 변수에 저장합니다.
	selectedObjInfoArr=[]
	for index in range(len(objArr)):
		if selectedNo == str(index+1):
			selectedObjInfoArr = (objArr[index]).split(' : ')
			break

	return selectedObjInfoArr


def start_instance():
	print("1.instance 리부팅 2.instance 시작")
	nextStep1_YN=goMain.goPage_inputValCheck(selected_first_menu) # 입력시 p, x 입력시 이전 메뉴 또는 프로그램 종료 진행
	search_instance_state="running"
	comment_1 = "리부팅"
	commd_str = "reboot-instances"
	if nextStep1_YN == "2":
		search_instance_state = "stopped"
		commd_str = "start-instances"
		comment_1 = "시작"
	if nextStep1_YN != "1" and nextStep1_YN != "2":
		print("다시 선택해주세요.")
		start_instance()

	print("ec2 Instance를 선택해 주세요.")
	selectedObjInfoArr = select_ec2instance("", "", "", search_instance_state)
	print("("+selectedObjInfoArr[0]+")"+selectedObjInfoArr[4]+" instance 를 "+comment_1+"하시겠습니까?(y/n)")
	nextStep2_YN=goMain.goPage_inputValCheck(selected_first_menu) # 입력시 p, x 입력시 이전 메뉴 또는 프로그램 종료 진행
	if nextStep2_YN[0] == 'Y' or nextStep2_YN[0] == 'y':
		command = "aws ec2 "+commd_str+" --instance-ids "+selectedObjInfoArr[4]
		retMsg = cmdUtil.exec_commd (command)
		print(comment_1+" 요청이 완료되었습니다.")
		goMain.go_second_menu(selected_first_menu)
	else:
		goMain.go_second_menu(selected_first_menu)
	return "success"	


def stop_instance():
	search_instance_state="running"
	print("중지할 ec2 Instance를 선택해 주세요.")
	selectedObjInfoArr = select_ec2instance("", "", "", search_instance_state)
	print("("+selectedObjInfoArr[0]+")"+selectedObjInfoArr[4]+" instance 를 중지하시겠습니까?(y/n)")
	nextStep2_YN=goMain.goPage_inputValCheck(selected_first_menu) # 입력시 p, x 입력시 이전 메뉴 또는 프로그램 종료 진행
	if nextStep2_YN[0] == 'Y' or nextStep2_YN[0] == 'y':
		command = "aws ec2 stop-instances --instance-ids "+selectedObjInfoArr[4]
		retMsg = cmdUtil.exec_commd (command)
		print("중지 요청이 완료되었습니다.")
		goMain.go_second_menu(selected_first_menu)
	else:
		goMain.go_second_menu(selected_first_menu)
	return "success"
	
def remove_instance():
	print("삭제할 ec2 Instance를 선택해 주세요.")
	search_instance_state="running,stopping,stopped"
	selectedObjInfoArr = select_ec2instance("", "", "", search_instance_state)
	print("("+selectedObjInfoArr[0]+")"+selectedObjInfoArr[4]+" instance 를 삭제하시겠습니까?(y/n)")
	nextStep2_YN=goMain.goPage_inputValCheck(selected_first_menu) # 입력시 p, x 입력시 이전 메뉴 또는 프로그램 종료 진행
	if nextStep2_YN[0] == 'Y' or nextStep2_YN[0] == 'y':
		command = "aws ec2 terminate-instances --instance-ids "+selectedObjInfoArr[4]
		retMsg = cmdUtil.exec_commd (command)
		print("삭제 요청이 완료되었습니다.")
		goMain.go_second_menu(selected_first_menu)
	else:
		goMain.go_second_menu(selected_first_menu)
	return "success"	