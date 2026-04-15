import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv(".env", override=True)

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")


def local_insight(log_line):
    log = log_line.lower()

    insights = []

    if "database" in log:
        insights.append("Possible database connectivity issue. Check service and credentials.")

    if "timeout" in log:
        insights.append("Request timeout detected. Check network latency or system load.")

    if "memory" in log:
        insights.append("High memory usage detected. Consider scaling or checking leaks.")

    if "refused" in log:
        insights.append("Connection refused. Verify target service is running and reachable.")

    if not insights:
        return "No specific issue detected. Review logs for context."

    return " ".join(insights)


def generate_insight(log_line):
    if not api_key:
        return local_insight(log_line)
    try:
        prompt = f"""
You are a DevOps assistant.
Analyze this log and give likely cause + recommended fix briefly.

Log: {log_line}
"""
        response = model.generate_content(
            prompt,
            request_options={"timeout": 5}
        )
        return response.text.strip()

    except Exception:
        return local_insight(log_line)