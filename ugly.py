from fractions import Fraction
from itertools import permutations, product
from tqdm import tqdm
import sys

NUMS = [2, 1, 1, 1, 1, 1]
TARGET = 8
OPS = {
    '+': lambda x, y: x + y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '-': lambda x, y: x - y
}

def test(numbers, inst, index):
    inst = list(inst)
    todo = []
    index_i = 0
    for n, number in enumerate(numbers):
        todo.append(number)
        while n >= index[index_i]:
            index_i += 1
            try:
                todo[-2:] = [OPS[inst.pop()](todo[-2], todo[-1])]
            except ZeroDivisionError:
                return None
            if index_i >= len(index):
                break
    return todo.pop(), index

def test1(p, inst, index, n):
    res = test(p, inst, index)
    if res is not None and res[0].denominator == 1 and (0 <= res[0] < 1000):
        yield res
    if n == -1:
        return
    for max in range(n-1):
        newindex = list(index)
        for increment in range(1, index[max]-index[max+1]+1):
            while index[max] == index[max-1]:
                newindex[max] += increment
                max -= 1
            newindex[max] += increment
            yield from test1(p, inst, newindex, max)

def represent(nums, inst, index):
    ints = [str(int(v)) for v in nums]
    inst = list(inst)
    result = []
    index_i = 0
    for i, v in enumerate(ints):
        result.append(v)
        while i >= index[index_i]:
            index_i += 1
            result[-2:] = [f'({result[-2]} {inst.pop()} {result[-1]})']
            if index_i >= len(index):
                break
    return result[0]

best_score = 501

for l in range(len(NUMS), 1, -1):
    for p in tqdm(list(set(permutations([Fraction(n) for n in sorted(NUMS, reverse=True)], r=l)))):
        print(p)
        for inst in product(list(OPS), repeat=(l-1)):
            index = list(range(1, l))
            max = l-2
            for i in range(l-2, 0, -1):
                issum1 = inst[i] in '+-'
                issum2 = inst[i-1] in '+-'
                if not issum1 ^ issum2:
                    index[i-1] = index[i]
                    if max == i:
                        max -= 1
            for soln, index in test1(p, inst, index, max):
                if abs(soln - TARGET) <= best_score:
                    best_score = abs(soln - TARGET)
                    tqdm.write(f"with score: {best_score} -- {represent(p, inst, index)}")
                    if best_score == 0:
                        sys.exit(0)
sys.exit(1)



