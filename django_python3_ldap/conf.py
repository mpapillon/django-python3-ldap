"""
Settings used by django-python3.
"""

from django.conf import settings
from six.moves import urllib


class LazySetting(object):

    """
    A proxy to a named Django setting.
    """

    def __init__(self, name, default=None):
        self.name = name
        self.default = default

    @classmethod
    def _parse_ldap_url(cls, django_settings):
        url = urllib.parse.urlparse(django_settings.LDAP_URL)

        # Remove query strings.
        path = url.path[1:]
        path = urllib.parse.unquote_plus(path.split('?', 2)[0])

        auth_url = 'ldap://%s:%s' % (url.hostname, url.port)

        return {
            'LDAP_AUTH_URL': auth_url,
            'LDAP_AUTH_CONNECTION_USERNAME': url.username if url.username else '',
            'LDAP_AUTH_CONNECTION_PASSWORD': url.password if url.password else '',
            'LDAP_AUTH_SEARCH_BASE': path,
            'LDAP_AUTH_USE_TLS': url.scheme == "ldaps"
        }

    def __get__(self, obj, cls):
        if obj is None:
            return self

        try:
            return getattr(obj._settings, self.name)
        except AttributeError:
            value = self._parse_ldap_url(obj._settings).get(self.name)
            return value if value else self.default


class LazySettings(object):

    """
    A proxy to ldap-specific django settings.

    Settings are resolved at runtime, allowing tests
    to change settings at runtime.
    """

    def __init__(self, settings):
        self._settings = settings

    LDAP_URL = LazySetting(
        name="LDAP_URL",
        default="ldap://localhost:389",
    )

    LDAP_AUTH_URL = LazySetting(
        name="LDAP_AUTH_URL",
        default="ldap://localhost:389",
    )

    LDAP_AUTH_USE_TLS = LazySetting(
        name="LDAP_AUTH_USE_TLS",
        default=False,
    )

    LDAP_AUTH_SEARCH_BASE = LazySetting(
        name="LDAP_AUTH_SEARCH_BASE",
        default="ou=people,dc=example,dc=com",
    )

    LDAP_AUTH_OBJECT_CLASS = LazySetting(
        name="LDAP_AUTH_OBJECT_CLASS",
        default="inetOrgPerson",
    )

    LDAP_AUTH_USER_FIELDS = LazySetting(
        name="LDAP_AUTH_USER_FIELDS",
        default={
            "username": "uid",
            "first_name": "givenName",
            "last_name": "sn",
            "email": "mail",
        },
    )

    LDAP_AUTH_USER_LOOKUP_FIELDS = LazySetting(
        name="LDAP_AUTH_USER_LOOKUP_FIELDS",
        default=(
            "username",
        ),
    )

    LDAP_AUTH_CLEAN_USER_DATA = LazySetting(
        name="LDAP_AUTH_CLEAN_USER_DATA",
        default="django_python3_ldap.utils.clean_user_data",
    )

    LDAP_AUTH_FORMAT_SEARCH_FILTERS = LazySetting(
        name="LDAP_AUTH_FORMAT_SEARCH_FILTERS",
        default="django_python3_ldap.utils.format_search_filters",
    )

    LDAP_AUTH_SYNC_USER_RELATIONS = LazySetting(
        name="LDAP_AUTH_SYNC_USER_RELATIONS",
        default="django_python3_ldap.utils.sync_user_relations",
    )

    LDAP_AUTH_FORMAT_USERNAME = LazySetting(
        name="LDAP_AUTH_FORMAT_USERNAME",
        default="django_python3_ldap.utils.format_username_openldap",
    )

    LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = LazySetting(
        name="LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN",
        default=None,
    )

    LDAP_AUTH_TEST_USER_USERNAME = LazySetting(
        name="LDAP_AUTH_TEST_USER_USERNAME",
        default="",
    )

    LDAP_AUTH_TEST_USER_PASSWORD = LazySetting(
        name="LDAP_AUTH_TEST_USER_PASSWORD",
        default="",
    )

    LDAP_AUTH_CONNECTION_USERNAME = LazySetting(
        name="LDAP_AUTH_CONNECTION_USERNAME",
        default=None,
    )

    LDAP_AUTH_CONNECTION_PASSWORD = LazySetting(
        name="LDAP_AUTH_CONNECTION_PASSWORD",
        default=None,
    )


settings = LazySettings(settings)
