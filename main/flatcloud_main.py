import network.my_vpcs as myvpcs
import network.my_subnet as mysubnet
import network.my_gateway as mygw
import network.my_net_route as myroute
import network.my_elb as myelb
import network.my_securitygroup as mysg
import instance.my_ec2instance as myec2
import json

def go_first_menu(selected_first_menu):
	second_common_menu = "p.뒤로가기 1.조회 2.신규생성 3.수정 4.삭제"	
	selected_second_menu=""
	if selected_first_menu == "1": # vpc 선택 
		print(second_common_menu) # 상세 메뉴 출력
		selected_second_menu=input()
		if selected_second_menu == "1":
			objArr = myvpcs.search_all_vpcs_arr()
		elif selected_second_menu == "2":
			json_res = myvpcs.create_vpc()
			print(json_res)
		elif selected_second_menu == "p":
			start_main()
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
		elif selected_second_menu == "p":
			start_main()			
		else:	
			print("준비중입니다.")
	elif selected_first_menu == "3": # gateway 선택	
		print(second_common_menu) # 상세 메뉴 출력
		print("5.Vpc연결 6.Vpc연결해제")
		selected_second_menu=input()
		if selected_second_menu == "1":
			objArr = mygw.search_all_gw_arr()
		elif selected_second_menu == "2":
			json_res = mygw.create_gateway()
		elif selected_second_menu == "p":
			start_main()			
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
		elif selected_second_menu == "p":
			start_main()			
		else:	
			print("준비중입니다.")				
	elif selected_first_menu == "5": # Security Group 선택
		print(second_common_menu) # 상세 메뉴 출력
		print("5.Inbound/Outbound 조회")
		print("6.Inbound 추가 7.Outbound 추가")
		print("8.Inbound/Outbound 삭제")
		selected_second_menu=input()
		if selected_second_menu == "1":
			objArr = mysg.search_all_sg_arr()
		elif selected_second_menu == "2":
			objArr = mysg.create_sg()
		elif selected_second_menu == "5":
			objArr = mysg.search_inoutBound("inout")
		elif selected_second_menu == "6":
			objArr = mysg.add_inoutBound("in")			
		elif selected_second_menu == "7":
			objArr = mysg.add_inoutBound("out")
		elif selected_second_menu == "8":
			objArr = mysg.del_inoutBound()
		elif selected_second_menu == "p":
			start_main()				
		else:				
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
		elif selected_second_menu == "p":
			start_main()
		else:
			print("준비중입니다")
	elif selected_first_menu == "7": # load balance 선택
		print(second_common_menu) # 상세 메뉴 출력 
		selected_second_menu=input()
		if selected_second_menu == "1":
			objArr = myelb.search_all_elb()
		elif selected_second_menu == "2":
			objArr = myelb.create_loadBalance()
		elif selected_second_menu == "4":
			objArr = myelb.del_elb()
		else:
			print("준비중입니다")
	else:
		print("준비중입니다")
	print("")
	print("상세 실행할 항목을 선택하세요.")
	go_first_menu(selected_first_menu)

def start_main():
	try:
		first_menu1 = "1.Vpc 2.Subnet 3.Internet Gateway 4.Route Table 5.Security Group"
		first_menu2 = "6.ec2 instance 7.load Balance"
		first_menu3 = "x.flatCloud 종료"

		print("\n아래 관리 항목중 하나를 선택하세요.")
		print(first_menu1) # 메뉴 출력
		print(first_menu2) # 메뉴 출력
		print(first_menu3) # 메뉴 출력

		selected_first_menu=input()
		if selected_first_menu == "x":
			print("프로그램을 종료합니다.")
			exit()

		print("상세 실행할 항목을 선택하세요.")
		go_first_menu(selected_first_menu)
		start_main()
	except KeyboardInterrupt:
		print("프로그램을 종료합니다.")
		exit() #종료
	except Exception as e:
		print("프로그램 실행중 오류가 발생하였습니다.",e)
		