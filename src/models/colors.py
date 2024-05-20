class Colors:
    def __init__(self, main: str, option_1: str, option_2: str):
        self.main = main
        self.option_1 = option_1
        self.option_2 = option_2

    def __str__(self):
        return f"Main: {self.main}, Option 1: {self.option_1}, Option 2: {self.option_2}"

