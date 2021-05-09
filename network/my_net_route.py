import utils.exec_aws_cmd_util as cmdUtil
import utils.go_main as goMain
import network.my_vpcs as myVpcs
import network.my_subnet as mySubnet
import network.my_gateway as myGw
import json

def route_startMain(selected_second_menu):
	json_res = ""
	if selected_second_menu == "1":
		json_res = search_all_routeTables_arr()
	elif selected_second_menu == "2":
		json_res = create_routeTable()			
	else:	
		print("준비중입니다.")
	return json_res

#진행중..
def create_routeTable():
	print("Route table을 생성합니다.")
	print("Route table 생성시 이름을 입력하세요 (예 test_public_RT): ")
	routeTableNm=input()	#생성될 object 이름.
	print("Route table을 생성할 Vpc를 선택합니다.")
	# 등록된 vpc 목록을 가져옵니다.
	selectedVpcInfoArr = myVpcs.select_vpc()
	print("Route table 생성중입니다.")	
	command = 'aws ec2 create-route-table --vpc-id '+selectedVpcInfoArr[2]+' --query RouteTable.RouteTableId --output text'
	credRtId = cmdUtil.create_resource(command, routeTableNm)
	print("Route table이 생성되었습니다.")
	retStr = {"RouteTableId":credRtId, "RouteTableName":routeTableNm}
	#route 생성..- gateway연결등 start..
	print("Public network 이용을 위해 route-table에 Gateway를 연결해야 합니다.")
	print("route-table에 Internet Gateway 또는 NAT Gateway를 연결을 진행하시겠습니까? (y/n)")
	nextStepYN=input()
	if nextStepYN[0] == 'Y' or nextStepYN[0] == 'y':
		create_route()
	#route 생성..- gateway연결등 end..
	return retStr

def create_route():
	#print("먼저 Subnet을 선택합니다.")
	#selectedSubnetInfoArr = mySubnet.select_subnet()
	print("먼저 Vpc를 선택합니다.")
	selectedVpcInfoArr = myVpcs.select_vpc()
	print("Vpc에 만들어진 route-table를 선택합니다.")
	selectedRouteTableArr = select_routeTable(selectedVpcInfoArr[2])
	selectedGatewayArr = myGw.select_gw()
	#"aws ec2 describe-route-tables --filter Name=vpc-id,Values=vpc-0ee42dfba9b4f6010"
	command = 'aws ec2 create-route --route-table-id '+selectedRouteTableArr[1]+' --destination-cidr-block 0.0.0.0/0 --gateway-id '+selectedGatewayArr[1]
	json_res = cmdUtil.exec_commd(command)
	return json_res

def get_simple_routeTable_info(jsonObj):
	routeTableId = jsonObj.get("RouteTableId")
	VpcId = jsonObj.get("VpcId")
	tagValue = ""
	tagKey = "Name"
	if cmdUtil.is_json_key_present(jsonObj,"Tags"):
		tagValue = cmdUtil.getString_tagValue(jsonObj.get("Tags"),tagKey)
	else:
		tagValue = "noname"
	retRouteTableInfo = cmdUtil.nullToNoname(tagValue,"noname")+" : "+routeTableId+" : "+VpcId
	return retRouteTableInfo

def search_routeTables(srcStr):
	if srcStr == 'search-all':
		command = 'aws ec2 describe-route-tables --query RouteTables[*]'
	else:
		command = 'aws ec2 describe-route-tables --filter Name=vpc-id,Values='+srcStr+' --query RouteTables[*]'
	json_res = cmdUtil.getJson_exec_commd(command)
	return json_res

def search_all_routeTables_arr():
	ret_obj = search_routeTables("search-all")
	objArr=[]
	if len(ret_obj) < 1:
		print("먼저 route table을 생성해 주세요.")
		goMain.go_main()
	else:
		i=0
		for oneObj in ret_obj:
			i+=1
			objInfo = get_simple_routeTable_info(oneObj)
			objArr.append(objInfo)
			print(str(i)+"."+objInfo)
	return objArr

def select_routeTable(searchVpcId):
	ret_obj = search_routeTables(searchVpcId)
	objArr=[]	
	if len(ret_obj) < 1:
		print("먼저 Route Table 을 생성해 주세요.")
		goMain.go_main()
	else:
		i=0
		for oneObj in ret_obj:
			i+=1
			objInfo = get_simple_routeTable_info(oneObj)
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