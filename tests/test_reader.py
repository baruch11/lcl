"""Tests for lcl pdf reader"""
#  pylint: disable="missing-function-docstring"
import os
import pprint
from reader_pdf import extract_df_from_bank_statement, select_table_lines


def test_reader_pdf():
    dirname = os.path.dirname(__file__)
    pdf_file = os.path.join(dirname, "../data",
                            "RLV_00441082681V_20211005.pdf")
    dfd = extract_df_from_bank_statement(pdf_file)
    assert len(dfd) == 32


def test_select_lines():
    table = [['', '', '', '', ''],
             ['ECRIT', 'URES DE LA PERIODE', '', '', ''],
             ['', '', '', '', ''],
             ['DATE', 'LIBELLE', 'VALEUR', 'DEBIT', 'CREDIT'],
             ['', '', '', '', ''],
             ['03.09', 'ANCIEN SOLDE', '', '', '59 348,40'],
             ['', '', '', '', ''],
             ['06.09', 'CB GOOGLE GOOGLE S 04/09/21', '06.09.21', '1,99', ''],
             ['', '', '', '', ''],
             ['', 'LONDON EUR 1,99', '', '', ''],
             ['', '', '', '', ''],
             ['06.09', 'CB SC-REST.PICOTTE 03/09/21', '06.09.21', '28,50', ''],
             ['07.09', 'CB Tipeee 06/09/21', '07.09.21', '8,21', ''],
             ['08.09', 'CB MK2 QUAI SEINE 06/09/21', '08.09.21', '12,20', ''],
             ['08.09', 'CB VELIB METROPOLE 03/09/21', '08.09.21', '11,10', ''],
             ['15.09', 'VIREMENT Marco Chev', '15.09.21', '75,00', ''],
             ['', '', '', '', ''],
             ['', 'seance 15 sept', '', '', ''],
             ['', '', '', '', ''],
             ['', '', '', '', ''],
             ['', '', '', '', 'Page 1 / 3'],
             ['', '', '', '', ''],
             ['Crédit Ly',
              'onnais-SA au capital de 2 037 713 591 euros',
              '18 rue de la R',
              'épublique 69002 Lyo',
              'n - N° ORIAS 07 00 1']]
    expected_table = [
        ['03.09', 'ANCIEN SOLDE', '', '', '59 348,40'],
        ['06.09', 'CB GOOGLE GOOGLE S 04/09/21\nLONDON EUR 1,99', '06.09.21',
         '1,99', ''],
        ['06.09', 'CB SC-REST.PICOTTE 03/09/21', '06.09.21', '28,50', ''],
        ['07.09', 'CB Tipeee 06/09/21', '07.09.21', '8,21', ''],
        ['08.09', 'CB MK2 QUAI SEINE 06/09/21', '08.09.21', '12,20', ''],
        ['08.09', 'CB VELIB METROPOLE 03/09/21', '08.09.21', '11,10', ''],
        ['15.09', 'VIREMENT Marco Chev\nseance 15 sept', '15.09.21', '75,00',
         '']]
    columns = ['DATE', 'LIBELLE', 'VALEUR', 'DEBIT', 'CREDIT']
    assert select_table_lines(table, columns) == expected_table
