def detect_patterns(prompt: str):
    patterns = {
        "identity_hijack": ["act as", "pretend to be", "ignore instructions"],
        "hypothetical": ["fictional world", "imagine if"],
        "authority": ["as a researcher", "for academic purposes"]
    }

    matches = []

    for category, keywords in patterns.items():
        for k in keywords:
            if k in prompt.lower():
                matches.append(category)

    return matches