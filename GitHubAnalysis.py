#!/usr/bin/env python
import os
import csv
from datetime import datetime, timedelta  # Current time
from time import sleep  # Waiting time before API reset
from pytz import timezone  # API reset timezone
import traceback


from github import Github
import json
from ssl import SSLError
import traceback
import git
from git.exc import GitCommandError


class GitHubAnalysis:
    def __init__(self, git_hub_user_name, git_hub_password, log_flag=False, waiting_between_request=0,
                 waiting_after_many_request=(1000, 600), waiting_after_exception=300, core_api_threshold=50,
                 error_log_file_name='error_log.txt'):
        self.git_hub = Github(git_hub_user_name, git_hub_password)
        self.log_flag = log_flag
        self.error_log_file_name = error_log_file_name
        self.waiting_between_request = waiting_between_request  # second
        self.waiting_after_many_request = waiting_after_many_request  # (Number of request, Waiting time (seconds))
        self.rate_limit_count = 0
        self.exception_number = 0  # the exception number shows number time function is called,
        # sub-exception shows the number of exception exception

        self.waiting_after_exception = waiting_after_exception  # the waiting time after exception

        self.core_api_threshold = core_api_threshold  # only check the api limit from github if the number jump
        # below this number of core api thresholds
        self.core_api_left_tracker = 0  # keep tracker of api call

    def log(self, log_str):
        if self.log_flag:
            print(log_str)

    def log_error(self, exception, extra=None, starter=None):
        with open(self.error_log_file_name, 'a') as f_handler:
            if starter is not None:
                f_handler.write(starter + os.linesep)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            f_handler.write(current_time + os.linesep)
            if hasattr(exception, 'message'):
                f_handler.write(str(exception.message) + os.linesep)
            else:
                f_handler.write(exception + os.linesep)
            if extra is not None:
                f_handler.write(extra + os.linesep)
            f_handler.write('***********************' + os.linesep)

    def rate_limit_control(self, minimum_api_rate_limit=5, api_call=1):

        self.rate_limit_count += api_call
        self.core_api_left_tracker -= api_call
        sleep(self.waiting_between_request)  # politeness waiting

        if self.core_api_left_tracker < self.core_api_threshold or self.core_api_threshold == -1:

            # waiting after many requests
            if self.rate_limit_count == self.waiting_after_many_request[0]:
                self.log('Waiting for ' + str(self.waiting_after_many_request[1]) + ' second(s) after ' +
                         str(self.waiting_after_many_request[0]) + ' call(s)')
                self.log('Current time ' + str(datetime.now()))
                sleep(self.waiting_after_many_request[1])

            core_call_left = self.git_hub.get_rate_limit().core.remaining
            core_reset_time = self.git_hub.get_rate_limit().core.reset
            search_call_left = self.git_hub.get_rate_limit().search.remaining
            search_reset_time = self.git_hub.get_rate_limit().search.reset

            self.core_api_left_tracker = core_call_left

            # check API limit rate
            if core_call_left < minimum_api_rate_limit or \
               search_call_left < minimum_api_rate_limit:

                # find the reset time
                reset_time = core_reset_time
                if reset_time < search_reset_time:
                    reset_time = search_reset_time
                # Current time in the GitHub API time zone
                current_time = datetime.now(timezone('UTC')).replace(tzinfo=None)
                # Sleeping time with extra 30 seconds
                sleeping_seconds = (reset_time - current_time).seconds + 30
                self.log("Core Reach rate limit ( " + str(core_call_left) + " , " + str(core_reset_time) +
                         " API call (left, to reset time (UTC)) " + os.linesep +
                         "Search rate limit ( " + str(search_call_left) + " , " + str(search_reset_time) +
                         " Core API call (left, to reset time (UTC)) " + os.linesep +
                         "Waiting until " + str(datetime.now() + timedelta(seconds=sleeping_seconds)) + " )")
                sleep(sleeping_seconds)

    def find_issues(self, repo_name, issue_label_name='bug', state='closed'):
        self.rate_limit_control()  # control api rate limit call
        repo = self.git_hub.get_repo(repo_name)
        if issue_label_name:
            self.rate_limit_control()  # control api rate limit call
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

            self.rate_limit_control()  # control api rate limit call

            for issue in paginated_list_issues:

                self.rate_limit_control()  # control api rate limit call

                dictionary_data = dict()
                dictionary_data[number] = row_number
                dictionary_data[issue_title] = issue.title.encode('utf-8')
                dictionary_data[repository_name] = issue.repository.full_name.encode('utf-8')

                self.rate_limit_control()  # control api rate limit call

                paginated_list_issue_events = issue.get_events()
                dictionary_data[issue_commit_id] = ''
                for issue_event in paginated_list_issue_events:

                    self.rate_limit_control()  # control api rate limit call

                    if issue_event.event == 'merged':
                        dictionary_data[issue_commit_id] = issue_event.commit_id.encode('utf-8')

                issue_pull_request = issue.pull_request

                self.rate_limit_control()  # control api rate limit call

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

    def write_issue_to_json_file_exception_proof(self, file_name, repo_name, issue_label_name='bug', state='closed'):

        sub_exception_number = 0
        self.exception_number += 1
        continue_the_loop = True
        while continue_the_loop:
            try:
                self.write_issue_to_json_file(file_name=file_name, repo_name=repo_name,
                                              issue_label_name=issue_label_name, state=state)
                continue_the_loop = False
            except Exception as e:
                extra = traceback.format_exc()
                sub_exception_number += 1
                starter = str(self.exception_number)+'.'+str(sub_exception_number)+'- '
                self.log(log_str=starter + os.linesep + extra)
                self.log(log_str='***********************' + os.linesep)
                self.log_error(exception=e, starter=starter, extra=extra)
                sleep(self.waiting_after_exception)

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
            self.rate_limit_control()  # control api rate limit call TODO redundant

            repo_full_name = None
            for issue in paginated_list_issues:

                self.rate_limit_control()  # control api rate limit call (might redundant, only the api call first time)

                dictionary_data = dict()
                dictionary_data[number_fn] = row_number

                dictionary_data[issue_number_fn] = issue.number

                dictionary_data[issue_title_fn] = issue.title.encode('utf-8')

                if not repo_full_name:
                    repo_full_name = issue.repository.full_name.encode('utf-8')
                    self.rate_limit_control(api_call=2)  # control api rate limit call

                dictionary_data[repository_name_fn] = repo_full_name

                paginated_list_issue_events = issue.get_events()

                list_issue_commit_id = []
                list_issue_closed_commit_id = []
                for issue_event in paginated_list_issue_events:

                    if issue_event.event == 'merged':
                        list_issue_commit_id.append(issue_event.commit_id.encode('utf-8'))
                    if issue_event.event == 'closed' and issue_event.commit_id:
                        list_issue_closed_commit_id.append(issue_event.commit_id.encode('utf-8'))
                else:
                    self.rate_limit_control()  # control api rate limit call

                issue_labels = issue.get_labels()

                list_issue_labels = []
                # try:
                for issue_label in issue_labels:
                    list_issue_labels.append(issue_label.name)
                else:
                    self.rate_limit_control()  # control api rate limit call
                # except SSLError as e:
                #     extra = dictionary_data[repository_name_fn] + os.linesep + dictionary_data[issue_title_fn] \
                #             + os.linesep + traceback.format_exc() + os.linesep
                #     self.log_error(e, extra)
                #     raise e
                if len(list_issue_labels):
                    dictionary_data[issue_labels_fn] = list_issue_labels

                list_issue_comments = []
                if issue.body:
                    list_issue_comments.append(issue.body.encode('utf-8'))

                paginated_list_comments = issue.get_comments()
                for issue_comment in paginated_list_comments:
                    list_issue_comments.append(issue_comment.body.encode('utf-8'))
                else:
                    self.rate_limit_control()  # control api rate limit call

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

                json_file.write(json.dumps(dictionary_data))
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
                    similar_commit_ids = [l.strip() for l in log_commit_ids.split(os.linesep)]

                    def filter_append(c):
                        if c and c not in set_discovered_commits:
                            set_similar_commit_ids.add(c)

                    list(map(filter_append, similar_commit_ids))
                json_line[field_similar_commit_to_issue_title] = list(set_similar_commit_ids)
                result_issues_file_handler.write(json.dumps(json_line) + os.linesep)
                self.log('******************************')
                self.log(json_line)

    def convert_json_csv(self, json_file_address, csv_file_address, list_ignored_columns=None):

        if list_ignored_columns is None:
            list_ignored_columns = []

        def utf8_encode(to_encode):
            if type(to_encode) is list:
                return [t.encode('utf8') for t in to_encode]
            elif type(to_encode) is str:
                to_encode = to_encode.encode('utf8')
                return to_encode
            else:
                return to_encode

        with open(json_file_address, 'r+') as json_file_handler, open(csv_file_address, 'w+') as csv_file_handler:
            json_field_names = json.loads(json_file_handler.readline(), encoding='utf8')
            for col in list_ignored_columns:
                json_field_names.remove(col)

            # BOM (optional...Excel needs it to open UTF-8 file properly)
            csv_file_handler.write('\ufeff'.encode('utf8'))
            # self.log(json_field_names)
            csv_writer = csv.DictWriter(csv_file_handler, fieldnames=json_field_names)
            csv_writer.writeheader()
            for json_text in json_file_handler:
                json_line = json.loads(json_text.strip(), encoding='utf8')
                for col in list_ignored_columns:
                    del json_line[col]
                self.log(json_text)
                csv_writer.writerow({k: utf8_encode(v) for k, v in list(json_line.items())})
