"""Visualization module."""

import matplotlib.pyplot as plt
from mplhep import histplot


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
    bins = hists[0][1]

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

    fig, ax = plt.subplots()

    if all(v is not None for v in [labels, scale_factors]):
        labels = [
            label if sf == 1 else f"{label} X {sf}"
            for label, sf in zip(labels, scale_factors)
        ]
    if scale_factors is not None:
        hists = [h[0] * sf for h, sf in zip(hists, scale_factors)]
    else:
        hists = [h[0] for h in hists]

    ax = histplot(
        hists,
        bins=bins,
        stack=True,
        histtype="fill",
        label=labels,
        color=color,
        alpha=alpha,
    )
    ax.semilogy()

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc="best")

    return fig, ax
