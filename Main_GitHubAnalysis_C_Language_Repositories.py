#!/usr/bin/python
from GitHubAnalysis import GitHubAnalysis

if __name__ == '__main__':

    ###########################
    # Get Bug Fix Issues
    ###########################

    log_flag = True
    git_hub_user_name = 'M3N'
    git_hub_password = 'GitHub1'
    git_hub_analysis = GitHubAnalysis(git_hub_user_name=git_hub_user_name, git_hub_password=git_hub_password,
                                      log_flag=log_flag)

    repo_name = 'netdata/netdata'
    issue_label_name = 'bug'
    file_name = './Output/netdata_bug_fix_issues.json'
    git_hub_analysis.write_issue_to_json_file(file_name=file_name, repo_name=repo_name,
                                              issue_label_name=issue_label_name)
    print(repo_name + 'is finished')

    ###########################
    # Get All Issues
    ###########################

    log_flag = True
    git_hub_user_name = 'M3N'
    git_hub_password = 'GitHub1'
    git_hub_analysis = GitHubAnalysis(git_hub_user_name=git_hub_user_name, git_hub_password=git_hub_password,
                                      log_flag=log_flag)

    repo_name = 'netdata/netdata'
    file_name = './Output/netdata_issues.json'
    git_hub_analysis.write_issue_to_json_file(file_name=file_name, repo_name=repo_name,
                                              issue_label_name=None)
    print repo_name + 'is finished'











