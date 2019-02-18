import argparse
import re
import sys
import requests
import yaml


from github import Github


parser = argparse.ArgumentParser(description='check github/zenhub milestone')
parser.add_argument('-m', '--milestone', type=str)
args = parser.parse_args()


class Zenhub:

    api_host = 'https://api.zenhub.io'

    def __init__(self, token):
        self.headers = {'X-Authentication-Token': token}

    def get_issue(self, repo_id, issue_id):
        endpoint = f'{self.api_host}/p1/repositories/{repo_id}/issues/{issue_id}'  # NOQA
        response = requests.get(endpoint, headers=self.headers)

        return response.json()


def csv_output(**params):
    output_params = [
        'name',
        'issue_no',
        'issue_title',
        'pipeline',
        'assignee',
        'story_point',
        'working_time',
        'url'
    ]
    print(','.join([f'"{params.get(key)}"' for key in output_params]))


def get_sprint_data(sprint_name):

    f = open("./config.yaml", "r")
    config = yaml.load(f)

    target_organization = config.get('target_organization')
    target_repositories = config.get('target_repositories')

    g = Github(config.get('github_token'))
    z = Zenhub(config.get('zenhub_token'))

    repositories = []

    for _repo in g.get_organization(target_organization).get_repos(type='private'):  # NOQA
        if _repo.name in target_repositories:
            repositories.append(_repo)

    for repo in repositories:
        mss = repo.get_milestones()
        milestone = None
        for ms in mss:
            if ms.title == sprint_name:
                milestone = ms
                break
        else:
            print(f'milestone not found in {repo.name}')
            sys.exit()

        for _issue in repo.get_issues(milestone=milestone, state='all'):
            issue = z.get_issue(repo.id, _issue.number)
            issue_time = 0.0
            if _issue.comments > 0:
                for _comment in _issue.get_comments():
                    text = _issue.get_comment(_comment.id)
                    for l in text.body.split('\n'):
                        m = re.match(r'作業時間.* (\d+(\.\d+)?)h', l)
                        if m:
                            issue_time = m.groups()[0]

            assignee = None
            if _issue.assignees:
                assignee = _issue.assignees[0].login

            params = {
                'name': repo.name,
                'issue_no': _issue.number,
                'issue_title': _issue.title,
                'pipeline': issue["pipeline"]["name"],
                'assignee': assignee,
                'story_point': issue.get("estimate", {}).get("value"),
                'working_time': issue_time,
                'url': f'https://github.com/pathee/{repo.name}/issues/{_issue.number}'  # NOQA
            }
            csv_output(**params)


if __name__ == '__main__':
    if not args.milestone:
        parser.print_help()
        sys.exit()

    get_sprint_data(args.milestone)
