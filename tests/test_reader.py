"""Tests for lcl pdf reader"""
#  pylint: disable="missing-function-docstring"
import os
from reader_pdf import extract_df_from_bank_statement


def test_reader_pdf():
    pdf_file = "../data/COMPTEDEDEPOTS_00441082681_20211005.pdf"
    dfd = extract_df_from_bank_statement(pdf_file)
    assert len(dfd) == 25
