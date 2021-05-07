import utils.exec_aws_cmd_util as cmdUtil
import utils.go_main as goMain
import network.my_subnet as mySubnet
import network.my_securitygroup as mysg
import instance.my_ec2instance as myec2
import json

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
    objArr = search_elb()
    i=0
    for obj in objArr:
        i+=1
        print(str(i)+"."+obj)
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

def search_all_elb():
    objArr = search_elb()
    i=0
    for obj in objArr:
        i+=1
        print(str(i)+"."+obj)
    # return objArr

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

