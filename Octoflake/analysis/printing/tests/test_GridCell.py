from unittest import TestCase

from printing.grid.GridCell import GridCell
from printing.utils import OctoConfigs
from printing.utils.OctoUtil import ORIGIN

TEST_CONFIG = OctoConfigs.config_25


class TestGridCell(TestCase):
    def test_render(self):
        cell = GridCell(ORIGIN)
        # TODO: Put back a generic testing config
        self.assertRaises(NotImplementedError, cell.render, TEST_CONFIG)


class Test(TestCase):
    def test_stitch_belts(self):

        self.fail()
