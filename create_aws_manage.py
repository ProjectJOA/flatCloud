import subprocess

def start_main(cur_step):
	inp_step=''
	if cur_step == 0:
		print("1. 신규생성 2.삭제 3.수정 4.ec2 인스턴스 스타트/스탑 ")
		inp_step=input()
	return inp_step

def exec_commd (commd):
	retId=((subprocess.check_output(commd, stderr=subprocess.STDOUT, shell=True)).decode("utf-8")).rstrip('\r\n')
	return retId

def create_tagName (resourceId, tagNm):
	cmd = 'aws ec2 create-tags --resources '+resourceId+' --tags Key=Name,Value='+tagNm
	exec_commd(cmd)

def create_resource(commd, tagNm):
	retId = exec_commd(commd)
	create_tagName(retId, tagNm)
	return retId

def manage_step1_controll(step1):
	if step1 == 1:
		print("1. 네트워크 관련 생성 2.ec2 인스턴스 생성 3.기타")
	else-if step1 == 2:
		print("1. 네트워크 관련 삭제 2.ec2 인스턴스 삭제 3.기타")
	else-if step1 == 3:
		print("1. 네트워크 관련 수정 2.ec2 인스턴스 수정 3.기타")
	else-if step1 == 4:
		print("1. ec2 인스턴스 스타트 2. ec2 인스턴스 스탑")
	else:
		print('잘못 입력 하셨습니다. 다시 선택해주세요.')
		start_main(0) #처음부터 다시 하는 방법 확인 필요
	inp_step=input()
	return inp_step

def manage_step2_comment(gbn, step2):
	comment = ''
	if step == 1:
		comment = "1. Vpc관련 "+gbn+" 2. 서브넷 관련 "+gbn+" 3. 게이트웨이 "+gbn+" 4. 라우터 관련 "+gbn
	else-if step == 2:
		comment = "1. ec2 인스턴스 "+gbn+" 2. ec2 시큐어그룹 "+gbn
	else-if step == 3:
		comment = "1. s3 버킷 "+gbn+" 2. iam policy "+gbn
	return comment

def manage_step2_controll(step1, step2):
	gbn=""
	if step1 == 1:
		gbn = "생성"
	else-if step1 == 2:
		gbn = "삭제"
	else-if step1 == 3:
		gbn = "수정"
	manage_step2_comment(gbn, step2)

# 입력변수 선언
manage_step1=''
manage_step2=''
manage_step3=''

# 시작
print("AWS 서비스 관리를 시작합니다.\n아래 관리하고자 하는 항목을 선택하세요.")
manage_step1 = start_main(0) 
manage_step2 = manage_step1_controll(manage_step1)
manage_step3 = manage_step2_controll(manage_step1, manage_step2)

print("AWS VPC를 생성합니다.")
print("AWS VPC, EC2 instance 생성시 이름을 입력하세요 : ")
pre_name=input()		#생성될 object들의 접두사.
vpcNm = pre_name+"_vpc" #vpc tag name
credVpcId='' 			#vpc id
subNm = pre_name+"_subnet"	#subnet tag name
credSubnetId=''				#subnet id
gwNm = pre_name+"_gw"		#gateway tag name
routerNm = pre_name+"_public_RT"

print("AWS VPC 의 IP 대역을 입력하세요. 예)10.5.0.0/16 ")
vpc_ips=input()

command = 'aws ec2 create-vpc --cidr-block '+vpc_ips+' --query Vpc.VpcId --output text'
credVpcId = create_resource(command, vpcNm)

print("AWS VPC가 생성되었습니다. vpc-id : ", credVpcId)
print("AWS VPC의 subnet을 IP 대역을 입력하세요. 예)10.5.10.0/24 ")
sub_ips=input()

command = 'aws ec2 create-subnet --vpc-id '+credVpcId+' --cidr-block '+sub_ips+' --availability-zone ap-northeast-2a --query Subnet.SubnetId --output text'
credSubnetId = create_resource(command, subNm)
print("AWS VPC의 subnet을 생성합니다.")
print("AWS VPC의 subnet이 생성되었습니다. subnet_id : ",credSubnetId)

print("AWS VPC의 gateway를 생성합니다.")
command = 'aws ec2 create-internet-gateway --query InternetGateway.InternetGatewayId --output text'
credGwId = create_resource(command, gwNm)
command = 'aws ec2 attach-internet-gateway --internet-gateway-id '+credGwId+' --vpc-id '+credVpcId
exec_commd(command)
print("AWS VPC의 gateway를 생성되었습니다 gateway-id : ",credGwId)

print("Subnet의 router table을 생성합니다.")
command = 'aws ec2 create-route-table --vpc-id '+credVpcId +'--query RouteTable.RouteTableId --output text'
creRtId = create_resource(command, routerNm)
print("Subnet의 router table을 생성했습니다. router-table-id : ", creRtId)

print("Subnet의 router와 gateway를 연결합니다.")
command = 'aws ec2 create-route --route-table-id '+creRtId+' --destination-cidr-block 0.0.0.0/0 --gateway-id '+credGwId
exec_commd(command)
print("Subnet의 router와 gateway를 연결되었습니다.")

print("Subnet의 router와 subnet을 연결합니다.")
command = 'aws ec2 associate-route-table --route-table-id '+creRtId+' --subnet-id '+credSubnetId
exec_commd(command)
print("Subnet의 router와 subnet을 연결되었습니다.")

