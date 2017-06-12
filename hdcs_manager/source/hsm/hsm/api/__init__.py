
import paste.urlmap

from hsm import flags

FLAGS = flags.FLAGS


def root_app_factory(loader, global_conf, **local_conf):
    if not FLAGS.enable_v1_api:
        del local_conf['/v1']
    return paste.urlmap.urlmap_factory(loader, global_conf, **local_conf)
