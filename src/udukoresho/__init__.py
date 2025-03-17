import matplotlib
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Any, Tuple, List, Optional
import platform
import os



@dataclass
class LatexSetupConfig:
    # NOTE: the values are the default values for IEEE tran papers
    font_size: int = 10  # in pt
    line_width: int = 252  # express in pt


# Color-Blind friendly palette
cb_palette = [
    "#E69F00",
    "#56B4E9",
    "#009E73",
    "#F0E442",
    "#0072B2",
    "#D55E00",
    "#CC79A7",
    "#000000"
]

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

def pt_to_inch(pt):
    return pt/72.27

def setup_matplotlib_for_latex(matplotlib_module: matplotlib, customizations: LatexSetupConfig = None):
    """Set up matplotlib's RC params for LaTeX plotting."""
    config = customizations or LatexSetupConfig()
    # On MacOS, the PATH is not set correctly, so we need to add the path to the TeX binaries
    if platform.system() == "Darwin":
        if os.system("which kpsewhich") != 0:
            os.environ['PATH'] += ':/Library/TeX/texbin'
    matplotlib_module.rcParams.update({
        'backend': 'ps',
        'text.latex.preamble': r"""
        \usepackage[T1]{fontenc}
        \usepackage[tt=false, type1=true]{libertine}
        \usepackage{amsmath}
        \usepackage[varqu]{zi4}
        \usepackage{gensymb}
        \usepackage[libertine]{newtxmath}
        """,
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
    customizations: LatexSetupConfig,
    width: Optional[float] = None,
    height: Optional[float] = None,
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
    figsize = (set_width, set_height) if kwargs.get("figsize") is None else kwargs["figsize"]
    if kwargs.get("figsize"):
        del kwargs["figsize"]
    return plt.subplots(*nrow_ncols, figsize=figsize, **kwargs)
