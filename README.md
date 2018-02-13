# Autotest

[Fedmsg](http://fedmsg.com) consumer that listens to fedmsg and automates tests.

Set up your environment with:

    $ virtualenv my-env --system-site-packages
    $ source my-env/bin/activate

    $ python setup.py develop
    $ python setup.py build


And then run it with::

    $ fedmsg-hub

It should pick up the autotest consumer and start running.


### Hacking

0. Create a virtualenv, then install deps and itself with `python setup.py develop`
1. Can you run it?  Try running `PYTHONPATH=. fedmsg-hub` in your virtualenv.
   Does it look like it starts without tracebacks?
2. In another terminal run `fedmsg-tail --really-pretty`.  It should start up
