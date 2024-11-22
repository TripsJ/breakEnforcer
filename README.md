# breakEnforcer

This is Break Enforcer, a python programm that forces you to step away by fully occupying your screen
The program implements a pomodoro timer but it shows you an image scaled to fill your screen instead of a countdown, when the pomodoro is in a break phase.
Work phases are the usual countdown.

Thhis program was created as a Final Project for CS50P in 2024.

## Motivation

The inspiration for this program was 2 fold, on one hand The pomodoro technique that consist in making regular, well defined breaks at specific intervals, and on the other hand, my tendency to igniore any and all timers that go off while i am coding

## Implementation
The programm has 3 main parts, implemented in 3 files

### The Configurator class

The job of the Configurator is to handle the creation, reading, saving and validation of a persistent configuration.
The program can be configured using a .toml file and the corresponding TOML syntax. that way the user can set a custom lenghts for long and short breaks as well as work sessions and a few other parameters, which i will enumerate below.
I chose the toml format for 2 Main reasons
1. it is very simple to write as it does not care about indentation or punctuation. it is a list of key value pairs separated by = signes and optionally divided into titeled sections between []

Example:
/[section 1/]
key1 = value 1
key2 = value 2

2. There is a very good toml library that allowes to easily read and write toml files from and to dictionarys, which makes handling configuration variables easy.

The Configuration class implements the following methods:


#### Accepted configuration keys


## Technologies used

I use the following during my coding process
- pipenv to manage the projects dependencies, makes it easy to keep your virtual environment clean
- black to format the code
- pre-commit to automate the execution of black and clean up my code before committing
- micro and Emacs as a texteditor/IDE
- pytest to test the code i wrote

I also used PGP to signe commits before they went into my private repository

The following Python libraries were used
- Tkinter for the GUI parts
- requests to querry the nasa AIOTD API
- PIL to resize and save the image as well as figuring out the screen size
- toml to read and write the configuration file
- typing to add type hints to functions that can have variable return types
- pytest for testing
- unittest mainly for unittest.mock to simulate certain inputs
## Resources

+ Testing for internet connection: https://stackoverflow.com/questions/17440343/python-checking-internet-connection-more-than-once
+ automating black on commits with precommit: https://pre-commit.com and https://black.readthedocs.io/en/stable/integrations/source_version_control.html
+ pytest course that turned out to be very helpfull in understanding how powerfull pytest actually is https://youtu.be/cHYq1MRoyI0

## Notes

git can force commit signing with git config commit.gpgsign true
git hooks can be used to verify that commits are signed according to this stack overflow answer
https://stackoverflow.com/questions/75864275/how-can-i-prevent-unsigned-git-commits-from-being-pushed-to-the-repository
