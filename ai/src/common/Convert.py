def toDec(number: str, base: int) -> int:
    llen = len(number)
    power = 1
    num = 0
    for i in range(llen - 1, -1, -1):
        if int(number[i]) >= base:
            print('Invalid Number ' + number)
            return -1
        num += int(number[i]) * power
        power = power * base
    return num
