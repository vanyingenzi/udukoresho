import re
from typing import List, Dict, Any, Tuple
import json
from datetime import datetime
import colorsys
import matplotlib
import matplotlib.pyplot as plt
from dataclasses import dataclass

colors_impl_mapping = {
    "mpquic": "#E69F00",
    "mcmpquic": "#56B4E9",
    "mcmpquic-aff": "#009E73",
    "mcmpquic-rfs": "#CC79A7",
}

linestyles = [
    (0, (1, 1)),
    (5, (10, 3)),
    (0, (5, 5)),
    (0, (5, 1)),
    (0, (3, 10, 1, 10)),
    (0, (3, 5, 1, 5)),
    (0, (3, 1, 1, 1)),
    (0, (3, 5, 1, 5, 1, 5)),
    (0, (3, 10, 1, 10, 1, 10)),
    (0, (3, 1, 1, 1, 1, 1))
]


@dataclass
class LatexSetupConfig:
    # NOTE: the values are the default values for IEEE tran papers
    font_size: int = 10  # in pt
    line_width: int = 252  # express in pt


def get_color_for_impl(impl: str):
    return colors_impl_mapping.get(impl, "black")


def mcmpquic_extract_nb_paths(filepath: str) -> int:
    """ Extract path information from the logs of a mcMPQUIC endpoint. Idealy from the server as it is the one
    that validates a path lastly. [MPQUIC detail]
    """
    pattern = re.compile(r".*(p|P)ath.*is now validated")
    nb_paths = 0
    with open(filepath) as f:
        for line in f:
            if pattern.match(line):
                nb_paths += 1
    return nb_paths + 1  # +1 for the default path


def get_test_start_end_time(time_json_file) -> Tuple[int, int]:
    with open(time_json_file) as f:
        data = json.load(f)
        return data["start"], data["end"]


def get_transfer_time_client(time_json_file) -> float:
    with open(time_json_file) as f:
        data = json.load(f)
    start = datetime.fromtimestamp(int(data["start"]) / 1e9)
    end = datetime.fromtimestamp(int(data["end"]) / 1e9)
    diff = end - start
    return diff.total_seconds()


def hex_to_rgb(hex_value):
    hex_value = hex_value.lstrip('#')
    return tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))


def get_color_for_impl_n_path(impl: str, nb_paths: int, max_nb_paths: int = 16) -> Tuple[float, float, float]:
    base_color_hex = get_color_for_impl(impl)
    base_color_rgb = hex_to_rgb(base_color_hex)
    base_color_rgb_normalized = [x / 255 for x in base_color_rgb]
    h, s, _ = colorsys.rgb_to_hsv(*base_color_rgb_normalized)
    step = 100 / max_nb_paths
    v = step * nb_paths
    v = v / 100
    return colorsys.hsv_to_rgb(h, s, v)


def setup_matplotlib_for_latex(matplotlib_module: matplotlib, customizations: LatexSetupConfig = None):
    """Set up matplotlib's RC params for LaTeX plotting."""
    config = customizations or LatexSetupConfig()
    matplotlib_module.rcParams.update({
        'backend': 'ps',
        'text.latex.preamble': r'\usepackage[T1]{fontenc} \usepackage{gensymb}',
        'axes.labelsize': config.font_size,
        'axes.titlesize': config.font_size,
        'font.size': config.font_size,
        'legend.fontsize': config.font_size,
        'xtick.labelsize': config.font_size,
        'ytick.labelsize': config.font_size,
        'text.usetex': True,
        'grid.alpha': 0.25,
        'pgf.texsystem': 'pdflatex',
        'mathtext.default': 'regular',
        'font.family': 'serif',
    })


def create_fig(
    width: float | None,
    height: float | None,
    customizations: LatexSetupConfig,
    nrow_ncols: Tuple[int, int] = (1, 1),
    **kwargs: Any
) -> Tuple[plt.Figure, List[plt.Axes]]:
    """
    height: in pt
    width: in pt
    """
    from math import sqrt
    set_height = None
    set_width = None
    if width is None:
        set_width = customizations.line_width / 72.27
    if height is None:
        golden_mean = (sqrt(5)-1.0)/2.0    # Aesthetic ratio
        set_height = set_width * golden_mean
    figsize = (set_width, set_height) if kwargs.get(
        "figsize") is None else kwargs["figsize"]
    if kwargs.get("figsize"):
        del kwargs["figsize"]
    return plt.subplots(*nrow_ncols, figsize=figsize, **kwargs)
