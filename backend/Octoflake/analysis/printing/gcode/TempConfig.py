from dataclasses import dataclass


@dataclass
class TempConfig:
    extruder_temp: int = 210
    bed_temp: int = 60

    def __post_init__(self):
        if not 170 <= self.extruder_temp <= 270:
            raise ValueError()
        if not 0 <= self.bed_temp <= 100:
            raise ValueError()




DEFAULT = TempConfig(210, 60)
RAINBOW = TempConfig(240, 85)
QUANTUM = TempConfig(250, 85)
