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
First up, we can do the easy example.
TypeTastic uses a Robot to type commands for you.
In the simplest form you can pass the commands in as an array.

Look here, in Python's interactive mode:
```
% python
Python 3.8.2 (default, Mar 11 2020, 00:29:50)
>>> import typetastic
>>> robot = typetastic.Robot()
>>> robot.load(['ls', 'echo "Hello World!"'])
{'commands': ['ls', 'echo "Hello World!"']}
>>> robot.run()
$ ls
LICENSE			build			dist			nosetests.json		setup.py		typetastic
README.md		deploy_locally.sh	examples		package_admin.md	tests			typetastic.egg-info
$ echo "Hello World!"
Hello World!
2
>>>
```
## Something Useful
Now we see the gist of it, we can do something more useful.
Let's say we want to show Mac OSX users how to find their shell profile.

The config section has defaults, so we can leave that out of our YAML file.
```
# ./tt-something-useful.yaml

config:
    prompt-string: "$ "
    typing-color: cyan
    typing-speed: moderate

commands:
    - echo ~
    - ls -l ~/.zshrc
    - cat ~/.zshrc
```
When we run this:
```
dougb % python examples/tt-robot.py examples/tt-something-useful.yaml
$ echo ~
/Users/dougb
$ ls -l ~/.zshrc
-rw-r--r--  1 dougb  staff  93 13 Mar 09:14 /Users/dougb/.zshrc
$ cat ~/.zshrc
export GPG_TTY=$(tty)
export PATH="/usr/local/opt/python@3.8/bin:$PATH"
alias python=python3
```
