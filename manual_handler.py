from packets import Result


class ManualHandler:

    def __init__(self):
        pass

    @staticmethod
    def get_guess() -> (int, int):
        row = int(input("Enter row to attack: "))
        col = int(input("Enter column to attack: "))
        return row, col

    @staticmethod
    def get_result(row: int, col: int) -> int:
        print(f"Opponent strikes row-{row} column-{col}")
        result = int(input("enter your response: 0.MISS, 1.HIT, 2.SINK, 3.DEFEAT\n"))
        return result

    @staticmethod
    def set_result(row: int, col: int, result: int) -> None:
        result_str = ""
        if result == Result.MISS.value:
            result_str = "MISS"
        elif result == Result.HIT:
            result_str = "HIT"
        elif result == Result.DESTROY:
            result_str = "SINK"
        elif result == Result.DEFEAT:
            print("You won, good job!")
            return
        print(f"your attack on row-{row} column-{col} was a {result_str}")
