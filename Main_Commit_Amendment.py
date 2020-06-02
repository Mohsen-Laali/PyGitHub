#! ./venv/bin/python
from GitHubAnalysis import GitHubAnalysis

if __name__ == '__main__':
    log_flag = True
    git_hub_user_name = 'M3N'
    git_hub_password = 'GitHub1'
    git_hub_analysis = GitHubAnalysis(git_hub_user_name=git_hub_user_name, git_hub_password=git_hub_password,
                                      log_flag=log_flag)

    # issue_json_file_address = \
    #     r'/home/mohsen/git/Temp/Languages_Issues/all_issues_c_repositories/numpy_issues_2019_04_19.json'
    # result_issues_json_file_address = \
    #     r'/home/mohsen/git/Temp/Languages_Issues/all_issues_c_repositories/numpy_issues_2019_04_19_amendment.json'
    # repository_file_address = '/home/mohsen/git/Temp/Temp_Repositories/Temp_C_Repositories/numpy'
    #
    # git_hub_analysis.\
    #     find_similar_commit_message_to_issue_title(issues_json_file_address=issue_json_file_address,
    #                                                result_issues_json_file_address=result_issues_json_file_address,
    #                                                repository_file_address=repository_file_address)
    #
    # issue_json_file_address = \
    #     r'/home/mohsen/git/Temp/Languages_Issues/all_issues_c_repositories/systemd_issues_2019_04_20.json'
    # result_issues_json_file_address = \
    #     r'/home/mohsen/git/Temp/Languages_Issues/all_issues_c_repositories/systemd_issues_2019_04_20_amendment.json'
    # repository_file_address = '/home/mohsen/git/Temp/Temp_Repositories/Temp_C_Repositories/systemd'
    #
    # git_hub_analysis.\
    #     find_similar_commit_message_to_issue_title(issues_json_file_address=issue_json_file_address,
    #                                                result_issues_json_file_address=result_issues_json_file_address,
    #                                                repository_file_address=repository_file_address)
    #
    # issue_json_file_address = \
    #     r'/home/mohsen/git/Temp/Languages_Issues/all_issues_c_repositories/Arduino_issues_2019_04_21.json'
    # result_issues_json_file_address = \
    #     r'/home/mohsen/git/Temp/Languages_Issues/all_issues_c_repositories/Arduino_issues_2019_04_21_amendment.json'
    # repository_file_address = '/home/mohsen/git/Temp/Temp_Repositories/Temp_C_Repositories/Arduino'
    #
    # git_hub_analysis.\
    #     find_similar_commit_message_to_issue_title(issues_json_file_address=issue_json_file_address,
    #                                                result_issues_json_file_address=result_issues_json_file_address,
    #                                                repository_file_address=repository_file_address)
    #
    # issue_json_file_address = \
    #     r'/home/mohsen/git/Temp/Languages_Issues/all_issues_c_repositories/sway_issues_2019_04_21.json'
    # result_issues_json_file_address = \
    #     r'/home/mohsen/git/Temp/Languages_Issues/all_issues_c_repositories/sway_issues_2019_04_21_amendment.json'
    # repository_file_address = '/home/mohsen/git/Temp/Temp_Repositories/Temp_C_Repositories/sway'
    #
    # git_hub_analysis.\
    #     find_similar_commit_message_to_issue_title(issues_json_file_address=issue_json_file_address,
    #                                                result_issues_json_file_address=result_issues_json_file_address,
    #                                                repository_file_address=repository_file_address)
    #
    # issue_json_file_address = \
    #     r'/home/mohsen/git/Temp/Languages_Issues/all_issues_c_repositories/jq_issues_2019_04_22.json'
    # result_issues_json_file_address = \
    #     r'/home/mohsen/git/Temp/Languages_Issues/all_issues_c_repositories/jq_issues_2019_04_22_amendment.json'
    # repository_file_address = '/home/mohsen/git/Temp/Temp_Repositories/Temp_C_Repositories/jq'
    #
    # git_hub_analysis.\
    #     find_similar_commit_message_to_issue_title(issues_json_file_address=issue_json_file_address,
    #                                                result_issues_json_file_address=result_issues_json_file_address,
    #                                                repository_file_address=repository_file_address)

    # issue_json_file_address = \
    #     r'/home/mohsen/git/Temp/Languages_Issues/all_issues_c_repositories/Marlin_issues_2019_04_19.json'
    # result_issues_json_file_address = \
    #     r'/home/mohsen/git/Temp/Languages_Issues/all_issues_c_repositories/Marlin_issues_2019_04_19_amendment.json'
    # repository_file_address = '/home/mohsen/git/Temp/Temp_Repositories/Temp_C_Repositories/Marlin'
    #
    # git_hub_analysis.\
    #     find_similar_commit_message_to_issue_title(issues_json_file_address=issue_json_file_address,
    #                                                result_issues_json_file_address=result_issues_json_file_address,
    #                                                repository_file_address=repository_file_address)

    c_sharp_base_issue_address = r'/home/mohsen/git/GitHub_Issues/C#_Repos/'
    c_sharp_base_repository_address = r'/home/mohsen/git/Temp/Temp_Repositories/Temp_C_Sharp_Repositories/'

    # issue_json_file_address = c_sharp_base_issue_address + 'EntityFrameworkCore_issues_2019_05_01.json'
    # result_issues_json_file_address = c_sharp_base_issue_address+'EntityFrameworkCore_issues_2019_05_01_amendment.json'
    # repository_file_address = c_sharp_base_repository_address + 'EntityFrameworkCore'
    #
    # git_hub_analysis.\
    #     find_similar_commit_message_to_issue_title(issues_json_file_address=issue_json_file_address,
    #                                                result_issues_json_file_address=result_issues_json_file_address,
    #                                                repository_file_address=repository_file_address)
    #
    # issue_json_file_address = c_sharp_base_issue_address + 'Xamarin.Forms_issues_2019_05_01.json'
    # result_issues_json_file_address = c_sharp_base_issue_address+'Xamarin.Forms_issues_2019_05_01_amendment.json'
    # repository_file_address = c_sharp_base_repository_address + 'Xamarin.Forms'
    #
    # git_hub_analysis.\
    #     find_similar_commit_message_to_issue_title(issues_json_file_address=issue_json_file_address,
    #                                                result_issues_json_file_address=result_issues_json_file_address,
    #                                                repository_file_address=repository_file_address)

    issue_json_file_address = c_sharp_base_issue_address + 'corefx_issues_2019_04_29.json'
    result_issues_json_file_address = c_sharp_base_issue_address + 'corefx_issues_2019_04_29_amendment.json'
    repository_file_address = c_sharp_base_repository_address + 'corefx'

    git_hub_analysis. \
        find_similar_commit_message_to_issue_title(issues_json_file_address=issue_json_file_address,
                                                   result_issues_json_file_address=result_issues_json_file_address,
                                                   repository_file_address=repository_file_address)


