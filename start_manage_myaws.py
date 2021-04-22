#start main
import network.my_vpcs as myvpcs
import network.my_subnet as mysubnet
import network.my_gateway as mygw
import network.my_net_route as myroute
import json

'''
print("VPC를 검색합니다. vpc이름을 검색할 검색어를 입력하세요")
vpc_src_str=input()
json_res = myvpcs.search_vpcs(vpc_src_str)
print(type(json_res))
for myvpc in json_res:
	tagNm=''
	print(myvpc)
	tags = myvpc.get("Tags")
	for name, val in tags:
		if name == 'Name':
			tagNm='('+val+')'
	print(tagNm)
	print(myvpc.myvpc["VpcId"])
	#print(myVpc.Tags[*].myvpc.VpcId
'''
print("아래 관리 항목중 하나를 선택하세요.")
print("1.vpc 생성 2.subnet 생성 3.gateway 생성 4.Route table 생성")
print("5.Route 생성 6.security group 생성 ")
print("70.vpc 조회 71.subnet 조회 72.gateway 조회 73.Router 조회")
print("74.Router table 조회 75.security group 조회")
print("80.s3 조회 ")
print("90.ec2 instance 조회 \n")
my_step1=input()
if my_step1 == "1":
	json_res = myvpcs.create_vpc()
	print(json_res)
elif my_step1 =='2':
	json_res = mysubnet.create_subnet()
	print(json_res)
elif my_step1 =='3':
	json_res = mygw.create_gateway()
	print(json_res)
elif my_step1 =='4':
	json_res = myroute.create_routeTable()
	print(json_res)
elif my_step1 =='5':
	json_res = myroute.create_route()
	print(json_res)	