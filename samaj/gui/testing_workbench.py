"""Testing workbench placeholder view."""

from samaj.gui.placeholder import PlaceholderView


class TestingWorkbenchView(PlaceholderView):
    def __init__(self, parent=None) -> None:
        super().__init__("Testing Workbench", "Phase 8", parent)

