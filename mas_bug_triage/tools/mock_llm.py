class OllamaLLM:
    def __init__(self, model=None):
        self.model = model

    def invoke(self, prompt):
        p = prompt.lower()

        if "severity" in p:
            return "CRITICAL"
        elif "analysis" in p:
            return "The issue is caused by improper input handling or missing validation."
        elif "fix" in p:
            return "Add proper validation, null checks, and error handling."
        else:
            return "Generated structured response."