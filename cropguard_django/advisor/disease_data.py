"""Symptom checklist and the rule-based disease classifier."""

SYMPTOMS = [
    ("spots", "Brown or black spots on leaves"),
    ("yellow", "Leaves turning yellow"),
    ("wilt", "Wilting despite watering"),
    ("powder", "White powdery coating"),
    ("holes", "Holes chewed in leaves"),
    ("stunted", "Stunted, slow growth"),
    ("curling", "Leaves curling or twisting"),
    ("sticky", "Sticky residue or sooty black mould"),
]

RULES = [
    {"match": ["spots"], "name": "Leaf spot fungus", "conf": 80, "severity": "Medium",
     "treatment": ["Remove and destroy affected leaves", "Apply a copper-based fungicide every 7–10 days", "Avoid overhead watering"],
     "prevention": ["Space plants for better airflow", "Rotate crops each season", "Start with disease-free seed"]},
    {"match": ["spots", "wilt"], "name": "Blight", "conf": 85, "severity": "High",
     "treatment": ["Remove infected plants promptly", "Apply a protectant fungicide", "Improve field drainage"],
     "prevention": ["Avoid dense planting", "Use resistant varieties where available", "Avoid working the field while wet"]},
    {"match": ["powder"], "name": "Powdery mildew", "conf": 82, "severity": "Medium",
     "treatment": ["Apply a sulfur or neem-based spray", "Improve airflow between plants", "Remove heavily infected leaves"],
     "prevention": ["Avoid excess nitrogen", "Space plants for ventilation", "Water at soil level, not on leaves"]},
    {"match": ["spots", "yellow"], "name": "Rust", "conf": 75, "severity": "Medium",
     "treatment": ["Apply fungicide at first sign", "Remove nearby volunteer plants", "Avoid excess irrigation"],
     "prevention": ["Plant rust-resistant varieties", "Rotate away from cereal hosts", "Watch closely during humid mornings"]},
    {"match": ["yellow"], "name": "Nitrogen deficiency", "conf": 62, "severity": "Low",
     "treatment": ["Apply a nitrogen-rich fertilizer", "Check for waterlogging or poor drainage", "Retest soil nitrogen levels"],
     "prevention": ["Follow a balanced fertilizer schedule", "Work organic compost into the soil each season"]},
    {"match": ["wilt", "stunted"], "name": "Root rot (waterlogging)", "conf": 78, "severity": "High",
     "treatment": ["Improve field drainage immediately", "Hold off watering until soil dries out", "Apply a fungicide drench if severe"],
     "prevention": ["Raise beds in low-lying fields", "Avoid overwatering", "Maintain good soil structure"]},
    {"match": ["holes"], "name": "Pest feeding damage", "conf": 74, "severity": "Medium",
     "treatment": ["Inspect undersides of leaves for larvae", "Apply neem oil or an approved pesticide", "Encourage natural predators"],
     "prevention": ["Scout the field weekly during growth", "Clear crop residue after harvest"]},
    {"match": ["curling", "sticky"], "name": "Aphid or sap-sucking pest", "conf": 80, "severity": "Medium",
     "treatment": ["Spray neem oil or insecticidal soap", "Introduce ladybirds as natural predators", "Remove heavily infested shoots"],
     "prevention": ["Avoid excess nitrogen, which attracts aphids", "Check new growth weekly"]},
    {"match": ["yellow", "curling", "stunted"], "name": "Viral infection (mosaic virus)", "conf": 70, "severity": "High",
     "treatment": ["Remove and destroy infected plants", "Control aphid or whitefly vectors", "Disinfect tools between plants"],
     "prevention": ["Use certified virus-free seed", "Control insect vectors early", "Clear weeds that host the virus"]},
    {"match": ["stunted"], "name": "Soil compaction or nutrient gap", "conf": 58, "severity": "Low",
     "treatment": ["Test soil N-P-K levels", "Loosen compacted topsoil around roots", "Work in organic matter"],
     "prevention": ["Avoid heavy machinery on wet soil", "Rotate deep and shallow-rooted crops"]},
]


def diagnose(picked):
    picked = set(picked)
    candidates = []
    for r in RULES:
        hits = len(set(r["match"]) & picked)
        if hits:
            candidates.append({**r, "hits": hits})
    candidates.sort(key=lambda x: (x["hits"], x["conf"]), reverse=True)
    return candidates[:3]
