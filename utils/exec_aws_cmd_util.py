#aws command 실행
import subprocess
import json
import io

def getJson_exec_commd (commd):
	retMsg=subprocess.check_output(commd, stderr=subprocess.STDOUT, shell=True)
	retMsg=retMsg.replace(b"'", b'"')
	return json.load(io.BytesIO(retMsg))

def exec_commd (commd):
	retMsg=((subprocess.check_output(commd, stderr=subprocess.STDOUT, shell=True)).decode("utf-8")).rstrip('\r\n')
	return retMsg

def create_anytag (resourceId, tagNm, tagValue):
	cmd = 'aws ec2 create-tags --resources '+resourceId+' --tags Key='+tagNm+',Value='+tagValue
	exec_commd(cmd)

def create_tagName (resourceId, tagValue):
	cmd = 'aws ec2 create-tags --resources '+resourceId+' --tags Key=Name,Value='+tagValue
	exec_commd(cmd)

def create_resource(commd, tagValue):
	retId = exec_commd(commd)
	create_tagName(retId, tagValue)
	return retId	

def getString_tagValue(tagsArr, targetKey):
	retTagValue=""
	if len(tagsArr) > 0:
		for tagp in tagsArr:
			if targetKey == tagp.get("Key"):
				retTagValue = tagp.get("Value")
				break
	return 	retTagValue			
		
def is_json_key_present(json, key):
	try:
		buf = json.get(key)
		if buf != None:
			return True
		else:
			return False
	except KeyError:
		return False
	
	return True

def nullToNoname(str, defaultStr):
	try:
		if str == "":
			str = defaultStr
		elif str == None:
			str = defaultStr

		return str
	except:
		return defaultStr

def ipValidate(ipStr):
	retTF = True
	#ip check
	#p = '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
	return retTF