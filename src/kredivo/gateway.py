import http
from collections import namedtuple

import requests


class KredivoGateway:
    def __init__(self, server_key, use_sandbox=False):
        self.server_key = server_key
        self.use_sandbox = use_sandbox

    @property
    def base_url(self):
        return "https://sandbox.kredivo.com/kredivo" if self.use_sandbox \
            else "https://api.kredivo.com/kredivo"

    def checkout(self, request_data):
        pass

    def validate(self, request_data):
        pass
