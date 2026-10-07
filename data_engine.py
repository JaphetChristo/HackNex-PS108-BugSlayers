import pandas as pd
from pathlib import Path


def load_dataset(file_path):
    """
    Load a CSV or Excel dataset.

    Returns:
        pandas.DataFrame
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = file_path.suffix.lower()

    if extension == ".csv":
        df = pd.read_csv(file_path)

    elif extension in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)

    else:
        raise ValueError(
            "Unsupported file type. Please upload a CSV or Excel file."
        )

    return df


def inspect_dataset(df):
    """
    Analyze the basic structure and quality of a dataset.

    Returns:
        dictionary containing dataset information
    """

    # Basic information
    rows = df.shape[0]
    columns = df.shape[1]

    # Column names
    column_names = df.columns.tolist()

    # Data types
    data_types = {
        column: str(dtype)
        for column, dtype in df.dtypes.items()
    }

    # Missing values
    missing_values = df.isnull().sum()

    missing_values_dict = {
        column: int(count)
        for column, count in missing_values.items()
        if count > 0
    }

    # Total missing values
    total_missing = int(df.isnull().sum().sum())

    # Duplicate rows
    duplicate_rows = int(df.duplicated().sum())

    # Numerical columns
    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    # Text/categorical columns
    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    return {
        "rows": rows,
        "columns": columns,
        "column_names": column_names,
        "data_types": data_types,
        "missing_values": missing_values_dict,
        "total_missing_values": total_missing,
        "duplicate_rows": duplicate_rows,
        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns,
    }


def get_preview(df, number_of_rows=5):
    """
    Return the first few rows of the dataset.
    """

    return df.head(number_of_rows)


def get_basic_statistics(df):
    """
    Generate basic statistics for numerical columns.
    """

    if len(df.select_dtypes(include="number").columns) == 0:
        return None

    return df.describe()


def print_dataset_report(df):
    """
    Print a human-readable dataset report.
    """

    information = inspect_dataset(df)

    print("\n" + "=" * 50)
    print("VERITAS DATASET REPORT")
    print("=" * 50)

    print(f"\nRows: {information['rows']}")
    print(f"Columns: {information['columns']}")

    print("\nColumn names:")
    for column in information["column_names"]:
        print(f"  - {column}")

    print("\nData types:")
    for column, dtype in information["data_types"].items():
        print(f"  - {column}: {dtype}")

    print("\nMissing values:")

    if information["missing_values"]:
        for column, count in information["missing_values"].items():
            print(f"  - {column}: {count}")
    else:
        print("  None")

    print(
        f"\nTotal missing values: "
        f"{information['total_missing_values']}"
    )

    print(
        f"Duplicate rows: "
        f"{information['duplicate_rows']}"
    )

    print("\nNumerical columns:")
    for column in information["numerical_columns"]:
        print(f"  - {column}")

    print("\nCategorical columns:")
    for column in information["categorical_columns"]:
        print(f"  - {column}")

    print("\n" + "=" * 50)
    print("FIRST 5 ROWS")
    print("=" * 50)

    print(get_preview(df))

    print("\n" + "=" * 50)
    print("BASIC STATISTICS")
    print("=" * 50)

    statistics = get_basic_statistics(df)

    if statistics is not None:
        print(statistics)
    else:
        print("No numerical columns found.")

    print("\n" + "=" * 50)


# ---------------------------------------------------------
# TESTING
# ---------------------------------------------------------

if __name__ == "__main__":

    # Change this to your test dataset
    FILE_PATH = "../data/sales_clean.csv"

    try:

        # Load dataset
        dataframe = load_dataset(FILE_PATH)

        # Print report
        print_dataset_report(dataframe)

    except Exception as error:

        print("\nERROR:")
        print(error)