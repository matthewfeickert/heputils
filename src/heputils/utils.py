import functools
import operator


def sum_hists(hists):
    """
    Create a histogram from the sum of a list of `hist` histograms.

    Example:

        >>> import numpy as np
        >>> import hist
        >>> import heputils.utils as utils
        >>> np.random.seed(0)
        >>> h1 = hist.Hist(hist.axis.Regular(10, 0, 10), storage=hist.storage.Double())
        >>> h2 = h1.copy()
        >>> h1.fill(np.random.normal(loc=5, scale=1, size=100))
        Hist(Regular(10, 0, 10, label='Axis 0'), storage=Double()) # Sum: 100.0
        >>> h2.fill(np.random.normal(loc=6, scale=2, size=100))
        Hist(Regular(10, 0, 10, label='Axis 0'), storage=Double()) # Sum: 98.0 (100.0 with flow)
        >>> stack_hist = utils.sum_hists([h1, h2])
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
