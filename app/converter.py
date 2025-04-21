import zipfile
import pandas as pd
import json
import os

def build_json(region_row: pd.Series, states_df: pd.DataFrame):
    indicator_title = region_row["Indicadores (cor laranja)"].strip()
    subtitle = region_row["Descrição"]
    value = region_row["Valor_Nordeste"]
    note = region_row["Fonte"]
    panel = region_row["Painel"]
    link = region_row["Link"]

    data = {
        "region": {
            "name": "Nordeste",
            "title": indicator_title,
            "subtitle": subtitle,
            "data": value,
            "note": note,
            "link": link
        },
        "states": []
    }

    for _, state in states_df.iterrows():
        state_name = state["Estado"]
        indicator_column = next(
            (col for col in states_df.columns if col.strip().lower() == indicator_title.strip().lower()), None
        )

        if not indicator_column:
            continue

        data["states"].append({
            "name": state_name,
            "data": state[indicator_column],
            "note": note,
            "link": link
        })

    return data

def convert_excel_to_json(file_path: str, json_folder: str) -> str:
    sheets = pd.read_excel(file_path, sheet_name=None)
    region_df = list(sheets.values())[0]
    states_df = list(sheets.values())[1]

    zip_file_path = os.path.join(json_folder, 'generated_json.zip')
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for _, row in region_df.iterrows():
            data = build_json(row, states_df)
            filename = row["Indicadores (cor laranja)"].strip().lower().replace(" ", "_") + ".json"

            with zipf.open(filename, 'w') as json_file:
                json_file.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))

    return zip_file_path
