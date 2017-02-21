#!usr/bin/env python
# -*- coding:utf-8 -*-
# Create : 2017.2.20

import os
import datetime
import string
import traceback

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
        help = 'Start a new project for xspider.'

        def add_arguments(self, parser):
            parser.add_argument('projectname', nargs='+', type=str)

        def handle(self, *args, **options):
            for _projectname in options['projectname']:
                try:
                    # print settings.BASE_DIR, settings.PROJECTS_PTAH
                    spider_path = os.path.join(settings.PROJECTS_PTAH, _projectname)
                    if not os.path.exists(spider_path):
                        os.makedirs(spider_path)
                    tmpl_path = os.path.join(settings.BASE_DIR, 'libs', 'template', 'spider.tmpl')
                    with open(tmpl_path, 'rb') as fp:
                        raw = fp.read().decode('utf8')
                    create_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                    content = string.Template(raw).substitute(CREATE_TIME=create_time,
                                                              PROJECTS_NAME=_projectname,
                                                              START_URL='http://www.example.com')
                    spider_file_path = os.path.join(spider_path, '%s_spider.py' % (_projectname))
                    if os.path.exists(spider_file_path):
                        print 'Failed create project %s , file already exists' % (_projectname)
                    else:
                        with open(spider_file_path, 'w') as fp:
                            fp.write(content.encode('utf8'))

                        print 'Successfully create a new project %s '%(_projectname)

                except Exception:
                    print traceback.format_exc()
                    raise CommandError('Failed to create new project %s' % (_projectname))
