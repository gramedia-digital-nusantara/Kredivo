Feature: Kredivo API Gateway

  Scenario: Base URL for Sandbox API
    Given a gateway with server_key 123, sandbox is True
    When i check base url
    Then i get url "https://sandbox.kredivo.com/kredivo"

 Scenario: Base URL for Production API
    Given a gateway with server_key 123, sandbox is False
    When i check base url
    Then i get url "https://api.kredivo.com/kredivo"
