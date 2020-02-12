#!/bin/bash

## This is a script file that will detect changes made to this document and push it to my personal webpage. This
## script is meant to exist on the machine or filesystem serving my personal webpage, though it could be adapted to
## push the file up to a remote location.

pushd ~/dissertation/thesis/ &> /dev/null

unset touched

git pull 2> /dev/null | grep 'Already up-to-date.' > /dev/null || touched=1

if [ ${touched} ]; then
    make 2> dissertation.err 1> dissertation.out && cp thesis.pdf ~/public_html/dissertation.pdf
    # pdflatex betaPSkeleton.tex &> /dev/null
    # bibtex betaPSkeleton &> /dev/null
    # pdflatex betaPSkeleton.tex &> /dev/null
    # pdflatex betaPSkeleton.tex 1> bskeleton.out 2> bskeleton.err && cp betaPSkeleton.pdf ~/public_html/files/betaPSkeleton.pdf
fi

popd &> /dev/null

# DOW=$(date +%u)
## If I send these every day, I will become numb, let's spread them out a bit.
## How about: Tu, Th, Sat, Sun
# if [[ "$DOW" =~ ^[0|2|4|6]$ ]]; then
#     mail -s 'When are you working on your dissertation today?' maljovec002@gmail.com < reminder.txt
# fi