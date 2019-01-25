import http
import json
from enum import Enum

import requests
from requests import HTTPError

from kredivo.models import SerializableMixin, KredivoTransactionResponse, CancelPurcaseResponse


class KredivoGateway:
    """

    """
    def __init__(self, server_key, use_sandbox=False):
        self.server_key = server_key
        self.use_sandbox = use_sandbox

    @property
    def base_url(self):
        """

        :return: `str` Kredivo URL SANDBOX or PRODUCTION
        """
        return "https://sandbox.kredivo.com/kredivo" if self.use_sandbox \
            else "https://api.kredivo.com/kredivo"

    def checkout(self, request_data):
        """

        :param `dict` request_data:
        :return: `objec` KredivoCheckoutResponse
        """
        response = requests.post(url=f"{self.base_url}/v2/checkout_url",
                                 data=self.build_checkout_request_body(request_data),
                                 headers=self._build_headers())

        if response.status_code != http.HTTPStatus.OK:
            raise KredivoUnexpectedError(response.status_code, **response.json())
        elif 'error' in response.json():
            raise KredivoCheckoutError(**response.json()['error'])

        return KredivoCheckoutResponse.from_json(response)

    @staticmethod
    def _build_headers():
        return {'Content-Type': 'application/json', 'Accept': 'application/json', 'cache-control': "no-cache"}

    def build_checkout_request_body(self, request_data):
        request_body = request_data
        request_body['payment_type'] = '30_days'
        request_body['server_key'] = self.server_key
        return json.dumps(request_body)

    def check_payment_status(self, transaction_id, signature_key):
        """
        Validate(Confirm) Order to Kredivo API make sure they have our Order
        :param `six.string_types` transaction_id: Transaction Id given by Kredivo
        :param `six.string_types` signature_key: Signature key to validate if the notification is originated from Kredivo
        :return:
        """
        response = requests.get(
            url=f"{self.base_url}/v2/update?transaction_id={transaction_id}&signature_key={signature_key}",
            headers=self._build_headers())

        if response.status_code != http.HTTPStatus.OK:
            raise HTTPError

        return KredivoPaymentStatusResponse(response)

    def transaction_status(self, order_id):
        """
        get status from Kredivo API
        :param `int` order_id:  merchant order id
        :return: `object` KredivoTransactionResponse
        """
        body = {
            "server_key": self.server_key,
            "order_id": order_id
        }
        response = requests.post(
            url=f"{self.base_url}/v2/transaction/status",
            data=json.dumps(body),
            headers=self._build_headers()
        )

        if response.status_code != http.HTTPStatus.OK:
            raise HTTPError

        return KredivoTransactionResponse(response)

    def _confirm_push_notification(self):
        pass

    def cancel_transaction(self, order_id, transaction_id, cancellation_reason,
                           cancelled_by, cancellaction_date, cancellation_amount=None):
        body = {
            "server_key": self.server_key,
            "order_id": order_id,
            "transaction_id": transaction_id,
            "cancellation_reason": cancellation_reason,
            "cancelled_by": cancelled_by,
            "cancellaction_date": cancellaction_date
        }

        if cancellation_amount:
            body["cancellation_amount"] = cancellation_amount

        response = requests.post(
            url=f"{self.base_url}/v2/cancel_transaction",
            data=json.dumps(body),
            headers=self._build_headers()
        )

        if response.json().get('status') == KredivoStatus.ERROR.name:
            return KredivoCancelOrderException(response.json())

        return CancelPurcaseResponse(response)


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


class KredivoCancelOrderException(Exception):

    def __init__(self, json_response, **kwargs):
        if json_response.get("error"):
            self.message = json_response.get("error").get("message")
        else:
            self.message = json_response.get("message")
        self.status = json_response.get("status")

    def __str__(self):
        return "<KredivoCancelOrderException(message={message}, kind={kind})>".format(**vars(self))


class KredivoStatus(Enum):
    OK = "OK"
    ERROR = "ERROR"


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


class KredivoPaymentStatusResponse(SerializableMixin):
    __fields__ = ["status", "legal_name", "fraud_status", "order_id", "transaction_time",
                 "amount", "payment_type", "transaction_status", "message", "transaction_id"]
