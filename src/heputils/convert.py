"""Convert between different histogram representations"""

import hist
from hist import Hist
import functools
import operator


def uproot_to_hist(uproot_hist):
    """
    Convert an `uproot` histogram to a `hist` histogram.

    Example:

        >>> import uproot4 as uproot
        >>> import heputils.convert as convert
        >>> root_file = uproot.open("example.root") # doctest: +SKIP
        >>> type(root_file["jet_mass"]) # doctest: +SKIP
        uproot4.dynamic.Model_TH1F_v3
        >>> hist_jet_mass = convert.uproot_to_hist(root_file["jet_mass"]) # doctest: +SKIP
        >>> type(hist_jet_mass) # doctest: +SKIP
        <class 'hist.hist.Hist'>

    Args:
        uproot_hist (hist): An uproot histogram

    Returns:
        hist.Hist.hist: The converted `hist` histogram
    """
    # This is a one liner once bug is fixed
    # c.f. https://github.com/scikit-hep/hist/issues/115
    # return uproot_hist.to_hist()
    values, edges = uproot_hist.to_numpy()
    return numpy_to_hist(values, edges)


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


def stack_hists(hists):
    """
    Create a stacked histogram from a list of `hist` histograms.

    Example:

        >>> import numpy as np
        >>> import hist
        >>> import heputils.convert as convert
        >>> np.random.seed(0)
        >>> h1 = hist.Hist(hist.axis.Regular(10, 0, 10), storage=hist.storage.Double())
        >>> h2 = h1.copy()
        >>> h1.fill(np.random.normal(loc=5, scale=1, size=100))
        Hist(Regular(10, 0, 10, label='Axis 0'), storage=Double()) # Sum: 100.0
        >>> h2.fill(np.random.normal(loc=6, scale=2, size=100))
        Hist(Regular(10, 0, 10, label='Axis 0'), storage=Double()) # Sum: 98.0 (100.0 with flow)
        >>> stack_hist = convert.stack_hists([h1, h2])
        >>> print(stack_hist)
                       +-------------------------------------------------------------+
        [-inf,   0) 0  |                                                             |
        [   0,   1) 0  |                                                             |
        [   1,   2) 1  |=                                                            |
        [   2,   3) 3  |===                                                          |
        [   3,   4) 30 |===================================                          |
        [   4,   5) 45 |====================================================         |
        [   5,   6) 52 |============================================================ |
        [   6,   7) 29 |=================================                            |
        [   7,   8) 23 |===========================                                  |
        [   8,   9) 6  |=======                                                      |
        [   9,  10) 9  |==========                                                   |
        [  10, inf) 2  |==                                                           |
                       +-------------------------------------------------------------+

    Args:
        hists (`list`): A list of `hist` histograms

    Returns:
        hist.Hist.hist: The histogram that is the sum of the histograms in the list.
    """
    return functools.reduce(operator.add, hists)
