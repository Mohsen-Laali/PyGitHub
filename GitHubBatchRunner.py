import os
import shutil
from datetime import datetime
import json
import traceback

from github import Github
from GitHubAnalysis import GitHubAnalysis
from git import Repo


class RepoDetails:
    def __init__(self, repo_name, bug_issue_labels=None):
        if not bug_issue_labels:
            self.bug_issue_labels = []
        self.repo_labels = bug_issue_labels
        self.repo_name = repo_name


class GitHubBatchRunner:
    def __init__(self, batch_file, output_folder, github_user_name, github_password, log_flag=True,
                 error_log_file_name='error_log.txt', amend_result=True, temp_folder='tempt', waiting_between_request=0,
                 waiting_after_many_request=(1000, 600), waiting_after_exception=300, core_api_threshold=50):

        self.batch_file = batch_file
        self.output_folder = output_folder
        self.github_user_name = github_user_name
        self.github_password = github_password
        self.log_flag = log_flag
        self.error_log_file_name = error_log_file_name
        self.amend_result = amend_result
        self.temp_folder = temp_folder

        self.github = Github(login_or_token=github_user_name, password=github_password)
        self.github_analysis = GitHubAnalysis(git_hub_user_name=github_user_name,
                                              git_hub_password=github_password, log_flag=log_flag,
                                              waiting_between_request=waiting_between_request,
                                              waiting_after_many_request=waiting_after_many_request,
                                              waiting_after_exception=waiting_after_exception,
                                              core_api_threshold=core_api_threshold,
                                              error_log_file_name=error_log_file_name)

    def log(self, log_str):
        if self.log_flag:
            print(log_str)

    def log_error(self, exception, starter=None, extra=None):

        with open(self.error_log_file_name, 'a') as f_handler:
            if starter:
                f_handler.write(starter + os.linesep)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            f_handler.write(current_time + os.linesep)
            if hasattr(exception, 'message') and exception:
                f_handler.write(str(exception.message) + os.linesep)
            elif exception:
                f_handler.write(str(exception) + os.linesep)
            if extra:
                f_handler.write(extra + os.linesep)
            f_handler.write('***********************' + os.linesep)

    def creat_folder(self, folder_path):
        try:
            os.makedirs(folder_path)
        except OSError as e:
            extra = traceback.format_exc()
            error_message = "Creation of the directory " + folder_path + " failed"
            self.log(log_str=error_message)
            self.log(log_str=extra)
            self.log(log_str='***********************' + os.linesep)
            self.log_error(exception=e, starter=error_message, extra=extra)
            raise e
        else:
            message = "Successfully created the directory " + folder_path
            self.log(log_str=message)

    def delete_folder(self, folder_path):
        try:
            shutil.rmtree(folder_path)
        except OSError as e:
            extra = traceback.format_exc()
            error_message = "Deletion of the directory " + folder_path + "  failed"
            self.log(log_str=error_message)
            self.log(log_str=extra)
            self.log(log_str='***********************' + os.linesep)
            self.log_error(exception=e, starter=error_message)
            raise e
        else:
            message = "Successfully deleted the directory " + folder_path
            self.log(log_str=message)

    def run_batch(self):
        list_json_repos = self.read_batch_file()
        list_repos = self.check_repos(list_json_repos=list_json_repos)
        if not os.path.exists(self.output_folder):
            self.creat_folder(folder_path=self.output_folder)
        for repo in list_repos:
            current_time = datetime.now().strftime("%Y_%m_%d")
            file_name = repo.repo_name.split(r'/').pop() + '_issues_' + current_time + '.json'
            file_address = os.path.join(self.output_folder, file_name)
            self.github_analysis.write_issue_to_json_file_exception_proof(file_name=file_address,
                                                                          repo_name=repo.repo_name,
                                                                          issue_label_name=None)
            bug_issue_labels = repo.bug_issue_labels
            if bug_issue_labels:
                for bug_issue_label in bug_issue_labels:
                    file_name = repo.repo_name.split(r'/').pop() + '_' + bug_issue_label.replace(' ', '_') \
                                + '_issues.json'
                    os.path.join(self.output_folder, file_name)
                    self.github_analysis.write_issue_to_json_file_exception_proof(file_name=file_name,
                                                                                  issue_label_name=bug_issue_label)

    def check_repos(self, list_json_repos=None):
        if not list_json_repos:
            list_json_repos = self.read_batch_file()
        list_repos = []
        for json_repo in list_json_repos:
            try:
                repo_name = json_repo['repo_name']
                repo = self.github.get_repo(repo_name)
                message = 'Repo: ' + repo_name + ' is retrieved successfully'
                self.log(log_str=message)
            except Exception as e:
                extra = traceback.format_exc()
                message = 'Repo ' + repo_name + ' is not accessible'
                self.log(log_str=message)
                self.log(log_str=extra)
                self.log(log_str='***********************' + os.linesep)
                self.log_error(exception=e, starter=message, extra=extra)
                raise e
            try:
                bug_issue_labels = json_repo['bug_issue_labels']
                list_repos.append(RepoDetails(repo_name=repo_name, bug_issue_labels=bug_issue_labels))
                for bug_issue_label in bug_issue_labels:
                    repo.get_label(bug_issue_label)
                    message = 'Repo: ' + bug_issue_label + ' is retrieved successfully'
                    self.log(log_str=message)
            except Exception as e:
                extra = traceback.format_exc()
                message = 'Bug issue label ' + bug_issue_label + ' is not accessible'
                self.log(log_str=message)
                self.log(log_str=extra)
                self.log(log_str='***********************' + os.linesep)
                self.log_error(exception=e, starter=message, extra=extra)
                raise e
        return list_repos

    def read_batch_file(self):
        list_json_repo = []
        with open(self.batch_file, 'r+') as file_handler:
            for line in file_handler:
                # skip empty line
                if not line.strip():
                    continue
                json_repo = json.loads(line)
                list_json_repo.append(json_repo)

        return list_json_repo

    @staticmethod
    def amend_issue(batch_file_address):
        json_list = []
        with open(batch_file_address, 'r+') as file_handler:
            for json_line in file_handler:
                json_list.append(json.loads(json_line))

        repo_base_address = json_list[0]["repo_base_address"]
        issue_base_address = json_list[0]["issue_base_address"]
        output_issue_base_address = json_list[0]["output_issue_base_address"]
        clone_repo = json_list[0]['clone_repo']

        for json_issue_details in json_list[1:]:
            print "Start " + json_issue_details['repo_name']
            print "***********************"
            # creat folder for the repo
            repo_address = os.path.join(repo_base_address, json_issue_details["repo_name"])
            if clone_repo:
                os.makedirs(repo_address)
                # cloning the repo
                repo = Repo.clone_from(json_issue_details['repo_clone_address'], repo_address)
            else:
                # connect to the repo
                repo = Repo(path=repo_address)

            # filter commit base on the last scanned issue
            str_filter_date = json_issue_details['filtered_date']
            filter_date = datetime.strptime(str_filter_date, "%Y-%m-%d")
            # get all commit id after the filter date
            # log_commit_ids = repo.git.log(since=filter_date.date(), pretty='format:%H')
            log_commit_ids = repo.git.log(since=filter_date.date(), pretty='format:%H')
            commit_sha = [log.strip() for log in log_commit_ids.split(os.linesep)][-1]
            # check if there is any commit after the filter date
            if commit_sha:
                print commit_sha
                repo.git.reset(commit_sha, hard=True)

            issue_file_address = os.path.join(issue_base_address, json_issue_details["issue_file_name"])
            issue_output_file_address = os.path.join(output_issue_base_address,
                                                     json_issue_details["issue_output_file_name"])

            GitHubAnalysis.find_similar_commit_message_to_issue_title(issues_json_file_address=issue_file_address,
                                                                      result_issues_json_file_address=
                                                                      issue_output_file_address,
                                                                      repository_file_address=repo_address)
            print "End " + json_issue_details['repo_name']
            print "***********************"







