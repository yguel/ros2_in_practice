
=================================
First time for translation setup
=================================

.. code-block:: bash

    # Install sphinx-intl
    pip install sphinx-intl

    # Create gettext files
    make gettext

    # Update gettext files
    sphinx-build -b gettext source build/gettext

    # Update all po files
    sphinx-intl update -p build/gettext -d source/locales


==================================
Update translation files
==================================

.. code-block:: bash

    # Update gettext files
    sphinx-build -b gettext source build/gettext

    # Update all po files
    sphinx-intl update -p build/gettext -d source/locales


Then you have to add the translations in the `source/locales/en_US/LC_MESSAGES/*.po` files.
Then you can build the html files with the following command corresponding to the language you want to build.

.. code-block:: bash
   
    # Build html files for the language en in html/en
    sphinx-build -b html -D language=fr ./source ./build/html/humble/fr
    sphinx-build -b html -D language=en ./source ./build/html/humble/en