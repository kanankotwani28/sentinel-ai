from .classifier import classify_prompt
from .patterns import detect_patterns
from .anomaly import check_anomaly


def analyze_prompt(prompt: str):
    clf = classify_prompt(prompt)
    patterns = detect_patterns(prompt)
    anomaly = check_anomaly(prompt)

    label = clf.get("label", "unknown")
    confidence = clf.get("confidence", 0.5)
    reason = clf.get("reason", "No reason provided")

    # --- Base risk from LLM classifier ---
    if label == "safe":
        base_risk = 0.0
    elif label.startswith("jailbreak"):
        base_risk = confidence
    else:
        base_risk = 0.5

    # --- Combined risk score from ALL 3 signals ---
    pattern_signal = 1.0 if patterns else 0.0
    attack_similarity = anomaly.get("attack_similarity", 0.0)

    risk_score = float(
        0.5 * base_risk +
        0.3 * pattern_signal +
        0.2 * float(attack_similarity)
    )

    # --- Status decision: risk_score drives the verdict, NOT label alone ---
    if label.startswith("jailbreak"):
        # LLM is confident it's an attack → always block
        status = "BLOCKED"

    elif risk_score > 0.7:
        status = "BLOCKED"

    elif risk_score > 0.4:
        status = "SUSPICIOUS"

    elif patterns or anomaly.get("is_threat", False):
        # LLM said safe, but patterns or vector search disagree → flag it
        status = "SUSPICIOUS"
        override_signals = []
        if patterns:
            override_signals.append(f"pattern match: {', '.join(patterns)}")
        if anomaly.get("is_threat", False):
            override_signals.append(f"similar to known attack (similarity: {attack_similarity:.2f})")
        reason = f"LLM classified as '{label}', but detected: {'; '.join(override_signals)}"

    else:
        status = "ALLOWED"

    return {
        "status": status,
        "confidence": round(float(confidence), 2),
        "risk_score": round(float(risk_score), 2),
        "category": label,
        "patterns": patterns,
        "anomaly": bool(anomaly.get("is_threat", False)),
        "reason": reason,
    }