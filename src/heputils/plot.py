"""Visualization module."""

import matplotlib.pyplot as plt
from mplhep import histplot


def stack_hist(hists, **kwargs):
    fig, ax = plt.subplots()
    bins = hists[0][1]
    scale_factors = kwargs.pop("scale_factors", None)
    labels = kwargs.pop("labels", None)
    color = kwargs.pop("color", None)
    xlabel = kwargs.pop("xlabel", None)
    ylabel = kwargs.pop("ylabel", None)
    title = kwargs.pop("title", None)

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
        hists, bins=bins, stack=True, histtype="fill", label=labels, color=color
    )
    ax.semilogy()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc="best")
    return fig, ax
