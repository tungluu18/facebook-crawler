import os
import sys

filename = '{}.csv'.format(sys.argv[1])

cmd = 'scrapy crawl fanpage -a from_file=pages/{filename} -o profiles/url/{filename}\
 && scrapy crawl profile -a from_file=profiles/url/{filename} -o profiles/uid/{filename}'.format(filename=filename)

os.system(cmd)
