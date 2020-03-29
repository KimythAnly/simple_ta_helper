import argparse
import requests
import json
import datetime

def get_args():
    parser = argparse.ArgumentParser(description='Get the competition scores from the Kaggle leaderboard.')
    parser.add_argument('--competition', '-c', help='Kaggle competition id or name.', type=str, default='ml2020spring-hw1')
    parser.add_argument('--student_list', '-l', help='Input student-list csv. The format is <student_id>,<some_text> each line.', type=str, default='../student_list.csv')
    parser.add_argument('--output', '-o', help='Output csv. The format is <id>,<public_score>,<private_score> each line. <id> is <student_id> if student_list is specified, otherwise, it is the teamName in the competition.', type=str, default='/tmp/kaggle_scores.csv')
    return parser.parse_args()


def fetch(competition_id_or_name, private):
    params = {
        'includeBeforeUser': 'true',
        'includeAfterUser': 'true',
    }
    if private:
        params['type'] = 'private'

    url = 'https://www.kaggle.com/c/{}/leaderboard.json'.format(competition_id_or_name)
    r = requests.get(url, params=params)
    print(r.url)
    return json.loads(r.content)

def get_leaderboard(competition_id_or_name, student_list_csv=''):
    p = fetch(competition_id_or_name, private=False)
    merge_public = p['beforeUser'] + p['afterUser']
    p = fetch(competition_id_or_name, private=True)
    merge_private = p['beforeUser'] + p['afterUser']
    fmt = '%Y-%m-%dT%H:%M:%S'
    ret = {}

    if student_list_csv is '':
        print('Total rankings: {}'.format(len(merge_public)) )
        for d in merge_public:
            ret[d['teamName']] = {'public': d['score']}
        for d in merge_private:
            ret[d['teamName']]['private']= d['score']
        return ret

    student_list = {}
    with open(student_list_csv, 'r') as f:
        for line in f:
            student_id = line.split(',')[0]
            student_list[student_id] = None
    print('Total rankings: {} | Total students: {}'.format(len(merge_public), len(student_list)) )
    for d in merge_public:
        sid = d['teamName'].split('_')
        if sid is not None:
            if sid[0] in student_list.keys():
                # multi accounts
                if student_list[sid[0]] is not None:
                    print('Warning: Student {} uses multiple accounts.'.format(sid[0]))
                    d1 = datetime.datetime.strptime(d['lastSubmission'].split('.')[0], fmt)
                    index0 = student_list[sid[0]]['rank'] - 1
                    d0 = datetime.datetime.strptime(merge_public[index0]['lastSubmission'].split('.')[0], fmt)
                    if d1 > d0:
                        student_list[sid[0]] = d
                        ret[sid[0]] = {'public': d['score']}
                else:
                    student_list[sid[0]] = d
                    ret[sid[0]] = {'public': d['score']}
    for d in merge_private:
        sid = d['teamName'].split('_')
        if sid is not None:
            if sid[0] in student_list.keys():
                if student_list[sid[0]]['teamName'] == d['teamName']:
                    ret[sid[0]]['private'] = d['score']
                else:
                    print('Warning: Skip {} on private leaderboard.'.format(d['teamName']))
    return ret

if __name__ == '__main__':
    args = get_args()
    print(args)
    p = get_leaderboard(args.competition, student_list_csv=args.student_list)
    with open(args.output, 'w') as f:
        for k, v in p.items():
            f.write('{},{},{}\n'.format(k, v['public'], v['private']))
