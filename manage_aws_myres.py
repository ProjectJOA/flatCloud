import subprocess

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
command = 'aws ec2 create-route-table --vpc-id '+credVpcId +' --query RouteTable.RouteTableId --output text'
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

