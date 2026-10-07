from app.code_safety import check_code_safety
from app.verifier import verify_analysis


def run_trust_pipeline(code, actual_result, expected_result):
    """
    Run the basic trust pipeline:
    1. Check generated code safety.
    2. Verify the numerical result.
    """

    safety = check_code_safety(code)

    if safety["status"] == "UNSAFE":
        return {
            "status": "FAILED",
            "stage": "CODE SAFETY",
            "reason": safety["reason"]
        }

    verification = verify_analysis(
        actual_result,
        expected_result
    )

    if verification["status"] == "VERIFIED":
        return {
            "status": "VERIFIED",
            "stage": "RESULT VERIFICATION",
            "safety": safety,
            "verification": verification
        }

    return {
        "status": "FAILED",
        "stage": "RESULT VERIFICATION",
        "safety": safety,
        "verification": verification
    }