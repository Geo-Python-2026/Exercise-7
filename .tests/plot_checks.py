"""Helpers for inspecting the figures and image files a notebook produced."""

import os

import numpy as np
from matplotlib.collections import PathCollection
from PIL import Image


def section(section_data, name):
    """Return the data recorded for one tagged section, or fail with a clear message."""
    assert name in section_data, f"Section '{name}' was not found in the notebook"
    return section_data[name]


def all_axes(figures):
    return [ax for fig in figures for ax in fig.get_axes()]


def norm(text):
    return " ".join(str(text).split()).casefold()


def titles(figures):
    """All non-empty axes titles and figure suptitles."""
    found = []
    for fig in figures:
        if fig._suptitle is not None and fig._suptitle.get_text().strip():
            found.append(fig._suptitle.get_text())
        for ax in fig.get_axes():
            for loc in ("center", "left", "right"):
                text = ax.get_title(loc=loc)
                if text.strip():
                    found.append(text)
    return found


def scatter_collections(figures):
    """All scatter-plot point collections (with their axes)."""
    return [
        (ax, coll)
        for ax in all_axes(figures)
        for coll in ax.collections
        if isinstance(coll, PathCollection) and len(coll.get_offsets()) > 0
    ]


def lines(figures):
    """All data lines (with their axes)."""
    return [(ax, line) for ax in all_axes(figures) for line in ax.get_lines()]


def is_valid_png(path):
    if not isinstance(path, (str, os.PathLike)) or not os.path.isfile(path):
        return False
    try:
        with Image.open(path) as img:
            img.verify()
            return img.format == "PNG"
    except Exception:
        return False


def as_float_array(values):
    arr = np.asarray(values)
    assert arr.dtype.kind == "f", "values should be floats"
    return arr
