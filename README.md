# Simple TA Helper

Please study the slides for more details.
Link: https://goo.gl/FEm6gR


- step 0: Download the classroom_roster.csv from Github Classroom.
    - example
    https://classroom.github.com/classrooms/61244606-ntu-machine-learning-spring-2020/roster#download-csv-modal
    

- step 1: Create student_list_csv.
    - usage:
    ``` 
    $ bash make_student_list.sh <roster_csv> <student_list_csv>
    ```
    - example:
    ```
    $ bash make_student_list.sh ../classroom_roster.csv ../student_list.csv
    ```

- step 2: Get Kaggle leaderboard scores. (Optional.) One can get the scores directly from the kaggle leaderboard or get the scores from all submissions.
    - usage 
    ```
    $ # directly get scores from leaderboard
    $ python get_kaggle_score.py -c <competition> -l <student_list_csv> -o <output_csv>
    ```
    or
    ```
    $ # get scores from all team-submissions
    $ python get_kaggle_score_submission.py -c <competition> -l <student_list_csv> -o <output_csv> -p <cpus> -b <browser>
    ```
    - example:
    ```
    $ python get_kaggle_score.py -c ml2020spring-hw1 -l ../student_list.csv -o /tmp/kaggle_hw1_score.csv
    ```
    or 
    ```
    $ python get_kaggle_score_submission.py -c ml2020spring-hw1 -l ../student_list.csv -o /tmp/kaggle_hw1_score.csv -p 8
    ```
    - Note: You should login as the host of the competition to run the second code.  If it fails using chrome cookies, run chrome with `--password-store=basic`.

- step 3: Setup a environment for a specific homework.
    - edit config
    - run setup.sh
    ```
    bash setup.sh
    ```

- step 4: Run main.sh (FIXME)
    - usage:
    ```
    $ bash main.sh <student_list_csv> <git_pull_or_not>
    ```
    - example:
    ```
    $ bash main.sh ../student_list.csv true
    ```
    
