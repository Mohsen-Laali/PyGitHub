import numbers
from github.GithubObject import NotSet
from github.Label import Label
from github import Github
from ssl import SSLError,SSL_ERROR_EOF

# try:
#     raise SSLError
# except SSLError as e:
#     print(e.message)
#     print('********')
#     print(e.filename)
#     print('++++++++')
#     print(e.strerror)
ttt = []
if not ttt:
    print 'hi'
else:
    print 'niiii'

raw_input('press any key')

te = 'teretet'
print te.title()
print te
# import csv
#
# with open("t.csv", "w+") as cvs_file:
#     header = ['a', 'b']
#     writer = csv.DictWriter(cvs_file, header)
#     dictionary = {'a': 1, 'b': 2}
#     writer.writeheader()
#     writer.writerow(dictionary)
#     reader = csv.DictReader(cvs_file)
#
# raw_input('press any key')
# XXX: Specify your own access token here

# ACCESS_TOKEN = 'ff1ba45dc52ef7c142eb56c1e1671225c2b27f15'
g = Github("M3N", "GitHub1")

# for repo in g.get_user().get_repos():
#     print repo.name
# USER = 'ptwobrussell'
# REPO = 'Mining-the-Social-Web'
#
# user = g.get_user(USER)
#
# repo = user.get_repo(REPO)
#
# print repo.clone_url


# repo = g.get_repo('spring-projects/spring-boot')
# bug_label = repo.get_label('type: bug ')

repo = g.get_repo('netty/netty')
bug_label = repo.get_label('type: bug ')

# filter_ = 'UnableToRegisterMBeanException with Actuator 1.5.1'
issue_number = 694
# paginated_list_issues = repo.get_issues(filter=filter_)
paginated_list_issues = repo.get_issues(state='closed', labels=[bug_label])
# paginated_list_issues = repo.get_issues(state='closed')


issue_ = repo.get_issue(number=issue_number)
issue_
print 'title'
print issue_.title
print 'id'
print issue_.id
print 'number'
print issue_.number
print 'body'
print issue_.body
print 'comment'
print issue_.comments
print 'comment url'
print issue_.comments_url
print 'event url'
print issue_.events_url
print 'labels'
print issue_.labels
print 'label url'
print issue_.labels_url

issue_events = issue_.get_events()
for issue_event in issue_events:
    print 'actor:'
    print issue_event.actor
    print 'commit id'
    print issue_event.commit_id
    print 'event'
    print issue_event.event
    print 'id'
    print issue_event.id
    print 'issue'
    print issue_event.issue
    print 'url'
    print issue_event.url
    if issue_event.event == 'closed' and issue_event.commit_id:
        print '###########Closed################'
        print issue_event.commit_id.encode('utf-8')
    elif issue_event.event == 'closed':
        print '************notCommit************'
    raw_input('press any key')


raw_input('press any key')
# number = 1
# for issue in paginated_list_issues:
#     print str(number) + ' #' + issue.title
#     number += 1
# raw_input('press any key')
# issue = g.search_issues('', NotSet, 'asc', repo='elastic/elasticsearch', label='bug', state='closed')
# issue_page_0 = issue.get_page(0)

for issue in paginated_list_issues:
    print 'issue title: ' + issue.title
    repository = issue.repository
    print 'repository name: ' + repository.full_name
    numberOfComment = issue.comments
    print '+++++++++'
    issue_labels = issue.get_labels()

    for label in issue_labels:
        print 'label: ' + str(label.name)
        # raw_input('press any key')

    issue_pull_request = issue.pull_request
    if issue_pull_request is not None:
        print '*********'
        print 'issue pull request'
        print 'diff url ' + issue_pull_request.diff_url
        print 'html_url ' + issue_pull_request.html_url
        print 'patch_url ' + issue_pull_request.patch_url
        print '*********'

    issue_events = issue.get_events()

    issue_events_page_0 = issue_events.get_page(0)

    print '&&&&&&&&&'
    for issue_event in issue_events:
        print 'Commit ID ' + str(issue_event.commit_id)
        print 'Event ' + issue_event.event
        print 'Event url ' + issue_event.url
        # raw_input('press any key')
    print '&&&&&&&&&'
    print '--------'
    print 'number of comments ' + str(numberOfComment)

    comments = issue.get_comments()
    comments_page_0 = comments.get_page(0)

    for issue_comment in comments_page_0:
        print
        print issue_comment.body
        print '--------'
        # raw_input('Press any key')
    print '+++++++++'

# g.legacy_search_repos()

# stargazers = [s for s in repo.get_stargazers()]
# print 'Number of stargazers', len(stargazers)
