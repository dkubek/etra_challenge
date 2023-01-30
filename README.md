# ETRA Challenge

Data Analysis of the ETRA Dataset.

You can view the render of this report here: 
https://github.com/dkubek/etra-challenge

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

To generate a pdf run
```sh
quarto render etra_challenge.qmd --to pdf
```

The output of these commands will be stored in ``output/``.

## Publishing to github pages

Enter the ``poetry`` environment.

Locally run
```sh
quarto publish gh-pages
```
this will render the report and push the output to branch ``gh-pages``.
