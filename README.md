### Overview
This is a python project that contains custom indicators, strategies, and helpers to backtest trading the financial markets.
We are using [backtrader](https://www.backtrader.com) as the main backtesting library.

### Installation
The recommended method is using [poetry](https://python-poetry.org)
```
poetry install
```

If you want to install using your own tools, the depencies are:

```
backtrader = {extras = ["plotting"], version = "^1.9.76"}
matplotlib = "3.2.2"
texttable = "^1.6.3"
```

### Usage
It is recommended you run using poetry because it keeps track of your .venv
`poetry run python main.py`

If not, you will have to make sure that the dependencies are available in your python env.