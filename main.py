"""Project 6 — Event-Driven Self-Review Loop

Entry point demonstrating the calculator module.
"""

from src.calculator import sum_range, average


def main():
    # Demo dataset
    numbers = [1, 2, 3, 4, 5]

    print("=" * 40)
    print("Project 6 — Calculator Demo")
    print("=" * 40)
    print(f"Numbers      : {numbers}")
    print(f"sum_range()  : {sum_range(numbers)}")
    print(f"average()    : {average(numbers)}")
    print("=" * 40)


if __name__ == "__main__":
    main()
