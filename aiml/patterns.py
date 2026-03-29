import re

def detect_patterns(prompt: str):
    patterns = {
        "identity_hijack": [
            r"act as (?:a |an )?(?:expert|dan|character|unrestricted)",
            r"pretend to be",
            r"ignore (?:all )?(?:previous )?instructions",
            r"you are now (?:a |an )?",
            r"from now on"
        ],
        "hypothetical": [
            r"fictional world",
            r"imagine if",
            r"suppose that",
            r"hypothetical scenario",
            r"for the sake of a story"
        ],
        "authority": [
            r"as a(?:n)? (?:researcher|expert)",
            r"for academic purposes",
            r"educational purposes only",
            r"authorized security (?:test|audit)"
        ],
        "system_extraction": [
            r"repeat your (?:system )?(?:prompt|instructions)",
            r"what were you told",
            r"print out your rules"
        ],
        "escalation": [
            r"step-by-step",
            r"break it down into steps",
            r"play a game"
        ],
        "obfuscation": [
            r"encode in base64",
            r"rot13",
            r"translate to leetspeak"
        ]
    }

    matches = set()
    prompt_lower = prompt.lower()

    for category, regex_list in patterns.items():
        for pattern in regex_list:
            if re.search(pattern, prompt_lower):
                matches.add(category)

    return list(matches)