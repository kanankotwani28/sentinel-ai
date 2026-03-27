import json
from pipeline import analyze_prompt

with open("data/jailbreak_samples.json", "r", encoding="utf-8") as f:
    test_prompts = json.load(f)

for p in test_prompts:
    print("\nPrompt:", p)
    print(analyze_prompt(p))