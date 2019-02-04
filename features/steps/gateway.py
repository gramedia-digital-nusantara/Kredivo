import http
from unittest.mock import MagicMock, patch

from behave import given, when, then, step
from requests import Response

from features.steps import fixtures
from kredivo import KredivoGateway
from kredivo.models import KredivoStatus


@given("a gateway with server key {server_key} sandbox is {sandbox}")
def step_impl(context, server_key, sandbox):
    context.gateway = KredivoGateway(
        server_key=123,
        use_sandbox=(True if sandbox == "True" else False)
    )


@when("i check base url")
def step_impl(context):
    context.base_url = context.gateway.base_url


@then('i get url "{url}"')
def step_impl(context, url):
    assert context.base_url == url


@given("Build checkout request body")
def step_impl(context):
    context.request_data = fixtures.checkout_request_body


@when("I make a successful new order request")
def step_impl(context):
    mock_post = MagicMock(spec=Response)
    mock_post.status_code = http.HTTPStatus.OK

    mock_post.json.return_value = fixtures.checkout_success_response
    patcher = patch("kredivo.gateway.requests")

    fake_requests = patcher.start()

    fake_requests.post.return_value = mock_post

    context.response = context.gateway.checkout(context.request_data)

    patcher.stop()


@then("i get response status OK")
def step_impl(context):
    assert context.response.status == KredivoStatus.OK


@given("Check status for Order id {order_id}")
def step_impl(context, order_id):
    context.order_id = order_id


@step("Using signature")
def step_impl(context):
    context.signature = "o5KZPDcxgEA9QutAVcIQwE3suQRkTEIA1VXcoHp7KaWJnpHx0uuHETBVpxfYLbaPyS8RJg34uVxTUX64cfUTzVVhCrSif"


@when("I make a successful Order status request")
def step_impl(context):
    mock_post = MagicMock(spec=Response)
    mock_post.status_code = http.HTTPStatus.OK

    mock_post.json.return_value = fixtures.transaction_status
    patcher = patch("kredivo.gateway.requests")

    fake_requests = patcher.start()

    fake_requests.post.return_value = mock_post

    context.response_order_status = context.gateway.transaction_status(context.order_id)

    patcher.stop()


@then("i get response transaction status pending")
def step_impl(context):
    assert context.response_order_status.transaction_status == "pending"


@when("I Cancel Order id {order_id}")
def step_impl(context, order_id):
    transaction_id = fixtures.cancel_transaction.get("transaction_id")
    cancellation_reason = fixtures.cancel_transaction.get("cancellation_reason")
    cancelled_by = fixtures.cancel_transaction.get("cancelled_by")
    cancellation_date = fixtures.cancel_transaction.get("cancellation_date")

    mock_post = MagicMock(spec=Response)
    mock_post.status_code = http.HTTPStatus.OK

    mock_post.json.return_value = fixtures.cancel_transaction_success
    patcher = patch("kredivo.gateway.requests")

    fake_requests = patcher.start()

    fake_requests.post.return_value = mock_post

    context.response_order_status = context.gateway.cancel_transaction(
        order_id, transaction_id, cancellation_reason, cancelled_by, cancellation_date)

    patcher.stop()


@then("I got response status OK from kredivo")
def step_impl(context):
    assert context.response_order_status.status == "OK"


@when("I Cancel with wrong Order id {order_id}")
def step_impl(context, order_id):
    transaction_id = fixtures.cancel_transaction.get("transaction_id")
    cancellation_reason = fixtures.cancel_transaction.get("cancellation_reason")
    cancelled_by = fixtures.cancel_transaction.get("cancelled_by")
    cancellation_date = fixtures.cancel_transaction.get("cancellation_date")

    mock_post = MagicMock(spec=Response)
    mock_post.status_code = http.HTTPStatus.OK

    mock_post.json.return_value = fixtures.cancel_transaction_failed
    patcher = patch("kredivo.gateway.requests")

    fake_requests = patcher.start()

    fake_requests.post.return_value = mock_post

    context.response_order_status = context.gateway.cancel_transaction(
        order_id, transaction_id, cancellation_reason, cancelled_by, cancellation_date)

    patcher.stop()


@then("I got response status {error} from kredivo")
def step_impl(context, error):
    assert context.response_order_status.status == error


@when("Make sure the signature is from Kredivo")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.transaction_id = fixtures.response_transaction_status.get("transaction_id")

    mock_get = MagicMock(spec=Response)
    mock_get.status_code = http.HTTPStatus.OK

    mock_get.json.return_value = fixtures.response_transaction_status
    patcher = patch("kredivo.gateway.requests")

    fake_requests = patcher.start()

    fake_requests.get.return_value = mock_get

    context.response_order_status = context.gateway.check_payment_status(
        transaction_id=context.transaction_id, signature_key="3u12h321uh3u21jndjsdjajdjhhew23232")

    patcher.stop()


@then("I get response transaction status settlement")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.transaction_id == context.response_order_status.transaction_id
