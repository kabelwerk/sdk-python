Kabelwerk's SDK for Python
==========================

Welcome to the documentation of the `Kabelwerk`_ SDK for Python!


Installation
------------

The SDK is available at the `Cheese Shop`_:

.. code:: sh

    # usually inside a virtual environment
    pip install kabelwerk

Releases follow semantic versioning. Make sure to check the `CHANGELOG.rst`_
whenever upgrading to a newer version.


Configuration
-------------

You will need:

- The URL of the Kabelwerk backend you will make requests to.
- A valid API token for authenticating the requests.

You can set this in the SDK's config at runtime:

.. code:: python

    import kabelwerk.api
    import kabelwerk.config

    kabelwerk.config.KABELWERK_URL = 'example.kabelwerk.io'
    kabelwerk.config.KABELWERK_API_TOKEN = '<secret>'

    # once the config is set you can use the API functions
    kabelwerk.api.update_user(key='test-1234', name='Test user')

Alternatively, you can set the environment variables ``KABELWERK_URL`` and
``KABELWERK_API_TOKEN`` — these will be read when you first import the SDK.


Reference
---------

.. toctree::
    :maxdepth: 2

    api
    exceptions


.. _`Kabelwerk`: https://kabelwerk.io
.. _`Cheese Shop`: https://pypi.org/project/kabelwerk/
.. _`CHANGELOG.rst`: https://github.com/kabelwerk/sdk-python/blob/master/CHANGELOG.rst
