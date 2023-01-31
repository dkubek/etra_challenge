# ETRA Challenge

Data Analysis of the ETRA Dataset.

You can view the render of this report here: 
https://dkubek.github.io/etra_challenge/

## Setup

Firstly, you need to have [poetry](https://python-poetry.org/docs/) installed.
```sh
curl -sSL https://install.python-poetry.org | python3 -
```

Then setup the environment by running
```sh
poetry install
```

Finally, enter the environment with
```sh
poetry shell
```

## Generating report

Firstly, install [Quarto](https://quarto.org/docs/get-started/index.html) and
enter the poetry environment with all dependencies installed (``publish`` group
is sufficient).

To generate an html report run
```sh
quarto render etra_challenge.qmd --to html
```

To generate a pdf first make sure you have TeX installed. You can use
``sh
quarto install tinytex
``
Note that this is not installed in the ``PATH`` and does not affect your global
tex.

Now render with:
```sh
quarto render etra_challenge.qmd --to pdf
```

The output of these commands will be stored in ``output/``.

To convert the report to a jupyter notebook see [Converting Notebooks](https://quarto.org/docs/tools/jupyter-lab.html#converting-notebooks).

## Publishing to github pages

Enter the ``poetry`` environment.

Locally run
```sh
quarto publish gh-pages
```
this will render the report and push the output to branch ``gh-pages``.
