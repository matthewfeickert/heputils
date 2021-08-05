import hist
import matplotlib.pyplot as plt
import numpy as np
import pytest
from hist import Hist

import heputils


@pytest.fixture
def hist_tuple():
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

    return hist_1, hist_2, hist_3


def test_data_hist_xlabel_passed_through_ax(hist_tuple):
    np.random.seed(0)
    heputils.plot.set_style("ATLAS")

    hists = list(hist_tuple[:2])
    hist_3 = hist_tuple[-1]

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
