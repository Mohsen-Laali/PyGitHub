from GitHubBatchRunner import GitHubBatchRunner
import os

if __name__ == '__main__':
    batch_file = "repo_names.json"
    output_folder = r'./output/all_issues_c_repositories'

    github_user_name = 'M3N'
    github_password = 'GitHub1'
    log_flag = True
    error_log_file_name = r'error_log_file.txt'
    amend_result = True
    temp_folder = None

    github_batch_runner = GitHubBatchRunner(batch_file=batch_file, output_folder=output_folder,
                                            github_user_name=github_user_name, github_password=github_password,
                                            log_flag=log_flag, error_log_file_name=error_log_file_name,
                                            amend_result=amend_result, temp_folder=temp_folder)

    github_batch_runner.run_batch()
    # github_batch_runner.check_repos()








