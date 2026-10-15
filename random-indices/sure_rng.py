import random

random.seed()

# Randomly selects n non-duplicate numbers from the range [start, end].
def getRandomNumbers(n, start, end):
    numbers = set()
    while len(numbers) < n:
        rn = random.randint(start, end)
        if rn not in numbers:
            numbers.add(rn)
    return numbers


randomNumbers = set()

for x in range(25):
    l = 100 + (x * 24)
    r = l + 23
    randomNumbers.update(getRandomNumbers(4, l, r))

print(randomNumbers)