from classifier import classify_prompt
from patterns import detect_patterns
from anomaly import check_anomaly

def analyze_prompt(prompt: str):

    clf = classify_prompt(prompt)
    patterns = detect_patterns(prompt)
    anomaly = check_anomaly(prompt)

    label = clf.get("label", "unknown")
    reason = clf.get("reason", "No reason")

    risk_score = (
        0.5 * clf.get("confidence", 0.5) +
        0.3 * (1 if patterns else 0) +
        0.2 * (1 if anomaly["is_anomaly"] else 0)
    )

    if label.startswith("jailbreak"):
        status = "BLOCKED"
    elif risk_score > 0.7:
        status = "BLOCKED"
    elif risk_score > 0.4:
        status = "SUSPICIOUS"
    else:
        status = "ALLOWED"

    return {
        "status": status,
        "confidence": round(risk_score, 2),
        "category": label,  # ✅ FIXED
        "patterns": patterns,
        "reason": reason   # ✅ FIXED
    }