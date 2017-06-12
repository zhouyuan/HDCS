# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Hsm base exception handling.

Includes decorator for re-raising Hsm-type exceptions.

SHOULD include dedicated exception logging.

"""

from oslo_config import cfg
import webob.exc

from hsm import flags
from hsm.openstack.common import log as logging

LOG = logging.getLogger(__name__)

exc_log_opts = [
    cfg.BoolOpt('fatal_exception_format_errors',
                default=False,
                help='make exception message format errors fatal'),
]

FLAGS = flags.FLAGS
FLAGS.register_opts(exc_log_opts)

class ConvertedException(webob.exc.WSGIHTTPException):
    def __init__(self, code=0, title="", explanation=""):
        self.code = code
        self.title = title
        self.explanation = explanation
        super(ConvertedException, self).__init__()

class ProcessExecutionError(IOError):
    def __init__(self, stdout=None, stderr=None, exit_code=None, cmd=None,
                 description=None):
        self.exit_code = exit_code
        self.stderr = stderr
        self.stdout = stdout
        self.cmd = cmd
        self.description = description

        if description is None:
            description = 'Unexpected error while running command.'
        if exit_code is None:
            exit_code = '-'
        message = '%(description)s\nCommand: %(cmd)s\n' \
                  'Exit code: %(exit_code)s\nStdout: %(stdout)r\n' \
                  'Stderr: %(stderr)r' % locals()
        IOError.__init__(self, message)

class Error(Exception):
    pass

class DBError(Error):
    code="E-5081"
    """Wraps an implementation specific exception."""
    def __init__(self, inner_exception=None):
        self.inner_exception = inner_exception
        super(DBError, self).__init__(str(inner_exception))

def wrap_db_error(f):
    def _wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except UnicodeEncodeError:
            raise InvalidUnicodeParameter()
        except Exception, e:
            LOG.exception('DB exception wrapped.')
            raise DBError(e)
    _wrap.func_name = f.func_name
    return _wrap

class HsmException(Exception):
    """Base Hsm Exception

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.

    """
    message = "An unknown exception occurred."
    code = 500
    headers = {}
    safe = False

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if not message:
            try:
                message = self.message % kwargs

            except Exception as e:
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs
                LOG.exception('Exception in string format operation')
                for name, value in kwargs.iteritems():
                    LOG.error("%s: %s" % (name, value))
                if FLAGS.fatal_exception_format_errors:
                    raise e
                else:
                    # at least get the core message out if something happened
                    message = self.message

        super(HsmException, self).__init__(message)

class NotAuthorized(HsmException):
    message = "Not authorized."
    code = 403

class AdminRequired(NotAuthorized):
    code = "E-8849"
    message = "User does not have admin privileges"

class PolicyNotAuthorized(NotAuthorized):
    message = "Policy doesn't allow %(action)s to be performed."

class Invalid(HsmException):
    message = "Unacceptable parameters."
    code = 400

class InvalidInput(Invalid):
    message = "Invalid input received" + ": %(reason)s"

class InvalidContentType(Invalid):
    message = "Invalid content type %(content_type)s."

class InvalidUnicodeParameter(Invalid):
    message = "Invalid Parameter: " \
              "Unicode is not supported by the current database."

class NotFound(HsmException):
    message = "Resource could not be found."
    code = 404
    safe = True

class ServiceNotFound(NotFound):
    code = "E-F158"
    message = "Service %(service_id)s could not be found."

class HostBinaryNotFound(NotFound):
    message = "Could not find binary %(binary)s on host %(host)s."

class FileNotFound(NotFound):
    code = "E-D55E"
    message = "File %(file_path)s could not be found."

class Duplicate(HsmException):
    pass

class MalformedRequestBody(HsmException):
    message = "Malformed message body: %(reason)s"

class ConfigNotFound(NotFound):
    code = "E-89AF"
    message = "Could not find config at %(path)s"

class PasteAppNotFound(NotFound):
    message = "Could not load paste app '%(name)s' from %(path)s"

class StatusTrackingError(HsmException):
    message = 'Status traceking Error.'


####################
# Server    E-0AXXX
####################
class ServerNotFound(NotFound):
    code = "E-0A001"
    message = "Server %(server_id)s could not be found."

####################
# Hs_Instance    E-0BXXX
####################
class HsInstanceNotFound(NotFound):
    code = "E-0B001"
    message = "Hyperstash Instance %(hs_instance_id)s could not be found."

####################
# RBD    E-0CXXX
####################
class RbdNotFound(NotFound):
    code = "E-0C001"
    message = "RBD %(rbd_id)s could not be found."

####################
# RBD Cache Config    E-0DXXX
####################
class RbdCacheConfigNotFound(NotFound):
    code = "E-0D001"
    message = "RBD Cache Config %(rbd_cache_config_id)s could not be found."


