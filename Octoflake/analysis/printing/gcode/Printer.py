from dataclasses import dataclass

from printing.gcode.Gcoder import GCoder
from printing.gcode.Print import Print
from printing.gcode.PrinterConfig import PrinterConfig
from printing.grid.OctoVector import OctoVector


@dataclass
class Printer:
    """
    This class actually knows all the steps to do a print, but doesn't know any Gcode.


    The printer config, temp config, and the layer and path



    """

    movement_config : PrinterConfig = PrinterConfig()


    # purge_config :
    # ramming_config : int

    # Current settings

    location: OctoVector = OctoVector()

    hotend_temp : float = 210
    bed_temp : float = 60


    def execute_debug_print(self, Print):
        """This printing method assumes that the printer already has the filament loaded"""
        with GCoder(filenames=["test.gcode"]) as gcoder:
            self.purge(gcoder)


    def initialize_print(self, rapid_iteration = False):
        pass

    def end_print(self, rapid_iteration = False):
        pass

    def move_to(self ):
        pass

    def retract(self, path=None):
        pass

    def set_layer_config(self):
        pass




    def purge(self, gcoder):
        gcoder.write_section_title("Purge Line")

        gcoder.move(z=5, comment="Schooch Up")
        gcoder.write_line(f"M109 S{self.hotend_first_layer_temp} ; wait for extruder temp")
        gcoder.write_line(f"M190 S{self.bed_first_layer_temp} ; wait for bed temp")
        gcoder.move(y=-3, f=self.travel_speed)
        # self.gcoder.write_line("Tc ; Load to nozzle")
        gcoder.move(z=1)
        gcoder.move(f=20)
        gcoder.move(x=55, z=.4, e=10)
        gcoder.move(z=.3)
        gcoder.move(x=240, e=25)
        gcoder.move(y=-2)
        # self.gcoder.write_line(f"M109 S{self.hotend_first_layer_temp} ; wait for extruder temp")
        # self.gcoder.write_line(f"M190 S{self.bed_first_layer_temp} ; wait for bed temp")
        gcoder.move(x=55, e=25)
        gcoder.move(z=0.2)
        gcoder.move(x=5, e=4)


if __name__=="__main__":

    print = Print()

    printer = Printer()
    printer.debug_print(print)
