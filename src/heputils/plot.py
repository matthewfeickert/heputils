"""Visualization module."""

import math

import matplotlib.pyplot as plt
import mplhep
import numpy as np
from mplhep import histplot

from . import utils

# To be able to reset
_experiment_label_info_defaults = {
    "name": None,
    "status": "Internal",
    "center_of_mass_energy": 13,
    "center_of_mass_energy_units": "TeV",
    "luminosity": 132,
    "luminosity_units": "fb",
}
global _experiment_label_info
_experiment_label_info = _experiment_label_info_defaults.copy()


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
    set_experiment_info(reset=True)
    if isinstance(style, str):
        set_experiment_info(name=style.lower())


def get_style(style=None):
    """
    Set the experiment specific plotting style

    Example:

        >>> import heputils
        >>> heputils.plot.set_style("ATLAS")
        >>> heputils.plot.get_style()["figure.figsize"]
        [8.0, 6.0]
        >>> heputils.plot.get_style("CMS")["figure.figsize"]
        (10.0, 10.0)

    Args:
        style (str): The experiment style string alias

    Returns:
        dict: The style dict requested
    """
    style = dict(plt.rcParams) if style is None else getattr(mplhep.style, style)
    return style


def set_experiment_info(**kwargs):
    """
    Set the experiment level information displayed in the label.

    Example:

        >>> import heputils
        >>> heputils.plot.set_style("ATLAS")
        >>> heputils.plot.set_experiment_info(status="Internal")
        >>> heputils.plot.set_experiment_info(
        ...     center_of_mass_energy=13,
        ...     center_of_mass_energy_units="TeV",
        ...     luminosity=132,
        ...     luminosity_units="fb",
        ... )
        >>> for key, info in heputils.plot.get_experiment_info().items():
        ...     print(f"{key}: {info}")
        ...
        name: atlas
        status: Internal
        center_of_mass_energy: 13
        center_of_mass_energy_units: TeV
        luminosity: 132
        luminosity_units: fb

    Args:
        kwargs (dict): The keyword args used to describe the experiment.
    """
    global _experiment_label_info
    reset = kwargs.pop("reset", False)
    for key in _experiment_label_info.keys():
        if key in kwargs:
            _experiment_label_info[key] = kwargs[key]
    if reset:
        _experiment_label_info = _experiment_label_info_defaults.copy()


def get_experiment_info():
    """
    Retrieve the current experiment level information.

    Example:

        >>> import heputils
        >>> heputils.plot.set_style("ATLAS")
        >>> for key, info in heputils.plot.get_experiment_info().items():
        ...     print(f"{key}: {info}")
        ...
        name: atlas
        status: Internal
        center_of_mass_energy: 13
        center_of_mass_energy_units: TeV
        luminosity: 132
        luminosity_units: fb

    Returns:
        dict: The dictionary of descriptors of the experiment.
    """
    return _experiment_label_info


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


def draw_experiment_label(ax, **kwargs):
    """
    Draw label information to the axes.

    Args:
        ax (`matplotlib.axes.Axes`): The axis object to mutate

    Returns:
        `matplotlib.axes.Axes`: matplotlib axis object
    """
    _horizontal_offset = 0.05
    _vertical_offset = 0.95  # From mplhep

    # TODO: Figure out how to apply only once to avoid drawing multiple times
    label_info = get_experiment_info()
    status = kwargs.pop("status", label_info["status"])
    center_of_mass_energy = kwargs.pop(
        "center_of_mass_energy", label_info["center_of_mass_energy"]
    )
    center_of_mass_energy_units = kwargs.pop(
        "center_of_mass_energy_units", label_info["center_of_mass_energy_units"]
    )
    lumi_info = kwargs.pop("lumi_info", True)
    if lumi_info:
        luminosity = kwargs.pop("luminosity", label_info["luminosity"])
        luminosity_units = kwargs.pop(
            "luminosity_units", label_info["luminosity_units"]
        )
    max_height = kwargs.pop("max_height", None)
    semilogy = kwargs.pop("logy", None)
    density = kwargs.pop("density", False)

    # Make experiment agnostic
    getattr(mplhep, label_info["name"]).label(loc=1, llabel=status, rlabel="", ax=ax)

    label_text_energy = (
        r"$\sqrt{s}=$" + rf"${center_of_mass_energy}~${center_of_mass_energy_units}"
    )
    label_text = label_text_energy
    if lumi_info:
        label_text_lumi = rf"${luminosity}$" + rf"$~{luminosity_units}$" + "$^{-1}$"
        label_text += ", " + label_text_lumi
    _label_text = ax.text(
        _horizontal_offset - 0.01,
        _vertical_offset - 0.08,
        label_text,
        horizontalalignment="left",
        verticalalignment="top",
        transform=ax.transAxes,
    )

    # https://matplotlib.org/tutorials/advanced/transforms_tutorial.html
    bounding_box = _label_text.get_window_extent(
        renderer=ax.figure.canvas.get_renderer()
    )
    bb_label_axes_coords = ax.transAxes.inverted().transform(
        (bounding_box.xmin, bounding_box.ymin)
    )
    if max_height is not None:
        # max_height is in data coordinates, so transform to display coordinates
        # and then transform to axes coordinates
        # 0 used as generic standin, but has no meaning
        display_coords = ax.transData.transform((0.0, max_height))
        axes_coords = ax.transAxes.inverted().transform(display_coords)

        # Scale density plots differently from other semilogy plots
        _scale_factor = 1.7 if semilogy and not density else 1.25
        if _scale_factor * axes_coords[1] > bb_label_axes_coords[1]:
            offset_display_coords = ax.transAxes.transform(
                (
                    axes_coords[0],
                    (_scale_factor * axes_coords[1]) - bb_label_axes_coords[1],
                )
            )
            offset_data_coords = ax.transData.inverted().transform(
                _scale_factor * offset_display_coords
            )
            _current_ylim = ax.get_ylim()[1]
            ax.set_ylim(top=_current_ylim + math.fabs(offset_data_coords[1]))

    return ax


def _max_hist_height(hists, density, stacked=False):
    """
    Determine the maximum entry in a list of histograms.

    Args:
        hists (`lst`): List of histograms
        density (`bool`): If the histograms are density histograms
        stacked (`bool`): If the histograms are stacked histograms

    Returns:
        `float`: The maximum value of any of the given histograms.
    """
    if not isinstance(hists, list):
        hists = [hists]
    if not density:
        if stacked:
            max_hist = max(utils.sum_hists(hists).values())
        else:
            max_hist = max(max(hist.values()) for hist in hists)
    else:
        max_hist = max(max(hist.density()) for hist in hists)
    return max_hist


def _plot_uncertainty(model_hist, ax):
    """
    Plot the model uncertainty as a bar plot

    Args:
        model_hist (`hist.Hist`): The histogram to calculate uncertainty for
        ax (`matplotlib.axes.Axes`): The axis the bar plot is drawn on

    Returns:
        `matplotlib.axes.Axes`: The axis the bar plot is drawn on
    """

    stat_uncert = np.sqrt(model_hist.variances())
    bin_centers = model_hist.axes.centers[0]
    bin_widths = model_hist.axes.widths[0]
    bar_bottom = model_hist.values() - stat_uncert
    # Ensure uncertainties don't extend below 0
    bar_bottom[bar_bottom < 0] = 0
    uncert_label = "Stat Uncertainty"

    ax.bar(
        bin_centers,
        height=2 * stat_uncert,
        width=bin_widths,
        bottom=bar_bottom,
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
        uncert = np.sqrt(hist.values())
    if ax is None:
        ax = plt.gca()

    # get all the kwargs
    color = kwargs.pop("color", "black")
    label = kwargs.pop("label", "Data")
    density = kwargs.pop("density", False)
    if density:
        histtype = "step"
        uncert = False  # histplot treats yerr as iterable or bool
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

    ax = draw_experiment_label(ax, density=density, **kwargs)
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
    if color is not None and len(color) != len(hists):
        color = color[: len(hists)]
    semilogy = kwargs.pop("logy", False)
    _data_hist = kwargs.pop("data_hist", None)
    data_uncert = kwargs.pop("data_uncert", None)
    data_label = kwargs.pop("data_label", "Data")
    density = kwargs.pop("density", True)
    histtype = kwargs.pop("histtype", "fill")
    _default_alpha = 0.1 if histtype == "fill" else None
    alpha = kwargs.pop("alpha", _default_alpha)

    if ax is None:
        ax = plt.gca()

    histplot(
        hists,
        stack=False,
        histtype=histtype,
        density=density,
        yerr=False,
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
        max_hist = _max_hist_height(hists, density)
        ax.set_ylim(top=max_hist * 100)

    # TODO: Avoid drawing twice
    if _data_hist is not None:
        max_hist = max(
            _max_hist_height(hists, density), _max_hist_height(_data_hist, density)
        )
    else:
        max_hist = _max_hist_height(hists, density)
    ax = draw_experiment_label(
        ax, max_height=max_hist, logy=semilogy, density=density, **kwargs
    )

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
    if color is not None and len(color) != len(hists):
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
        ax.set_ylim(top=max(stack_hist.values()) * 100)

    # TODO: Avoid drawing twice
    max_hist = _max_hist_height(hists, density=False, stacked=True)
    ax = draw_experiment_label(ax, max_height=max_hist, **kwargs)

    return _plot_ax_kwargs(ax, **kwargs)


def stack_ratio_plot(hists, **kwargs):
    """
    Stack plot on top, ratio plot on bottom
    """
    fig = kwargs.pop("fig", plt.gcf())

    # Scale figure height to deal with ratio subplot being added
    fig_height_scale = kwargs.pop("fig_height_scale", 1.25)
    _fig_width, _fig_height = get_style()["figure.figsize"]
    fig.set_size_inches(_fig_width, _fig_height * fig_height_scale, forward=True)

    # Setup figure subplot grid and axis dict for hist.plot_ratio
    grid = fig.add_gridspec(2, 1, hspace=0, height_ratios=[3, 1])
    main_ax = fig.add_subplot(grid[0])
    subplot_ax = fig.add_subplot(grid[1], sharex=main_ax)
    ax_dict = {"main_ax": main_ax, "ratio_ax": subplot_ax}

    labels = kwargs.pop("labels", None)
    color = kwargs.pop("color", None)
    if color is not None and len(color) != len(hists):
        color = color[: len(hists)]
    alpha = kwargs.pop("alpha", None)
    semilogy = kwargs.pop("logy", True)
    _data_hist = kwargs.pop("data_hist", None)

    # Setup and plot the ratio plot
    ratio_plot_numerator = kwargs.pop("ratio_numerator", "data")
    ratio_plot_kwargs = {
        "ax_dict": ax_dict,
        "rp_ylim": kwargs.pop("rp_ylim", None),
        "rp_uncertainty_type": kwargs.pop("rp_uncertainty_type", "poisson"),
        "rp_uncert_draw_type": kwargs.pop("rp_uncert_draw_type", "line"),
    }

    num_hists = utils.sum_hists(hists)
    if ratio_plot_numerator.lower() in ["simulation", "sim", "mc"]:
        ratio_plot_kwargs["rp_ylabel"] = kwargs.pop("rp_ylabel", "MC/Data")
        num_hists.plot_ratio(_data_hist, **ratio_plot_kwargs)
    else:
        ratio_plot_kwargs["rp_ylabel"] = kwargs.pop("rp_ylabel", "Data/MC")
        _data_hist.plot_ratio(num_hists, **ratio_plot_kwargs)
    subplot_ax.set_xlabel(kwargs.get("xlabel", None))

    # FIXME: Ugly hack to overwrite ratio plot main axis
    main_ax.clear()
    main_ax = stack_hist(
        hists,
        labels=labels,
        color=color,
        alpha=alpha,
        logy=semilogy,
        data_hist=_data_hist,
        ax=main_ax,
        **kwargs,
    )

    # Hide tick marks of main_ax
    plt.setp(main_ax.get_xticklabels(), visible=False)
    # Trying to get things looking okay
    if semilogy and fig_height_scale < 1.25:
        # Ensure enough space for legend
        main_ax.set_ylim(top=main_ax.get_ylim()[-1] * 100)

    return main_ax, subplot_ax
