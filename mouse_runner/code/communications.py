class communcation_class():
    def __init__(self) -> None:
        self.global_kill = ("ALIVE", 0)
                        # Jump Reset
        self.controls_state = 0b00