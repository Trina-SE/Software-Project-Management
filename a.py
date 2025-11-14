import math

def is_prime(number: int) -> bool:
    """
    Checks if a given integer is a prime number.

    A prime number is a natural number greater than 1 that has no positive divisors
    other than 1 and itself.

    Args:
        number: The integer to check for primality.

    Returns:
        True if the number is prime, False otherwise.

    Raises:
        TypeError: If the input 'number' is not an integer.
    """
    if not isinstance(number, int):
        raise TypeError("Input must be an integer.")

    if number <= 1:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False

    limit = int(math.sqrt(number))
    for i in range(3, limit + 1, 2):
        if number % i == 0:
            return False
    return True