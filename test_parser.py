from app.parser import extract_errors

with open(r"C:\Users\Aditya Gaur\Downloads\.vscode\ci_cd_ai_analyzer\logs\sample.log", "r") as f:
    logs = f.read()

print("LOG CONTENT:")
print(logs)

errors = extract_errors(logs)

print("\nExtracted Errors:")
for e in errors:
    print(e)