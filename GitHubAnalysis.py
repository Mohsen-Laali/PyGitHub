#!/usr/bin/python
import os
import csv
from github import Github
import json
from ssl import SSLError
import traceback
import git
from git.exc import GitCommandError


class GitHubAnalysis:
    def __init__(self, git_hub_user_name, git_hub_password, log_flag=False):
        self.git_hub = Github(git_hub_user_name, git_hub_password)
        self.log_flag = log_flag
        self.error_log_file_name = 'error_log.txt'

    def log(self, log_str):
        if self.log_flag:
            print log_str

    def log_error(self, exception, extra=None):
        with open(self.error_log_file_name, 'a') as f_handler:
            f_handler.write(exception.message + os.linesep)
            f_handler.write(extra + os.linesep)
            f_handler.write('***********************' + os.linesep)

    def find_issues(self, repo_name, issue_label_name='bug', state='closed'):
        repo = self.git_hub.get_repo(repo_name)
        if issue_label_name:
            issue_label_name = repo.get_label(issue_label_name)
            paginated_list_issues = repo.get_issues(state=state, labels=[issue_label_name])
        else:
            paginated_list_issues = repo.get_issues(state=state)
        return paginated_list_issues

    def write_bug_fix_commits_to_file(self, file_name, repo_name, issue_label_name='bug', state='closed'):
        with open(file_name, 'w+') as csv_file:
            fields_names = ['number', 'repository_name', 'issue_title', 'issue_commit_id',
                            'diff_url', 'html_url', 'patch_url']
            number, repository_name, issue_title, issue_commit_id, diff_url, html_url, patch_url = fields_names
            writer = csv.DictWriter(csv_file, fieldnames=fields_names)
            writer.writeheader()
            paginated_list_issues = self.find_issues(repo_name, issue_label_name, state)
            row_number = 1

            for issue in paginated_list_issues:
                dictionary_data = dict()
                dictionary_data[number] = row_number
                dictionary_data[issue_title] = issue.title.encode('utf-8')
                dictionary_data[repository_name] = issue.repository.full_name.encode('utf-8')

                paginated_list_issue_events = issue.get_events()
                dictionary_data[issue_commit_id] = ''
                for issue_event in paginated_list_issue_events:
                    if issue_event.event == 'merged':
                        dictionary_data[issue_commit_id] = issue_event.commit_id.encode('utf-8')

                issue_pull_request = issue.pull_request
                dictionary_data[diff_url] = ''
                dictionary_data[html_url] = ''
                dictionary_data[patch_url] = ''
                if issue_pull_request is not None:
                    dictionary_data[diff_url] = issue_pull_request.diff_url.encode('utf-8')
                    dictionary_data[html_url] = issue_pull_request.html_url.encode('utf-8')
                    dictionary_data[patch_url] = issue_pull_request.patch_url.encode('utf-8')

                line = str(row_number) + ',' + dictionary_data[repository_name] + ',' + dictionary_data[issue_title] \
                    + ',' + dictionary_data[issue_commit_id] + ','
                self.log(line)
                line += dictionary_data[diff_url] + ',' + dictionary_data[html_url] + ','
                line += dictionary_data[patch_url]

                # write(line.encode('utf-8') + os.linesep)
                writer.writerow(dictionary_data)
                self.log('+++++++++++++++')
                row_number += 1

    def write_issue_to_json_file(self, file_name, repo_name, issue_label_name='bug', state='closed'):
        with open(file_name, 'w+') as json_file:
            fields_names = ['number', 'issue_number', 'repository_name', 'issue_title', 'issue_labels',
                            'issue_comments', 'issue_commit_id', 'issue_closed_commit_id',
                            'diff_url', 'html_url', 'patch_url']

            number_fn, issue_number_fn, repository_name_fn, issue_title_fn, issue_labels_fn,\
                issue_comments_fn, issue_commit_id_fn, issue_closed_commit_id_fn, \
                diff_url_fn, html_url_fn, patch_url_fn = fields_names

            json_file.write(json.dumps(fields_names, sort_keys=True))
            json_file.write(os.linesep)

            paginated_list_issues = self.find_issues(repo_name=repo_name, issue_label_name=issue_label_name,
                                                     state=state)
            row_number = 1
            for issue in paginated_list_issues:
                dictionary_data = dict()
                dictionary_data[number_fn] = row_number
                dictionary_data[issue_number_fn] = issue.number
                dictionary_data[issue_title_fn] = issue.title.encode('utf-8')
                dictionary_data[repository_name_fn] = issue.repository.full_name.encode('utf-8')

                paginated_list_issue_events = issue.get_events()
                list_issue_commit_id = []
                list_issue_closed_commit_id = []
                for issue_event in paginated_list_issue_events:
                    if issue_event.event == 'merged':
                        list_issue_commit_id.append(issue_event.commit_id.encode('utf-8'))
                    if issue_event.event == 'closed' and issue_event.commit_id:
                        list_issue_closed_commit_id.append(issue_event.commit_id.encode('utf-8'))

                issue_labels = issue.get_labels()
                list_issue_labels = []
                try:
                    for issue_label in issue_labels:
                        list_issue_labels.append(issue_label.name)
                except SSLError as e:
                    extra = dictionary_data[repository_name_fn] + os.linesep + dictionary_data[issue_title_fn] \
                            + os.linesep + traceback.format_exc() + os.linesep
                    self.log_error(e, extra)
                    continue

                if len(list_issue_labels):
                    dictionary_data[issue_labels_fn] = list_issue_labels
                if issue.body:
                    list_issue_comments = [issue.body.encode('utf-8')]
                paginated_list_comments = issue.get_comments()
                for issue_comment in paginated_list_comments:
                    list_issue_comments.append(issue_comment.body.encode('utf-8'))

                if len(list_issue_comments):
                    dictionary_data[issue_comments_fn] = list_issue_comments

                if len(list_issue_commit_id):
                    dictionary_data[issue_commit_id_fn] = list_issue_commit_id
                if len(list_issue_closed_commit_id):
                    dictionary_data[issue_closed_commit_id_fn] = list_issue_closed_commit_id

                issue_pull_request = issue.pull_request
                if issue_pull_request is not None:
                    dictionary_data[diff_url_fn] = issue_pull_request.diff_url.encode('utf-8')
                    dictionary_data[html_url_fn] = issue_pull_request.html_url.encode('utf-8')
                    dictionary_data[patch_url_fn] = issue_pull_request.patch_url.encode('utf-8')

                # write(line.encode('utf-8') + os.linesep)
                # json.dump(dictionary_data, json_file)
                json_file.write(json.dumps(dictionary_data, sort_keys=True))
                json_file.write(os.linesep)
                if self.log_flag:
                    self.log(json.dumps(dictionary_data, sort_keys=True, indent=2))
                    self.log('++++++++++++++++++++++++')
                row_number += 1

    def find_similar_commit_message_to_issue_title(self, issues_json_file_address, result_issues_json_file_address,
                                                   repository_file_address):

        repo = git.Repo(path=repository_file_address)

        def check_if_exist(hash_commit_to_test):
            try:
                repo.git.cat_file(hash_commit_to_test, t=True)
            except GitCommandError as e:
                if e.stderr == 'fatal: git cat-file: could not get object info':
                    return False
                else:
                    raise e
            return True

        with open(issues_json_file_address, 'r+') as issues_json_file_handler, \
                open(result_issues_json_file_address, 'w+') as result_issues_file_handler:
            field_names = json.loads(issues_json_file_handler.readline())
            field_similar_commit_to_issue_title = 'commit_id_similar_to_issue_title'
            field_names += field_similar_commit_to_issue_title
            result_issues_file_handler.write(json.dumps(field_names) + os.linesep)
            for json_text in issues_json_file_handler:
                set_similar_commit_ids = set()
                json_line = json.loads(json_text.strip(), encoding='utf8')
                # json_line = {k: utf8_encode(v) for k, v in json_line.items()}

                set_discovered_commits = set()
                if 'issue_closed_commit_id' in json_line:
                    not_exit_commits = set()
                    for issue_closed_commit_id in json_line['issue_closed_commit_id']:
                        issue_closed_commit_id = issue_closed_commit_id.strip()
                        # check if the hash commit exist in the repository
                        if check_if_exist(issue_closed_commit_id):
                            set_discovered_commits.add(issue_closed_commit_id)
                        else:
                            not_exit_commits.add(issue_closed_commit_id)
                    # remove commits not exist in the repository
                    json_line['issue_closed_commit_id'] = list(set(json_line['issue_closed_commit_id']) -
                                                               not_exit_commits)
                    # if  there is not any commit left, field would be removed
                    if not json_line['issue_closed_commit_id']:
                        del json_line['issue_closed_commit_id']
                    # map(set_discovered_commits.add, json_line['issue_closed_commit_id'])

                if 'issue_commit_id' in json_line:
                    not_exit_commits = set()
                    for issue_commit_id in json_line['issue_commit_id']:
                        issue_commit_id = issue_commit_id.strip()
                        # check if the hash commit exist in the repository
                        if check_if_exist(issue_commit_id):
                            set_discovered_commits.add(issue_commit_id)
                        else:
                            not_exit_commits.add(issue_commit_id)
                    # remove commits not exist in the repository
                    json_line['issue_commit_id'] = list(set(json_line['issue_commit_id']) -
                                                        not_exit_commits)
                    # if there is not any commit left, field would be removed
                    if not json_line['issue_commit_id']:
                        del json_line['issue_commit_id']
                    # map(set_discovered_commits.add, json_line['issue_commit_id'])

                issue_title = json_line['issue_title']
                log_commit_ids = repo.git.log(all=True, grep=issue_title, pretty='format:%H', i=True,
                                              F=True)
                if len(log_commit_ids) > 0:
                    similar_commit_ids = map(lambda l: l.strip(), log_commit_ids.split(os.linesep))

                    def filter_append(c):
                        if c and c not in set_discovered_commits:
                            set_similar_commit_ids.add(c)

                    map(filter_append, similar_commit_ids)
                json_line[field_similar_commit_to_issue_title] = list(set_similar_commit_ids)
                result_issues_file_handler.write(json.dumps(json_line) + os.linesep)
                self.log('******************************')
                self.log(json_line)

    def convert_json_csv(self, json_file_address, csv_file_address, list_ignored_columns=[]):

        def utf8_encode(to_encode):
            if type(to_encode) is list:
                return map(lambda t: t.encode('utf8'), to_encode)
            elif type(to_encode) is unicode:
                to_encode = to_encode.encode('utf8')
                return to_encode
            else:
                return to_encode

        with open(json_file_address, 'r+') as json_file_handler, open(csv_file_address, 'w+') as csv_file_handler:
            json_field_names = json.loads(json_file_handler.readline(), encoding='utf8')
            for col in list_ignored_columns:
                json_field_names.remove(col)

            # BOM (optional...Excel needs it to open UTF-8 file properly)
            csv_file_handler.write(u'\ufeff'.encode('utf8'))
            # self.log(json_field_names)
            csv_writer = csv.DictWriter(csv_file_handler, fieldnames=json_field_names)
            csv_writer.writeheader()
            for json_text in json_file_handler:
                json_line = json.loads(json_text.strip(), encoding='utf8')
                for col in list_ignored_columns:
                    del json_line[col]
                self.log(json_text)
                csv_writer.writerow({k: utf8_encode(v) for k, v in json_line.items()})
