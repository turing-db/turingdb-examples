def create_ID_column(df_):
    df = df_.copy()
    df = df.reset_index()
    df = df.rename(columns={"index": "Patient ID"})
    df["Patient ID"] = df["Patient ID"].astype(str)
    max_len = max([len(_) for _ in df["Patient ID"].values])
    df["Patient ID"] = [(max_len - len(id_)) * "0" + id_ for id_ in df["Patient ID"]]

    return df
