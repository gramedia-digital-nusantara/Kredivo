import http
import json
from enum import Enum

import requests
from requests import HTTPError

from kredivo.models import SerializableMixin, KredivoTransactionResponse


class KredivoGateway:
    def __init__(self, server_key, use_sandbox=False):
        self.server_key = server_key
        self.use_sandbox = use_sandbox

    @property
    def base_url(self):
        return "https://sandbox.kredivo.com/kredivo" if self.use_sandbox \
            else "https://api.kredivo.com/kredivo"

    def checkout(self, request_data):
        response = requests.post(url=f"{self.base_url}/v2/checkout_url",
                                 data=self.build_checkout_request_body(request_data),
                                 headers=self._build_headers())

        if response.status_code != http.HTTPStatus.OK:
            raise KredivoUnexpectedError(response.status_code)
        elif 'error' in response.json():
            raise KredivoCheckoutError(**response.json()['error'])

        return KredivoCheckoutResponse.from_json(response)

    def validate(self, request_data):
        pass

    @staticmethod
    def _build_headers():
        return {'Content-Type': 'application/json', 'Accept': 'application/json', 'cache-control': "no-cache"}

    def build_checkout_request_body(self, request_data):
        request_body = request_data
        request_body['payment_type'] = '30_days'
        request_body['server_key'] = self.server_key
        return json.dumps(request_body)

    def get_payment_status(self, transaction_id, signature_key):
        """
        :param `six.string_types` transaction_id: Transaction Id given by Kredivo
        :param `six.string_types` signature_key: Signature key to validate if the notification is originated from Kredivo
        :return:
        """
        response = requests.get(
            url=f"{self.base_url}/v2/update?transaction_id={transaction_id}&signature_key={signature_key}",
            headers=self._build_headers())

        if response.status_code != http.HTTPStatus.OK:
            raise HTTPError

        return KredivoConfirmResponse.from_json(response)

    def transaction_status(self, order_id):
        body = {
            "server_key": self.server_key,
            "order_id": order_id
        }
        response = requests.post(
            url=f"{self.base_url}/v2/transaction/status",
            data=json.dumps(body),
            headers=self._build_headers()
        )

        return KredivoTransactionResponse(response)

    def _confirm_push_notification(self):
        pass


class KredivoCheckoutError(Exception):
    def __init__(self, message, kind, **kwargs):
        self.message = message if len(message) else "An unknown error occurred"
        self.kind = kind
        self.additional_error_attrs = kwargs

    def __str__(self):
        return "<KredivoCheckoutError(message={message}, kind={kind})>".format(**vars(self))


class KredivoUnexpectedError(Exception):
    def __init__(self, status_code, **kwargs):
        self.message = "Kredivo doesn't response our checkout request"
        self.status_code = status_code

    def __str__(self):
        return "<KredivoUnexpectedError(message={message}, status_code={status_code})>".format(**vars(self))


class KredivoStatus(Enum):
    ok = "OK"
    error = "ERROR"


class KredivoTransactionStatus(Enum):
    """
    Transaction status of a transaction, the values is:
    CAPTURE: Transaction has been captured
    SETTLEMENT: Transaction has been settled
    PENDING: Transaction has not been completed
    DENY: Transaction has been denied
    CANCEL: Transaction has been cancelled
    EXPIRE: Transaction has been expired
    """
    capture = "CAPTURE"
    settlement = "SETTLEMENT"
    pending = "PENDING"
    deny = "DENY"
    cancel = "CANCEL"
    expire = "EXPIRE"


class KredivoFraudStatus(Enum):
    """
    Detection result by Fraud Detection System (FDS), the values is:
    ACCEPT: Approved by FDS
    DENY: Denied by FDS. Transaction automatically failed
    """
    accept = "ACCEPT"
    deny = "DENY"


class KredivoCheckoutResponse(object):
    def __init__(self, status=None, message=None, redirect_url=None, **kwargs):
        """
        :param `KredivoStatus` status:
        :param `six.string_types` message:
        :param `six.string_types` redirect_url:
        """
        self.status = status
        self.message = message
        self.redirect_url = redirect_url

    @classmethod
    def from_json(cls, api_response):
        """
        :param `requests.Response` api_response:
        """
        resp_json = api_response.json()
        status = KredivoStatus(resp_json.pop('status'))
        return cls(status=status, **resp_json)


class KredivoConfirmResponse(SerializableMixin):

    def __init__(self, status=None, message=None, payment_type=None,
                 transaction_id=None, transaction_status=None,
                 transaction_time=None, order_id=None, amount=None,
                 fraud_status=None, **kwargs):
        """
        :param `six.string_types` status:
        :param `six.string_types` message:
        :param `six.string_types` payment_type:
        :param `six.string_types` transaction_id:
        :param `six.string_types` transaction_status:
        :param `int` transaction_time: UNIX timestamp (epoch)
        :param `int` order_id:
        :param `six.string_types` amount:
        :param `six.string_types` fraud_status:
        """
        self.status = status
        self.message = message
        self.payment_type = payment_type
        self.transaction_id = transaction_id
        self.transaction_status = transaction_status
        self.transaction_time = transaction_time
        self.order_id = order_id
        self.amount = amount
        self.fraud_status = fraud_status

    @classmethod
    def from_json(cls, api_response):
        return cls(**api_response.json())
