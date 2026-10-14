from typing import List, Tuple


def find_min_max(numbers: List[float]) -> Tuple[float, float]:
    """
    Знаходить мінімальний та максимальний елементи масиву
    методом "розділяй і володарюй".

    Returns:
        tuple: (minimum, maximum)
    """

    if not numbers:
        raise ValueError("Масив не може бути порожнім")

    def divide_and_conquer(left: int, right: int) -> Tuple[float, float]:
        # Один елемент
        if left == right:
            return numbers[left], numbers[left]

        # Два елементи
        if right == left + 1:
            if numbers[left] < numbers[right]:
                return numbers[left], numbers[right]
            return numbers[right], numbers[left]

        # Розділяємо масив навпіл
        middle = (left + right) // 2

        left_min, left_max = divide_and_conquer(left, middle)
        right_min, right_max = divide_and_conquer(middle + 1, right)

        # Об'єднуємо результати
        return min(left_min, right_min), max(left_max, right_max)

    return divide_and_conquer(0, len(numbers) - 1)


if __name__ == "__main__":
    numbers = [3, -5, 10, 2, 8, 0, 15, -2]

    minimum, maximum = find_min_max(numbers)

    print(f"Масив: {numbers}")
    print(f"Мінімум: {minimum}")
    print(f"Максимум: {maximum}")