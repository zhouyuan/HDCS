
import os

import diamond.collector

import redis

class HyperstashCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(HyperstashCollector,
                            self).get_default_config_help()
        config_help.update({
            'redis_host': 'The host to connect redis',
            'redis_port': 'The port of redis',
            'redis_db': 'The db of redis to fetch data',
            'hyperstash_metrics': 'The monitoring metrics of hyperstash'
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """

        config = super(HyperstashCollector, self).get_default_config()
        config.update({
            'redis_host': 'localhost',
            'redis_port': '6379',
            'redis_db': '0',
            'hs_metrics': 'cache_total_size,'
                          'cache_used_size,'
                          'cache_dirty_size,'
                          'cache_promote,'
                          'cache_flush,'
                          'cache_evict,'
                          'cache_read,'
                          'cache_read_miss,'
                          'cache_write,'
                          'cache_write_miss,'
                          'cache_bw,'
                          'cache_latency',
        })
        return config

    def _get_rbd_list(self):
        general_conf = "/etc/rbc/general.conf"
        rbd_list = []
        if os.path.exists(general_conf):
            file_obj = open(general_conf)
            for line in file_obj.readlines():
                line = line.strip("\n")
                if line.startswith("[") and line != "[global]":
                    rbd_name = line.lstrip("[").rstrip("]")
                    rbd_list.append(rbd_name)
        return rbd_list

    def collect(self):
        rbd_list = self._get_rbd_list()
        self.log.debug("==========rbd_list: %s" % str(rbd_list))
        self.log.debug("==========host: %s" % str(self.config['redis_host']))
        self.log.debug("==========redis_port: %s" % str(self.config['redis_port']))
        self.log.debug("==========redis_db: %s" % str(self.config['redis_db']))
        self.log.debug("==========hs_metrics: %s" % str(self.config['hs_metrics']))

        r = redis.StrictRedis(host=self.config['redis_host'],
                              port=int(self.config['redis_port']),
                              db=int(self.config['redis_db']))
        hs_metrics = self.config['hs_metrics']
        hs_metrics_list = hs_metrics.split(',')
        for rbd in rbd_list:
            for metric in hs_metrics_list:
                metric = metric.strip(" ")
                new_metric = rbd + "_" + metric
                m_value = r.get(new_metric)
                try:
                    self.publish(new_metric, m_value)
                except:
                    self.publish(new_metric, 0)
        return
