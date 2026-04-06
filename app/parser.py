def classify_logs(file_path: str):
    logs = {
        "ERROR": [],
        "WARNING": [],
        "INFO": [],
        "OTHER": []
    }

    with open(file_path, "r") as file:
        for line in file:
            line_clean = line.strip()
            line_lower = line.lower()

            if "error" in line_lower:
                logs["ERROR"].append(line_clean)
            elif "warning" in line_lower:
                logs["WARNING"].append(line_clean)
            elif "info" in line_lower:
                logs["INFO"].append(line_clean)
            else:
                logs["OTHER"].append(line_clean)

    return logs

def classify_single_log(line):
    if "ERROR" in line:
        return "ERROR"
    elif "WARNING" in line:
        return "WARNING"
    elif "INFO" in line:
        return "INFO"
    else:
        return "OTHER"