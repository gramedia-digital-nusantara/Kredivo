import http
from unittest.mock import MagicMock, patch

from behave import given, when, then, step
from requests import Response

from features.steps import fixtures
from kredivo import KredivoGateway


@given("a gateway with {server_key} sandbox is {sandbox}")
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
    assert context.response.status.value == http.HTTPStatus.OK.name


@given("Check status for Order id {order_id}")
def step_impl(context, order_id):
    context.order_id = order_id


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
    assert context.response_order_status.json().get("transaction_status") == "pending"
