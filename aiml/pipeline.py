from classifier import classify_prompt
from patterns import detect_patterns
from anomaly import check_anomaly


def analyze_prompt(prompt: str):
    clf = classify_prompt(prompt)
    patterns = detect_patterns(prompt)
    anomaly = check_anomaly(prompt)

    label = clf.get("label", "unknown")
    confidence = clf.get("confidence", 0.5)
    reason = clf.get("reason", "No reason provided")

    if label == "safe":
        base_risk = 0
    elif label.startswith("jailbreak"):
        base_risk = confidence
    else:
        base_risk = 0.5 

    risk_score = (
        0.5 * base_risk +
        0.3 * (1 if patterns else 0) +
        0.2 * (1 if anomaly["is_anomaly"] else 0)
    )
    if label == "safe":
        status = "ALLOWED"

    elif label.startswith("jailbreak"):
        status = "BLOCKED"

    elif risk_score > 0.7:
        status = "BLOCKED"

    elif risk_score > 0.4:
        status = "SUSPICIOUS"

    else:
        status = "ALLOWED"
    return {
        "status": status,
        "confidence": round(confidence, 2),
        "risk_score": round(risk_score, 2),
        "category": label,
        "patterns": patterns,
        "anomaly": bool(anomaly.get("is_anomaly", False)),
        "reason": reason
    }