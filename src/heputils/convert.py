"""Convert between different histogram representations"""

import numpy as np
import uproot4 as uproot
import hist
from hist import Hist


def uproot_to_hist(uproot_hist):
    """
    Convert an `uproot` histogram to a `hist` histogram.

    Example:

        >>> import uproot4 as uproot
        >>> import heputils.convert as convert
        >>> root_file = uproot.open("example.root")
        >>> type(root_file["jet_mass"])
        uproot4.dynamic.Model_TH1F_v3
        >>> hist_jet_mass = convert.uproot_to_hist(root_file["jet_mass"])
        >>> type(hout)
        <class 'hist.hist.Hist'>

    Args:
        uproot_hist (hist): An uproot histogram

    Returns:
        hist.Hist.hist: The converted `hist` histogram
    """
    # This is a one liner once a bug is fixed
    # return uproot_hist.to_hist()
    values, edges = uproot_hist.to_numpy()
    _hist = Hist(
        hist.axis.Regular(
            len(edges) - 1, edges[0], edges[-1], name=uproot_hist.all_members["fName"]
        ),
        storage=hist.storage.Double(),
    )
    _hist[:] = values
    return _hist


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
