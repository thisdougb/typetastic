# TypeTastic
[![thisdougb](https://circleci.com/gh/thisdougb/typetastic.svg?style=shield)](https://circleci.com/gh/thisdougb/typetastic)

Python utility to make creating screencasts easier, and doing live demo's less stressful.

## Intro
A while back I did some Ansible training sessions, for which I did some screen recordings.
Frustrated by the time it takes to make a screen capture look good, I built a little robot to help.
The bot runs the commands for me, so I am able to record perfectly paced typing in a repeatable way.

I'm doing some more training sessions, so I thought I'd clean up the project and open-source it.
Feedback welcome, just log an issue.

Main features:
* No more typos in your screen recordings!
* Let the bot do your show-and-tell demo, while you focus on your audience
* Define a list of commands, and replay as often as you like.
* SSH into other hosts and run stuff.
* Choose the typing speed, and color the commands for clarity.
* Config and commands live together, so building a library is easy.

What this is not:
* A video recording tool.
* An orchestration tool.
* A way to skive at work by having the bot do your bidding! 😈

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
>>> robot.load(['ls', 'echo "Hello World\!"'])
>>> robot.run()
$ ls
LICENSE			build			dist			nosetests.json		setup.py		typetastic
README.md		deploy_locally.sh	examples		package_admin.md	tests			typetastic.egg-info
$ echo "Hello World!"
Hello World!
>>>
```
## Something Useful
Now we see the gist of it, we can do something more useful.
To run TypeTastic command files, I use this simple runner script.
```
# tt-robot.py
#
# Run a typetastic command file.
#
# Usage:
#   tt-robot.py <file>

import argparse
import typetastic


def main():
    """Run a typetastic file."""

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("inputfile")
    args = arg_parser.parse_args()

    robot = typetastic.Robot()
    robot.load(args.inputfile)
    robot.run()


if __name__ == "__main__":
    main()
```
Let's say we want to show Mac OSX users how to find their shell profile.

Our yaml file has a config and a commands section.
The config section has defaults, so it's optional.
The commands are simply listed as you'd type them.
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
$
```
## Config
The config options are fairly simple.

#### Prompt String
Keep it simple is my advice.
Plain strings are good, complicated escape codes are less good.

#### Typing Color
The options are: black, red, green, yellow, blue, purple, cyan, white.

Additional modifiers are <i>bold</i> and <i>bright</i>.
These can be used as, <i>bold-green</i> or <i>bold-bright-green</i>.

#### Typing Speed
The options are: slow, moderate, supersonic.

Supersonic is great for testing.  🚀

## Meta Commands
Screen recording often requires stitching together video clips, or pausing for a voice-over.
So I added a couple of meta commands to help with the mechanics of making a great video.

#### NEWLINE
This does what is says, just prints a new line with the prompt.
It has the same effect as pressing <i>return</i> in a real session.

I use this mainly to create whitespace around something to make it clearer for the viewer.
For example, when you cat some files, a blank line often helps visually separate them.
```
# using NEWLINE

commands:
    - clear
    - cat ~/.aws/credentials
    - NEWLINE
    - cat ~/.aws/config
    - NEWLINE
    - aws sts get-caller-identity
```
#### PAUSE
In this example of using AWS CLI, we use the meta command PAUSE.
This will pause the robot until a key is pressed.

I find this useful on two counts.
First to give time to give a voice-over explanation of the config files.
A pause makes it easier to cut the recording in iMovie, etc.

And second, in a parallel (not recorded) terminal window I can copy in fake .aws files so I don't show my real credentials.
This is a nifty use of PAUSE that helps make real use cases in a safe way.
It avoids having to blur or block-out passwords, etc.
```
# using PAUSE

commands:
    - clear
    - cat ~/.aws/credentials
    - NEWLINE
    - cat ~/.aws/config
    - NEWLINE
    - PAUSE
    - aws sts get-caller-identity
    - PAUSE
```
Just tap a key to resume the bot.
## Editor Commands
Editors are tricky for the bot.
By tricky I mean it's impossible to automate an interactive editor (vi, emacs, etc) session.

So I made editor commands simply call PAUSE instead.
This lets you splice into your screencast a second screen recording of just the editor session.

Recording an editor session still needs to be done manually.
But, it will be a much smaller overall effort (using TypeTastic for the bulk of the work).
And what you do in an editor typically isn't reliant on a smooth typing pace for longer commands.

The key thing here is that after you splice the editor clip into the main screencast, it visually just flows.
The visible shell history makes logical sense, just like you exited the editor for real.

Remember to tap a key to resume the bot.

Detected editor commands are:
* vi
* emacs
* crontab

This is maybe best with a video example.
In [this screencast](https://vimeo.com/413113839) I use the technique to edit the crontab.
I recorded the crontab edit afterwards, and spliced it into the main screen recording.
