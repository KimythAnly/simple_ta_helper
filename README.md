# Simple TA Helper

Please study the slides for more details.
Link: https://goo.gl/FEm6gR


- step 0: Download the ruster.csv from Github Classroom.

- step 1: Create student-list.
    - usage:
    ``` 
    $ bash make_student_list <ruster_csv> <student_list_csv>
    ```
    - example:
    ```
    $ bash make_student_list ../ruster.csv ../student_list.csv
    ```

- step 2: Download Kaggle leaderboard scores. (Optional.)
    - usage
    ```
    $ python get_kaggle_score.py -c <competition> -l <student_list_csv> -o <output_csv>
    ```
    - example:
    ```
    $ python get_kaggle_score.py -c ml2020spring-hw1 -l ../student_list.csv -o /tmp/kaggle_hw1_score.csv
    ```

