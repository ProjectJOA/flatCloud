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
	print("subnet이 생성되었습니다.")
	retStr = {"GatewayId":credGwId}
	return retStr