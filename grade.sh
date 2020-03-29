#! /bin/bash 

if [ "$#" -eq 2 ]; then
    stu_id=$(echo $1 | cut -d' ' -f1)
    repo_name=$(echo $1 | cut -d' ' -f2)
    git_pull=$2
else
    stu_id=$1
    repo_name=$2
    git_pull=$3
    delay_time=$4
fi

. config
. github_account
. program_config

if [ "$use_classroom" == "true" ]; then
    repo_name="github.com/$classroom_domain/$prefix-$repo_name.git"
fi

echo "Github repo: $repo_name"
echo "Git pull: $git_pull"


if [ "$delay_time" != "" ]; then
    deadline="$delay_time"
fi


# Export environment parameters
# It will be also used in child process, "run.sh" and "eval.sh"
export MAIN_DIR=$save_dir/$course/$hw
export STU_ID=$stu_id


### git ###
if [ "$git_pull" == "true" ]; then
    [ -d $MAIN_DIR/code/$STU_ID ] && rm -rf $MAIN_DIR/code/$STU_ID
    mkdir -p $MAIN_DIR/code/$STU_ID
    cd $MAIN_DIR/code/$STU_ID

    git init
    git remote add origin -f https://$github_username:$github_password@$repo_name
    git config core.sparseCheckout true
    if [ "$only_report" = true ]; then
        echo "/*.pdf" >> .git/info/sparse-checkout
        # echo "/${hw,,}/*.pdf" >> .git/info/sparse-checkout
    else
        echo "/*" >> .git/info/sparse-checkout
        # echo "/${hw,,}/*" >> .git/info/sparse-checkout
    fi

    #git pull origin $branch
    # TO save the disk usage, only clone the latest commit record
    git pull origin $branch

    if [ "$branch" != "master" ]; then
        git checkout $branch
    fi

    # checkout to latest HEAD before deadline
    git checkout `git rev-list -n 1 --before="$deadline" $branch`
else
    cd $MAIN_DIR/code/$STU_ID
fi

if [ "$only_report" != true ]; then
    # Create a tmp directory to copy student's homeword and TA grading files to this directory.
    tmp_grade_dir=$(mktemp -d)

    export DATA_DIR=$tmp_grade_dir/data
    export OUTPUT_DIR=$tmp_grade_dir/output
    export SCORE=$tmp_grade_dir/score
    export PROGRAM_DIR=$tmp_grade_dir/program
    export STU_DIR=$tmp_grade_dir/$stu_id
    
    # trap "rm -rf $tmp_grade_dir" EXIT


    # Create a soft link to link data in tmp student's directory
    ln -s $MAIN_DIR/data $tmp_grade_dir
    
    # Copy all student's files and run.sh to tmp directory
    cp -R $MAIN_DIR/code/$STU_ID $tmp_grade_dir
    cp -R $MAIN_DIR/program $PROGRAM_DIR

    # Change working directory to student's tmp directory
    cd $STU_DIR
    
    mkdir -p $OUTPUT_DIR
    touch $SCORE

    # student script DOS to unix
    for fn in `ls $STU_DIR/*.sh`
    do
        dos2unix $fn
    done

    # run.sh
    timeout -k 9 $limit_time bash -c "bash $PROGRAM_DIR/run.sh $args1 2> $MAIN_DIR/err/$stu_id 1> $MAIN_DIR/log/$stu_id" \
    || echo "timeout" >> $MAIN_DIR/err/$stu_id

    # eval.sh
    bash $PROGRAM_DIR/eval.sh $args2 2> $MAIN_DIR/err2/$stu_id 1> $MAIN_DIR/log2/$stu_id

    mkdir -p $MAIN_DIR/output/$stu_id/
    cp -f $OUTPUT_DIR/* $MAIN_DIR/output/$stu_id/
    cp -f $SCORE $MAIN_DIR/score/$stu_id

fi
