"""Module to get a well formated pandas.DataFrame from a bank statement"""
import re
import pdfplumber
import pandas as pd


def extract_df_from_bank_statement(pdf_file):
    """extract a cleaned up dataframe from LCL bank statement
    Args:
        pdf_file (str): full path of the pdf of the bank statement
    Returns:
        pd.DataFrame
    """
    pdf = pdfplumber.open(pdf_file)

    return pd.concat([extract_df_one_page(page) for page in pdf.pages]
                     ).reset_index(drop=True)


def extract_df_one_page(page):
    """Extract main bank statement table
    Assuming that page comes from a lcl bank statement

    Args:
        page: pdfplumber.page.Page
    """

    table = page.extract_table(
        table_settings={
            "explicit_vertical_lines": [37, 70, 358, 409, 483, 559],
            "snap_x_tolerance": 3,
            "vertical_strategy": "explicit",
            "horizontal_strategy": "text",
        }
    )
    columns = ['DATE', 'LIBELLE', 'VALEUR', 'DEBIT', 'CREDIT']

    dfret = pd.DataFrame(select_table_lines(table, columns),
                         columns=columns)
    dfret[['DEBIT', 'CREDIT']] = dfret[['DEBIT', 'CREDIT']].apply(
        amount_to_float, axis=1)
    dfret.VALEUR = dfret.VALEUR.apply(
        lambda x: None if x == '' else pd.to_datetime(x, format='%d.%m.%y'))

    return dfret


def select_table_lines(table, columns):
    """From pdfplumber output to relevant bank statement lines
    also merge libellé on multiple lines

    Args:
        table (list of list of string) : pdfplumber extract_table output
    Returns:
        list of list of string
    """

    ret = []
    start_select, stop_select = False, False
    for row in table:
        # use date format and money amount to detect table boundaries
        not_a_date = (row[0] != "" and
                      re.match(r"\d{2}\.\d{2}", row[0]) is None)
        pattern_amount = re.compile("[0-9 ,]*")

        #  special cases lcl
        if row[-1] == '.':  # "tenue de compte"
            row[-1] = ''
        if row[-2] == '.':  # '.' in DEBIT
            row[-2] = ''
        if row[1] == "TOTAUX" or "SOLDE INTERMEDIAIRE" in row[1]:
            continue

        not_amount = pattern_amount.fullmatch(row[-1]) is None
        if start_select and (not_a_date or not_amount):
            stop_select = True
        if start_select and not stop_select and row != [""] * len(columns):
            # detect multiple line libelle and merge with previous one
            if row[0] == "":
                ret[-1][1] = "\n".join([ret[-1][1], row[1]])
                continue
            ret.append(row)

        if row == columns:
            start_select = True

    return ret


def amount_to_float(s_amount):
    """Transform money amount (str) in float"""
    def _amount_to_float(amount):
        """ '12 345,4' -> 12345.4 (float)"""
        if amount == '':
            return None
        return float(amount.replace(" ", "").replace(",", "."))
    return s_amount.apply(_amount_to_float)

