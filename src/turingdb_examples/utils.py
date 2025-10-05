import re
import pandas as pd


def create_ID_column(df_):
    df = df_.copy()
    df = df.reset_index()
    df = df.rename(columns={"index": "Patient ID"})
    df["Patient ID"] = df["Patient ID"].astype(str)
    max_len = max([len(_) for _ in df["Patient ID"].values])
    df["Patient ID"] = [(max_len - len(id_)) * "0" + id_ for id_ in df["Patient ID"]]

    return df


def get_return_statements(query):
    # Extract everything after RETURN
    match = re.search(r"RETURN\s+(.+)", query, re.IGNORECASE)
    if match:
        return_statement = match.group(1).strip()
        return return_statement.split(", ")
    else:
        print("No RETURN clause found")


def escape_for_cypher(value):
    if pd.isna(value):  # Handle NaN/None
        return ""
    if not isinstance(value, str):
        return str(value)

    # Escape backslashes first (most important!)
    value = value.replace("\\", "\\\\")
    # Escape double quotes
    value = value.replace('"', '\\"')
    # Escape newlines and other control characters
    value = value.replace("\n", "\\n")
    value = value.replace("\r", "\\r")
    value = value.replace("\t", "\\t")

    return value
