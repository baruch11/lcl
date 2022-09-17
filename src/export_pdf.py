"""main script to export bank statements """
import os
import pickle
from tqdm import tqdm
from reader_pdf import extract_df_from_bank_statement


INPUT_PATH = os.path.join(os.path.dirname(__file__), "../data")
OUTPUT_PATH = os.path.join(INPUT_PATH, "dataframes")

if __name__ == "__main__":
    for elt in tqdm(os.scandir(INPUT_PATH)):
        if elt.is_file() and os.path.splitext(elt.name)[-1] == ".pdf":
            df_extract = extract_df_from_bank_statement(elt.path)
            pkl = os.path.join(OUTPUT_PATH,
                               os.path.splitext(elt.name)[0] + ".pkl")
            with open(pkl, "wb") as pklout:
                pickle.dump(df_extract, pklout)
