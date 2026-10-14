from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами
    та обмеженнями принтера.

    Args:
        print_jobs: список завдань на друк
        constraints: обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """

    printer = PrinterConstraints(**constraints)

    if printer.max_volume <= 0:
        raise ValueError("max_volume має бути більше 0")

    if printer.max_items <= 0:
        raise ValueError("max_items має бути більше 0")

    # Перетворюємо словники на PrintJob
    jobs = [PrintJob(**job) for job in print_jobs]

    # Перевіряємо коректність завдань
    for job in jobs:
        if job.volume <= 0:
            raise ValueError(
                f"Об'єм завдання {job.id} має бути більше 0"
            )

        if job.print_time <= 0:
            raise ValueError(
                f"Час друку завдання {job.id} має бути більше 0"
            )

        if job.priority not in (1, 2, 3):
            raise ValueError(
                f"Пріоритет завдання {job.id} має бути 1, 2 або 3"
            )

        if job.volume > printer.max_volume:
            raise ValueError(
                f"Завдання {job.id} перевищує максимальний "
                f"об'єм принтера"
            )

    # Сортуємо за пріоритетом.
    # Python sort стабільний, тому для однакового priority
    # початковий порядок зберігається.
    jobs.sort(key=lambda job: job.priority)

    print_order = []
    total_time = 0

    current_group = []
    current_volume = 0.0

    for job in jobs:
        can_add_to_group = (
            len(current_group) < printer.max_items
            and current_volume + job.volume <= printer.max_volume
        )

        # Якщо нова модель не поміщається,
        # завершуємо поточну групу
        if not can_add_to_group and current_group:
            group_time = max(
                item.print_time for item in current_group
            )

            total_time += group_time

            current_group = []
            current_volume = 0.0

        # Додаємо модель до групи
        current_group.append(job)
        current_volume += job.volume
        print_order.append(job.id)

    # Друкуємо останню групу
    if current_group:
        group_time = max(
            item.print_time for item in current_group
        )

        total_time += group_time

    return {
        "print_order": print_order,
        "total_time": total_time
    }


def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {
            "id": "M1",
            "volume": 100,
            "priority": 1,
            "print_time": 120
        },
        {
            "id": "M2",
            "volume": 150,
            "priority": 1,
            "print_time": 90
        },
        {
            "id": "M3",
            "volume": 120,
            "priority": 1,
            "print_time": 150
        }
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {
            "id": "M1",
            "volume": 100,
            "priority": 2,
            "print_time": 120
        },
        {
            "id": "M2",
            "volume": 150,
            "priority": 1,
            "print_time": 90
        },
        {
            "id": "M3",
            "volume": 120,
            "priority": 3,
            "print_time": 150
        }
    ]

    # Тест 3: Перевищення обмежень об'єму групи
    test3_jobs = [
        {
            "id": "M1",
            "volume": 250,
            "priority": 1,
            "print_time": 180
        },
        {
            "id": "M2",
            "volume": 200,
            "priority": 1,
            "print_time": 150
        },
        {
            "id": "M3",
            "volume": 180,
            "priority": 2,
            "print_time": 120
        }
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
    