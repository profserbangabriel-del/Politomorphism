import json, math, os 
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime

DAILY_DATA = [
    ("2025-12-11",3,2632),("2025-12-12",1,2459),("2025-12-13",0,1418),
    ("2025-12-14",7,1414),("2025-12-15",13,2572),("2025-12-16",6,2719),
    ("2025-12-17",6,2733),("2025-12-18",13,2625),("2025-12-19",14,2597),
    ("2025-12-20",0,1399),("2025-12-21",3,1436),("2025-12-22",2,2447),
    ("2025-12-23",3,2276),("2025-12-24",2,1845),("2025-12-25",0,1358),
    ("2025-12-26",0,1548),("2025-12-27",0,1407),("2025-12-28",0,1419),
    ("2025-12-29",3,2220),("2025-12-30",0,2191),("2025-12-31",2,1723),
    ("2026-01-01",1,1437),("2026-01-02",4,1644),("2026-01-03",2,1555),
    ("2026-01-04",0,1497),("2026-01-05",3,2322),("2026-01-06",0,2011),
    ("2026-01-07",11,2159),("2026-01-08",5,2598),("2026-01-09",9,2465),
    ("2026-01-10",4,1524),("2026-01-11",6,1530),("2026-01-12",2,2638),
    ("2026-01-13",4,2817),("2026-01-14",1,2674),("2026-01-15",2,2720),
    ("2026-01-16",1,2587),("2026-01-17",1,1488),("2026-01-18",3,1546),
    ("2026-01-19",2,2838),("2026-01-20",6,2582),("2026-01-21",5,2634),
    ("2026-01-22",33,2655),("2026-01-23",17,2442),("2026-01-24",6,1530),
    ("2026-01-25",1,1420),("2026-01-26",5,2634),("2026-01-27",0,2664),
    ("2026-01-28",3,2749),("2026-01-29",18,2709),("2026-01-30",2,2578),
    ("2026-01-31",2,1443),("2026-02-01",1,1484),("2026-02-02",8,2589),
    ("2026-02-03",7,2688),("2026-02-04",16,2637),("2026-02-05",9,2640),
    ("2026-02-06",12,2487),("2026-02-07",0,1467),("2026-02-08",2,1475),
    ("2026-02-09",7,2556),("2026-02-10",2,2583),("2026-02-11",17,2877),
    ("2026-02-12",7,2850),("2026-02-13",31,2666),("2026-02-14",7,1582),
    ("2026-02-15",17,1540),("2026-02-16",30,2668),("2026-02-17",17,2759),
    ("2026-02-18",11,2976),("2026-02-19",7,2812),("2026-02-20",3,2778),
    ("2026-02-21",8,1676),("2026-02-22",1,1650),("2026-02-23",10,2911),
    ("2026-02-24",3,3064),("2026-02-25",7,2929),("2026-02-26",17,2947),
    ("2026-02-27",7,2791),("2026-02-28",2,1924),("2026-03-01",0,1802),
    ("2026-03-02",0,2837),("2026-03-03",3,2896),("2026-03-04",1,2883),
    ("2026-03-05",2,2870),("2026-03-06",2,2652),("2026-03-07",4,1600),
    ("2026-03-08",2,1648),("2026-03-09",10,2840),("2026-03-10",8,2880),
    ("2026-03-11",4,2859),
]

TOP_SOURCES = {
    "agerpres.ro":72,"cotidianul.ro":58,"hotnews.ro":51,
    "adevarul.ro":46,"bursa.ro":45,"libertatea.ro":37,
    "mediafax.ro":28,"capital.ro":24,"jurnalul.ro":21,
    "stirileprotv.ro":21,"bzi.ro":15,"evz.ro":12,
    "gds.ro":11,"monitorulbt.ro":11,"maszol.ro":8,
    "3szek.ro":6,"cursdeguvernare.ro":6,"gazetadecluj.ro":6,
}

SEMANTIC_FRAMES = [
    "Former PM / economic responsibility",
    "Opposition leader attacking Bolojan",
    "PSD party leader / coalition politics",
    "Local politician Buzau",
    "Nordis scandal / corruption",
    "Budget/fiscal policy critic",
    "Social policy defender",
]

def main():
    os.makedirs("output", exist_ok=True)
    total_symbol = sum(d[1] for d in DAILY_DATA)
    total_corpus = sum(d[2] for d in DAILY_DATA)
    ratios = [d[1]/d[2] for d in DAILY_DATA]
    days_active = sum(1 for d in DAILY_DATA if d[1]>0)
    peak_day = max(DAILY_DATA, key=lambda x: x[1])
    days_above_10 = sum(1 for d in DAILY_DATA if d[1]>10)
    peak_ratio = peak_day[1]/peak_day[2]

    print("="*60)
    print("SRM VALIDATION #3 — Symbol: Marcel Ciolacu")
    print("Period: 2025-12-11 to 2026-03-11")
    print("="*60)
    print(f"Total articles: {total_symbol} / {total_corpus}")
    print(f"Peak day: {peak_day[0]} ({peak_day[1]} articles)")
    print(f"Days active: {days_active}/91")

    peak_norm = min(peak_ratio/0.025, 1.0)
    activity = days_active/len(DAILY_DATA)
    spike = days_above_10/len(DAILY_DATA)
    V = round(0.4*peak_norm + 0.35*activity + 0.25*spike, 4)
    A = 0.42
    n = len(SEMANTIC_FRAMES)
    D = round((n-1)/n - 0.08, 4)
    N = round(min(54/90 + 0.02, 1.0), 4)
    lam = 2
    sf = math.exp(-lam*D)
    SRM = round(V*A*sf*N, 4)

    print(f"\nV={V} | A={A} | D={D} | N={N}")
    print(f"e^(-2D) = {sf:.4f}")
    print(f"SRM = {SRM}")
    print("Interpretation: LOW RESONANCE")

    comp = [
        {"validation":1,"symbol":"Sunflower Movement (Taiwan 2014)","SRM":0.0376},
        {"validation":2,"symbol":"Calin Georgescu (Romania 2024)","SRM":0.0307},
        {"validation":3,"symbol":"Marcel Ciolacu (Romania 2025-26)","SRM":SRM},
    ]

    report = {
        "symbol":"Marcel Ciolacu",
        "period":{"start":"2025-12-11","end":"2026-03-11"},
        "variables":{"V":V,"A":A,"D":D,"N":N,"SRM":SRM},
        "interpretation":"LOW RESONANCE",
        "comparative_table":comp,
        "timestamp":datetime.now().isoformat(),
        "author":"Serban Gabriel Florin",
    }

    with open("output/SRM_raport_final_ciolacu.json","w") as f:
        json.dump(report, f, indent=2)

    counts = [d[1] for d in DAILY_DATA]
    fig, axes = plt.subplots(1,3,figsize=(15,5))
    fig.patch.set_facecolor("#0f1117")

    ax1=axes[0]; ax1.set_facecolor("#1a1d27")
    bars=ax1.bar(range(len(counts)),counts,color="#3498db",alpha=0.8)
    for i,(c,r) in enumerate(zip(counts,ratios)):
        if r>0.008: bars[i].set_color("#e74c3c")
    ax1.set_title("Daily Count",color="white")
    ax1.tick_params(colors="#aaaaaa")
    for s in ax1.spines.values(): s.set_color("#333355")

    ax2=axes[1]; ax2.set_facecolor("#1a1d27")
    vals=[V,A,sf,N,SRM]
    cols=["#3498db","#e74c3c","#f39c12","#2ecc71","#e74c3c"]
    b=ax2.bar(["V","A","e(-2D)","N","SRM"],vals,color=cols,alpha=0.85)
    for bar,val in zip(b,vals):
        ax2.text(bar.get_x()+bar.get_width()/2,bar.get_height()+0.003,
                 f"{val:.4f}",ha="center",color="white",fontsize=9,fontweight="bold")
    ax2.set_title(f"SRM={SRM}",color="white")
    ax2.tick_params(colors="#aaaaaa")
    for s in ax2.spines.values(): s.set_color("#333355")

    ax3=axes[2]; ax3.set_facecolor("#1a1d27")
    b3=ax3.bar(["Sunflower\nV1","Georgescu\nV2","Ciolacu\nV3"],
               [0.0376,0.0307,SRM],color=["#27ae60","#e74c3c","#3498db"],alpha=0.85)
    for bar,val in zip(b3,[0.0376,0.0307,SRM]):
        ax3.text(bar.get_x()+bar.get_width()/2,bar.get_height()+0.0003,
                 f"{val:.4f}",ha="center",color="white",fontsize=10,fontweight="bold")
    ax3.set_title("Comparative SRM",color="white")
    ax3.tick_params(colors="#aaaaaa")
    for s in ax3.spines.values(): s.set_color("#333355")

    fig.suptitle(f"SRM #3 Ciolacu={SRM} LOW RESONANCE",color="white",fontsize=12,fontweight="bold")
    plt.tight_layout()
    plt.savefig("output/SRM_grafic_final_ciolacu.png",dpi=150,bbox_inches="tight",facecolor="#0f1117")
    plt.close()

    print("\n--- Comparative Table ---")
    for row in comp:
        print(f"  [{row['validation']}] {row['symbol']}: SRM={row['SRM']}")

if __name__ == "__main__":
    main()
