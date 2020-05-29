input='_student_list.csv'

#bash main.sh $input false

#cd /workspace/

#python announcement.py hw9_scores.csv ML2020/hw9/

cd /tmp/simple_ta_helper
while IFS=',' read -r sidd rep other
do
    #if [ $rep = 0 ]; then
        #timeout 1000 bash run_by_stuid.sh $sidd $input
	bash check_deadline.sh $sidd
    #fi
done < ML2020/hw9/announce.csv
