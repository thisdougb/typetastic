# type-tastic
Python utility to make creating screencasts easier.

## Intro
A while back I did some Ansible training sessions, for which I did some screen recordings.
To make life easier I built a little tool to automate the execution of commands in a terminal window.
I'm doing some more training sessions, so I thought I'd clean up the project and open-source it.

Main features:
* No more typos in your screen recordings!
* Define a list of commands, and replay as often as you like.
* SSH into other hosts and run stuff.
* Choose the typing speed, and color the commands for clarity.
* Config and commands live together, so building a library is easy.

What this is not:
* A video recording tool.
* An orchestration tool.
* A way to skive at work!

There's a video [here on Vimeo](https://vimeo.com/224764672) of the screencast I did that led me to building this tool.
It shows examples of most features.
## Hello World
First up, we define our config and commands in YAML.
This is YAML because it's easy to read, and easy to parse.
The learning curve is fairly shallow.
```
# ./tt-hello-world.yaml

- config:
    typing-color: cyan
    typing-speed: moderate

- commands:
    - echo "Hello, World!"
```
Now, we can run it in Python's interactive mode.
```
$ python
Python 3.8.2 (default, Mar 11 2020, 00:29:50)
>>> import type-tastic
>>> tt = type-tastic.load('tt-hello-world.yaml')
>>> tt.run()
$ echo "Hello World!"
Hello World!
```
## Something Useful
Now we see the gist of it, we can do something more useful.
Let's say we want to show Mac OSX users how to find their shell profile.

The config section has defaults, so we can leave that out of our YAML file.
```
# ./tt-show-mac-shell-profile.yaml

- commands:
    - echo ~
    - ls -l ~/.zshrc
    - cat ~/.zshrc
```
When we run this
```
dougb % python tt-runner.py tt-show-mac-shell-profile.yaml
$ echo ~
/Users/dougb
$ ls -l ~/.zshrc
-rw-r--r--  1 dougb  staff  93 13 Mar 09:14 /Users/dougb/.zshrc
$ cat ~/.zshrc
export GPG_TTY=$(tty)
export PATH="/usr/local/opt/python@3.8/bin:$PATH"
alias python=python3
$  
```
