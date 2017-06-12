
import logging

from hsm.conductor import api as conductor_api

LOG = logging.getLogger(__name__)


def API(*args, **kwargs):
    api = conductor_api.API
    return api(*args, **kwargs)
