Django integration
==================

If you are using the SDK in a `Django`_ project, you can add ``kabelwerk`` to
your ``INSTALLED_APPS`` — and the relevant ``KABELWERK_*`` variables in your
Django settings will be picked up by the SDK.

.. code:: python

    # add 'kabelwerk' to your INSTALLED_APPS
    INSTALLED_APPS = [
        # ...
        'kabelwerk',
    ]

    # configure the Kabelwerk SDK
    KABELWERK_URL = 'example.kabelwerk.io'
    KABELWERK_API_TOKEN = '<secret>'

This way you can keep the Kabelwerk SDK config together with the rest of your
settings.


.. _`Django`: https://www.djangoproject.com/
.. _`INSTALLED_APPS`: https://docs.djangoproject.com/en/4.2/ref/settings/#installed-apps
