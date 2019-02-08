import http
import json

import requests
from requests import HTTPError

from kredivo.exceptions import KredivoCancelOrderException, KredivoUnexpectedError, KredivoCheckoutError
from kredivo.models import KredivoTransactionResponse, CancelPurchaseResponse, KredivoPaymentStatusResponse, \
    KredivoStatus


__all__ = ['KredivoGateway', ]


class KredivoGateway:
    """ This class for communication with Kredivo API
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
        request_data['server_key'] = self.server_key

        return json.dumps(request_data)

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
        :param `string` order_id:  merchant order id
        :return: `object` KredivoTransactionResponse
        """
        body = {
            "server_key": self.server_key,
            "order_id": order_id
        }
        response = requests.post(
            url=f"{self.base_url}/transaction/status",
            data=json.dumps(body),
            headers=self._build_headers()
        )

        if response.status_code != http.HTTPStatus.OK:
            raise HTTPError

        return KredivoTransactionResponse(response)

    def _confirm_push_notification(self):
        pass

    def cancel_transaction(self, order_id, transaction_id, cancellation_reason,
                           cancelled_by, cancellation_date, cancellation_amount=None):
        body = {
            "server_key": self.server_key,
            "order_id": order_id,
            "transaction_id": transaction_id,
            "cancellation_reason": cancellation_reason,
            "cancelled_by": cancelled_by,
            "cancellation_date": cancellation_date
        }

        if cancellation_amount:
            body["cancellation_amount"] = cancellation_amount

        response = requests.post(
            url=f"{self.base_url}/v2/cancel_transaction",
            data=json.dumps(body),
            headers=self._build_headers()
        )

        if response.json().get('status') == KredivoStatus.ERROR:
            return KredivoCancelOrderException(response.json())

        return CancelPurchaseResponse(response)


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

        status = KredivoStatus.OK if resp_json.pop('status') == 'OK' else KredivoStatus.ERROR
        return cls(status=status, **resp_json)

