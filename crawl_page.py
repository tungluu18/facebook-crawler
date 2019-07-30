import os
import sys

FB_EMAIL = 'tungcl0n3.1@gmail.com'
FB_PASSWORD = 'tungclone1'
DATE = '2017-01-01'

page = sys.argv[1]
filename = '{}.csv'.format(sys.argv[2])

cmd_crawl_post = 'scrapy crawl fb -a email={} -a password={} -a date={} -a lang=it -a page={} -o pages/{}'.format(
    FB_EMAIL,
    FB_PASSWORD,
    DATE,
    page,
    filename
)
cmd_crawl_reaction = 'scrapy crawl fanpage -a from_file=pages/{filename} -o profiles/url/{filename}'.format(filename=filename)
cmd_crawl_uid = 'scrapy crawl profile -a from_file=profiles/url/{filename} -o profiles/uid/{filename}'.format(filename=filename)

try:
    only = sys.argv[3]
    if only == 'uid':
        cmd = cmd_crawl_uid
    elif only == 'reaction':
        cmd = cmd_crawl_reaction
    elif only == 'post':
        cmd = cmd_crawl_post
    elif only == 'reaction,uid':
        cmd = '{} && {}'.format(cmd_crawl_reaction, cmd_crawl_uid)
    else:
        raise Exception()
except Exception as e:
    cmd = '{} && {} && {}'.format(
        cmd_crawl_post,
        cmd_crawl_reaction,
        cmd_crawl_uid
    )

os.system(cmd)
