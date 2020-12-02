# heputils

[![GitHub Project](https://img.shields.io/badge/GitHub--blue?style=social&logo=GitHub)](https://github.com/matthewfeickert/heputils)
[![GitHub Actions Status: CI](https://github.com/matthewfeickert/heputils/workflows/CI/badge.svg?branch=master)](https://github.com/matthewfeickert/heputils/actions?query=workflow%3ACI+branch%3Amaster)
[![Code Coverage](https://codecov.io/gh/matthewfeickert/heputils/graph/badge.svg?branch=master)](https://codecov.io/gh/matthewfeickert/heputils?branch=master)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/matthewfeickert/heputils/master.svg)](https://results.pre-commit.ci/latest/github/matthewfeickert/heputils/master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/matthewfeickert/heputils/HEAD?urlpath=lab/tree/examples/dev-example.ipynb)

[![PyPI version](https://badge.fury.io/py/heputils.svg)](https://badge.fury.io/py/heputils)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/heputils.svg)](https://pypi.org/project/heputils/)

Helper utilities around the [Scikit-HEP ecosystem][Scikit-HEP] for common tasks in HEP

**This library is not meant for wide use and will probably be deprecated in favor of a Scikit-HEP library soon.**
This library should be viewed as a testing grounds for API design decisions.

## Installation

In a fresh virtual environment you can install from PyPI with

```
python -m pip install heputils
```

### Development releases

If you want to install _unsupported_ development releases you can do so from TestPyPI.
**First** install `heputils` like normal from PyPI to get stable releases of all dependencies

```
python -m pip install heputils
```

**then** install the development release of `heputils` from TestPyPI with the following

```
python -m pip install --upgrade --extra-index-url https://test.pypi.org/simple/ --pre heputils
```

which will get the release on TestPyPI that corresponds to the most recent commit on `master`.

You can of course also install directly from the Git repository "locally" by first cloning the repo and then from the top level of it running

```
python -m pip install .
```

## Contributing

As this library is experimental contributions of all forms are welcome.
If you have ideas on how to improve the API or conceptually how a library meant to introduce people to the Scikit-HEP ecosystem should be structured please open an Issue.
You are of course also most welcome and encouraged to open PRs.

### Developing

To develop, use a virtual environment.
Once the environment is activated, clone the repo from GitHub

```
git clone git@github.com:matthewfeickert/heputils.git
```

and install all necessary packages for development

```
python -m pip install --ignore-installed --upgrade --editable .[complete]
```

Then setup the Git pre-commit hooks by running

```
pre-commit install
```

## Acknowledgements

This library is built upon the hard work of many people in the [Scikit-HEP ecosystem][Scikit-HEP] and is only possible because of the exchange of ideas and contributions of people working together, across experiments and fields to improve science.
This is not an inevitability, but rather the result of directed thought, time, and effort, to which I am most thankful to have benefited from and have been involved in.

## Requests

Cite the software you use in your papers.

[Scikit-HEP]: https://scikit-hep.org/
