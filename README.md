# Simple TA Helper

Please study the slides for more details.
Link: https://goo.gl/FEm6gR


- step 0: Download the classroom_roster.csv from Github Classroom.
    - example
    https://classroom.github.com/classrooms/61244606-ntu-machine-learning-spring-2020/roster.csv
    

- step 1: Create student_list_csv.
    - usage:
    ``` 
    $ bash make_student_list <roster_csv> <student_list_csv>
    ```
    - example:
    ```
    $ bash make_student_list ../classroom_roster.csv ../student_list.csv
    ```

- step 2: Get Kaggle leaderboard scores. (Optional.)
    - usage
    ```
    $ python get_kaggle_score.py -c <competition> -l <student_list_csv> -o <output_csv>
    ```
    - example:
    ```
    $ python get_kaggle_score.py -c ml2020spring-hw1 -l ../student_list.csv -o /tmp/kaggle_hw1_score.csv
    ```

- step 3: Setup a environment for a specific homework.
    - edit config
    - run setup.sh
    ```
    bash setup.sh
    ```

- step 4: Run main.sh
    - usage:
    ```
    $ bash main.sh <student_list_csv> <git_pull_or_not>
    ```
    - example:
    ```
    $ bash main.sh ../student_list.csv true
    ```
    
