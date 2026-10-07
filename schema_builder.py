def build_schema(df):
    schema = "Columns:\n"

    for column in df.columns:
        data_type = str(df[column].dtype)

        schema += f"- {column}: {data_type}\n"

    return schema