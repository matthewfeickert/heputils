"""Convert between different histogram representations"""

import hist
from hist import Hist


def uproot_to_hist(uproot_hist):
    """
    Convert an `uproot` histogram to a `hist` histogram.
    DEPRECATION: This should now longer be needed as of `heputils` `v0.0.6` and
    will be removed in a later version of `heputils`.

    Example:

        >>> import uproot
        >>> import heputils.convert as convert
        >>> root_file = uproot.open("example.root") # doctest: +SKIP
        >>> type(root_file["jet_mass"]) # doctest: +SKIP
        uproot.dynamic.Model_TH1F_v3
        >>> hist_jet_mass = convert.uproot_to_hist(root_file["jet_mass"]) # doctest: +SKIP
        >>> type(hist_jet_mass) # doctest: +SKIP
        <class 'hist.hist.Hist'>

    Args:
        uproot_hist (hist): An uproot histogram

    Returns:
        hist.Hist.hist: The converted `hist` histogram
    """
    return uproot_hist.to_hist()


def uproot_to_numpy(uproot_hist):
    """
    Convert an `uproot` histogram to a `numpy` histogram.

    Args:
        uproot_hist (hist): An uproot histogram

    Returns:
        Tuple of NumPy arrays: The converted `numpy` histogram
    """
    # return values, edges
    return uproot_hist.to_numpy()


def numpy_to_hist(values, edges, name=None):
    """
    Convert a `numpy` histogram to a `hist` histogram.

    Args:
        values (array): The bin counts
        edges (array): The bin edges
        name (str): The name of the histogram axis

    Returns:
        hist.Hist.hist: The converted `hist` histogram
    """
    _hist = Hist(
        hist.axis.Regular(len(edges) - 1, edges[0], edges[-1], name=name),
        storage=hist.storage.Double(),
    )
    _hist[:] = values
    return _hist
