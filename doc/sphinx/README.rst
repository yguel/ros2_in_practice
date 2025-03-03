
=================================
First time for translation setup
=================================

.. code-block:: bash

    # Install sphinx-intl
    pip install sphinx-intl

    # Create gettext files
    make gettext

    # Update gettext files
    sphinx-intl update -p build/gettext -l en_US

Then you have to add the translations in the `source/locales/en_US/LC_MESSAGES/*.po` files.
Then you can build the html files with the following command corresponding to the language you want to build.

.. code-block:: bash
   
    # Build html files for the language en_US in html/en_US
    sphinx-build -b html -D language=fr ./source ./build/html/fr
    sphinx-build -b html -D language=en_US ./source ./build/html/en_US