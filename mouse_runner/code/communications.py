class communcation_class():
    def __init__(self) -> None:
        self.global_kill = ("ALIVE", 0)
                        # Jump Reset
        self.controls_state = 0b00
        self.player_y = 0
        self.tile_states = []
        self.tile_offset_x = 0
        self.background_sprites = dict()
        self.obstacles = []