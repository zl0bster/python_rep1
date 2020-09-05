# UTF-8
# TODO
# Дан целочисленный массив из n элементов.
# Найти непустой подотрезок с наименьшей по модулю суммой.
# Время O(n log n).

def find_min_sequence(InputArray):
    """Finds a non-empty subsequence with the smallest amount.
    Zero means empty. Value sign is significant.
    No check for the correctness of the values or value type.
    Returns minimal subsequence amount and its start position."""

    def set_subseq_values(amount, pos, length):
        nonlocal minimalSubseqSum, minimalSubseqPos, minimalSubseqLen
        minimalSubseqSum = abs(amount)
        minimalSubseqPos = pos
        minimalSubseqLen = length

    # variables initiation
    minimalSubseqSum = None
    minimalSubseqPos = None
    minimalSubseqLen = None
    previousWasEmpty = True

    for i in range(0, len(InputArray) - 1):
        if InputArray[i] != 0:
            if previousWasEmpty:
                currentSubseqAmount = InputArray[i]
                currentSubseqPos = i
                currentSubseqLen = 1
            else:
                currentSubseqAmount += InputArray[i]
                currentSubseqLen += 1
            previousWasEmpty = False
        else:
            if not previousWasEmpty:
                if minimalSubseqSum is None:
                    set_subseq_values(currentSubseqAmount, currentSubseqPos, currentSubseqLen)
                elif minimalSubseqSum > abs(currentSubseqAmount):
                    set_subseq_values(currentSubseqAmount, currentSubseqPos, currentSubseqLen)
            previousWasEmpty = True
    return minimalSubseqSum, minimalSubseqPos, minimalSubseqLen


if __name__ == '__main__':
    arrayInt = [0, 0, -32, 4, 0, 12, 2, 0, 0, -6, 14, 1, 3, 0, 0, 0]
    print(find_min_sequence(arrayInt))
    arrayInt1 = [0, 0, 0]
    print(find_min_sequence(arrayInt1))
