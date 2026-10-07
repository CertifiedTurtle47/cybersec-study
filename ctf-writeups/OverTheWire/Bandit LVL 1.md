# Bandit LVL 1

> Unix/Linux Basics
>
> The password for the next level is stored in a file called **readme** located in the home directory. Use this password to log into bandit1 using SSH. Whenever you find a password for a level, use SSH (on port 2220) to log into that level and continue the game.

## Tools Used:

- ssh: program that allows logging into a remote machine and for executing commands on a remote machine
    - Usage here: ssh [username]:bandit.labs.overthewire.org -p 2220
        - '-p' argument allows calling for specific port number for access
- ls: list contents of a directory
    - Usage here: "ls"
- cd: change the working directory (i.e., move to specified directory)
    - Usage here: None
- cat: concatenate files and print on the standard output (i.e., print out text in a given file)
    - Usage here: cat [insertfilename]
- find: search for files in a directory hierarchy
    - Usage here: None
- file: determine file type

## Steps to Pass

1. Terminal command: ssh bandit1:bandit.labs.overthewire.org -p 2220
2. Enter password acquired from level 0 to access bandit1
3. Terminal command 'ls' to scan current directory for mentioned file
4. Terminal command 'cat readme'
5. Copy resulting password
6. ssh bandit2@bandit.labs.overthewire.org:2220
7. Use copied password
8. Move on to level 2

