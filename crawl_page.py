import os
import sys

filename = '{}.csv'.format(sys.argv[1])

cmd_crawl_reactions = 'scrapy crawl fanpage -a from_file=pages/{filename} -o profiles/url/{filename}'.format(filename=filename)
cmd_crawl_uid = 'scrapy crawl profile -a from_file=profiles/url/{filename} -o profiles/uid/{filename}'.format(filename=filename)

only = sys.argv[2] == 'uid'

if only:
    cmd = cmd_crawl_uid
else:
    cmd = '{} && {}'.format(cmd_crawl_reactions, cmd_crawl_uid)

os.system(cmd)
