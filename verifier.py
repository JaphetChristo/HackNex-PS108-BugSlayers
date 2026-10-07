from app.analysis_engine import percentage_change
def verify_result(actual, expected):
    """
    Compare the actual result with the independently
    calculated expected result.
    """

    if actual == expected:
        return {
            "status": "VERIFIED",
            "actual": actual,
            "expected": expected,
            "message": "The result matches the expected result."
        }

    return {
        "status": "FAILED",
        "actual": actual,
        "expected": expected,
        "message": "The result does not match the expected result."
    }



def verify_columns(df, required_columns):
    """
    Check whether all required columns exist in the dataset.
    """

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        return {
            "status": "FAILED",
            "missing_columns": missing_columns,
            "message": "One or more required columns do not exist."
        }

    return {
        "status": "VERIFIED",
        "missing_columns": [],
        "message": "All required columns exist."
    }


def verify_result_quality(result):
    """
    Check whether an analysis result is usable.
    """

    if result is None:
        return {
            "status": "FAILED",
            "reason": "Result is None"
        }

    if isinstance(result, str) and result.strip() == "":
        return {
            "status": "FAILED",
            "reason": "Result is empty"
        }

    return {
        "status": "VERIFIED",
        "reason": "Result is usable"
    }


def detect_contradiction(df1, df2, id_column, value_column1, value_column2):
    """
    Compare values for matching IDs in two datasets.
    Returns rows where the values are different.
    """

    merged = df1.merge(
        df2,
        on=id_column
    )

    contradictions = merged[
        merged[value_column1] != merged[value_column2]
    ]

    if contradictions.empty:
        return {
            "status": "VERIFIED",
            "contradictions": []
        }

    return {
        "status": "FAILED",
        "contradictions": contradictions.to_dict("records")
    }

def verify_analysis(actual, expected):
    """
    Complete verification of an analysis result.
    """

    quality_check = verify_result_quality(actual)

    if quality_check["status"] == "FAILED":
        return {
            "status": "FAILED",
            "reason": quality_check["reason"]
        }

    result_check = verify_result(actual, expected)

    return {
        "status": result_check["status"],
        "actual": actual,
        "expected": expected,
        "message": result_check["message"]
    }

def verify_total(df, column, expected):
    """
    Calculate the total of a column and verify the result.
    """

    if column not in df.columns:
        return {
            "status": "FAILED",
            "reason": f"Column '{column}' does not exist."
        }

    actual = df[column].sum()

    return verify_analysis(actual, expected)

def verify_average(df, column, expected):
    """
    Calculate the average of a column and verify the result.
    """

    actual = df[column].mean()

    return verify_analysis(actual, expected)
def verify_count(df, column, expected):
    """
    Count values in a column and verify the result.
    """

    actual = df[column].count()

    return verify_analysis(actual, expected)


def verify_minimum(df, column, expected):
    """
    Find the minimum value and verify the result.
    """

    actual = df[column].min()

    return verify_analysis(actual, expected)


def verify_maximum(df, column, expected):
    """
    Find the maximum value and verify the result.
    """

    actual = df[column].max()

    return verify_analysis(actual, expected)

def verify_percentage_change(old_value, new_value, expected):
    """
    Calculate percentage change and verify the result.
    """

    actual = percentage_change(old_value, new_value)

    if actual is None and expected is None:
        return {
            "status": "VERIFIED",
            "actual": actual,
            "expected": expected,
            "message": "Percentage change cannot be calculated because the old value is zero."
        }

    return verify_analysis(actual, expected)
def create_evidence(operation, actual, expected):
    """
    Create a simple evidence record for a verified result.
    """

    result = verify_analysis(actual, expected)

    return {
        "operation": operation,
        "actual": actual,
        "expected": expected,
        "status": result["status"],
        "evidence": f"{operation}: calculated {actual}, expected {expected}"
    }