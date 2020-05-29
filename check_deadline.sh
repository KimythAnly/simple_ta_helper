#! /bin/bash 

if [ $# -lt 1 ]; then
    echo "Usage:"
    echo "$0 [student id] [delay deadline (optional)]"
    echo ""
    echo "./check_deadline.sh b01999001"
    echo ""
    echo "Description:"
    echo "    Check deadline for a specific student."
    echo ""
    exit
fi

stu_id=$1 # stu_id must be above config

. config
. program_config

if [ "$2" != "" ]; then
    deadline=$2
fi

echo "student id: $stu_id"
pwd=$pwd
cd $save_dir/$course/$hw/code/${stu_id,,}
commit_date=`date -ud $(git show -s --format=%cI)`
echo "commit date: $commit_date"
deadline_date=`date -ud "${deadline}UTC+8"`
echo "deadline: $deadline_date"
if [ `date -d "$commit_date" +%s` -gt `date -d "$deadline_date" +%s` ]; then
    echo "Invalid. This commit is delayed."
else
    echo "Successful."
fi
echo "============================================================================="

echo

