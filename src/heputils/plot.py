"""Visualization module."""

import matplotlib.pyplot as plt
from mplhep import histplot
import mplhep
import numpy as np
from . import utils


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


def get_style(style=None):
    """
    Set the experiment specific plotting style

    Example:

        >>> import heputils
        >>> heputils.plot.set_style("ATLAS")
        >>> heputils.plot.get_style()["figure.figsize"]
        [8.75, 5.92]
        >>> heputils.plot.get_style("CMS")["figure.figsize"]
        (10.0, 10.0)

    Args:
        style (str): The experiment style string alias

    Returns:
        dict: The style dict requested
    """
    if style is not None:
        style = getattr(mplhep.style, style)
    else:
        style = dict(plt.rcParams)
    return style


def _plot_ax_kwargs(ax, **kwargs):
    """
    Apply kwargs to an axis.

    Args:
        ax (`matplotlib.axes.Axes`): The axis object to mutate

    Returns:
        `matplotlib.axes.Axes`: matplotlib axis object
    """
    # get all the kwargs
    xlabel = kwargs.pop("xlabel", ax.get_xlabel())
    ylabel = kwargs.pop("ylabel", ax.get_ylabel())
    title = kwargs.pop("title", ax.get_title())
    semilogy = kwargs.pop("logy", None)
    legend_loc = kwargs.pop("legend_loc", "best")
    return_artists = kwargs.pop("return_artists", False)

    if semilogy is not None:
        if semilogy:
            ax.semilogy()
        else:
            ax.set_yscale("linear")
            # Ensure scale is sensible
            ax.relim()
            ax.autoscale()
    else:
        ax.set_yscale(ax.get_yscale())

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    # Ensure uncertainty and data at top of legend
    handles, labels = ax.get_legend_handles_labels()
    # FIXME: Make this user defined and not hardcoded
    for label in ["Stat Uncertainty", "Data"]:
        if label in labels:
            handles.insert(0, handles.pop(labels.index(label)))
            labels.insert(0, labels.pop(labels.index(label)))
    ax.legend(handles, labels, loc=legend_loc)

    return (ax, ax.get_children()) if return_artists else ax


def _plot_uncertainty(model_hist, ax):
    """
    Plot the model uncertainty as a bar plot

    Args:
        model_hist (`hist.Hist`): The histogram to calculate uncertainty for
        ax (`matplotlib.axes.Axes`): The axis the bar plot is drawn on

    Returns:
        `matplotlib.axes.Axes`: The axis the bar plot is drawn on
    """

    stat_uncert = np.sqrt(model_hist)
    bin_centers = model_hist.axes.centers[0]
    bin_widths = model_hist.axes.widths[0]
    uncert_label = "Stat Uncertainty"

    ax.bar(
        bin_centers,
        height=2 * stat_uncert,
        width=bin_widths,
        bottom=model_hist - stat_uncert,
        fill=False,
        linewidth=0,
        edgecolor="gray",
        hatch=3 * "/",
        label=uncert_label,
    )
    return ax


def data_hist(hist, uncert=None, ax=None, **kwargs):
    """
    Plot a histogram styled as data.

    Args:
        hist (`hist.Hist`): The histogram containing the data
        uncert (`array`): The uncertainty values for the `hist`
        ax (`matplotlib.axes.Axes`): The axis object to plot on

    Returns:
        `matplotlib.axes.Axes`: matplotlib subplot axis object
    """
    if uncert is None:
        uncert = np.sqrt(hist)
    if ax is None:
        ax = plt.gca()

    # get all the kwargs
    color = kwargs.pop("color", "black")
    label = kwargs.pop("label", "Data")
    density = kwargs.pop("density", False)
    if density:
        histtype = "step"
    else:
        histtype = "errorbar"

    histplot(
        hist,
        yerr=uncert,
        histtype=histtype,
        density=density,
        color=color,
        label=label,
        ax=ax,
    )

    return _plot_ax_kwargs(ax, **kwargs)


def shape_hist(hists, ax=None, **kwargs):
    """
    Plot the shape outline of all the input histograms

    Args:
        hists (list): List of `hist.Hist` objects representing histograms
        ax (`matplotlib.axes.Axes`): The axis object to plot on
        kwargs: Keyword arguments to matplotlib

    Returns:
        `matplotlib.axes.Axes`: matplotlib subplot axis object
    """
    if not isinstance(hists, list):
        hists = [hists]

    labels = kwargs.pop("labels", None)
    color = kwargs.pop("color", None)
    if color is not None:
        if len(color) != len(hists):
            color = color[: len(hists)]
    alpha = kwargs.pop("alpha", 0.1)
    semilogy = kwargs.pop("logy", False)
    _data_hist = kwargs.pop("data_hist", None)
    data_uncert = kwargs.pop("data_uncert", None)
    data_label = kwargs.pop("data_label", "Data")
    density = kwargs.pop("density", True)

    if ax is None:
        ax = plt.gca()

    histplot(
        hists,
        stack=False,
        histtype="fill",
        density=density,
        label=labels,
        color=color,
        alpha=alpha,
        ax=ax,
    )

    if _data_hist is not None:
        ax = data_hist(
            _data_hist, uncert=data_uncert, label=data_label, density=density, ax=ax
        )

    if semilogy:
        ax.semilogy()
        # Ensure enough space for legend
        if not density:
            max_hist = max([max(hist) for hist in hists])
        else:
            max_hist = max([max(hist.density()) for hist in hists])
        ax.set_ylim(top=max_hist * 100)

    return _plot_ax_kwargs(ax, **kwargs)


def stack_hist(hists, ax=None, **kwargs):
    """
    Plot a stacked histogram of all the input histograms

    Args:
        hists (list): List of `hist.Hist` objects representing histograms
        ax (`matplotlib.axes.Axes`): The axis object to plot on
        kwargs: Keyword arguments to matplotlib

    Returns:
        `matplotlib.axes.Axes`: matplotlib subplot axis object
    """
    if not isinstance(hists, list):
        hists = [hists]

    # get all the kwargs
    scale_factors = kwargs.pop("scale_factors", None)
    labels = kwargs.pop("labels", None)
    color = kwargs.pop("color", None)
    if color is not None:
        if len(color) != len(hists):
            color = color[: len(hists)]
    alpha = kwargs.pop("alpha", None)
    semilogy = kwargs.pop("logy", True)
    _data_hist = kwargs.pop("data_hist", None)
    data_uncert = kwargs.pop("data_uncert", None)
    data_label = kwargs.pop("data_label", "Data")

    if ax is None:
        ax = plt.gca()

    if all(v is not None for v in [labels, scale_factors]):
        labels = [
            label if sf == 1 else f"{label} X {sf}"
            for label, sf in zip(labels, scale_factors)
        ]
    if scale_factors is not None:
        hists = [h * sf for h, sf in zip(hists, scale_factors)]

    histplot(
        hists,
        stack=True,
        histtype="fill",
        label=labels,
        color=color,
        alpha=alpha,
        ax=ax,
    )

    # Inspired by cabinetry
    # https://github.com/alexander-held/cabinetry/blob/aa36561eba458d47a17a4a7db1ffdce08417ce89/src/cabinetry/contrib/matplotlib_visualize.py#L87
    stack_hist = utils.sum_hists(hists)
    ax = _plot_uncertainty(stack_hist, ax)

    if _data_hist is not None:
        ax = data_hist(_data_hist, uncert=data_uncert, label=data_label, ax=ax)

    if semilogy:
        ax.semilogy()
        # Ensure enough space for legend
        ax.set_ylim(top=max(stack_hist) * 100)

    return _plot_ax_kwargs(ax, **kwargs)
