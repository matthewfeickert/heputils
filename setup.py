from setuptools import setup

extras_require = {}
extras_require["lint"] = sorted(set(["pyflakes", "black"]))
extras_require["develop"] = sorted(
    set(
        extras_require["lint"]
        + [
            "check-manifest",
            "pytest~=5.2",
            "pytest-cov~=2.8",
            "pytest-console-scripts~=0.2",
            "bumpversion~=0.5",
            "pre-commit",
            "twine",
        ],
    )
)
extras_require["complete"] = sorted(set(sum(extras_require.values(), [])))

setup(
    extras_require=extras_require,
    entry_points={
        "console_scripts": ["heputils=heputils.commandline:heputils"]
    },
)
