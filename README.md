# p2j - Python-to-Jupyter parser with zero intervention
[![PyPI version](https://badge.fury.io/py/p2j.svg)](https://badge.fury.io/py/p2j)

Convert your Python source code to Jupyter notebook ~~with **zero intervention**~~.  
For my use case I prefer having the control of selecting what to convert to a code cell or to a markdown cell.  
Therefore you need to provide cell separators in the form of '## code' or '## markdown'.  
The first cell is always assumed to be a code cell if not specified otherwise.

Convert this source Python file:

```python
# Evaluate the model
model.evaluate()

## markdown
# Run the model for a while.
# Then we hide the model.

##code
run()
hide()

print(type(data))

## markdown
# Multiple paragraphs are possible in a single markdown cell.
# This one has two.

# The data that we are interested in is made of 8x8 images of digits.
# Let's have a look at the first 4 images, which is of course
# stored in the `images` attribute of the dataset.  

## code
images = list(zip(mnist.images))
```

to the following Jupyter notebook:

![example](screenshot.png)

The purpose of this package is to be able to run a code on Jupyter notebook without having to copy each paragraph of the code into every cell. It's also useful if we want to run our code in Google Colab. This parser isn't perfect, but you would be satisfactorily pleased with what you get.

Contents of this README:

- [Installation](#installation)
- [Converting](#converting)
- [Tests](#tests)
- [Requirements](#requirements)
- [Code format](#code-Format)
- [How it works](#how-it-works)
- [Feedback and pull requests](#feedback-and-pull-requests)

## Installation

Clone this repository and run Python's setup.py

```bash
git clone https://github.com/Lun4m/python2jupyter.git
python setup.py install
```

or

```bash
pip install git+https://github.com/Lun4m/python2jupyter#egg=p2j
```

### Converting a Python script

```bash
p2j train.py
```

and you will get a `train.ipynb` Jupyter notebook.

#### Command line usage

To see the command line usage, run `p2j -h` and you will get something like this:

```txt
usage: p2j [-h] [-r] [-t TARGET_FILENAME] [-o] source_filename

Convert a Python script to Jupyter notebook

positional arguments:
  source_filename       Python script to parse

optional arguments:
  -h, --help            show this help message and exit
  -r, --reverse         To convert Jupyter to Python script
  -t TARGET_FILENAME, --target_filename TARGET_FILENAME
                        Target filename of Jupyter notebook. If not specified,
                        it will use the filename of the Python script and
                        append .ipynb
  -o, --overwrite       Flag whether to overwrite existing target file.
                        Defaults to false
```

## Requirements

- Python >= 3.6

No third party libraries are used.

## Tests

Tested on macOS 10.14.3 with Python 3.6.

## Code format

You need to provide *cell separators* in order to tell the parser how to convert your code.  
A *separator* is a line that starts with "##c" or "## c" for code cells, and "##m" or "## m" for markdown cells.  
You can be creative but I suggest to use '## code' or '## markdown'.  

The parser can convert docstring or multiline comments (starting and ending with triple quotes) to markdown cells provided they are preceded by the 
'## markdown' separator.

## How it works

Jupyter notebooks are just JSON files, like below. A Python script is read line by line and a dictionary of key-value pairs is generated along the way, using a set of rules. Finally, this dictionary is dumped as a JSON file whose file extension is `.ipynb`.

```json
{
    "cells": [
        {
            "cell_type": "markdown",
            "execution_count": null,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Import standard functions"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "source": [
                "import os"
            ]
        },
    ],
    "metadata": {},
    "nbformat": 4,
    "nbformat_minor": 2
}
```

There are 4 basic rules (and exceptions) that I follow to parse the Python script.

## Feedback and pull requests

If you do like this, star me maybe? Pull requests are very much encouraged!
