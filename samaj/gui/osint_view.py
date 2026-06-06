"""OSINT placeholder view."""

from samaj.gui.placeholder import PlaceholderView


class OsintView(PlaceholderView):
    def __init__(self, parent=None) -> None:
        super().__init__("OSINT", "Phase 5", parent)

