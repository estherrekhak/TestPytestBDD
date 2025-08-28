Feature: Checkout process
  @smoke
  Scenario: Successful checkout
    Given the user has items in the cart
    When the user completes the checkout process
    Then the user should see the confirmation page
