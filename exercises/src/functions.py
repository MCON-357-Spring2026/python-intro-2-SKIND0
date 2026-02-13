"""
Exercise 1: Functions
=====================
Practice: positional args, keyword args, defaults, *args, **kwargs, lambdas

Instructions:
- Complete each function where you see TODO
- Run this file to test your solutions
- All tests should print "PASSED"

Run with: python exercise_1_functions.py
"""
import html

# =============================================================================
# EXERCISE 1.1: Basic Function with Positional Arguments
# =============================================================================
"""
Create a function that calculates the area of a rectangle.

Parameters:
    width (float): The width of the rectangle
    height (float): The height of the rectangle

Returns:
    float: The area (width * height)

Example:
    calculate_area(5, 3) -> 15
    calculate_area(10, 10) -> 100
"""

def calculate_area(width: float, height: float) -> float:
    # TODO: Implement this function
    return width * height
    #pass


# =============================================================================
# EXERCISE 1.2: Function with Default Values
# =============================================================================
"""
Create a function that formats a price with currency symbol.

Parameters:
    amount (float): The price amount
    currency (str): The currency symbol (default: "$")
    decimals (int): Number of decimal places (default: 2)

Returns:
    str: Formatted price string

Example:
    format_price(19.99) -> "$19.99"
    format_price(19.99, "€") -> "€19.99"
    format_price(100, "$", 0) -> "$100"
    format_price(49.999, "£", 1) -> "£50.0"
"""

def format_price(amount: float, currency: str = "$", decimals: int = 2) -> str:
    # TODO: Implement this function
    # Hint: Use round() and f-strings
    return f"{currency}{round(amount, decimals)}"
    #pass


# =============================================================================
# EXERCISE 1.3: Function with *args
# =============================================================================
"""
Create a function that finds the maximum value from any number of arguments.

Parameters:
    *args: Any number of numeric values

Returns:
    float: The maximum value

Raises:
    ValueError: If no arguments are provided

Example:
    find_max(1, 5, 3) -> 5
    find_max(10) -> 10
    find_max(-5, -2, -10) -> -2
    find_max() -> raises ValueError
"""

def find_max(*args) -> float:
    # TODO: Implement this function
    # Hint: Check if args is empty first
    if not args:
        raise ValueError("No arguments are provided")
    maximum = float('-inf')
    for arg in args:
        if arg > maximum:
            maximum = arg

    return maximum
    #pass


# =============================================================================
# EXERCISE 1.4: Function with **kwargs
# =============================================================================
"""
Create a function that builds an HTML tag with attributes.

Parameters:
    tag_name (str): The HTML tag name (e.g., "div", "a", "img")
    **kwargs: Any HTML attributes as keyword arguments

Returns:
    str: The opening HTML tag with attributes

Example:
    build_tag("div") -> "<div>"
    build_tag("a", href="https://example.com") -> '<a href="https://example.com">'
    build_tag("img", src="photo.jpg", alt="A photo") -> '<img src="photo.jpg" alt="A photo">'
"""

def build_tag(tag_name: str, **kwargs) -> str:
    # TODO: Implement this function
    # Hint: Loop through kwargs.items() to build attribute string
    tag = f"<{tag_name}"
    for key, value in kwargs.items():
        tag += f' {key}="{value}"'
    tag += ">"
    return tag

# =============================================================================
# EXERCISE 1.5: Combining Parameters
# =============================================================================
"""
Create a function that sends a notification message.

Parameters:
    recipient (str): Required - who receives the message
    message (str): Required - the message content
    *cc: Optional - any number of CC recipients
    **options: Optional - any additional options (urgent, read_receipt, etc.)

Returns:
    dict: A dictionary with the notification details

Example:
    send_notification("alice@example.com", "Hello!")
    -> {"to": "alice@example.com", "message": "Hello!", "cc": [], "options": {}}

    send_notification("bob@example.com", "Meeting", "alice@example.com", "charlie@example.com", urgent=True)
    -> {"to": "bob@example.com", "message": "Meeting", "cc": ["alice@example.com", "charlie@example.com"], "options": {"urgent": True}}
"""

def send_notification(recipient: str, message: str, *cc, **options) -> dict:
    return {
        "to": recipient,
        "message": message,
        "cc": list(cc),
        "options": options,
    }


# =============================================================================
# EXERCISE 1.6: Lambda Expressions
# =============================================================================
"""
Complete the lambda expressions below.
"""

# TODO: Create a lambda that doubles a number
# Example: double(5) -> 10
double = lambda x: x * 2


# TODO: Create a lambda that checks if a number is even
# Example: is_even(4) -> True, is_even(7) -> False
is_even = lambda x: x % 2 == 0


# TODO: Create a lambda that returns the last character of a string
# Example: last_char("hello") -> "o"
last_char = lambda s: s[-1]


# TODO: Use a lambda with sorted() to sort these words by their LENGTH
words = ["python", "java", "go", "javascript", "c"]
# Expected result: ["c", "go", "java", "python", "javascript"]
sorted_by_length = sorted(words, key=lambda w:len(w))


# TODO: Use a lambda with filter() to get only positive numbers
numbers = [-3, 5, -1, 8, 0, -2, 10]
# Expected result: [5, 8, 10]
positive_only = list(filter(lambda n: n > 0, numbers))


