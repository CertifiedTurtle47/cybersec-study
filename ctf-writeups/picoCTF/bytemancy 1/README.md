# bytemancy 1
> picoCTF
> General Skills

> Can you conjure the right bytes? The program's source code can be downloaded here.

> ### Hints:
> No copy-pasta, please - use Python!

## Initial Thoughts:

- This may involve crafting a Python script
- I will need to reference ASCII character codes to find the right input and understand it properly.

## Info Gathering:

- When looking at the source code, it prompts the user to send '101' **1751** times.
	- by looking at the rest of the code, there's a plaintext if statement that checks to see if the user inputs "'\x65'*1751"
	- as per the hint, I'll look into solving the input with Python. The main question is "how"?
	- using ord() python function works to get ascii decimal value. now it's just about inputting it properly to get the flag
- typing in Python formatted code doesn't seem to do anything
- entering '\x' escape characters also doesn't do anything
- attempting to draft a simple script and pass using following format app.py $(script_file)
	- nothing
- pipeline got a response, just the wrong one
	format: nc xebec.cylabacademy.net 15894 | python3 101.py
- found the flag, needed to flip the command order of the last attempt
	- correct format: python3 101.py | nc xebec.cylabacademy.net [insert session ID]

## Solution:

### Solution 1 (Initial Attempt/Script Execution):
1. Check source code for required input
2. Launch instance to get netcat (nc) command with server information
3. Create python script file as follows:
#!/usr/bin/env python3

print("\x65" * 1751)

- following works as well:
    #!/usr/bin/env python3 		
    print(ord(101) * 1751) 
			
4. Using Python, pipeline code into one line with the following format: ` ***python3 [insert python script file] | nc xebec.cylabacademy.net [insert session id]*** `
5. Find flag in response from server

### Solution 2 (Single-Line Execution + Pipeline)
1. Check source code for required input
2. Launch instance to get netcat (nc) command with server information
3. Using Python, pipeline code into one line with the following format:

    ` python3 -c 'print("\x65" * 1751)' | nc xebec.cylabacademy.net [insert session id] `
   
	- as in solution 1, ord(101) works in place of "\x65"
5. Find flag in response from server

## Notes:

1. Remember to check order when pipelining commands
	- python3 101.py | nc xebec.cylabacademy.net 19542 and nc xebec.cylabacademy.net 19542 | python3 101.py
		- Python -> Server vs. Server -> Python
			- The first takes the output of the script and passes that to the server, generating a server response
			- The second accesses the server first and uses its output as input for any functions in the python script that capture input. Since there are no such functions in the script, there is nothing to output as a result

2. Remember to, whenever available, review source code carefully for hidden clues on accessing a system
3. ASCII encodings are important to remember
	- https://www.ascii-code.com/
4. Remember 'python3 -c '[insert code]' for single-line execution
	- if using python script file, just 'python3 [filename]' works

		

## Review:

### Vulnerabilities Discovered:

1. Required output revealed in plaintext in source code
2. Unrestricted access to source code
3. Unsanitized input for program
4. Port listening enabled for all outside sources

### How To Prevent:
1. Source code review for any plaintext clues on core functions which allow elevated access
2. Sanitize input to prevent execution of unexpected code or scripts

### How To Detect:
1. Log input attempts, ensuring to alert on possible code input
