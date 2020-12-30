from packets import Result

DEFENCE_FILE_PATH = "defence_grid.sub"
ATTACK_FILE_PATH = "attack_grid.sub"


class Board:

    def __init__(self, file_path):
        self.file_path = file_path
        self.info_cache = self.read_from_file()

    def read_from_file(self):
        with open(self.file_path, 'r') as board_file:
            raw_data = board_file.read()
            lines = raw_data.split()
            info = []
            for line in lines:
                line_info = []
                for char in line:
                    line_info.append(char)
                info.append(line_info)
        return info

    def attack_tile(self):




class AutoHandler:

    def __init__(self):
        self.defence_board = init_board(DEFENCE_FILE_PATH)
        self.attack_board = init_board(ATTACK_FILE_PATH)

    @staticmethod
    def get_guess() -> (int, int):
        row = int(input("Enter row to attack: "))
        col = int(input("Enter column to attack: "))
        return row, col

    def get_result(self, row: int, col: int) -> int:
        print(f"Opponent strikes row-{row} column-{col}")
        result = self.defence_board.attack_tile(row, col)
        return result

    def set_result(self, row: int, col: int, result: int) -> None:
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
        self.attack_board.update(row, col, result)
