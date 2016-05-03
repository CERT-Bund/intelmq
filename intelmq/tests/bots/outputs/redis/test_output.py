# -*- coding: utf-8 -*-

import json
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.outputs.redis.output import RedisOutputBot

import redis

EXAMPLE_EVENT = {"classification.type": "malware",
                 "destination.port": 9796,
                 "feed.accuracy": 100.0,
                 "destination.ip": "52.18.196.169",
                 "malware.name": "salityp2p",
                 "event_description.text": "Sinkhole attempted connection",
                 "time.source": "2016-04-19T23:16:08+00:00",
                 "source.ip": "152.166.119.2",
                 "feed.url": "http://alerts.bitsighttech.com:8080/stream?",
                 "source.geolocation.country": "Dominican Republic",
                 "time.observation": "2016-04-19T23:16:08+00:00",
                 "source.port": 65118,
                 "__type": "Event",
                 "feed.name": "BitSight",
                 "extra.non_ascii": "ççãããã\x80\ua000 \164 \x80\x80 abcd \165\166",
                 "raw": "eyJ0cm9qYW5mYW1pbHkiOiJTYWxpdHlwMnAiLCJlbnYiOnsic"
                 "mVtb3RlX2FkZHIiOiIxNTIuMTY2LjExOS4yIiwicmVtb3RlX3"
                 "BvcnQiOiI2NTExOCIsInNlcnZlcl9hZGRyIjoiNTIuMTguMTk"
                 "2LjE2OSIsInNlcnZlcl9wb3J0IjoiOTc5NiJ9LCJfdHMiOjE0"
                 "NjExMDc3NjgsIl9nZW9fZW52X3JlbW90ZV9hZGRyIjp7ImNvd"
                 "W50cnlfbmFtZSI6IkRvbWluaWNhbiBSZXB1YmxpYyJ9fQ=="
                 }


class TestRedisOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = RedisOutputBot
        cls.default_input_message = EXAMPLE_EVENT

    def test_event(self):
        """ Setup Redis connection """
        redis_ip = test.BOT_CONFIG['redis_server_ip']
        redis_port = test.BOT_CONFIG['redis_server_port']
        redis_db = test.BOT_CONFIG['redis_db']
        redis_queue = test.BOT_CONFIG['redis_queue']
        redis_password = test.BOT_CONFIG['redis_password']
        redis_timeout = test.BOT_CONFIG['redis_timeout']
        redis_conn = redis.ConnectionPool(host=redis_ip, port=redis_port, db=redis_db)
        redis_output = redis.StrictRedis(connection_pool=redis_conn, socket_timeout=redis_timeout, password=redis_password)

        self.run_bot()

        """ Get the message from Redis """
        event = utils.decode(redis_output.lpop(redis_queue))

        """ "assertMessageEqual" """
        self.assertIsInstance(event, str)
        event_dict = json.loads(event)
        self.assertDictEqual(EXAMPLE_EVENT, event_dict)


if __name__ == '__main__':
    unittest.main()