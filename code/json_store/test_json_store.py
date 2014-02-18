#!/bin/env python
import unittest
import sys
from threading import Thread

import json

import requests

from json_store import app



class Server(Thread):

    def __init__(self, httpd):
        self.httpd = httpd
        Thread.__init__(self)

    def run(self):
        self.httpd.serve_forever()


class JSONStoreTest(unittest.TestCase):

    base_url = 'http://localhost:9009/'
    initial_data = {
        "sniffles": [
            {"name": "fred"},
            {"name": "irma"},
            {"name": "wobble"},
        ],
        "snuffle": {"name": "gundar"},
    }

    def setup(self):
        """ test setup, i.e. clear document root """
        requests.put(self.base_url, data='{}')

    def store_initial_document_at_root(self):
        data = json.dumps(self.initial_data)
        requests.put(self.base_url, data=data)

    def test_store_document_at_root(self):
        """ I want to be able to send and store a JSON document at the root
        url. """
        self.store_initial_document_at_root()
        response = requests.get(self.base_url)

        self.assertEqual(
            response.json(),
            self.initial_data
        )

    def test_get_subpart(self):
        """ I want to be able to look at a subpart of the JSON document by
        entering a resource identifier corresponding to the document path. """
        self.store_initial_document_at_root()
        response = requests.get("%ssniffles/" % self.base_url)

        self.assertEqual(
            response.json(),
            self.initial_data['sniffles'],
        )

    def test_modify_subpart_example1(self):
        """ I want to be able to modify parts of the JSON document by sending
        another JSON document to the resource identifier of the document part.
        """

        data = [ {"name": "irma"}, {"name": "wobble"}, ]

        self.store_initial_document_at_root()
        requests.put(
            "%ssniffles/" % self.base_url,
            data=json.dumps(data),
        )

        response = requests.get("%ssniffles/" % self.base_url)

        self.assertEqual(
            response.json(),
            data
        )



    def test_modify_subpart_example2(self):
        """ I want to be able to modify parts of the JSON document by sending
        another JSON document to the resource identifier of the document part.
        """

        self.store_initial_document_at_root()
        requests.put("%ssniffles/0/rank" % self.base_url, data='"sniffle chief"')

        response = requests.get("%ssniffles/0" % self.base_url)

        self.assertEqual(
            response.json(),
            { "name": "fred", "rank": "sniffle chief", },
        )




if __name__ == '__main__':

    from wsgiref.simple_server import make_server
    from wsgiref.simple_server import WSGIRequestHandler


    class SilentHandler(WSGIRequestHandler):
        def log_message(self, format, *args):
            return

    httpd = make_server('', 9009, app, handler_class=SilentHandler)

    server = Server(httpd)
    server.start()

    print "running tests"
    test = unittest.main(
        verbosity=2,
        exit=False
    )

    print "exiting"
    httpd.shutdown()

    if test.result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
