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
            return """SEVERITY: critical
TITLE: App crashes on login with special characters in password
COMPONENT: Authentication Module
REPORTED_BY: Ashan Fernando"""

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