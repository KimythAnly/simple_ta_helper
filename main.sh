#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage:"
    echo "$0 <student_list_csv> <git_pull_or_not>"
    echo ""
    echo "Description:"
    echo "    Run by student_list_csv."
    echo "    If you want to remove old directories and re-clone, <git_pull_or_not> is true."
    exit
fi

. config

stu_git_list=$1
git_pull_bool=$2

if [ -f "github_account" ]
then
    echo "Use github_account"
    . github_account
else
    echo -n "github_username:"
    read github_username
    echo -n "password:"
    read -s github_password
fi

echo $github_username
#cat $stu_git_list | awk -F"," '{print $1, $2}'
cat $stu_git_list | awk -F"," '{ print $1,$2 }' | parallel --gnu --progress -j $threads "bash grade.sh {} $git_pull_bool ${github_username} ${github_password}"
