#!/usr/bin/env zsh

# checks if branch has something pending
function parse_git_dirty() {
  git diff --quiet --ignore-submodules HEAD 2>/dev/null; [ $? -eq 1 ] && echo "*"
}

# gets the current git branch
function parse_git_branch() {
  git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e "s/* \(.*\)/\1$(parse_git_dirty)/"
}

# get last commit hash prepended with @ (i.e. @8a323d0)
function parse_git_hash() {
  git rev-parse --short HEAD 2> /dev/null | sed "s/\(.*\)/@\1/"
}

mkdir -p output
cp bender.png output

# pandoc example.md -o output/example.html -Mtoc= --mathjax --listings --number-sections --standalone --filter pandoc-crossref --filter pandoc-citeproc -Mcref -Mcolorlinks -MlinkReferences -Mlistings -Mgithash=$(parse_git_branch)$(parse_git_hash)
pandoc simple.md -s -o output/simple.html --standalone --filter pandoc-pythonexec --filter /home/linuxbrew/.linuxbrew/bin/pandoc-crossref -Mlistings
