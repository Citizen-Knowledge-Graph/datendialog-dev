import pandas as pd

# downloaded from https://www.statistikportal.de/de/veroeffentlichungen/anschriftenverzeichnis
EXCEL_FILE = "data/0/Anschriften_der_Gemeinde_und_Stadtverwaltungen_Stand_31012023_final.xlsx"

df = pd.read_excel(EXCEL_FILE, sheet_name="Anschriften_31_01_2023")
column = df.iloc[:, 5]  # column F

# 7 is when the first ARS starts
column.iloc[7:].dropna().to_csv("data/0/ars.csv", index=False, header=False)
