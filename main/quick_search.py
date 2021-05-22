import instance.my_ec2instance as myec2
import json

def get_ssh_access():
	ret_obj = myec2.search_ec2instance("", "", "", "")
	instArr=[]
	if len(ret_obj) < 1:
		print("instance가 존재하지 않습니다.")
	else:
		for idx, oneObj in enumerate(ret_obj):
			InstanceId = oneObj.get("InstanceId")
			objInfo = myec2.get_simple_ec2instance_info(oneObj)
			instArr = objInfo.split(" : ")
			if instArr[2] != 'no public ip':
				print(instArr[0])
				print("ssh -i ~/.ssh/vini_key.pem ec2-user@"+instArr[2])
				if instArr[0] != 'pvf_ins':
					print('aws s3 sync ~/aws/projectvini-viniilib s3://projectvini-viniilib')
					print('ssh -i ~/.ssh/vini_key.pem ec2-user@'+instArr[2]+' "./sti.sh"')

			print("")
	return "success"
