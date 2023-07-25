=================
How to contribute
=================

- `Submitting bug reports`_
- `Contributing code`_


Submitting bug reports
======================

If you want to report a bug you can use the repository's `issue tracker`_ or
you can contact us directly by email; the latter should be preferred if you
want to report a security vulnerability.


Contributing code
=================

.. code:: sh

    # clone the repo
    git clone https://github.com/kabelwerk/sdk-python
    cd sdk-python

    # create a virtual env
    # the venv dir is git-ignored
    python3 -m venv venv
    source venv/bin/activate

    # install the dependencies
    # you can also pip install -r requirements.txt
    pip install pip-tools
    pip-sync

    # run the unit tests
    pytest


Conventions
-----------

For file encoding, newlines, indentation: please use the ``.editorconfig``
rules (`take a look here`_ if this is new for you).

For coding style: please follow `PEP8`_.


.. _`issue tracker`: https://github.com/kabelwerk/sdk-python/issues

.. _`take a look here`: https://editorconfig.org/
.. _`PEP8`: https://www.python.org/dev/peps/pep-0008/
