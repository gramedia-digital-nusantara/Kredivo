Feature: Kredivo API Gateway

  Scenario: Base URL for Sandbox API
    Given a gateway with server_key 123, sandbox is True
    When i check base url
    Then i get url "https://sandbox.kredivo.com/kredivo"

  Scenario: Base URL for Production API
    Given a gateway with server_key 123, sandbox is False
    When i check base url
    Then i get url "https://api.kredivo.com/kredivo"

  Scenario: Send new order request to Kredivo Production API
    Given a gateway with secret_key 123, sandbox is True
    And Build checkout request body
    When I make a successful new order request
    Then i get response status OK

  Scenario: Request Check Status Order to Kredivo Production API
    Given a gateway with secret_key 123, sandbox is True
    And Check status for Order id KD14721
    When I make a successful Order status request
    Then i get response transaction status pending
