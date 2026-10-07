import ast


# Names that should not be used in generated analysis code.
BLOCKED_NAMES = {
    "eval",
    "exec",
    "compile",
    "__import__",
    "open",
    "input",
}

# Modules that generated analysis code should not import.
BLOCKED_MODULES = {
    "os",
    "subprocess",
    "socket",
    "requests",
    "shutil",
    "pathlib",
}


def check_code_safety(code):
    """
    Inspect Python code before execution.
    This is a basic first-pass checker, not a secure sandbox.
    """

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {
            "status": "UNSAFE",
            "reason": "The code contains a syntax error."
        }

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name.split(".")[0]

                if module in BLOCKED_MODULES:
                    return {
                        "status": "UNSAFE",
                        "reason": f"Blocked import: {module}"
                    }

        elif isinstance(node, ast.ImportFrom):
            module = (node.module or "").split(".")[0]

            if module in BLOCKED_MODULES:
                return {
                    "status": "UNSAFE",
                    "reason": f"Blocked import: {module}"
                }

        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in BLOCKED_NAMES:
                    return {
                        "status": "UNSAFE",
                        "reason": f"Blocked function: {node.func.id}"
                    }

            if isinstance(node.func, ast.Attribute):
                if node.func.attr.startswith("__"):
                    return {
                        "status": "UNSAFE",
                        "reason": "Blocked special attribute access."
                    }

        elif isinstance(node, ast.Name):
            if node.id.startswith("__"):
                return {
                    "status": "UNSAFE",
                    "reason": "Blocked special name."
                }

    return {
        "status": "SAFE",
        "reason": "No blocked patterns were detected."
    }