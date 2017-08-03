#!/usr/bin/python
from GitHubAnalysis import GitHubAnalysis

if __name__ == '__main__':
    t = 'start'
    # repo_name = 'PyGithub/PyGithub'

    # issue_label_name = 'bug'
    # file_name = 'elastic_search_bug_fix_commit.csv'

    # file_name = 't.json'
    # file_name = 't.csv'

    # git_hub_analysis.convert_json_csv('rx_java_bug_fix_issues.json', 'rx_java_bug_fix_issues.csv', ['issue_comments'])
    #
    # git_hub_analysis = GitHubAnalysis(git_hub_user_name=git_hub_user_name, git_hub_password=git_hub_password,
    #                                   log_flag=log_flag)
    # git_hub_analysis.convert_json_csv('elastic_search_bug_fix_issues.json', 'elastic_search_bug_fix_issues.csv'
    #                                   , ['issue_comments'])
    #
    # git_hub_analysis = GitHubAnalysis(git_hub_user_name=git_hub_user_name, git_hub_password=git_hub_password,
    #                                   log_flag=log_flag)
    # git_hub_analysis.convert_json_csv('spring_boot_bug_fix_issues.json', 'spring_boot_bug_fix_issues.csv'
    #                                   , ['issue_comments'])
    #
    # git_hub_analysis = GitHubAnalysis(git_hub_user_name=git_hub_user_name, git_hub_password=git_hub_password,
    #                                   log_flag=log_flag)
    # git_hub_analysis.convert_json_csv('netty_bug_fix_issues.json', 'netty_bug_fix_issues.csv'
    #                                   , ['issue_comments'])
    #
    # git_hub_analysis = GitHubAnalysis(git_hub_user_name=git_hub_user_name, git_hub_password=git_hub_password,
    #                                   log_flag=log_flag)
    # git_hub_analysis.convert_json_csv('druid_fix_issues.json', 'druid_fix_issues.csv'
    #                                   , ['issue_comments'])

    ###########################
    # Get Bug Fix Issues
    ###########################

    # log_flag = True
    # git_hub_user_name = 'M3N'
    # git_hub_password = 'GitHub1'
    # git_hub_analysis = GitHubAnalysis(git_hub_user_name=git_hub_user_name, git_hub_password=git_hub_password,
    #                                   log_flag=log_flag)

    # repo_name = 'ReactiveX/RxJava'
    # issue_label_name = 'Bug'
    # file_name = 'rx_java_bug_fix_issues.json'
    # git_hub_analysis.write_issue_to_json_file(file_name=file_name, repo_name=repo_name,
    #                                           issue_label_name=issue_label_name)
    # print repo_name + 'is finished'
    #
    # repo_name = 'elastic/elasticsearch'
    # issue_label_name = 'bug'
    # file_name = 'elastic_search_bug_fix_issues.json'
    # git_hub_analysis.write_issue_to_json_file(file_name=file_name, repo_name=repo_name,
    #                                           issue_label_name=issue_label_name)
    # print repo_name + 'is finished'
    #
    # issue_label_name = 'type: bug'
    # repo_name = 'spring-projects/spring-boot'
    # file_name = 'spring_boot_bug_fix_issues.json'
    # git_hub_analysis.write_issue_to_json_file(file_name=file_name, repo_name=repo_name,
    #                                           issue_label_name=issue_label_name)
    # print repo_name + 'is finished'
    #
    # issue_label_name = 'defect'
    # repo_name = 'netty/netty'
    # file_name = 'netty_bug_fix_issues.json'
    # git_hub_analysis.write_issue_to_json_file(file_name=file_name, repo_name=repo_name,
    #                                           issue_label_name=issue_label_name)
    # print repo_name + 'is finished'
    #
    # issue_label_name = 'Bug'
    # repo_name = 'druid-io/druid'
    # file_name = 'druid_bug_fix_issues.json'
    # git_hub_analysis.write_issue_to_json_file(file_name=file_name, repo_name=repo_name,
    #                                           issue_label_name=issue_label_name)
    # print repo_name + 'is finished'

    ###########################
    # Get All Issues
    ###########################

    # log_flag = True
    # git_hub_user_name = 'M3N'
    # git_hub_password = 'GitHub1'
    # git_hub_analysis = GitHubAnalysis(git_hub_user_name=git_hub_user_name, git_hub_password=git_hub_password,
    #                                   log_flag=log_flag)

    # repo_name = 'ReactiveX/RxJava'
    # file_name = 'rx_java_issues.json'
    # git_hub_analysis.write_issue_to_json_file(file_name=file_name, repo_name=repo_name,
    #                                           issue_label_name=None)
    # print repo_name + 'is finished'

    # repo_name = 'netty/netty'
    # file_name = 'netty_issues.json'
    # git_hub_analysis.write_issue_to_json_file(file_name=file_name, repo_name=repo_name,
    #                                           issue_label_name=None)
    # print repo_name + 'is finished'
    #
    # repo_name = 'druid-io/druid'
    # file_name = 'druid_issues.json'
    # git_hub_analysis.write_issue_to_json_file(file_name=file_name, repo_name=repo_name,
    #                                           issue_label_name=None)
    # print repo_name + 'is finished'
    #
    # repo_name = 'spring-projects/spring-boot'
    # file_name = 'spring_boot_issues.json'
    # git_hub_analysis.write_issue_to_json_file(file_name=file_name, repo_name=repo_name,
    #                                           issue_label_name=None)
    # print repo_name + 'is finished'
    #
    # repo_name = 'elastic/elasticsearch'
    # file_name = 'elastic_search_issues.json'
    # git_hub_analysis.write_issue_to_json_file(file_name=file_name, repo_name=repo_name,
    #                                           issue_label_name=None)
    # print repo_name + 'is finished'

    ###########################
    # Append similar issues
    ###########################

    log_flag = True
    git_hub_user_name = 'M3N'
    git_hub_password = 'GitHub1'
    git_hub_analysis = GitHubAnalysis(git_hub_user_name=git_hub_user_name, git_hub_password=git_hub_password,
                                      log_flag=log_flag)

    # issues_json_file_address = '/home/mohsen/PycharmProjects/PyGithub/Output/All_issues/druid_issues.json'
    # result_issues_json_file_address = \
    #     '/home/mohsen/PycharmProjects/PyGithub/Output/All_Issues_Similar_Commits_Amendment/druid_issues_amendment.json'
    # repository_file_address = '/home/mohsen/git/Human_Factor/Sample_Git_Repository/druid_15_Feb'
    #
    # git_hub_analysis.find_similar_commit_message_to_issue_title(issues_json_file_address=issues_json_file_address,
    #                                                             result_issues_json_file_address=
    #                                                             result_issues_json_file_address,
    #                                                             repository_file_address=repository_file_address)
    #
    # issues_json_file_address = '/home/mohsen/PycharmProjects/PyGithub/Output/All_issues/netty_issues.json'
    # result_issues_json_file_address = \
    #     '/home/mohsen/PycharmProjects/PyGithub/Output/All_Issues_Similar_Commits_Amendment/netty_issues_amendment.json'
    # repository_file_address = '/home/mohsen/git/Human_Factor/Sample_Git_Repository/netty_15_Feb'
    #
    # git_hub_analysis.find_similar_commit_message_to_issue_title(issues_json_file_address=issues_json_file_address,
    #                                                             result_issues_json_file_address=
    #                                                             result_issues_json_file_address,
    #                                                             repository_file_address=repository_file_address)
    #
    # issues_json_file_address = '/home/mohsen/PycharmProjects/PyGithub/Output/All_issues/rx_java_issues.json'
    # result_issues_json_file_address = \
    #     '/home/mohsen/PycharmProjects/PyGithub/Output/All_Issues_Similar_Commits_Amendment/' \
    #     'rx_java_issues_amendment.json'
    # repository_file_address = '/home/mohsen/git/Human_Factor/Sample_Git_Repository/RxJava_13_Feb'
    #
    # git_hub_analysis.find_similar_commit_message_to_issue_title(issues_json_file_address=issues_json_file_address,
    #                                                             result_issues_json_file_address=
    #                                                             result_issues_json_file_address,
    #                                                             repository_file_address=repository_file_address)
    #
    # issues_json_file_address = '/home/mohsen/PycharmProjects/PyGithub/Output/All_issues/spring_boot_issues.json'
    # result_issues_json_file_address = \
    #     '/home/mohsen/PycharmProjects/PyGithub/Output/All_Issues_Similar_Commits_Amendment/' \
    #     'spring_boot_issues_amendment.json'
    # repository_file_address = '/home/mohsen/git/Human_Factor/Sample_Git_Repository/spring-boot_15_Feb'
    #
    # git_hub_analysis.find_similar_commit_message_to_issue_title(issues_json_file_address=issues_json_file_address,
    #                                                             result_issues_json_file_address=
    #                                                             result_issues_json_file_address,
    #                                                             repository_file_address=repository_file_address)

    issues_json_file_address = '/home/mohsen/PycharmProjects/PyGithub/Output/All_issues/elastic_search_issues.json'
    result_issues_json_file_address = \
        '/home/mohsen/PycharmProjects/PyGithub/Output/All_Issues_Similar_Commits_Amendment/' \
        'elastic_search_issues_amendment.json'
    repository_file_address = '/home/mohsen/git/Human_Factor/Sample_Git_Repository/elasticsearch_17_Feb'

    git_hub_analysis.find_similar_commit_message_to_issue_title(issues_json_file_address=issues_json_file_address,
                                                                result_issues_json_file_address=
                                                                result_issues_json_file_address,
                                                                repository_file_address=repository_file_address)










