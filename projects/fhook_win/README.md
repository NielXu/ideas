# fhook_win
This is a script that detects a file change and execute the given command. Please note the following:
1. This is for demo purpose only, please use at your own risk because it uses the `system()` function to run the command and it might causes unexpected behaviors.
2. This script is for Windows only, if you are looking for a script for the Linux platform please check out `fhook_linux`.
3. The system call is blocking, which means the watcher cannot continue until the command exited.

# Environment
The script is developed and worked in the following environment:

```
$ systeminfo 
OS Name:                   Microsoft Windows 10 Pro
OS Version:                10.0.19041 N/A Build 19041
...

$ gcc --version
gcc.exe (tdm64-1) 5.1.0
```

# Setup
Compile the `fhook.c` file:

```
$ gcc fhook.c -o fhook
```

# Usage

```
$ ./fhook.exe 
Usage: ./fhook [monitor_file] [check_interval] (cmd)
[monitor_file]: required, the file to be monitored for changes
[check_interval]: required, the interval that the watcher check for changes, lower value will check more constantly
(cmd): optional, the command to be invoked when a file changes detected
```

An example:

```
$ touch example.txt

$ ./fhook.exe example.txt 2000 "wc -w example.txt"
Monitoring file: example.txt
Watcher active interval: 2000
Script to be executed when file changed: wc -w example.txt

Changed detected
1 example.txt
Executed command status: 0

Changed detected
2 example.txt
Executed command status: 0

Changed detected
1 example.txt
Executed command status: 0
```

To stop: simply do `ctrl+c`

You can also create a new bash script and run it when the file changed. In this way, multiple tasks can be chained toegther and triggered by making changes to the file. Some examples are:
1. Recompile something when the source code changed (In this case, recompiling c files sounds like a good idea)
2. Trigger some tasks, for example, updating one file when another file changed
3. ...
