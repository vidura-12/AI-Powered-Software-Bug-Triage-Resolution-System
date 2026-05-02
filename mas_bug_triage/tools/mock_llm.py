class OllamaLLM:
    def __init__(self, model=None):
        self.model = model

    def invoke(self, prompt):
        p = prompt.lower()

        # -------------------------------
        # Agent 1: Classifier
        # UNIQUE: "structured classification"
        # -------------------------------
        if "structured classification" in p:

            # Detect severity from actual prompt content
            if any(word in p for word in [
                "crash", "crashes", "data loss", "deleted", "wipe",
                "security breach", "permanently", "500 error",
                "unhandled exception", "security"
            ]):
                severity = "critical"
            elif any(word in p for word in [
                "fails", "timeout", "not working", "cannot",
                "broken", "throws", "error", "exception"
            ]):
                severity = "major"
            else:
                severity = "minor"

            # Extract title
            title = "unknown"
            for line in prompt.splitlines():
                line = line.strip()
                if line.lower().startswith("title:"):
                    title = line.split(":", 1)[1].strip()
                    break

            # Extract component
            component = "unknown"
            for line in prompt.splitlines():
                line = line.strip()
                if line.lower().startswith("component:"):
                    component = line.split(":", 1)[1].strip()
                    break

            # Extract reporter
            reported_by = "unknown"
            for line in prompt.splitlines():
                line = line.strip()
                if line.lower().startswith("reported by:"):
                    reported_by = line.split(":", 1)[1].strip()
                    break

            return (
                f"SEVERITY: {severity}\n"
                f"TITLE: {title}\n"
                f"COMPONENT: {component}\n"
                f"REPORTED_BY: {reported_by}\n"
            )

        # -------------------------------
        # Agent 2: Analyser
        # UNIQUE: "expert software debugger"
        # -------------------------------
        elif "expert software debugger" in p:
            return """ROOT_CAUSE: Crash occurs due to missing validation for special characters in password input (line 12)
BUGGY_LINES: 12
CONFIDENCE: high"""

        # -------------------------------
        # Agent 3: Fix Suggestion
        # UNIQUE: "suggest a precise fix"
        # -------------------------------
        elif "suggest a precise fix" in p:
            return """FIX:
Add validation to sanitize special characters before processing login.

CODE:
if not password.isalnum():
    raise ValueError("Invalid characters in password")
"""

        # -------------------------------
        # Agent 4: Reporter
        # -------------------------------
        else:
            return """Summary:
Application crashes when special characters are used.

Severity Explanation:
This is a critical issue because it causes a full system crash.

Root Cause:
Missing validation for user input.

Fix Recommendation:
Add input sanitization.

Conclusion:
Fixing this issue improves reliability and prevents crashes."""