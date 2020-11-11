"""Visualization module."""

import matplotlib.pyplot as plt
from mplhep import histplot
import mplhep
import hist
import numpy as np
from .convert import stack_hists
from .convert import numpy_to_hist


def set_style(style):
    """
    Set the experiment specific plotting style

    Example:

        >>> import heputils
        >>> import mplhep
        >>> heputils.plot.set_style("ATLAS")
        >>> heputils.plot.set_style(mplhep.style.CMS)

    Args:
        style (str or `mplhep.style` dict): The experiment style
    """
    mplhep.set_style(style)


def stack_hist(hists, **kwargs):
    """
    Plot a stacked histogram of all the input histograms

    Args:
        hists (list): List of numpy arrays representing histograms
        kwargs: Keyword arguments to matplotlib

    Returns:
        fig, ax: matplotlib subplot figure and axis objects
    """
    if not isinstance(hists, list):
        hists = [hists]
    # if isinstance(hists[0], hist.Hist):
    #     hists = [h.to_numpy() for h in hists]
    # bins = hists[0][1]

    # get all the kwargs
    scale_factors = kwargs.pop("scale_factors", None)
    labels = kwargs.pop("labels", None)
    color = kwargs.pop("color", None)
    if color is not None:
        if len(color) != len(hists):
            color = color[: len(hists)]
    alpha = kwargs.pop("alpha", None)
    xlabel = kwargs.pop("xlabel", None)
    ylabel = kwargs.pop("ylabel", None)
    title = kwargs.pop("title", None)
    semilogy = kwargs.pop("logy", True)
    return_artists = kwargs.pop("return_artists", False)

    fig, ax = plt.subplots()

    if all(v is not None for v in [labels, scale_factors]):
        labels = [
            label if sf == 1 else f"{label} X {sf}"
            for label, sf in zip(labels, scale_factors)
        ]
    if scale_factors is not None:
        hists = [h * sf for h, sf in zip(hists, scale_factors)]
    # else:
    #     hists = [h[0] for h in hists]

    histplot(
        hists,
        stack=True,
        histtype="fill",
        label=labels,
        color=color,
        alpha=alpha,
    )

    # draw uncertainty
    stack_hist = stack_hists(hists)
    stat_uncert = np.sqrt(stack_hist)
    bin_centers = stack_hist.axes.centers[0]
    bin_widths = stack_hist.axes.widths[0]
    uncert_label = "Stat Uncertainity"

    ax.bar(
        bin_centers,
        height=2 * stat_uncert,
        width=bin_widths,
        bottom=stack_hist - stat_uncert,
        fill=False,
        linewidth=0,
        edgecolor="gray",
        hatch=3 * "/",
        label=uncert_label,
    )

    if semilogy:
        ax.semilogy()
        ax.set_ylim(top=max(stack_hist) * 10)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc="best")

    return (ax, ax.get_children()) if return_artists else ax
