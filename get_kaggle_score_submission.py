import argparse
import requests
import browsercookie
import json
import datetime
import copy
import tqdm
from functools import partial
from joblib import Parallel, delayed

def get_args():
    parser = argparse.ArgumentParser(description='Get the competition scores from the Kaggle leaderboard.')
    parser.add_argument('--competition', '-c', help='Kaggle competition id or name.', type=str, default='ml2020spring-hw1')
    parser.add_argument('--student_list', '-l', help='Input student-list csv. The format is <student_id>,<some_text> each line.', type=str, default='../student_list.csv')
    parser.add_argument('--cpus', '-p', help='Number of cpus for multiprocessing.', type=int, default=4)
    parser.add_argument('--output', '-o', help='Output csv. The format is <id>,<public_score_1>,<private_score_1>,<public_score_2>,<private_score_2> each line. <id> is <student_id> if student_list is specified, otherwise, it is the teamName in the competition.', type=str, default='/tmp/kaggle_scores.csv')
    return parser.parse_args()

def partial_fetch_teams(url, params, start_index, step, cookies):
    ret = []
    index = start_index
    while True:
        params['page'] = index
        r = requests.get(url, params=params, cookies=cookies)
        c = json.loads(r.content)
        print(r.url)
        index += step
        for team in c['teamsList']:
            ret.append(team)
        if not c['hasMoreData']:
            break
    return ret

def fetch_teams(competition_id_or_name):
    params = {}
    cj = browsercookie.chrome()
    cj_dict = requests.utils.dict_from_cookiejar(cj)
    url = 'https://www.kaggle.com/c/{}/teams.json'.format(competition_id_or_name)
    i = 1
    teams = []
    func = partial(partial_fetch_teams, url=url, params=copy.deepcopy(params), cookies=copy.deepcopy(cj_dict))
    results = Parallel(n_jobs=args.cpus)(
            delayed(func)(start_index=i+1, step=args.cpus) for i in tqdm.tqdm(range(args.cpus)))
    teams = []
    for t in results:
        teams += t
    #for t in teams:
    #    print(t.keys())
    return teams

def get_teams(competition_id_or_name, student_list_csv=''):
    teams = fetch_teams(competition_id_or_name)
    ret = {}
    student_list = {}
    if student_list_csv != '':
        for line in open(student_list_csv, 'r'):
            k, v = line.split(',')
            student_list[k] = v
    for team in teams:
        if student_list_csv != '':
            sp = team['name'].split('_')
            if sp:
                student_id = sp[0]
                if student_id in student_list.keys():
                    if student_id in ret.keys():
                        print('Student {} has multiple id!'.format(student_id))
                    else:
                        ret[student_id] = team['id']
        else:
            ret[team['name']] = team['id']
    return ret

def fetch_submissions(competition_id_or_name, team, team_id):
    params = {'teamId': team_id}
    cj = browsercookie.chrome()
    url = 'https://www.kaggle.com/c/{}/team-submissions.json'.format(competition_id_or_name)
    r = requests.get(url, params=params, cookies=cj)
    submissions = json.loads(r.content)
    ret = []
    rest = []
    i=0
    for submission in submissions:
        if submission['isSelected'] and not submission['isAfterDeadline']:
            ret.append({'private': submission['privateScore'],
                        'public': submission['publicScore']})
        elif not submission['isSelected'] and submission['status'] != 'error' and not submission['isAfterDeadline']:
            rest.append({'private': submission['privateScore'],
                        'public': submission['publicScore']})
    if len(ret) != 2:
        rest = sorted(rest, key=lambda k: float(k['public']))
        ret = (ret + rest)[:2]
    assert len(ret) <= 2, 'Student {} has more than two submissions being selected.'.format(submissions[0]['teamName'])
    return (team, ret)

def get_submissions(competition_id_or_name, teams):
    ret = {}
    len_teams = len(teams)
    func = partial(fetch_submissions, competition_id_or_name=competition_id_or_name)
    results = Parallel(n_jobs=args.cpus)(
            delayed(func)(team=team, team_id=team_id) for (team, team_id) in tqdm.tqdm(teams.items()))
    for r in results:
        ret[r[0]] = r[1]
    return ret

if __name__ == '__main__':
    args = get_args()
    print(args)
    teams = get_teams(args.competition, student_list_csv=args.student_list)
    submissions = get_submissions(args.competition, teams)
    with open(args.output, 'w') as f:
        for k, v in submissions.items():
            if len(v) == 2:
                s1, s2, s3, s4 = v[0]['public'], v[0]['private'], v[1]['public'], v[1]['private']
            elif len(v) == 1:
                s1, s2, s3, s4 = v[0]['public'], v[0]['private'], 0, 0
            else:
                s1, s2, s3, s4 = 0, 0, 0, 0

            f.write('{},{},{},{},{}\n'.format(k, s1, s2, s3, s4))
