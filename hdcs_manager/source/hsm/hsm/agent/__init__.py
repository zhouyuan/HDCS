
import logging

from hsm.agent import api as agent_api

LOG = logging.getLogger(__name__)


def API(*args, **kwargs):
    api = agent_api.API
    return api(*args, **kwargs)
