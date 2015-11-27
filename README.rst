===============================
CastroRedux
===============================

.. image:: https://img.shields.io/pypi/v/castroredux.svg
        :target: https://pypi.python.org/pypi/castroredux


"screenCAST RObot REDUX" - a tiny fork of vnc2flv

Installation
------------

::

    $ [sudo] easy_install castroredux 

Example
-------

::

        from castroredux import CastroRedux

        c = CastroRedux(
                    'out.flv',
                    host = '192.168.0.12'
                    port = 5900,
                    pwdfile = "/home/user/.vnc/pwd"
            )

        c.start()

        # other stuff

        c.stop()
