Feature: Add to cart
  @smoke
  Scenario: Add item to cart
    Given the user is logged in
    When the user adds an item to the cart
    Then the cart should contain the item
