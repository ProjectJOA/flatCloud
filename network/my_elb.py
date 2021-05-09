import utils.exec_aws_cmd_util as cmdUtil
import utils.go_main as goMain
import main.flatcloud_main as flatMain
import network.my_subnet as mySubnet
import network.my_securitygroup as mysg
import instance.my_ec2instance as myec2
import json

selected_first_menu = "7" # 1 단계 선택 메뉴 번호

def elb_startMain(selected_second_menu):
	json_res = ""
	if selected_second_menu == "1":
		json_res = search_all_elb()
	elif selected_second_menu == "2":
		json_res = create_loadBalance()
	elif selected_second_menu == "4":
		json_res = del_elb()
	elif selected_second_menu == "5":
		json_res = search_elb_listeners()
	elif selected_second_menu == "6":
		json_res = add_elb_listener()
	elif selected_second_menu == "7":
		json_res = del_elb_listener()                              
	else:
		print("준비중입니다.")
	return json_res

def create_loadBalance():
    print("load Balance는 http(80) 만 생성 가능합니다.")
    print("생성할 ELB의 명칭을 입력하세요.(예: my-elb)")
    print("ELB 명칭은 알파벳과 - 만 입력가능합니다.")
    inputElbNm=input()
    print("Subnet을 선택합니다.")
    selectedSubnetInfoArr = mySubnet.select_subnet()
    print("ELB에 적용할 Security Group을 선택합니다.")
    selectedSGInfoArr = mysg.select_sg("vpc-id",selectedSubnetInfoArr[4])
    print("ELB에 연결할 instance 의 port를 입력하세요.(예: 80)")
    inputInstPort=input()
    # print("생성할 Protocol을 선택하세요.")
    # print("1.http/https 2.http 3.https ")
    # inputProtocol=input()
    command = 'aws elb create-load-balancer --load-balancer-name '+inputElbNm+' --listeners'
    command = command+' "Protocol=HTTP,LoadBalancerPort=80,InstanceProtocol=HTTP,InstancePort='+inputInstPort+'" '
    command = command+' --subnets '+selectedSubnetInfoArr[3]+' --security-groups '+selectedSGInfoArr[1]
    command = command+' --query DNSName'
    retStr = cmdUtil.exec_commd(command)
    print("ELB 도메인이 생성되었습니다.")
    print(retStr)
    # health check 설정
    retStr = set_configure_healthCheck(inputElbNm)
    if retStr == "success":
        # instance 연결
        register_Instance(inputElbNm, selectedSubnetInfoArr)

    return "success"

def set_configure_healthCheck(inputElbNm):
    print("ELB health check 설정을 진행합니다.")
    print("Health Check 할 Ping Path 를 입력해주세요.")
    inputFileNm=input()
    command = 'aws elb configure-health-check --load-balancer-name '+inputElbNm+' --health-check Target=HTTP:80/'+inputFileNm+',Interval=30,UnhealthyThreshold=2,HealthyThreshold=2,Timeout=3'
    cmdUtil.exec_commd(command)
    return "success"

def del_elb_listener():
    print("먼저 ELB를 선택합니다.")
    selectElbArr = select_elb()
    print("ELB 에 등록된 Port를 조회합니다.")
    objArr = select_elb_listeners(selectElbArr[0])

    print("삭제하실 Port를 선택하세요")
    while 1>0:
        selectPortNo=input()
        if (int(selectPortNo)-1)>len(objArr):
            print("잘못 선택하셨습니다. 다시 선택하세요.")
        else:
            selectedElbPort = objArr[(int(selectPortNo)-1)]
            selectedElbPortArr = selectedElbPort.split(" : ")
            print("선택하신 ("+selectedElbPort+")를 삭제하시겠습니까?(y/n)")
            nextStep2_YN=input()
            if nextStep2_YN.lower() == "y":
                command = 'aws elb delete-load-balancer-listeners --load-balancer-name '+selectElbArr[0]
                command = command +' --load-balancer-ports '+selectedElbPortArr[1]
                retStr = cmdUtil.exec_commd(command)
                break
            else:
                break

    if nextStep2_YN.lower() == "n":
        print("2단계 메뉴로 이동합니다.")
        flatMain.go_first_menu(selected_first_menu)

    return "success"    

def add_elb_listener():
    print("먼저 ELB를 선택합니다.")
    selectElbArr = select_elb()
    print("ELB 에 등록된 Port를 조회합니다.")
    objArr = select_elb_listeners(selectElbArr[0])

    print("허용 Port를 추가하시겠습니까?(y/n)")
    nextStep2_YN=input()
    if nextStep2_YN.lower() == "n":
        print("2단계 메뉴로 이동합니다.")
        flatMain.go_first_menu(selected_first_menu)

    print("Protocol을 선택하세요.")
    print("1.HTTP 2.TCP")
    inputProtocol="0"
    while 1>0:
        inputProtocol=input()
        if inputProtocol == "1" or inputProtocol == "2":
            if inputProtocol == "1":
                inputProtocol="HTTP"
            else:
                inputProtocol="TCP"
            break
        else:
            print("다시 선택해주세요.")
    print("ELB Port를 입력하세요.(예: 80)")
    inputElbPort=input()
    print("연결할 Instance의 Port를 입력하세요.(예: 80)")
    inputInstPort=input()
    print("추가 할 정보("+inputProtocol+" : "+inputElbPort+" : "+inputInstPort+")로 등록하시겠습니까?(y/n)")
    nextStep2_YN=input()
    if nextStep2_YN.lower() == "y":
        command = 'aws elb create-load-balancer-listeners --load-balancer-name '+selectElbArr[0]
        command = command+' --listeners "Protocol='+inputProtocol+',LoadBalancerPort='+inputElbPort+',InstanceProtocol='+inputProtocol+',InstancePort='+inputInstPort+'"'
        retStr = cmdUtil.exec_commd(command)
        print("ELB에 Port가 추가되었습니다.")
    else:
        print("2단계 메뉴로 이동합니다.")
        flatMain.go_first_menu(selected_first_menu)    

def deregister_Instance(elbNm):
    return ""

def register_Instance(inputElbNm, selectedSubnetInfoArr):
    instanceArr = myec2.search_all_ec2instance(selectedSubnetInfoArr[4], selectedSubnetInfoArr[3], "")
    i=0
    while 1>0:
        selectedNos = []
        selectedInstIds = ""
        if len(instanceArr)>0:
            print("ELB에 연결할 instance 들을 1개 이상 엔터로 선택하세요.(예: 1)")
            print("x 를 입력하면 선택이 종료됩니다.")
            
            while 1>0:
                inputInstNo=input()
                if inputInstNo.lower() == "x":
                    print("선택을 종료합니다.")
                    break                
                elif (int(inputInstNo)-1)>len(instanceArr):
                    print("잘못 선택하셨습니다. 다시 선택하세요.")
                else:
                    selectedNos.append(int(inputInstNo)-1)
                    # instanceArr[int(inputInstNo)-1]
                    print("계속 선택해주세요. 선택을 종료하시려면 x 를 입력하세요.")

            for indexNo in selectedNos:
                print(instanceArr[indexNo])
                selectedInstIds = selectedInstIds+" "+((instanceArr[indexNo]).split(' : '))[4]
            
            print("를 선택하셨습니다.")
            print("Instance 선택을 완료하시겠습니까?(y/n)")
            print("n 을 입력하시면 instance 를 다시 선택 가능합니다.")
            nextStep2_YN=input()
            if nextStep2_YN.lower() == "y":
                break

    command3 = 'aws elb register-instances-with-load-balancer --load-balancer-name '+inputElbNm+' --instances '+selectedInstIds

    retStr = cmdUtil.exec_commd(command3)
    return "success"

def del_elb():
    print("삭제할 ELB 를 선택해주세요")
    objArr = search_all_elb()
    selectedNo=""
    while 1>0:
        selectedNo=input()
        if int(selectedNo)>len(objArr):
            print("잘못 선택하셨습니다. 다시 선택해주세요.")
        else:
            break

    command = 'aws elb delete-load-balancer --load-balancer-name '+(objArr[int(selectedNo)-1]).split(' : ')[0]
    retStr = cmdUtil.exec_commd(command)
    print("삭제되었습니다.")
    return "success"

def get_simple_elb_info(jsonObj):
    elbObj = ""
    elbNm = jsonObj.get("LoadBalancerName")
    dnsNm = jsonObj.get("DNSName")
    instanceIds = ""
    instanceArr = jsonObj.get("Instances")
    if len(instanceArr) > 0:
        for instObj in instanceArr:
            instanceIds = instObj.get("InstanceId")+" "
    elbObj = elbNm+" : "+dnsNm+" : "+instanceIds
    return elbObj

def get_simple_elb_listener_info(jsonObj):
    elbObj = ""
    protocol = jsonObj.get("Protocol")
    elbPort = str(jsonObj.get("LoadBalancerPort"))
    instanceProtocol = jsonObj.get("InstanceProtocol")
    instancePort = str(jsonObj.get("InstancePort"))
    elbObj = protocol+" : "+elbPort+" : "+instanceProtocol+" : "+instancePort
    return elbObj    

def search_all_elb():
    objArr = search_elb()
    i=0
    for obj in objArr:
        i+=1
        print(str(i)+"."+obj)
    return objArr

def search_elb():
    command = 'aws elb describe-load-balancers --query LoadBalancerDescriptions[*]'
    json_res = cmdUtil.getJson_exec_commd(command)
    objArr=[]
    if len(json_res) < 1:
        print("먼저 ELB 를 생성해주세요.")
        goMain.go_main()
    else:
        for elbinfo in json_res:
            objArr.append(get_simple_elb_info(elbinfo))
    return objArr

def search_elb_listeners():
    print("먼저 ELB 를 선택해주세요")
    objArr = search_all_elb()
    selectedNo=0
    while 1>0:
        selectedNo=input()
        if int(selectedNo)>len(objArr):
            print("잘못 선택하셨습니다. 다시 선택해주세요.")
        else:
            break
    selectElbArr = (objArr[int(selectedNo) - 1]).split(' : ')
    objArr = select_elb_listeners(selectElbArr[0])
    return objArr

def select_elb():
    objArr = search_all_elb()
    selectedNo=0
    while 1>0:
        selectedNo=input()
        if int(selectedNo)>len(objArr):
            print("잘못 선택하셨습니다. 다시 선택해주세요.")
        else:
            break
    selectElbArr = (objArr[int(selectedNo) - 1]).split(' : ')
    return selectElbArr    

def select_elb_listeners(searchElbNm):
    command = 'aws elb describe-load-balancers --load-balancer-names '+searchElbNm+' --query LoadBalancerDescriptions[0].ListenerDescriptions[*].Listener '
    json_res = cmdUtil.getJson_exec_commd(command)
    objArr=[] 
    if len(json_res) < 1:
        print("ELB에 허용 Port가 설정되어 있지 않습니다.")
    else:
        print("현재 ELB에 허용 Port는 아래와 같습니다.")
        i=0
        for elbinfo in json_res:
            i+=1
            listenerObj = get_simple_elb_listener_info(elbinfo)
            print(str(i)+"."+listenerObj)
            objArr.append(listenerObj)
    return objArr      
