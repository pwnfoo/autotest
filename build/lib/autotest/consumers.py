# -*- coding: utf-8 -*-
# This file is part of simple-koji-ci project.
#
# simple_koji_ci is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# simple_koji_ci is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with simple_koji_ci.  If not, see <http://www.gnu.org/licenses/>.
"""
Fedmsg consumers that listen to various topics listed below.

Authors:    Ralph Bean <rbean@redhat.com>
            Pierre-Yves Chibon <pingou@pingoured.fr>
            Sachin S Kamath <skamath@redhat.com>

"""

import logging
import uuid

from requests.packages.urllib3.util import retry
import fedmsg
import fedmsg.consumers
import requests
import time
from termcolor import colored

from autotest import __version__


_log = logging.getLogger(__name__)




class Autotest(fedmsg.consumers.FedmsgConsumer):
    """
    The heart and soul of the package. This is the fedmsg consumer class
    that listens to topics mentioned in the topic list below.


    """

    # We can do multiple topics like this as of moksha.hub-1.4.4
    # https://github.com/mokshaproject/moksha/pull/25
    topic = [
        # New pull-request coming in
        'org.fedoraproject.stg.pagure.pull-request.new',
        'org.fedoraproject.prod.pagure.pull-request.new',
        'org.fedoraproject.prod.irc.karma',
        'org.fedoraproject.prod.wiki.article.edit',
    ]

    config_key = 'autotest.enabled'

    def __init__(self, hub):

        # If we're in development mode, rewrite some of our topics so that
        # local playback with fedmsg-dg-replay works as expected.
        if hub.config['environment'] == 'dev':
            # Keep the original set, but append a duplicate set for local work
            prefix, env = hub.config['topic_prefix'], hub.config['environment']
            self.topic = self.topic + [
                '.'.join([prefix, env] + topic.split('.')[3:])
                for topic in self.topic
            ]

        super(Autotest, self).__init__(hub)

        if not self._initialized:
            return

        # This is just convenient.
        self.config = self.hub.config

        _log.info("Autotest is all initialized")

    def consume(self, msg):
        """
        Called when a message arrives on the fedmsg bus.
        """
        print("HERE!!!!")
        topic, msg = msg['topic'], msg['body']
        if topic.endswith('irc.karma'):
            self.handle_karma(msg)
        else:
            _log.debug("Dropping %r %r" % (topic, msg['msg_id']))
            pass


    def handle_karma(self, msg):
        """
        Example message handler for handling karma

        Topic : ``org.fedoraproject.prod.irc.karma``

        Sample JSON
        ===========
        {
          "username": "daemon",
          "source_name": "datanommer",
          "certificate": xxxx,
          "i": 2178,
          "timestamp": 1518416468.0,
          "msg_id": "2018-4a937073-ae6a-4646-8e4d-5b8b8379dd84",
          "crypto": "x509",
          "topic": "org.fedoraproject.prod.irc.karma",
          "headers": {},
          "signature": xxxx,
          "source_version": "0.8.2",
          "msg": {
            "total_this_release": 8,
            "agent": "skamath",
            "vote": 1,
            "release": "f27",
            "line": "robyduck++",
            "total": 108,
            "recipient": "robyduck",
            "channel": "#fedora-ambassadors"
          }
        }

        """

        _log.info("Received a karma activity!")

        receiver = colored(msg['msg']['recipient'], 'green')
        giver = colored(msg['msg']['agent'], 'yellow')
        irc_line = colored(msg['msg']['line'], 'blue')
        readable_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                        time.localtime(msg['timestamp']))
        _log.info("On %s, %s gave %s a karma cookie by saying %s" %(
                    readable_time, giver, receiver, irc_line)
                    )


    def handle_pagure_new_pr(self, msg):
        """
        Message handler for new pull-request opened in pagure.

        Topic: ``org.fedoraproject.pagure.pull-request.new``

        """
        _log.info("Handling pagure msg %r" % msg.get('msg_id', None))

        prid = msg['msg']['pullrequest']['id']
        package = msg['msg']['pullrequest']['project']['name']
        namespace = msg['msg']['pullrequest']['project']['namespace']
        branch_to = msg['msg']['pullrequest']['branch']

        print(package)
