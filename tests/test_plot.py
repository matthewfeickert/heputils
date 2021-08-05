import hist

# from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from hist import Hist

import heputils

heputils.plot.set_style("ATLAS")


def test_xlabel_passed_through_ax():
    np.random.seed(0)

    hist_1 = Hist(
        hist.axis.Regular(
            50, -5, 5, name="x", label="x [units]", underflow=False, overflow=False
        ),
        storage=hist.storage.Weight(),
    ).fill(np.random.normal(size=1000), weight=1.0)
    hist_2 = Hist(
        hist.axis.Regular(
            50, -5, 5, name="x", label="x [units]", underflow=False, overflow=False
        ),
        storage=hist.storage.Weight(),
    ).fill(np.random.normal(size=1000), weight=1.0)
    hist_3 = Hist(
        hist.axis.Regular(
            50, -5, 5, name="x", label="x [units]", underflow=False, overflow=False
        ),
        storage=hist.storage.Weight(),
    ).fill(np.random.normal(size=1000), weight=1.0)

    hists = [hist_1, hist_2]

    fig, ax = plt.subplots()
    ax = heputils.plot.stack_hist(
        hists,
        xlabel="test_label",
        ylabel="Count",
        ax=ax,
    )
    assert ax.get_xlabel() == "test_label"
    ax = heputils.plot.data_hist(hist_3, ax=ax)
    assert ax.get_xlabel() == "test_label"
