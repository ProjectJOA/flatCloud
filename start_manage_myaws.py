#start main
import network.my_vpcs as myvpcs
import network.my_subnet as mysubnet
import network.my_gateway as mygw
import network.my_net_route as myroute
import network.my_securitygroup as mysg
import instance.my_ec2instance as myec2
import json

def start_main():
	first_menu1 = "1.Vpc 2.Subnet 3.Internet Gateway 4.Route Table 5.Security Group"
	first_menu2 = "6.ec2 instance"
	second_common_menu = "1.조회 2.신규생성 3.수정 4.삭제"

	print("\n아래 관리 항목중 하나를 선택하세요.")
	print(first_menu1) # 메뉴 출력
	print(first_menu2) # 메뉴 출력

	selected_first_menu=input()
	print("상세 실행할 항목을 선택하세요.")

	if selected_first_menu == "1": # vpc 선택 
		print(second_common_menu) # 상세 메뉴 출력
		selected_second_menu=input()
		if selected_second_menu == "1":
			objArr = myvpcs.search_all_vpcs_arr()
			start_main()
		elif selected_second_menu == "2":
			json_res = myvpcs.create_vpc()
			print(json_res)
		else:
			print("준비중입니다.")
	elif selected_first_menu == "2": # subnet 선택 
		print(second_common_menu) # 상세 메뉴 출력
		selected_second_menu=input()
		if selected_second_menu == "1":
			objArr = mysubnet.search_all_subnets_arr()
		elif selected_second_menu == "2":
			json_res = mysubnet.create_subnet()
			print(json_res)
		else:	
			print("준비중입니다.")
	elif selected_first_menu == "3": # gateway 선택	
		print(second_common_menu) # 상세 메뉴 출력
		print("5.Vpc연결 6.Vpc연결해제")
		selected_second_menu=input()
		if selected_second_menu == "1":
			objArr = mygw.search_all_gw_arr()
		elif selected_second_menu == "2":
			json_res = mysubnet.create_gateway()
		else:	
			print("준비중입니다.")
	elif selected_first_menu == "4": # Route Table 선택
		print(second_common_menu) # 상세 메뉴 출력
		print("5.Route 생성 6.Route 삭제")
		selected_second_menu=input()
		if selected_second_menu == "1":
			objArr = myroute.search_all_routeTables_arr()
		elif selected_second_menu == "2":
			json_res = myroute.create_routeTable()
			print(json_res)
		else:	
			print("준비중입니다.")				
	elif selected_first_menu == "5": # Security Group 선택
		print("준비중입니다.")
	elif selected_first_menu == "6": # ec2 instance 선택
		print(second_common_menu) # 상세 메뉴 출력
		print("5.instance 리부트/시작 6.instance 종료")
		selected_second_menu=input()
		if selected_second_menu == "1":
			objArr = myec2.search_all_ec2instance("","","")
		elif selected_second_menu == "2":
			objArr = myec2.create_instance()
		elif selected_second_menu == "4":
			objArr = myec2.remove_instance()						
		elif selected_second_menu == "5":
			objArr = myec2.start_instance()
		elif selected_second_menu == "6":
			objArr = myec2.stop_instance()						
	else:
		print("준비중입니다")

# 실행..
start_main()
#print("1.vpc 생성 2.subnet 생성 3.gateway 생성 4.Route table 생성")
#print("5.Route 생성 6.security group 생성 ")
#print("70.vpc 조회 71.subnet 조회 72.gateway 조회 73.Router 조회")
#print("74.Router table 조회 75.security group 조회")
#print("80.s3 조회 ")
#print("90.ec2 instance 조회 \n")
