import utils.exec_aws_cmd_util as cmdUtil
import network.my_vpcs as myVpcs
import network.my_subnet as mySubnet

def create_instance():
	print("ec2 instance 를 생성합니다.")
	print("instance 생성시 이름을 입력하세요 : ")
	instanceNm=input()		#생성될 object들의 접두사.
	print("instance 로 생성할 linux이미지를 선택합니다.")
	# 등록된 vpc 목록을 가져옵니다.
	selectedImageInfoArr = search_instance_image("")
	#selectedImageInfoArr[3]
	print("Subnet을 선택합니다.")
	selectedSubnetInfoArr = mySubnet.select_subnet()
	#selectedSubnetInfoArr[3]

	command = "aws ec2 run-instances --image-id "+selectedImageInfoArr[3]
	command = command+" --instance-type t2.micro --count 1"
	command = command+" --subnet-id "+selectedSubnetInfoArr[3]+" --associate-public-ip-address"
	command = command+" --security-group-ids sg-0adcfaa3510cb8958 "
	command = command+" --iam-instance-profile Name="+instanceNm+" --key-name vini_key"
	print(command)
	return ""

def search_ec2instance(search_vpc, search_subnet, search_tagname):
	search_word = ""
	if search_vpc != "":
		search_word = search_word+" Name=vpc-id,Values="+search_vpc
	if search_subnet != "":
		search_word = search_word+" Name=subnet-id,Values="+search_subnet
	if search_tagname != "":
		search_word = search_word+" Name=tag-value,Values="+search_tagname

	if search_subnet != "":
		search_word = "--filter"+search_word

	command = "aws ec2 describe-instances "+search_word+" --query Reservations[*].Instances[0]"
	json_res = cmdUtil.getJson_exec_commd(command)
	return json_res

def search_instance_image(searchStr):
	if searchStr == "":
		searchStr = "amzn2-ami-hvm-*-x86_64-gp2"
	else:
		searchStr = "*"+searchStr+"*"
	command = 'aws ec2 describe-images --owners amazon --filters "Name=name,Values='+searchStr+'" "Name=state,Values=available" --query "reverse(sort_by(Images, &CreationDate))"  --output text'
	ret_obj = cmdUtil.getJson_exec_commd(command)
	if len(ret_obj) < 1:
		print("해당 이미지가 없습니다.")
		exit()
	else:
		objArr=[]
		i=0
		for oneObj in ret_obj:
			i+=1
			objInfo = get_simple_image_info(oneObj)
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

def get_simple_image_info(oneObj):
	ImageId = jsonObj.get("ImageId")
	Architecture = jsonObj.get("Architecture")
	PlatformDetails = jsonObj.get("PlatformDetails")
	Name = jsonObj.get("Name")
	retInfo = Name+" : "+PlatformDetails+" : "+Architecture+" : "+ImageId
	return retInfo


def search_all_ec2instance(search_vpc, search_subnet, search_tagname):
	ret_obj = search_ec2instance(search_vpc, search_subnet, search_tagname)
	if len(ret_obj) < 1:
		print("먼저 ec2 Instance를 생성해 주세요.")
	else:
		i=0
		for oneObj in ret_obj:
			i+=1
			objInfo = get_simple_ec2instance_info(oneObj)
			print(str(i)+"."+objInfo)

def get_simple_ec2instance_info(jsonObj):
	PublicIpAddress = jsonObj.get("PublicIpAddress")
	PrivateIpAddress = jsonObj.get("PrivateIpAddress")
	InstanceId = jsonObj.get("InstanceId")
	SubnetId = jsonObj.get("SubnetId")
	VpcId = jsonObj.get("VpcId")
	currentState = (jsonObj.get("State")).get("Name")
	tagValue = ""
	tagKey = "Name"
	if cmdUtil.is_json_key_present(jsonObj,"Tags"):
		tagValue = cmdUtil.getString_tagValue(jsonObj.get("Tags"),tagKey)
	else:
		tagValue = "noname"
	retInfo = cmdUtil.nullToNoname(tagValue,"noname")+" : "+currentState+" : "+PublicIpAddress+" : "+PrivateIpAddress+" : "+InstanceId+" : "+VpcId+" : "+SubnetId
	return retInfo

def select_ec2instance(search_vpc, search_subnet, search_tagname):
	ret_obj = search_ec2instance(search_vpc, search_subnet, search_tagname)
	if len(ret_obj) < 1:
		print("먼저 ec2 Instance를 생성해 주세요.")
		exit()
	else:
		objArr=[]
		i=0
		for oneObj in ret_obj:
			i+=1
			objInfo = get_simple_ec2instance_info(oneObj)
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

def start_instance():
	print("먼저 ec2 Instance를 선택해 주세요.")
	selectedObjInfoArr = select_ec2instance("", "", "")
	print(selectedObjInfoArr)
	return selectedObjInfoArr