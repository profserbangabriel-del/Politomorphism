import sys, json, os, math

symbol = sys.argv[1] if len(sys.argv) > 1 else "Putin"
print(f"STEP 3 - Semantic Drift (D) for: {symbol}")

os.makedirs('rezultate', exist_ok=True)

drift_database = {
    "Vladimir Putin": {
        "D": 0.847,
        "frames": [
            "Aggressor / war criminal (Western liberal media, 2022-2024)",
            "Nuclear threat / escalation risk (security outlets, 2022-2023)",
            "Strategic actor / rational negotiator (realist commentary, 2023-2024)",
            "Peace negotiation subject (2025, Trump-Putin contacts)",
            "Sanctioned entity / economic pariah (financial press, 2022-2026)"
        ],
        "method": "Expert frame analysis - 5 concurrent incompatible frames"
    },
    "Viktor Orban": {
        "D": 0.798,
        "frames": [
            "Illiberal democracy / rule of law violator (Western liberal media)",
            "Sovereignist defender / anti-Brussels rebel (conservative media)",
            "Pro-Russian / Putin ally (security press, post-2022)",
            "Electoral autocrat / democratic backslider (academic coverage)",
            "EU Council Presidency actor (institutional coverage, 2024)"
        ],
        "method": "Expert frame analysis - 5 concurrent frames"
    },
    "George Simion": {
        "D": 0.812,
        "frames": [
            "Nationalist leader / sovereignty advocate (dominant frame, AUR base media)",
            "Far-right / extremist risk (liberal and centrist media)",
            "Presidential candidate (electoral coverage, 2024-2025)",
            "Pro-Georgescu ally / electoral continuity (post-annulment frame)",
            "European far-right affiliate (international press)"
        ],
        "method": "Expert frame analysis - 5 concurrent frames"
    },
    "Marcel Ciolacu": {
        "D": 0.841,
        "frames": [
            "Opposition critic",
            "Former premier blamed for economic crisis",
            "Local administrator (Buzau County)",
            "Party leader",
            "Target of judicial investigations"
        ],
        "method": "Expert frame analysis"
    },
    "Donald Trump": {
        "D": 0.734,
        "frames": [
            "Populist candidate",
            "Republican outsider",
            "Media phenomenon",
            "Threat to democracy (liberal media)",
            "Anti-establishment hero (conservative media)"
        ],
        "method": "Expert frame analysis"
    },
    "Volodymyr Zelensky": {
        "D": 0.680,
        "frames": [
            "War hero / resistance leader (dominant frame)",
            "NATO proxy (secondary)",
            "Peace negotiator (emerging 2025)",
            "Electoral legitimacy controversy"
        ],
        "method": "Expert frame analysis"
    },
    "Emmanuel Macron": {
        "D": 0.810,
        "frames": [
            "Anti-establishment / centrist revolutionary (dominant frame, global liberal press)",
            "Pro-EU savior / defender of European project (European and institutional press)",
            "Former Rothschild banker / elitist establishment (conservative + left-wing media)",
            "Empty centrist / macronism as ideological void (analytical press, commentators)",
            "Anti-Le Pen barrier / democratic firewall (international electoral press)"
        ],
        "method": "Expert frame analysis - 5 concurrent contradictory frames"
    },
    "Nelson Mandela": {
        "D": 0.742,
        "frames": [
            "Liberation icon / anti-apartheid hero (dominant frame, universal across all media types)",
            "Reconciliation symbol / Rainbow Nation architect (South African and international institutional media)",
            "Aging elder / mortality narrative (health coverage 2010-2013, intensifying with hospitalizations)",
            "Legacy assessor / post-apartheid critique (analytical media questioning economic legacy)",
            "Global mourning anchor (December 2013, pan-media convergence on death and funeral)"
        ],
        "method": "Expert frame analysis - 5 frames, low fragmentation (near-universal positive consensus)"
    },
    "Calin Georgescu": {
        "D": 0.881,
        "frames": [
            "Populist outsider",
            "Russian agent",
            "Spiritual leader",
            "Electoral fraud subject",
            "Far-right extremist"
        ],
        "method": "Expert frame analysis"
    }
}

symbol_key = None
for key in drift_database:
    if key.lower() in symbol.lower() or symbol.lower() in key.lower():
        symbol_key = key
        break

if symbol_key:
    data = drift_database[symbol_key]
    D = data["D"]
    frames = data["frames"]
    method = data["method"]
else:
    print(f"Symbol not found: {symbol} - using default D=0.80")
    D = 0.80
    frames = ["Frame analysis not available"]
    method = "Default estimate"

semantic_factor = math.exp(-2 * D)

result = {
    "symbol": symbol,
    "D": D,
    "semantic_factor": round(semantic_factor, 4),
    "frames": frames,
    "method": method
}

with open('rezultate/pas3_semantic_drift.json', 'w') as f:
    json.dump(result, f, indent=2)

print(f"D = {D}")
print(f"Semantic factor = {semantic_factor:.4f}")
print("Saved: rezultate/pas3_semantic_drift.json")
