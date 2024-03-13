# breakEnforcer

This is Break Enforcer, a python programm that forces you to step away by fully occupying your screen

## Motivation

The inspiration for this program was 2 fold, on one hand The pomodoro technique that consist in making regular, well defined breaks at specific intervals, and on the other hand, my tendency to igniore anny and all timers that go off while i am coding.

##Technologies used

I use the following during my coding process
- pipenv to manage the projects dependencies, makes it easy to keep your virtual environment clean
- black to format the code
- pre-commit to automate the execution of black and clean up my code before committing
- micro as a texteditor/IDE

I also used PGP to signe commits before they went into my private repository

The following Python libraries were used
- Tkinter for the GUI parts
- requests to querry the nasa AIOTD API
- PIL to resize and save the image as well as figuring out the screen size

## Resources

Testing for internet connection: https://stackoverflow.com/questions/17440343/python-checking-internet-connection-more-than-once
automating black on commits with precommit: https://pre-commit.com and https://black.readthedocs.io/en/stable/integrations/source_version_control.html

## Notes

git can force commit signing with git config commit.gpgsign true
git hooks can be used to verify that commits are signed according to this stack overflow answer
https://stackoverflow.com/questions/75864275/how-can-i-prevent-unsigned-git-commits-from-being-pushed-to-the-repository
