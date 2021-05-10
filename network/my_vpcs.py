import utils.exec_aws_cmd_util as cmdUtil
import utils.go_main as goMain
import json

selected_first_menu = "1" # 1 단계 선택 메뉴 번호

def vpc_startMain(selected_second_menu):
	json_res = ""
	if selected_second_menu == "1":
		json_res = search_all_vpcs_arr()
	elif selected_second_menu == "2":
		json_res = create_vpc()
	else:
		print("준비중입니다.")
	return json_res

#vpc 생성합니다.
def create_vpc():
	print("AWS VPC를 생성합니다.")
	print("AWS VPC 생성시 이름을 입력하세요 : ")
	vpcNm=input()		#생성될 object들의 접두사.
	#print("AWS VPC 의 IP 대역을 입력하세요. 예)10.5.0.0/16 ")
	vpc_ips="10.5.0.0/16" #default vpc cidr
	startNo=5
	print("VPC Cidr을 찾고 있습니다.")
	vpc_ips=get_unregistered_vpcmax_cidr(5)
	print(vpc_ips+" IP 대역으로 Vpc를 생성합니다.")
	print("1.생성합니다. 2.IP 대역을 직접 입력합니다.")
	step1=goMain.goPage_inputValCheck(selected_first_menu) # 입력시 p, x 입력시 이전 메뉴 또는 프로그램 종료 진행
	if step1 == "1":
		print("Vpc 생성을 시작합니다.")
	elif step1 == "2":
		while 0<1:
			print("IP 대역을 직접 입력해주세요. 예) 10.5.0.0/16")
			vpc_ips=goMain.goPage_inputValCheck(selected_first_menu) # 입력시 p, x 입력시 이전 메뉴 또는 프로그램 종료 진행
			ret_obj = search_vpcs_byCidr(vpc_ips)
			if len(ret_obj) > 0:
				print("입력하신 IP 대역이 이미 등록되어 있습니다. 다시 입력해주세요")
			else:
				break			
	else:
		print("잘못 입력하셨습니다.")
		goMain.go_second_menu(selected_first_menu)

	command = 'aws ec2 create-vpc --cidr-block '+vpc_ips+' --query Vpc.VpcId --output text'
	credVpcId = cmdUtil.create_resource(command, vpcNm)
	print("Vpc 가 생성되었습니다.")
	retStr = {"vpcId":credVpcId, "cidr":vpc_ips}
	return retStr

def search_vpcs(srcStr):
	if srcStr == 'search-all':
		command = 'aws ec2 describe-vpcs --query Vpcs[*]'
	else:
		command = 'aws ec2 describe-vpcs --filter Name=tag-value,Values=*'+srcStr+'* --query Vpcs[*]'
	json_res = cmdUtil.getJson_exec_commd(command)
	return json_res

def search_all_vpcs_arr():
	ret_obj = search_vpcs("search-all")
	vpcArr=[]
	if len(ret_obj) < 1:
		print("먼저 Vpc를 생성해 주세요.")
		goMain.go_second_menu(selected_first_menu)
	else:
		i=0
		for vpcObj in ret_obj:
			i+=1
			vpcInfo = get_simple_vpc_info(vpcObj)
			vpcArr.append(vpcInfo)
			print(str(i)+"."+vpcInfo)
	return vpcArr

def search_vpcs_byCidr(cidr ):
	command = 'aws ec2 describe-vpcs --filter Name=cidr,Values='+cidr +' --query Vpcs[*]'
	json_res = cmdUtil.getJson_exec_commd(command)
	return json_res	

def get_unregistered_vpcmax_cidr(startNo):
	srcCidr=""
	for i in range(startNo, 255):
		srcCidr="10."+str(i)+".0.0/16"
		json_vpcs = search_vpcs_byCidr(srcCidr)
		if len(json_vpcs) == 0:
			break
	return srcCidr

def get_simple_vpc_info(jsonObj):
	cidr = jsonObj.get("CidrBlock")
	vpcId = jsonObj.get("VpcId")
	tagValue = ""
	tagKey = "Name"
	if cmdUtil.is_json_key_present(jsonObj,"Tags"):
		tagValue = cmdUtil.getString_tagValue(jsonObj.get("Tags"),tagKey)
	retVpcInfo = tagValue+" : "+cidr+" : "+vpcId
	return retVpcInfo

#vpc 목록을 조회하고 사용자의 선택을 받아서 1개의 vpc만 return한다.
def select_vpc():
	vpcArr=[]
	ret_obj = search_vpcs("search-all")
	if len(ret_obj) < 1:
		print("먼저 Vpc를 생성해 주세요.")
		goMain.go_second_menu(selected_first_menu)
	else:
		i=0
		for vpcObj in ret_obj:
			i+=1
			vpcInfo = get_simple_vpc_info(vpcObj)
			vpcArr.append(vpcInfo)
			print(str(i)+"."+vpcInfo)
	selectedVpcNo=goMain.goPage_inputValCheck(selected_first_menu) # 입력시 p, x 입력시 이전 메뉴 또는 프로그램 종료 진행
	# 사용자가 입력한 번호가 vpc arr 보다 많으면 처음부터 다시 시작.
	if int(selectedVpcNo) > len(vpcArr):
		print("잘못 선택하셨습니다.")
		goMain.go_second_menu(selected_first_menu)
	# 선택한 번호에 맞는 vpcid를 변수에 저장합니다.
	selectedVpcInfoArr=[]
	for index in range(len(vpcArr)):
		if selectedVpcNo == str(index+1):
			selectedVpcInfoArr = (vpcArr[index]).split(' : ')
			break

	return selectedVpcInfoArr