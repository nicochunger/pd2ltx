"""
AUTHOR : Khaled Al Moulla & Nicolas Unger
DATE   : 2022-01-01 (updated on 2022-10-18)

Convert Pandas DataFrame to a LaTeX Table with error bars.
"""

# MODULES

import numpy as np
import pandas as pd

# FUNCTION


def pd2ltx(
    df,
    sort_column=None,
    sort_ascending=True,
    error=None,
    error_suffix=None,
    error_significant_figures=1,
    **kwargs,
):
    """
    Function that convert a Pandas DataFrame to a latex table but including useful features
    realted for values with error bars.
    This functions allow to add columns with the errors of your value columns. These errors will be
    formatted to show in latex as $ value \pm error $ for symmetrical errors and as
    $ value ^{+errup}_{-errlo} $ for assymetrical errors.
    The error columns labels have to have the exact same name as their corresponding value
    columns followed by a chosen suffix. For assymetrical errors the suffix for upper and lower
    bound errors have to have their own suffix (e.g. 'errup' and 'errlo').

    Make sure the dtypes of your columns are set correctly as it will interpret all 'object' type
    columns as string columns and thus show them as is.

    To stylyse the table you can pass along any keyword accepted by the
    pandas.io.formats.style.Styler.to_latex() function. Only column_format and siunitx are set by
    default to column_format with string columns aligned left and value columns center aligned and
    siunitx set to True to support math operations inside the cells.
    For example you can pass 'hrules=True' to add \toprule, \midrule and \bottomrule to the table.
    Or pass 'buf=<file name>' to export the table to a file instead of returning the string or
    set a caption with the 'caption' keyword.

    Parameters
    ----------
    df : Pandas DataFrame
        The Pandas DataFrame with the data that want to be shown on a latex table
    caption : str, tuple, optional
        If string, the LaTeX table caption included as: \caption{<caption>}.
        If tuple, i.e (“full caption”, “short caption”), the caption included as:
        \caption[<caption[1]>]{<caption[0]>}.
    sort_column : str, optional
        On which column the table should be sorted. If not specified, the table is left as is.
    sort_ascending : bool, optional
        If the sort is ascending or descending. This parameter and sort_column are directly
        passed to the pd.DataFrame.sort_values() function, so it supports multiple column sort
        as well.
    error : str, optional
        If you want to show values with error bars, here you indicate what type of errors they are.
        'symmetrical' for symmetrical and 'assymetrical' for assymetrical errors.
    error_suffix : str, list, optional
        The suffix that is used to find the corresponding error column for the value columns.
        A simple string for symmetrical errors, or a list of length 2 with the suffixes of
        the upper and lower errors respectively.
    error_significant_figures: int, default 1
        To how many significant figures should the errors be rounded to.
    **kwargs : dict
        Pass along to pandas.io.formats.style.Styler.to_latex()


    Returns
    -------
    latex_table : str
        A string with the table in Latex format. You have to print it to be able to copy
        it directly to a LaTex document.
    """

    # Nr. of rows and columns
    Nrow, Ncol = df.shape

    # Check that the input is DataFrame
    assert isinstance(df, pd.DataFrame), "df has to be of type pandas.DataFrame"
    assert isinstance(error_significant_figures, int), "error_significant_figures has to be an int"

    # Extract name of columns
    labels = df.columns

    # Index of string, variable and error columns
    # Get columns whose values are strings
    str_idx = np.nonzero(df.dtypes.values == np.dtype("O"))[0]
    # Get the columns that are errors
    if error == "symmetrical":
        err_idx = np.nonzero(labels.str.contains(error_suffix))[0]
    elif error == "asymmetrical":
        err_idx = np.nonzero(
            labels.str.contains(error_suffix[0]) | labels.str.contains(error_suffix[1])
        )[0]
    elif error is None:
        err_idx = np.array([])
    else:
        raise ValueError(f"Unsupported value for 'error': {error}")

    # Get the columns with the main values as the inverse group of the other two
    var_idx = np.delete(np.arange(len(labels)), np.concatenate([str_idx, err_idx]))

    # DataFrame: Sort
    if sort_column is not None:
        df = df.sort_values(by=sort_column, ascending=sort_ascending)

    # Construct LaTeX table DataFrame
    ltdf = df.copy(deep=True)
    for i in range(Nrow):
        for j in var_idx:
            # Figure out minimum decimal to round to between value and its errors
            if error == "symmetrical":
                err_cols = np.array([df.loc[i, labels[j] + error_suffix]])
            elif error == "asymmetrical":
                err_cols = (
                    df.loc[i, [labels[j] + error_suffix[c] for c in range(2)]].astype(float).values
                )

            # Figure out minimum order of magnitude of the errors
            dec = int(-1 * np.min(np.floor(np.log10(np.abs(err_cols)))))

            # Round and convert to strings
            significant_figures = dec + error_significant_figures - 1
            strval = f"{df.iloc[i, j]:.{significant_figures}f}"
            if error == "symmetrical":
                errpm = err_cols[0]
                strrep = f"${strval}\pm{errpm:.{significant_figures}f}$"
            elif error == "asymmetrical":
                errup, errlo = err_cols
                # Check if errup and errlo are within 5% and consider them equal using \pm
                if np.abs(errup - errlo) / errlo < 0.05:
                    errpm = np.mean([errup, errlo])
                    strrep = f"${strval}\pm{errpm:.{significant_figures}f}$"
                else:
                    strerrup = f"{errup:.{significant_figures}f}"
                    strerrlo = f"{errlo:.{significant_figures}f}"
                    strrep = f"${strval}^{{+{strerrup}}}_{{-{strerrlo}}}$"
            ltdf.iloc[i, j] = strrep
    ltdf = ltdf.drop(ltdf.columns[err_idx], axis=1)

    # Column Format. l for text column, c for numeric columns
    cols_order = np.argsort(np.concatenate([str_idx, var_idx]))
    col_arr = np.array(["l"] * len(str_idx) + ["c"] * len(var_idx))[cols_order]
    column_format = "".join(col_arr)

    latex_table = ltdf.style.hide(axis="index").to_latex(
        siunitx=True, column_format=column_format, **kwargs
    )

    return latex_table
