import instance.my_ec2instance as myec2
import utils.exec_aws_cmd_util as cmdUtil
import json

def get_tagNmValue(jsonObj, tagKey):
	tagValue = ''
	if cmdUtil.is_json_key_present(jsonObj,"Tags"):
		tagValue = cmdUtil.getString_tagValue(jsonObj.get("Tags"),tagKey)
		if tagValue == '':
			tagValue = "noname"
	else:
		tagValue = "noname"
	return tagValue

def get_sshStr(OsType, publicIpAddress):
	sshStr = 'ssh -i ~/.ssh/vini_key.pem '
	if OsType == 'ubuntu':
		sshStr = sshStr + 'ubuntu@'+publicIpAddress
	else:
		sshStr = sshStr + 'ec2-user@'+publicIpAddress
	return sshStr

def get_ssh_access():
	ret_obj = myec2.search_ec2instance("", "", "", "")
	
	instArr=[]
	if len(ret_obj) < 1:
		print("instance가 존재하지 않습니다.")
	else:
		for idx, oneObj in enumerate(ret_obj):
			InstanceId = oneObj.get("InstanceId")
			PublicIpAddress = cmdUtil.nullToNoname(oneObj.get("PublicIpAddress"),"no public ip")
			if PublicIpAddress != 'no public ip':
				InsName = get_tagNmValue(oneObj,'Name')
				print(InsName)
				OSType = get_tagNmValue(oneObj,'OSType')
				SshStr = get_sshStr(OSType,PublicIpAddress)
				print(SshStr)
				if InsName == 'pvh_ins':
					print('aws s3 sync ~/aws/projectvini-happiness s3://projectvini-happiness')
					print(SshStr+ " ./sti.sh")
				elif InsName != 'pvf_ins':
					print('aws s3 sync ~/aws/projectvini-viniilib s3://projectvini-viniilib')
					print(SshStr+ " ./sti.sh")

				print("")
	return "success"
