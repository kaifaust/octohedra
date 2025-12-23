"""Tests for GridCell base class."""
import pytest

from printing.grid.GridCell import GridCell
from printing.grid.OctoVector import OctoVector
from printing.utils import OctoConfigs


class TestGridCell:
    """Tests for GridCell rendering."""

    def test_render_raises_not_implemented(self):
        """GridCell.render() should raise NotImplementedError (abstract base)."""
        cell = GridCell()
        config = OctoConfigs.default.derive_render_config()
        center = OctoVector(0, 0, 0)

        with pytest.raises(NotImplementedError):
            cell.render(config, center)
