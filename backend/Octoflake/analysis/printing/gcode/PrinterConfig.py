from dataclasses import dataclass





@dataclass
class PrinterConfig:
    """
    This class


    """

    # name = "Movement Config"

    travel_speed: int = 50
    extrusion_speed: int = 10
    line_width: float = 0.25
    layer_height: float = 0.1
    first_layer_height: float = 0.15
    printer_model: str = "MK3SMMU2S"
    nozzle_width: float = 0.25

    # Temperature

    hotend_temp: int = 210
    hotend_purge_temp: int = None
    hotend_first_layer_temp: int = None

    bed_temp: int = 60
    bed_purge_temp: int = None
    bed_first_layer_temp: int = None

    # Movement Limits

    ACCEL_G_CODE = "M201"
    x_max_accel: float = 1500
    y_max_accel: float = 1500
    z_max_accel: float = 200
    e_max_accel: float = 5000

    FEEDRATE_G_CODE = "M203"
    x_max_feedrate: float = 200
    y_max_feedrate: float = 200
    z_max_feedrate: float = 12
    e_max_feedrate: float = 120

    DEFAULT_ACCEL_G_CODE = "M204"
    print_accel: float = 800
    retract_accel: float = 1500
    travel_accel: float = 1500

    ADV_SETTINGS_G_CODE = "M205"
    x_max_jerk: float = 8
    y_max_jerk: float = 8
    z_max_jerk: float = 0.4
    e_max_jerk: float = 4.5
    min_print_feedrate: float = 0
    min_travel_feedrate: float = 0





# TODO: All this moves into the gcoder, or perhaps a new printer config coder
    def __post_init__(self):
        if self.hotend_first_layer_temp is None:
            self.hotend_first_layer_temp = self.hotend_temp
        if self.hotend_purge_temp is None:
            self.hotend_purge_temp = self.hotend_first_layer_temp

        if self.bed_first_layer_temp is None:
            self.bed_first_layer_temp = self.bed_temp
            print("wat")
        if self.bed_purge_temp is None:
            self.bed_purge_temp = self.bed_first_layer_temp

    def movement_limit_config(self):
        return [
            section_title("Movement Limits"),
            f"{self.ACCEL_G_CODE} "
            f"X{self.x_max_accel} Y{self.y_max_accel} Z{self.z_max_accel} E{self.e_max_accel} "
            f"; Set maximum accelerations, (mm/sec^2)",
            f"{self.FEEDRATE_G_CODE} "
            f"X{self.x_max_feedrate} Y{self.y_max_feedrate} Z{self.z_max_feedrate} "
            f"E{self.e_max_feedrate} "
            f"; Set maximum feedrates, (mm/sec)",
            f"{self.DEFAULT_ACCEL_G_CODE} "
            f"P{self.print_accel} R{self.retract_accel} T{self.travel_accel} "
            f"; Set default accelerations (mm/sec^2)",
            f"{self.ADV_SETTINGS_G_CODE} "
            f"X{self.x_max_jerk} Y{self.y_max_jerk} Z{self.z_max_jerk} E{self.e_max_jerk} "
            f"S{self.min_print_feedrate} T{self.min_travel_feedrate} "
            f"; Set jerk and min feedrate limits"
            ]

    def checks(self):
        return [
            section_title("Checks"),
            f"M862.3 P \"{self.printer_model}\" ; printer model check",
            f"M862.1 P{self.nozzle_width} ; nozzle diameter check"
            ]

    def startup(self):
        return [
            section_title("Startup"),
            "G90 ; use absolute coordinates",
            "M83 ; extruder relative mode",
            f"M104 S{self.hotend_first_layer_temp} ; set extruder temp",
            f"M140 S{self.bed_first_layer_temp} ; set bed temp",
            "Tx ; Load filament to extruder but not nozzle",
            # f"M109 S{self.hotend_purge_temp} ; wait for extruder temp",
            # f"M190 S{self.bed_purge_temp} ; wait for bed temp",
            "G28 W ; home all without mesh bed level",
            # "G80 ; mesh bed leveling"
            ]

    def purge(self):
        self.gcoder.write_line(section_title("Purge Line"))

        self.gcoder.move(z=5, comment="Schooch Up")
        self.gcoder.write_line(f"M109 S{self.hotend_first_layer_temp} ; wait for extruder temp")
        self.gcoder.write_line(f"M190 S{self.bed_first_layer_temp} ; wait for bed temp")
        self.gcoder.move(y=-3, f=self.travel_speed)
        # self.gcoder.write_line("Tc ; Load to nozzle")
        self.gcoder.move(z=1)
        self.gcoder.move(f=20)
        self.gcoder.move(x=55, z=.4, e=10)
        self.gcoder.move(z=.3)
        self.gcoder.move(x=240, e=25)
        self.gcoder.move(y=-2)
        # self.gcoder.write_line(f"M109 S{self.hotend_first_layer_temp} ; wait for extruder temp")
        # self.gcoder.write_line(f"M190 S{self.bed_first_layer_temp} ; wait for bed temp")
        self.gcoder.move(x=55, e=25)
        self.gcoder.move(z=0.2)
        self.gcoder.move(x=5, e=4)

        # "G1 Y-3.0 F1000.0",
        # "G1 Z4 F1000.0",
        # "G1 Z0.4 F1000.0",

    def ramming(self):
        self.gcoder.write_lines([
            section_title("Ramming"),
            "M91 ; Enable relative mode",
            ])

        self.gcoder.move(e=-3)
        self.gcoder.move(z=5)
        self.gcoder.move(e=3)
        self.gcoder.write_line(RAMMING)

    def shutdown(self):

        self.gcoder.write_lines([
            section_title("Shutdown"),

            # "M140 S0 ; turn off heat bed",
            "M107 ; turn off fan",
            # "M702 C ; Unload current Filament",
            "G4 ; wait",
            "M221 S100 ; reset flow",
            "M900 K0 ; reset LA",
            # "M104 S0 ; turn off temperature",
            # "M84 ; disable motors",
            ]
                )

        # self.gcoder.move()
