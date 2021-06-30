from glob import glob
import os
import pkg_resources

from .__about__ import __version__

HERE = os.path.abspath(os.path.dirname(__file__))

templates = os.path.join(HERE, "templates")

config = {
   "add": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 20|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "OAUTH2_SECRET_SSO": "{{ 8|random_string }}",
    },
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY}}overhangio/openedx-credentials:{{ CREDENTIALS_VERSION }}",
        "HOST": "credentials.{{ LMS_HOST }}",
        "MYSQL_DATABASE": "credentials",
        "MYSQL_USERNAME": "credentials",
        "OAUTH2_KEY": "credentials",
        "OAUTH2_KEY_DEV": "credentials-dev",
        "OAUTH2_KEY_SSO": "credentials-sso",
        "OAUTH2_KEY_SSO_DEV": "credentials-sso-dev",
        "CACHE_REDIS_DB": "{{ OPENEDX_CACHE_REDIS_DB }}",
        "THEME_NAME": "edx.org",
    },
}

hooks = {
    "build-image": {"credentials": "{{ CREDENTIALS_DOCKER_IMAGE }}"},
    "remote-image": {"credentials": "{{ CREDENTIALS_DOCKER_IMAGE }}"},
    "init": ["mysql", "lms", "credentials"],
}


def patches():
    all_patches = {}
    for path in glob(os.path.join(HERE, "patches", "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
