import network.my_vpcs as myvpcs
import network.my_subnet as mysubnet
import network.my_gateway as mygw
import network.my_net_route as myroute
import network.my_elb as myelb
import network.my_securitygroup as mysg
import instance.my_ec2instance as myec2
import main.quick_search as quicksearch
import json

def print_second_menus(selected_first_menu):
	second_common_menu = "1.조회 \n2.신규생성 \n4.삭제"
	second_detail_menu = ""
	second_sys_common_menu = "p.뒤로가기 x.종료하기"

	if selected_first_menu == "3": # gateway 선택	
		second_detail_menu = "5.Vpc연결 \n6.Vpc연결해제"
	elif selected_first_menu == "4": # Route Table 선택
		second_detail_menu = "5.Route 생성 \n6.Route 삭제"
	elif selected_first_menu == "5": # Security Group 선택
		second_detail_menu = "5.Inbound/Outbound 조회 \n6.Inbound 추가 \n7.Outbound 추가 \n8.Inbound/Outbound 삭제"
	elif selected_first_menu == "6": # ec2 instance 선택
		second_detail_menu = "5.instance 리부트/시작 \n6.instance 종료 \n7.Instance 간략 조회"
	elif selected_first_menu == "7": # load balance 선택
		second_detail_menu = "5.허용 Port 조회 \n6.허용 Port 추가 \n7.허용 Port 삭제 \n8.연결된 instance 조회 \n9.instance 연결/해제"

	print(second_common_menu) # 2단계 메뉴 출력
	if second_detail_menu != "":
		print(second_detail_menu) # 상세 메뉴 출력
	print(second_sys_common_menu) # 뒤로가기, 종료 메뉴 


def go_first_menu(selected_first_menu):
	selected_second_menu=""
	print_second_menus(selected_first_menu)

	selected_second_menu=input()

	if selected_second_menu.lower() == "p":
		start_main()
	elif selected_second_menu.lower() == "x":
		print("프로그램을 종료합니다.")
		exit()
	json_res = ""
	if selected_first_menu == "1": # vpc 선택 
		json_res = myvpcs.vpc_startMain(selected_second_menu)
	elif selected_first_menu == "2": # subnet 선택 
		json_res = mysubnet.subnet_startMain(selected_second_menu)
	elif selected_first_menu == "3": # gateway 선택
		json_res = mygw.gw_startMain(selected_second_menu)
	elif selected_first_menu == "4": # Route Table 선택
		json_res = myroute.route_startMain(selected_second_menu)
	elif selected_first_menu == "5": # Security Group 선택
		json_res = mysg.sg_startMain(selected_second_menu)
	elif selected_first_menu == "6": # ec2 instance 선택
		json_res = myec2.ec2inst_startMain(selected_second_menu)
	elif selected_first_menu == "7": # load balance 선택
		json_res = myelb.elb_startMain(selected_second_menu)
	else:
		print("준비중입니다")
	print("")
	print("상세 실행할 항목을 선택하세요.")
	go_first_menu(selected_first_menu)

def start_main():
	try:
		first_menu1 = "0.Quick Search \n1.Vpc \n2.Subnet \n3.Internet Gateway \n4.Route Table \n5.Security Group"
		first_menu2 = "6.ec2 instance \n7.load Balance"
		first_menu3 = "x.flatCloud 종료"

		print("\n아래 관리 항목중 하나를 선택하세요.")
		print(first_menu1) # 메뉴 출력
		print(first_menu2) # 메뉴 출력
		print(first_menu3) # 메뉴 출력

		selected_first_menu=input()
		if selected_first_menu == "x":
			print("프로그램을 종료합니다.")
			exit()
		elif selected_first_menu == "0":
			quicksearch.get_ssh_access()
		else:
			print("상세 실행할 항목을 선택하세요.")
			go_first_menu(selected_first_menu)
		start_main()
	except KeyboardInterrupt:
		print("프로그램을 종료합니다.")
		exit() #종료
	except Exception as e:
		print("프로그램 실행중 오류가 발생하였습니다.",e)
		