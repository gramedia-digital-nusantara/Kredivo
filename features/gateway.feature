Feature: Kredivo API Gateway

  Scenario: Base URL for Sandbox API
    Given a gateway with server key 123, sandbox is True
    When i check base url
    Then i get url "https://sandbox.kredivo.com/kredivo"

  Scenario: Base URL for Production API
    Given a gateway with server key 123, sandbox is False
    When i check base url
    Then i get url "https://api.kredivo.com/kredivo"

  Scenario: Send new order request to Kredivo Production API
    Given a gateway with server key 123, sandbox is True
    And Build checkout request body
    When I make a successful new order request
    Then i get response status OK

  Scenario: Request Check Status Order to Kredivo Production API
    Given a gateway with server key 123, sandbox is True
    And Check status for Order id KD14721
    When I make a successful Order status request
    Then i get response transaction status pending

  Scenario: Request Check Payment Status Order to Kredivo Production API
    Given a gateway with server key 123, sandbox is True
    And Check status for Order id KD14721
    When Make sure the signature is from Kredivo
    Then I get response transaction status settlement

  Scenario: Cancel Order Transaction to Kredivo Production API
    Given a gateway with server key 123, sandbox is True
    When I Cancel Order id KD14721
    Then I got response status OK from kredivo

  Scenario: Cancel Order Transaction to Kredivo Production API
    Given a gateway with server key 123, sandbox is True
    When I Cancel with wrong Order id KD14721
    Then I got response status ERROR from kredivo
