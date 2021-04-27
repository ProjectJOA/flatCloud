import utils.exec_aws_cmd_util as cmdUtil
import utils.go_main as goMain
import network.my_vpcs as myVpcs
import json

def create_subnet():
	print("AWS Subnet을 생성합니다.")
	print("Subnet 생성시 이름을 입력하세요 : ")
	subnetNm=input()		#생성될 object들의 접두사.
	print("Subnet을 생성할 Vpc를 선택합니다.")
	# 등록된 vpc 목록을 가져옵니다.
	selectedVpcInfoArr = myVpcs.select_vpc()
	#print(selectedVpcInfoArr)		
	print("Subnet의 cidr-block을 선별하고 있습니다.")
	subnetCidrB = get_unregistered_subnetmax_cidr(selectedVpcInfoArr[2], selectedVpcInfoArr[1])
	print(subnetCidrB+" cidr-block으로 subnet을 생성하시겠습니까?")
	print("1.생성합니다. 2.IP 대역을 직접 입력합니다.")
	step1=input()
	if step1 == "1":
		print("subnet 생성 진행중입니다.")
	elif step1 == "2":
		print("IP 대역을 직접 입력해주세요. 예) "+subnetCidrB)
		subnetCidrB=input()
		ret_obj = search_subnets_byCidr(selectedVpcInfoArr[2], subnetCidrB)
		if len(ret_obj) > 0:
			print("입력하신 IP 대역이 이미 등록되어 있습니다.")
			goMain.go_main()
	else:
		print("잘못 입력하셨습니다. 프로그램을 다시 시작해주세요.")
		goMain.go_main()

	command = 'aws ec2 create-subnet --vpc-id '+selectedVpcInfoArr[2]+' --cidr-block '+subnetCidrB+' --availability-zone ap-northeast-2a --query Subnet.SubnetId --output text'
	credSubnetId = cmdUtil.create_resource(command, subnetNm)
	print("subnet이 생성되었습니다.")
	retStr = {"SubnetId":credSubnetId, "cidr-block":subnetCidrB}
	return retStr
#vpc 의 cidr 기준으로 3번째 자리로 해서 사용가능한 IP 대역을 return 한다.
def get_unregistered_subnetmax_cidr(selectedVpcId, vpcCidr):
	vpcCidrArr = vpcCidr.split('.')
	srcCidr=0
	for i in range(0, 255):
		srcCidr=vpcCidrArr[0]+"."+vpcCidrArr[1]+"."+str(i)+"."
		json_objs = search_subnets_byCidr(selectedVpcId, srcCidr)
		if len(json_objs) == 0:
			break
	srcCidr=srcCidr+"0/24"
	return srcCidr
#vpcid에 cidr로 subnet을 검색한다.
def search_subnets_byCidr(selectedVpcId, selectedSubnetCidr ):
	command = 'aws ec2 describe-subnets --filter Name=vpc-id,Values='+selectedVpcId+' Name=cidr-block,Values='+selectedSubnetCidr +'* --query Subnets[*]'
	json_res = cmdUtil.getJson_exec_commd(command)
	return json_res

def search_subnets(srcStr):
	if srcStr == 'search-all':
		command = 'aws ec2 describe-subnets --query Subnets[*]'
	else:
		command = 'aws ec2 describe-subnets  --filter Name=tag-value,Values=*'+srcStr+'* --query Subnets[*]'
	json_res = cmdUtil.getJson_exec_commd(command)
	return json_res

def search_all_subnets_arr():
	ret_obj = search_subnets("search-all")
	objArr=[]
	if len(ret_obj) < 1:
		print("먼저 subnet을 생성해 주세요.")
		goMain.go_main()
	else:
		i=0
		for oneObj in ret_obj:
			i+=1
			objInfo = get_simple_subnet_info(oneObj)
			objArr.append(objInfo)
			print(objInfo)
	return objArr

def get_simple_subnet_info(jsonObj):
	cidrBlock = jsonObj.get("CidrBlock")
	subnetId = jsonObj.get("SubnetId")
	VpcId = jsonObj.get("VpcId")
	availabilityZone = jsonObj.get("AvailabilityZone")
	tagValue = ""
	tagKey = "Name"
	if cmdUtil.is_json_key_present(jsonObj,"Tags"):
		tagValue = cmdUtil.getString_tagValue(jsonObj.get("Tags"),tagKey)
	else:
		tagValue = "noname"
	retSubnetInfo = tagValue+" : "+cidrBlock+" : "+availabilityZone+" : "+subnetId+" : "+VpcId
	return retSubnetInfo

def select_subnet():
	ret_obj = search_subnets('search-all')
	objArr=[]	
	if len(ret_obj) < 1:
		print("먼저 Subnet을 생성해 주세요.")
		goMain.go_main()
	else:
		i=0
		for oneObj in ret_obj:
			i+=1
			objInfo = get_simple_subnet_info(oneObj)
			objArr.append(objInfo)
			print(str(i)+"."+objInfo)
	selectedNo=input()
	# 사용자가 입력한 번호가 vpc arr 보다 많으면 처음부터 다시 시작.
	if int(selectedNo) > len(objArr):
		print("잘못 선택하셨습니다. 처음부터 다시 시작합니다.")
		goMain.go_main()
	# 선택한 번호에 맞는 vpcid를 변수에 저장합니다.
	selectedObjInfoArr=[]
	for index in range(len(objArr)):
		if selectedNo == str(index+1):
			selectedObjInfoArr = (objArr[index]).split(' : ')
			break

	return selectedObjInfoArr	