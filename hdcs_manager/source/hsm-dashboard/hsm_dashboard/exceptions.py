
from hsmclient import exceptions as hsmclient
from keystoneclient import exceptions as keystoneclient

UNAUTHORIZED = (keystoneclient.Unauthorized,
                keystoneclient.Forbidden,
                hsmclient.Unauthorized,
                hsmclient.Forbidden)

NOT_FOUND = (keystoneclient.NotFound,
             hsmclient.NotFound)

# NOTE(gabriel): This is very broad, and may need to be dialed in.
RECOVERABLE = (keystoneclient.ClientException,
               # AuthorizationFailure is raised when Keystone is "unavailable".
               keystoneclient.AuthorizationFailure,
               hsmclient.ClientException)
