# This is xspider
- 支持分布式
- 使用celery消息队列
- TODO


# Debug

from collector.models import Project
from collector.utils import *
project = Project.objects().first()
print project.name

generator = Generator(project)
task = generator.run_generator()

from collector.utils import Processor
baidu = Processor(task)
baidu.run_processor()
