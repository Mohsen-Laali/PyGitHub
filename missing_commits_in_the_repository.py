import git
from git.exc import GitCommandError
import json
import os
import re

# print re.escape('Remove unsafe char[] access in PlatformDependent')
# raw_input('press any key')


def missing_commit_from_repository(issues_json_file_address, result_issues_json_file_address, repository_file_address):
    repo = git.Repo(path=repository_file_address)

    def utf8_encode(to_encode):
        if type(to_encode) is list:
            return [t.encode('utf8') for t in to_encode]
        elif type(to_encode) is str:
            to_encode = to_encode.encode('utf8')
            return to_encode
        else:
            return to_encode

    def check_if_exist(repo_to_test, hash_commit_to_test):
        try:
            repo.git.cat_file(hash_commit_to_test, t=True)
        except GitCommandError as e:
            if e.stderr == 'fatal: git cat-file: could not get object info':
                return True
            else:
                raise e
        return False

    def check_if_exist_(repo_to_test, hash_commit_to_test):
        try:
            type_commit = repo_to_test.git.cat_file(hash_commit_to_test, t=True)
        except GitCommandError as e:
            print('**************')
            print(hash_commit_to_test)
            print('**************')
            if e.stderr == 'fatal: git cat-file: could not get object info':
                print('salam alakom nakardi')
            print('**************')
            print(e)
            input('press  any key')
        # if type_commit.strip() != 'commit':
        #     print hash_commit_to_test
        #     print type_commit
        #     raw_input('press any key')

    with open(issues_json_file_address, 'r+') as issues_json_file_handler, \
            open(result_issues_json_file_address, 'w+') as result_issues_file_handler:
        field_names = json.loads(issues_json_file_handler.readline())
        field_similar_commit_to_issue_title = 'commit_id_similar_to_issue_title'
        field_names += field_similar_commit_to_issue_title
        result_issues_file_handler.write(json.dumps(field_names)+os.linesep)
        not_working_commit = 0
        for json_text in issues_json_file_handler:
            set_similar_commit_ids = set()
            json_line = json.loads(json_text.strip(), encoding='utf8')
            # json_line = {k: utf8_encode(v) for k, v in json_line.items()}
            set_discovered_commits = set()
            if 'issue_closed_commit_id' in json_line:
                list(map(set_discovered_commits.add, json_line['issue_closed_commit_id']))
            if 'issue_commit_id' in json_line:
                list(map(set_discovered_commits.add, json_line['issue_commit_id']))
            issue_title = json_line['issue_title']
            # print '&&&&&&&&&&&&&&&&&&&&&&&&&&'
            # print json_line['issue_number']
            # print '=========================='
            # print 'set of discovered commits'
            # print set_discovered_commits
            # print '++++++++++++++++++++++++++'
            # print 'issue_title'
            # print issue_title
            # print '##########################'
            for commit_sha in set_discovered_commits:
                # print commit_sha
                if check_if_exist(repo_to_test=repo, hash_commit_to_test=commit_sha):
                    not_working_commit += 1
                    print(not_working_commit)
                    print(commit_sha)
                # raw_input('press any key')
            log_commit_ids = repo.git.log(all=True, grep=issue_title, pretty='format:%H', i=True, F=True)
            # print log_commit_ids.strip()

            if len(log_commit_ids) > 0:
                similar_commit_ids = [l.strip() for l in log_commit_ids.split(os.linesep)]
                # print map(lambda l: l.strip(), log_commit_ids.split(os.linesep))

                def filter_append(c):
                    if c not in set_discovered_commits:
                        set_similar_commit_ids.add(c)

                list(map(filter_append, similar_commit_ids))
            json_line[field_similar_commit_to_issue_title] = list(set_similar_commit_ids)
            # print {k: utf8_encode(v) for k, v in json_line.items()}

            result_issues_file_handler.write(json.dumps({k: utf8_encode(v) for k, v in list(json_line.items())}) + os.linesep)
            # raw_input('press any key')
            # print json_line
            # raw_input('press any key')


# repository_address = r'/home/mohsen/git/Human_Factor/Sample_Git_Repository/netty'
# issue_json_file_address = r'/home/mohsen/PycharmProjects/PyGithub/Output/netty_bug_fix_issues.json'
# result_json_file_address = r'similar_netty_bug_fix_issues.json'

repository_address = r'/home/mohsen/git/Human_Factor/Sample_Git_Repository/druid_15_Feb'
issue_json_file_address = r'/home/mohsen/PycharmProjects/PyGithub/Output/All_issues/druid_issues.json'
result_json_file_address = r'similar_druid_issues.json'

missing_commit_from_repository(issues_json_file_address=issue_json_file_address,
                               result_issues_json_file_address=result_json_file_address,
                               repository_file_address=repository_address)