#!usr/bin/env python
# -*- coding:utf-8 -*-
# Create on 2017.2.23

import json
import redis
from collector.models import Project
from django.conf import settings


class Manager (object):

    def __init__(self, ip='127.0.0.1', project_name=None):
        """
        :param ip:
        :param project_name:
        """
        self.ip = ip
        self.project_name = project_name
        self.redis_r = redis.Redis(self.REDIS_POOL)

    def _add_local_ip_record(reference_dict=None):
        if not reference_dict is None:
            reference_dict.update{
                self.ip: {
                "add_time": datetime.now(),
                "last_used_time": datetime.now(),
                "used_num": 1,
                }
            }
        if self.r.get(self.project_name):
            self.r.delete(self.project_name)
            self.r.set(self.project_name, json.dumps(reference_dict))
            self.r.save()
        else:
            self.r.set(self.project_name, json.dumps(reference_dict))

    def _update_proxies_ip_record(selfreference_dict=None):
        if not selfreference_dict is None:
            self.r.delete(self.project_name)
            self.r.set(self.project_name, json.dumps(selfreference_dict))
            self.r.save()

    def _is_the_first_local_ip_can_use(self, target_dict=None, reference_dict=None):
            downloader_interval = float(target_dict.get('downloader_interval', 10.0))
            last_used_time = float(reference_dict.get(self.ip).get('last_used_time'))
            now_time = float(self._get_now_timestamp())
            if last_used_time + downloader_interval <= now_time:
                return True, self.ip
            else:
                return False, '0.0.0.0'

    def _is_the_proxies_ip_can_use(self, target_dict=None, reference_dict=None):
        downloader_interval = float(target_dict.get('downloader_interval', 10.0))
        now_time = float(self._get_now_timestamp())
        for key, value in reference_dict.items():
            last_used_time = float(value.get('last_used_time'))
            if last_used_time + downloader_interval <= now_time:
                is_granted, ip_port =  True, key
                value.update({
                    'last_used_time': now_time,
                    'used_num': int(value.get('used_num')) + 1
                    })
                break
        else:
            is_granted, ip_port, = False, None
        if is_granted:
            self._update_proxies_ip_record(reference_dict=reference_dict)
        return is_granted, ip_port

    def _do_alanysis_with_redis(self, target_dict=None, reference_dict=None):
        """
        :param target_dict:
        :param reference_dict:
        :return: a_json_str
        """

        first_local_ip = reference_dict.get(self.ip)
        if first_local_ip:
            is_granted, ip_port = _is_the_first_local_ip_can_use(target_dict, reference_dict)
            if not is_granted:
                is_granted, ip_port = _is_the_proxies_ip_can_use(target_dict, reference_dict)
        else:
            self._add_local_ip_record(reference_dict=reference_dict)
            is_granted = True
            ip_port = self.ip

        return json.dump({
            'is_granted': is_granted,
            'local_ip': self.ip,
            'proxies_ip': ip_port,
            'count': 1
        })

    def _get_target_dict(self):
        """
        :return: a_dict
        """

        try:
            one_project = Project.objects.filter(name=self.project_name).first()
            print 'one_project.name: ', one_project.name
        except Exception as e:
            print (u'数据库查询出错了, %s project可能并不存在mongodb。' % (self.project_name))
            raise e
        if one_project is None:
            print (u'数据库查询出错了, %s project可能并不存在mongodb。' % (self.project_name))
            raise ValueError

        target_dict = {
            'name': one_project.name,
            'ip': self.ip,
            'generator_interval': one_project.generator_interval,
            'downloader_interval': one_project.downloader_interval,
            'downloader_dispatch': one_project.downloader_dispatch
        }
        return target_dict

    def _get_reference_dict(self):
        """
        :return: a_dict
        """
        reference_str = self.redis_r.get(self.project_name)
        if reference_str is None:
            return {}
        reference_dict = json.loads(reference_str)
        return reference_dict

    def get_ip(self):
        """
        :return: str that json.dump
        """
        # TODO:
            # 与 redis里的ip使用情况作对比

        target_dict = self._get_target_dict()
        reference_dict = self._get_reference_dict()
        result = self._do_alanysis_with_redis(reference_dict=reference_dict,
                                             target_dict=target_dict)
        return result

