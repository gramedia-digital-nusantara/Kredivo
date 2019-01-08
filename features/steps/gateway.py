from behave import given, when, then

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

