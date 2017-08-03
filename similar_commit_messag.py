import git
import json
import os
import re

# print re.escape('Remove unsafe char[] access in PlatformDependent')
# raw_input('press any key')


def find_similar_commit_message_to_issue_title(issues_json_file_address, result_issues_json_file_address, repository_file_address):
    repo = git.Repo(path=repository_file_address)

    def utf8_encode(to_encode):
        if type(to_encode) is list:
            return map(lambda t: t.encode('utf8'), to_encode)
        elif type(to_encode) is unicode:
            to_encode = to_encode.encode('utf8')
            return to_encode
        else:
            return to_encode

    with open(issues_json_file_address, 'r+') as issues_json_file_handler, \
            open(result_issues_json_file_address, 'w+') as result_issues_file_handler:
        field_names = json.loads(issues_json_file_handler.readline())
        field_similar_commit_to_issue_title = 'commit_id_similar_to_issue_title'
        field_names += field_similar_commit_to_issue_title
        result_issues_file_handler.write(json.dumps(field_names)+os.linesep)
        for json_text in issues_json_file_handler:
            set_similar_commit_ids = set()
            json_line = json.loads(json_text.strip(), encoding='utf8')
            # json_line = {k: utf8_encode(v) for k, v in json_line.items()}
            set_discovered_commits = set()
            if 'issue_closed_commit_id' in json_line:
                map(set_discovered_commits.add, json_line['issue_closed_commit_id'])
            if 'issue_commit_id' in json_line:
                map(set_discovered_commits.add, json_line['issue_commit_id'])
            issue_title = json_line['issue_title']
            print '&&&&&&&&&&&&&&&&&&&&&&&&&&'
            print json_line['issue_number']
            print '=========================='
            print 'set of discovered commits'
            print set_discovered_commits
            print '++++++++++++++++++++++++++'
            print 'issue_title'
            print issue_title
            print '##########################'
            log_commit_ids = repo.git.log(all=True, grep=issue_title, pretty='format:%H', i=True, F=True)
            print log_commit_ids.strip()

            if len(log_commit_ids) > 0:
                similar_commit_ids = map(lambda l: l.strip(), log_commit_ids.split(os.linesep))
                print map(lambda l: l.strip(), log_commit_ids.split(os.linesep))

                def filter_append(c):
                    if c not in set_discovered_commits:
                        set_similar_commit_ids.add(c)

                map(filter_append, similar_commit_ids)
            json_line[field_similar_commit_to_issue_title] = set_similar_commit_ids
            print {k: utf8_encode(v) for k, v in json_line.items()}

            result_issues_file_handler.write(json.dumps({k: utf8_encode(v) for k, v in json_line.items()}) + os.linesep)
            raw_input('press any key')
            print json_line
            raw_input('press any key')


repository_address = r'/home/mohsen/git/Human_Factor/Sample_Git_Repository/netty'
issue_json_file_address = r'/home/mohsen/PycharmProjects/PyGithub/Output/netty_bug_fix_issues.json'
result_json_file_address = r'similar_netty_bug_fix_issues.json'

find_similar_commit_message_to_issue_title(issues_json_file_address=issue_json_file_address,
                                           result_issues_json_file_address=result_json_file_address,
                                           repository_file_address=repository_address)

# repo = git.Repo(path=repository_address)
# issue_title = 'Allow to build netty when sun.misc.Unsafe is not avaible or -Dio.nett'
#
# print repo.git.log(all=True,
#                    pretty='format:%H', grep=issue_title)

