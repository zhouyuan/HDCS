
import logging

from hsm.scheduler import api as scheduler_api

LOG = logging.getLogger(__name__)


def API(*args, **kwargs):
    api = scheduler_api.API
    return api(*args, **kwargs)
