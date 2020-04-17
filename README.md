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

## Hello World
First up, we define our config and commands in YAML.
This is YAML because it's easy to read, and easy to parse.
The learning curve is fairly shallow.
```
# ./tt-hello-world.yaml

- config
    text-color: cyan
    typing-speed: moderate

- commands
    - echo "Hello, World!"
```
Now, we can run it in Python's interactive mode.
```
$ python
Python 3.8.2 (default, Mar 11 2020, 00:29:50)
>>> import type-tastic
>>> tt = type-tastic.load('tt-hello-world.yaml')
>>> tt.run()
echo "Hello World!"
Hello World!
```
