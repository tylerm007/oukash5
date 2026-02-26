import json

def parse_sqlserver_json(raw: str) -> list:
    """
    Safely parse SubbmissionMatches which is stored as a Python repr/str() of a
    list of dicts, e.g.:
        [{'companyName': "JP's Delights", 'Id': 1434742, ...}, ...]

    Keys always use single quotes; values that contain a single quote are wrapped
    in double quotes by Python's repr – so a naive s.replace("'", '"') destroys
    those values.  ast.literal_eval handles this format natively.

    Strategy:
      1. json.loads()        – data already stored as proper JSON
      2. ast.literal_eval()  – Python repr format (the common case here)
      3. Warning + []        – nothing worked, return empty list safely
    """
    import ast

    if not raw:
        return []

    # --- attempt 1: already valid JSON -----------------------------------------
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        pass

    # --- attempt 2: Python repr / str() format ---------------------------------
    try:
        result = ast.literal_eval(raw)
        if isinstance(result, list):
            return result
        if isinstance(result, dict):
            return [result]
    except (ValueError, SyntaxError):
        pass