"""Module to get a well formated pandas.DataFrame from a bank statement"""
import re
import pdfplumber
import pandas as pd


def extract_df_from_bank_statement(pdf_file):
    """extract a cleaned up dataframe from LCL bank statement """
    pdf = pdfplumber.open(pdf_file)
    page = pdf.pages[0]

    tables = page.extract_table(
        table_settings={
            "explicit_vertical_lines": [37, 70, 358, 409, 480, 559],
            "snap_x_tolerance": 3,
            "vertical_strategy": "explicit",
            "horizontal_strategy": "text",
        }
    )
    columns = ['DATE', 'LIBELLE', 'VALEUR', 'DEBIT', 'CREDIT']
    date_match = r"\d{2}\.\d{2}"

    first_line, last_line = -1, -1
    for irow, row in enumerate(tables):
        if ((first_line > 0 > last_line) and row[0] != "" and
            re.match(date_match, row[0]) is None):
            last_line = irow
        if row == columns:
            first_line = irow

    dfraw = pd.DataFrame(tables[first_line+1:last_line], columns=columns)

    empty_line = dfraw.apply(
        lambda row: (row==pd.Series([""] * 5, index=columns)).all(), axis=1)
    dfd = dfraw.drop(empty_line[empty_line].index)

    return dfd


if __name__ == "__main__":
    PDF_FILE = "../data/COMPTEDEDEPOTS_00441082681_20211005.pdf"
    print(extract_df_from_bank_statement(PDF_FILE))
