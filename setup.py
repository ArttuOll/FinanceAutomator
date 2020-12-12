from setuptools import setup

setup(
    name="fina",
    version="0.0.1",
    py_modules="src.finance_automator",
    install_requires=[
        "Click"
    ],
    entry_points="""
    [console_scripts]
    fina=src.finance_automator:cli
    """
)
