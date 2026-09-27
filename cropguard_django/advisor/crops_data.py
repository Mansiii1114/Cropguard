"""Crop knowledge base and the rule-based recommendation engine."""

CROPS = [
    {"name": "Rice", "n": (60, 100), "p": (30, 60), "k": (30, 50), "ph": (5.5, 7.0),
     "temp": (20, 35), "hum": (70, 95), "rain": (1000, 2500), "season": "Kharif (monsoon)",
     "desc": "A staple grown in flooded paddies across warm, wet regions.",
     "difficulty": "Moderate", "water": "High",
     "adv": ["Reliable staple demand and price support", "High yield per acre in good conditions", "Well-suited to monsoon rainfall"],
     "dis": ["Needs standing water — heavy irrigation cost", "Vulnerable to blast fungus in humid spells", "Labour-intensive at transplanting and harvest"]},
    {"name": "Wheat", "n": (80, 120), "p": (40, 60), "k": (30, 50), "ph": (6.0, 7.5),
     "temp": (10, 25), "hum": (40, 65), "rain": (350, 900), "season": "Rabi (winter)",
     "desc": "A cool-season cereal, the backbone of the winter cropping cycle.",
     "difficulty": "Easy", "water": "Medium",
     "adv": ["Tolerant of moderate drought once established", "Mechanised sowing and harvest are widely available", "Strong, stable market demand"],
     "dis": ["Late sowing sharply cuts yield", "Susceptible to rust in humid, warm spells", "Needs cold nights to grain properly"]},
    {"name": "Maize", "n": (70, 110), "p": (35, 60), "k": (25, 45), "ph": (5.8, 7.2),
     "temp": (18, 32), "hum": (50, 80), "rain": (500, 1200), "season": "Kharif (monsoon)",
     "desc": "A fast-growing cereal used for food, feed, and industry.",
     "difficulty": "Easy", "water": "Medium",
     "adv": ["Short duration, fits well in crop rotation", "Multiple end uses — food, feed, fodder", "Responds well to added nitrogen"],
     "dis": ["Attracts fall armyworm and stem borer", "Needs consistent moisture at flowering", "Storage losses if not dried properly"]},
    {"name": "Cotton", "n": (80, 120), "p": (30, 55), "k": (30, 55), "ph": (6.0, 8.0),
     "temp": (21, 35), "hum": (45, 70), "rain": (600, 1100), "season": "Kharif (monsoon)",
     "desc": "A long-duration cash crop grown for its fibre.",
     "difficulty": "Hard", "water": "Medium",
     "adv": ["High cash value if quality is good", "Deep roots cope with dry spells", "Strong industrial and export demand"],
     "dis": ["Long growing season ties up the field", "Heavy pesticide need against bollworm", "Price swings with global cotton markets"]},
    {"name": "Sugarcane", "n": (100, 150), "p": (40, 70), "k": (50, 90), "ph": (6.0, 7.5),
     "temp": (22, 35), "hum": (65, 90), "rain": (1100, 2000), "season": "Kharif (monsoon)",
     "desc": "A tall, water-hungry perennial grown for sugar and jaggery.",
     "difficulty": "Hard", "water": "High",
     "adv": ["High income per acre where mills are nearby", "Crop stands 10-12 months, less replanting", "Byproducts (bagasse, molasses) add value"],
     "dis": ["Very high water requirement", "Heavy nutrient drain on soil", "Needs nearby mill access to be profitable"]},
    {"name": "Chickpea", "n": (15, 40), "p": (35, 60), "k": (15, 35), "ph": (6.0, 7.8),
     "temp": (15, 28), "hum": (35, 60), "rain": (300, 650), "season": "Rabi (winter)",
     "desc": "A drought-tolerant pulse that also enriches the soil.",
     "difficulty": "Easy", "water": "Low",
     "adv": ["Fixes nitrogen, improving soil for the next crop", "Low water need suits dry winters", "Good protein-crop market price"],
     "dis": ["Pod borer can cut yield sharply", "Sensitive to waterlogging", "Slower growth than cereals"]},
    {"name": "Mustard", "n": (50, 80), "p": (25, 45), "k": (15, 30), "ph": (6.0, 7.5),
     "temp": (10, 25), "hum": (35, 60), "rain": (250, 550), "season": "Rabi (winter)",
     "desc": "An oilseed grown through the cool, dry winter months.",
     "difficulty": "Easy", "water": "Low",
     "adv": ["Very low water and input needs", "Short duration frees the field early", "Oil and cake both have market value"],
     "dis": ["Aphid attacks are common late season", "Sensitive to unseasonal rain at flowering", "Lower per-acre income than cash crops"]},
    {"name": "Watermelon", "n": (40, 70), "p": (30, 50), "k": (40, 70), "ph": (5.8, 7.0),
     "temp": (24, 35), "hum": (40, 65), "rain": (300, 600), "season": "Zaid (summer)",
     "desc": "A quick summer fruit crop grown on open, sandy fields.",
     "difficulty": "Moderate", "water": "Medium",
     "adv": ["Short cycle, quick cash return", "Strong summer market demand", "Good fit for sandy, well-drained soil"],
     "dis": ["Fruit fly and fungal wilt are frequent issues", "Needs steady irrigation through fruiting", "Bruises easily in transport"]},
    {"name": "Groundnut", "n": (15, 35), "p": (35, 60), "k": (25, 45), "ph": (6.0, 7.2),
     "temp": (22, 32), "hum": (50, 75), "rain": (500, 1000), "season": "Kharif (monsoon)",
     "desc": "A nitrogen-fixing legume grown mainly for oil and food.",
     "difficulty": "Moderate", "water": "Medium",
     "adv": ["Improves soil nitrogen for later crops", "Both oil and direct food market", "Reasonably drought-tolerant once established"],
     "dis": ["Needs well-drained, sandy loam to pod well", "Aflatoxin risk if stored damp", "Leaf spot common in humid weather"]},
]

SEASON_CHOICES = ["Kharif (monsoon)", "Rabi (winter)", "Zaid (summer)"]


def _in_range(value, bounds):
    if value is None:
        return 0.6
    lo, hi = bounds
    if lo <= value <= hi:
        return 1.0
    span = (hi - lo) or 1
    dist = (lo - value) if value < lo else (value - hi)
    return max(0.0, 1 - dist / span)


def recommend(n, p, k, ph, temp, hum, rain, season):
    scored = []
    for c in CROPS:
        score = (
            _in_range(n, c["n"]) + _in_range(p, c["p"]) + _in_range(k, c["k"]) +
            _in_range(ph, c["ph"]) + _in_range(temp, c["temp"]) + _in_range(hum, c["hum"]) +
            _in_range(rain, c["rain"])
        ) / 7
        if c["season"] == season:
            score += 0.08
        score = min(score, 1.0)

        volatility = 0.0
        if rain:
            mid = (c["rain"][0] + c["rain"][1]) / 2
            volatility = abs(rain - mid) / mid

        risk_score = round((1 - score) * 60 + volatility * 30 + (15 if c["season"] != season else 0))
        risk_score = max(4, min(96, risk_score))
        risk_label = "Low" if risk_score < 35 else "Medium" if risk_score < 65 else "High"

        reasons = []
        if c["season"] != season:
            reasons.append(f"Typically a {c['season']} crop, not {season}.")
        if rain and not (c["rain"][0] <= rain <= c["rain"][1]):
            reasons.append(f"Rainfall ({rain:g}mm) is outside its {c['rain'][0]}–{c['rain'][1]}mm range.")
        if ph and not (c["ph"][0] <= ph <= c["ph"][1]):
            reasons.append(f"Soil pH {ph:g} is outside the ideal {c['ph'][0]}–{c['ph'][1]} band.")
        if not reasons:
            reasons.append("Your inputs sit comfortably within the ideal range.")

        scored.append({**c, "score": score, "score10": round(score * 10, 1),
                        "risk_score": risk_score, "risk_label": risk_label, "reasons": reasons})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:3]


def get_crop(name):
    for c in CROPS:
        if c["name"].lower() == name.lower():
            return c
    return None
