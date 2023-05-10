# pd2ltx
Small package that solves a specific problem of converting a pandas DataFrame with numerical values and their uncertainties to a LaTex table that correctly formats these uncertainties for each parameter. It has support for symmetrical or assymetrical errors.

Please look at the example to understand how it works.


## Instalation instructions

Simply run the following command in your terminal

`pip install -i https://test.pypi.org/simple/ pd2ltx`

## Features

takes a Pandas DataFrame as input and converts it to a formatted LaTeX table string with support for error bars. The generated LaTeX table can be used directly in a LaTeX document. The function has various options to customize the table, including sorting, error bar formatting, and styling options.

Here is a summary of the main features and functionalities of the pd2ltx function:

- It takes a Pandas DataFrame and converts it to a LaTeX table.
- It supports sorting the table by a specified column, either ascending or descending.
- It handles error bars for data columns, allowing for either symmetrical or asymmetrical error representation.
- It formats the error bars in LaTeX notation, either as `$value \pm error$` for symmetrical errors or as `$value ^{+errup}_{-errlo}$` for asymmetrical errors.
- It rounds the values and their corresponding errors to the specified number of significant figures.
- It ensures that the data types of the DataFrame columns are set correctly, interpreting 'object' type columns as string columns.
- It allows customization of the table's style by passing additional keyword arguments accepted by the pandas.io.formats.style.Styler.to_latex() function.
- The generated LaTeX table string can be printed and directly copied into a LaTeX document.

## Example

Here's an example of how to use the `pd2ltx` function:

```
import pandas as pd
import numpy as np
from pd2ltx import pd2ltx  # Assuming pd2ltx is defined in the module named pd2ltx

# Create a sample DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'Dave'],
    'Score': [95.123, 87.456, 91.789, 83.012],
    'Score_err': [0.123, 0.456, 0.789, 1.012],
    'Height': [1.68, 1.82, 1.77, 1.90],
    'Height_err': [0.02, 0.03, 0.02, 0.01],
}

df = pd.DataFrame(data)

# Use the function
latex_table = pd2ltx(
    df,
    sort_column='Score',
    sort_ascending=False,
    error='symmetrical',
    error_suffix='_err',
    error_significant_figures=2,
)

# Print the LaTeX table
print(latex_table)

```

This script creates a sample DataFrame with four columns: 'Name', 'Score', 'Score_err', and 'Height'. The 'Score_err' column represents the symmetrical errors for the 'Score' values.

The `pd2ltx` function is called with this DataFrame, and additional parameters are provided to sort the DataFrame by the 'Score' column in descending order, to specify that the errors are symmetrical, to define the suffix used to identify error columns, and to specify that errors should be rounded to two significant figures.

The resulting LaTeX table is printed to the console, and can be directly copied into a LaTeX document.

Please note that the exact formatting and appearance of the LaTeX table can depend on the specific LaTeX environment and packages you are using in your LaTeX document.