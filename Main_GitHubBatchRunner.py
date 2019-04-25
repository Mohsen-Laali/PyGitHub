#! ./venv/bin/python
from GitHubBatchRunner import GitHubBatchRunner

if __name__ == '__main__':
    batch_file = "repo_names.json"
    output_folder = r'./Output/all_issues_c_repositories'

    github_user_name = 'user_name'
    github_password = 'password'
    log_flag = True
    error_log_file_name = r'error_log.txt'
    amend_result = True
    temp_folder = None
    waiting_between_request = 0
    waiting_after_many_request = (-1, 600)
    waiting_after_exception = 300
    core_api_threshold = 100

    github_batch_runner = GitHubBatchRunner(batch_file=batch_file, output_folder=output_folder,
                                            github_user_name=github_user_name, github_password=github_password,
                                            log_flag=log_flag, error_log_file_name=error_log_file_name,
                                            amend_result=amend_result, temp_folder=temp_folder,
                                            waiting_between_request=waiting_between_request,
                                            waiting_after_many_request=waiting_after_many_request,
                                            waiting_after_exception=waiting_after_exception,
                                            core_api_threshold=core_api_threshold)

    github_batch_runner.run_batch()
    # github_batch_runner.check_repos()








