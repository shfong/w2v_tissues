==========================================================
w2v_tissues
==========================================================


.. image:: https://img.shields.io/pypi/v/w2v_tissues.svg
        :target: https://pypi.python.org/pypi/w2v_tissues

.. image:: https://img.shields.io/travis/shfong/w2v_tissues.svg
        :target: https://travis-ci.org/shfong/w2v_tissues




WordToVectorTissues REST Server

`For more information please click here to visit our wiki <https://github.com/shfong/w2v_tissues/wiki>`_


Compatibility
-------------

 * Tested with Python 3.6 in Anaconda_

Dependencies to run
-------------------

 * `flask <https://pypi.org/project/flask/>`_
 * `flask-restplus <https://pypi.org/project/flast-restplus>`_

Additional dependencies to build
--------------------------------

 * GNU make
 * `wheel <https://pypi.org/project/wheel/>`_
 * `setuptools <https://pypi.org/project/setuptools/>`_
 

Installation
------------

It is highly reccommended one use `Anaconda <https://www.anaconda.com/>`_ for Python environment

.. code:: bash

  git clone https://github.com/shfong/w2v_tissues.git
  cd w2v_tissues
  make install

Running service in development mode
-----------------------------------


**NOTE:** Example below runs the REST service and not the task runner.

.. code:: bash

  # It is assumed the application has been installed as described above
  export FLASK_APP=w2v_tissues
  flask run # --host=0.0.0.0 can be added to allow all access from interfaces
  
  # Service will be running on http://localhost:5000


Example usage of service
------------------------

TODO

.. code:: bash
   
    TODO

Bugs
-----

Please report them `here <https://github.com/shfong/w2v_tissues/issues>`_

Acknowledgements
----------------


* Initial template created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _Anaconda: https://www.anaconda.com/
