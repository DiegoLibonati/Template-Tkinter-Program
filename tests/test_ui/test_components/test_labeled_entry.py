import tkinter as tk

from src.ui.components.labeled_entry import LabeledEntry
from src.ui.styles import Styles


class TestLabeledEntry:
    def test_instantiation(self, root: tk.Tk, styles: Styles) -> None:
        var: tk.StringVar = tk.StringVar(root)
        entry: LabeledEntry = LabeledEntry(parent=root, label_text="Username", styles=styles, variable=var)
        assert entry is not None
        entry.destroy()

    def test_instantiation_with_show(self, root: tk.Tk, styles: Styles) -> None:
        var: tk.StringVar = tk.StringVar(root)
        entry: LabeledEntry = LabeledEntry(parent=root, label_text="Password", styles=styles, variable=var, show="*")
        assert entry is not None
        entry.destroy()

    def test_variable_value_is_readable(self, root: tk.Tk, styles: Styles) -> None:
        var: tk.StringVar = tk.StringVar(root, value="test_value")
        entry: LabeledEntry = LabeledEntry(parent=root, label_text="Label", styles=styles, variable=var)
        assert var.get() == "test_value"
        entry.destroy()

    def test_variable_update_reflects_correctly(self, root: tk.Tk, styles: Styles) -> None:
        var: tk.StringVar = tk.StringVar(root)
        entry: LabeledEntry = LabeledEntry(parent=root, label_text="Label", styles=styles, variable=var)
        var.set("updated")
        assert var.get() == "updated"
        entry.destroy()

    def test_empty_label_text_accepted(self, root: tk.Tk, styles: Styles) -> None:
        var: tk.StringVar = tk.StringVar(root)
        entry: LabeledEntry = LabeledEntry(parent=root, label_text="", styles=styles, variable=var)
        assert entry is not None
        entry.destroy()
