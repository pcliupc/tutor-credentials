Credentials plugin for `Tutor <https://docs.tutor.overhang.io>`__
===================================================================================

This is a plugin for `Tutor <https://docs.tutor.overhang.io>`_ to easily add the credentials service to an Open edX platform. This app allows to award course and program certificates to students (Now it is only used for issuing program certificates officially).

Installation
------------

This plugin requires tutor>=12.0.0.::

    pip install git+https://github.com/pcliupc/tutor-credentials

Usage
-----

::

    tutor plugins enable tutorcredentials

You will have to re-generate the environment::

    tutor config save

The, run migrations::

    tutor local init -l credentials

This last step is unnecessary if you run instead ``tutor local quickstart``.

Operations
----------

Creating a user
~~~~~~~~~~~~~~~

The credentials user interface will be available at http://credentials.local.overhang.io for a local test instance. In order to run commands from the UI, a user must be created::

  tutor local exec credentials ./manage.py createsuperuser

Then, you can login with this user at http://credentials.local.overhang.io/admin.

Pulling catalog from discovery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Credentials service need to pull program and course metadata from discovery before configuring certificates for a program::

    tutor local exec credentials ./manage.py copy_catalog

Creating program certificate configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Program certificate configuration needs to be created before certificates can be awared, and you can do this through credentails admin: http://credentials.local.overhang.io/admin/credentials/programcertificate/ 

Issuing program certificates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Program certificates can be awarded when students have finished all the courses in a program. To enable this, you need to enable credentials api config in lms: http://local.overhang.io/admin/credentials/credentialsapiconfig/.
Awarded programs certificates can be viewed through: http://credentials.local.overhang.io/credentials/{your-certificate-id}/.

Configurations
--------------

- ``CREDENTIALS_MYSQL_PASSWORD`` (default: ``"{{ 8|random_string }}"``)
- ``CREDENTIALS_SECRET_KEY`` (default: ``"{{ 24|random_string }}"``)
- ``CREDENTIALS_OAUTH2_SECRET`` (default: ``"{{ 24|random_string }}"``)
- ``CREDENTIALS_OAUTH2_SECRET_SSO`` (default: ``"{{ 24|random_string }}"``)
- ``CREDENTIALS_DOCKER_IMAGE`` (default: ``"{{ DOCKER_REGISTRY }}overhangio/openedx-credentials:{{ CREDENTIALS_VERSION }}"``)
- ``CREDENTIALS_HOST`` (default: ``"credentials.{{ LMS_HOST }}"``)
- ``CREDENTIALS_MYSQL_DATABASE`` (default: ``"credentials"``)
- ``CREDENTIALS_CACHE_REDIS_DB`` (default: ``"{{ OPENEDX_CACHE_REDIS_DB }}"``)
- ``CREDENTIALS_THEME_NAME`` (default: ``"edx.org"``)

License
-------

This software is licensed under the terms of the AGPLv3.
