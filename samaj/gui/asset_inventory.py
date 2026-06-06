"""Asset inventory placeholder view."""

from samaj.gui.placeholder import PlaceholderView


class AssetInventoryView(PlaceholderView):
    def __init__(self, parent=None) -> None:
        super().__init__("Asset Inventory", "Phase 2", parent)

