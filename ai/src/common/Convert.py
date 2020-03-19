def toDec(a: int, base: int) -> int:
    """
    Converts an integer of base (base) to a decimal integer.
    """

    ans = 0  # output sum
    inc = 1  # incrementing number (what you multiply each digit by)
    while a:
        digit = inc * (a % 10)  # last digit of a times the incrementer
        ans += digit  # digit added to sum
        a //= 10  # cuts off the last digit of a (// is integer division in python 3.x)
        inc *= base  # base (2 for binary, 3 for ternary, etc)

    return ans
