import argparse
import urllib
import urllib2
import postfile
import hashlib
import os
import json
import time

def send_file(fullpath):
	if os.path.isdir(fullpath):
		list_files = os.listdir(fullpath)
		counter = 0
		for filename in list_files:
			fullname = os.path.join(fullpath, filename)
			send_file(fullname)
			counter += 1
			if counter == 4:
				time.sleep(90)
	else:
		host = "www.virustotal.com"
		web = "https://www.virustotal.com/vtapi/v2/file/scan"
		fields = [("apikey", "b484ad3a564ba4697eca233e8f425353b9c43657fb15889ebf1bd3d8a166e7fd")]
		file_object = open(fullpath, 'rb')
		file_read = file_object.read()
		file_object.close()
		files = [("file", str(fullpath), fullpath)]
		json_result = postfile.post_multipart(host, web, fields, files)
		return json_result

def file_result(path):	
	#  Report if the file has or not virus
	dic = {}
	if os.path.isdir(path):
		list_files = os.listdir(path)
		if list_files != None:
			for filename in list_files:
				fullname = os.path.join(path, filename)
				res, kind = file_result(fullname)
				if kind == 1:
					dic[fullname] = res
				else:
					for fullname in res:
						dic[fullname] = res[fullname]
		return (dic, 0)
	else:
		while True:
			url = "https://www.virustotal.com/vtapi/v2/file/report"
			parameters = {"resource": hashlib.md5(path).hexdigest(),
    	  		  	  	  "apikey": "b484ad3a564ba4697eca233e8f425353b9c43657fb15889ebf1bd3d8a166e7fd"}
			data = urllib.urlencode(parameters)
			req = urllib2.Request(url, data)
			response = urllib2.urlopen(req)
			json_result = response.read()
			length_json = len(json_result)
			if length_json != 0 and 'Scan finished' in json_result:
				json_res = json.loads(json_result)
				break				
			else:
				print "Wait 30 second" + json_result
				time.sleep(30)
		return (json_res, 1)

def main():
	terminal = argparse.ArgumentParser()
	terminal.add_argument('-f', '--file==PATH', dest='File', help="type the file", metavar='PATH')
	args = terminal.parse_args()
	send_file(args.File)
	report, kind = file_result(args.File)
	print report
	
if __name__ == "__main__":
	main()