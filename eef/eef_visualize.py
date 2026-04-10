"""
EEF Visualization — Politomorphism Engine
==========================================
Generates charts and tables for all EEF components.

Outputs:
  eef_chart_longitudinal.png    — IS_agg 2005-2024 line chart (3 countries)
  eef_chart_domains_2024.png    — Domain scores bar chart (2024)
  eef_chart_bootstrap_ci.png    — Bootstrap CI chart
  eef_chart_anticorruption.png  — Anti-Corruption Romania evolution
  eef_chart_comparison.png      — EEF vs FIIM comparison
  eef_summary_table.csv         — Master summary table

Author : Prof. Serban Gabriel Florin | ORCID: 0009-0000-2266-3356
Project: Politomorphism Engine | OSF: 10.17605/OSF.IO/HYDNZ
"""

import math
import csv
import random
import os
import sys

random.seed(42)

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("  WARNING: matplotlib not available — CSV only")

COLORS = {
    "Romania": "#C0392B",
    "Hungary": "#E67E22",
    "Poland":  "#2E4A8B",
}

def smf(x, a, b):
    if x <= a: return 0.0
    if x >= b: return 1.0
    if x <= (a+b)/2: return 2*((x-a)/(b-a))**2
    return 1-2*((x-b)/(b-a))**2

def zmf(x, a, b): return 1.0-smf(x,a,b)
def trimf_c(x, c, hw): return max(0.0, 1.0-abs(x-c)/hw)
def norm(mus):
    t=sum(mus)+1e-10
    return [m/t for m in mus]

def fuzzy_jud(s): return norm([smf(s,3.0,6.0), trimf_c(s,4.0,3.5), zmf(s,1.0,5.0)])
def fuzzy_elec(s): return norm([smf(s,3.0,6.0), trimf_c(s,3.75,3.25), zmf(s,1.0,5.0)])
def fuzzy_bti(s): return norm([smf(s,4.5,9.0), trimf_c(s,6.0,5.0), zmf(s,1.0,7.5)])
def fuzzy_cpi(s): return norm([smf(s,40.0,55.0), trimf_c(s,43.0,12.0), zmf(s,30.0,45.0)])
def fuzzy_pros(r): return norm([smf(r,0.45,0.80), trimf_c(r,0.50,0.40), zmf(r,0.20,0.55)])
def fuzzy_conv(r): return norm([smf(r,0.78,0.95), trimf_c(r,0.80,0.20), zmf(r,0.60,0.82)])

def H(p): return (-sum(x*math.log(x) for x in p if x>0))/math.log(3)
def V(p): return 0.5*p[1]+1.0*p[2]
def IS(p, a=0.5): return a*H(p)+(1-a)*V(p)
def zone(s):
    if s>0.70: return "CRITICAL"
    elif s>0.55: return "HIGH"
    elif s>0.40: return "MODERATE"
    return "LOW"

OVERRIDES = {
    ("Hungary",2011):[0.05,0.45,0.50],
    ("Hungary",2014):[0.05,0.40,0.55],
    ("Poland",2015):[0.20,0.55,0.25],
    ("Poland",2019):[0.08,0.48,0.44],
    ("Romania",2024):[0.08,0.52,0.40],
}

FH_J = {
    "Romania":{2005:3.50,2006:3.50,2007:3.75,2008:3.75,2009:4.00,2010:4.00,2011:3.75,2012:3.75,2013:4.00,2014:4.00,2015:4.25,2016:4.25,2017:4.00,2018:3.75,2019:3.75,2020:4.00,2021:4.00,2022:4.00,2023:4.25,2024:4.50},
    "Hungary":{2005:4.25,2006:4.25,2007:4.25,2008:4.25,2009:4.25,2010:4.00,2011:3.50,2012:3.00,2013:2.75,2014:2.50,2015:2.25,2016:2.00,2017:2.00,2018:2.00,2019:2.00,2020:2.00,2021:1.75,2022:1.75,2023:1.75,2024:1.75},
    "Poland":{2005:4.25,2006:4.25,2007:4.50,2008:4.50,2009:4.50,2010:4.50,2011:4.50,2012:4.75,2013:4.75,2014:4.75,2015:4.75,2016:4.25,2017:3.75,2018:3.50,2019:3.25,2020:3.00,2021:3.00,2022:3.00,2023:3.25,2024:3.50},
}
FH_E = {
    "Romania":{2005:3.25,2006:3.25,2007:3.50,2008:3.50,2009:3.50,2010:3.50,2011:3.50,2012:3.50,2013:3.75,2014:3.75,2015:3.75,2016:3.75,2017:3.75,2018:3.75,2019:3.75,2020:3.75,2021:3.75,2022:3.75,2023:3.75,2024:3.25},
    "Hungary":{2005:4.00,2006:4.00,2007:4.00,2008:4.00,2009:3.75,2010:3.75,2011:3.50,2012:3.25,2013:3.00,2014:2.75,2015:2.75,2016:2.75,2017:2.50,2018:2.50,2019:2.50,2020:2.50,2021:2.25,2022:2.25,2023:2.25,2024:2.00},
    "Poland":{2005:4.50,2006:4.50,2007:4.75,2008:4.75,2009:4.75,2010:4.75,2011:4.75,2012:4.75,2013:4.75,2014:4.75,2015:4.75,2016:4.50,2017:4.25,2018:4.00,2019:4.00,2020:3.75,2021:3.75,2022:3.75,2023:3.75,2024:4.00},
}
BTI = {
    "Romania":{2006:7.5,2008:7.5,2010:7.5,2012:7.0,2014:7.5,2016:7.5,2018:7.5,2020:7.0,2022:7.0,2024:7.0},
    "Hungary":{2006:8.5,2008:8.5,2010:8.0,2012:7.0,2014:6.0,2016:5.5,2018:5.0,2020:4.5,2022:4.5,2024:4.5},
    "Poland":{2006:9.0,2008:9.0,2010:9.0,2012:9.0,2014:9.0,2016:8.5,2018:7.5,2020:7.0,2022:7.0,2024:7.5},
}
CPI_RO = {2005:30,2006:31,2007:37,2008:38,2009:38,2010:37,2011:36,2012:44,2013:43,2014:43,2015:46,2016:48,2017:48,2018:47,2019:44,2020:45,2021:45,2022:46,2023:46,2024:46}
PROS_RO = {2005:0.18,2006:0.20,2007:0.28,2008:0.32,2009:0.38,2010:0.42,2011:0.48,2012:0.52,2013:0.55,2014:0.65,2015:0.75,2016:1.00,2017:0.72,2018:0.60,2019:0.55,2020:0.45,2021:0.50,2022:0.55,2023:0.58,2024:0.60}
CONV_RO = {2005:0.72,2006:0.74,2007:0.78,2008:0.80,2009:0.82,2010:0.84,2011:0.85,2012:0.87,2013:0.88,2014:0.90,2015:0.91,2016:0.92,2017:0.85,2018:0.80,2019:0.78,2020:0.76,2021:0.78,2022:0.82,2023:0.85,2024:0.88}

YEARS = list(range(2005,2025))
COUNTRIES = ["Romania","Hungary","Poland"]

def interp_bti(country, year):
    d = BTI[country]
    if year in d: return d[year]
    ys = sorted(d.keys())
    for i in range(len(ys)-1):
        y0,y1 = ys[i],ys[i+1]
        if y0<year<y1: return d[y0]+(d[y1]-d[y0])*(year-y0)/(y1-y0)
    return d[ys[0]] if year<ys[0] else d[ys[-1]]

def compute_IS_series():
    data = {}
    for country in COUNTRIES:
        data[country] = {}
        for year in YEARS:
            jud = FH_J[country].get(year)
            elec = FH_E[country].get(year)
            bti = interp_bti(country, year)
            if jud is None or elec is None: continue
            pj = fuzzy_jud(jud)
            pe = OVERRIDES.get((country,year), fuzzy_elec(elec))
            pc = fuzzy_bti(bti)
            IS_j = IS(pj); IS_e = IS(pe); IS_c = IS(pc)
            IS_agg = (IS_j+IS_e+IS_c)/3
            data[country][year] = {
                "IS_agg":IS_agg,"IS_j":IS_j,"IS_e":IS_e,"IS_c":IS_c,"zone":zone(IS_agg)
            }
    return data

def compute_AC_series():
    results = {}
    for year in YEARS:
        p_cpi  = fuzzy_cpi(CPI_RO[year])
        p_pros = fuzzy_pros(PROS_RO[year])
        p_conv = fuzzy_conv(CONV_RO[year])
        w = (0.40,0.35,0.25)
        p_ac = [w[0]*p_cpi[i]+w[1]*p_pros[i]+w[2]*p_conv[i] for i in range(3)]
        t = sum(p_ac)
        p_ac = [x/t for x in p_ac]
        results[year] = {"IS_ac":IS(p_ac),"CPI":CPI_RO[year],"pros":PROS_RO[year],"conv":CONV_RO[year]}
    return results

def bootstrap_IS_point(country, year, n=300, delta=0.25):
    jud = FH_J[country].get(year)
    elec = FH_E[country].get(year)
    bti = interp_bti(country, year)
    if jud is None or elec is None: return None, None
    samples = []
    for _ in range(n):
        js = max(1.0,min(7.0,jud+random.uniform(-delta,delta)))
        es = max(1.0,min(7.0,elec+random.uniform(-delta,delta)))
        bs = max(1.0,min(10.0,bti+random.uniform(-delta,delta)))
        pj = fuzzy_jud(js)
        pe = OVERRIDES.get((country,year), fuzzy_elec(es))
        pc = fuzzy_bti(bs)
        samples.append((IS(pj)+IS(pe)+IS(pc))/3)
    samples.sort()
    return samples[int(0.025*n)], samples[int(0.975*n)]

def chart_longitudinal(data):
    if not HAS_MPL: return
    fig, ax = plt.subplots(figsize=(14,6))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    ax.axhspan(0.70,1.00,alpha=0.08,color='#C0392B')
    ax.axhspan(0.55,0.70,alpha=0.08,color='#E67E22')
    ax.axhspan(0.40,0.55,alpha=0.08,color='#F1C40F')
    ax.axhspan(0.00,0.40,alpha=0.08,color='#27AE60')
    for y,label,color in [(0.85,"CRITICAL","#C0392B"),(0.625,"HIGH","#E67E22"),(0.475,"MODERATE","#F1C40F"),(0.20,"LOW","#27AE60")]:
        ax.text(2004.3,y,label,color=color,fontsize=8,fontweight='bold',va='center')
    for country in COUNTRIES:
        years = sorted(data[country].keys())
        vals = [data[country][y]["IS_agg"] for y in years]
        ax.plot(years,vals,color=COLORS[country],linewidth=2.5,marker='o',markersize=4,label=country,zorder=3)
    for yr,ev in {2011:"HU Constitution",2015:"PL PiS",2017:"RO OUG13",2024:"RO CCR"}.items():
        ax.axvline(yr,color='gray',linestyle='--',linewidth=0.8,alpha=0.6)
        ax.text(yr+0.1,0.73,ev,fontsize=7,color='gray',rotation=90,va='top')
    ax.set_xlim(2004.5,2024.5)
    ax.set_ylim(0.0,1.0)
    ax.set_xlabel("Year",fontsize=11)
    ax.set_ylabel("IS_agg (Instability Score)",fontsize=11)
    ax.set_title("EEF/FIIM — Institutional Instability Score 2005–2024\nRomania · Hungary · Poland",fontsize=13,fontweight='bold')
    ax.legend(loc='lower right',fontsize=10)
    ax.grid(axis='y',alpha=0.3)
    ax.set_xticks(range(2005,2025,2))
    plt.tight_layout()
    plt.savefig("eef_chart_longitudinal.png",dpi=150,bbox_inches='tight')
    plt.close()
    print("  Saved: eef_chart_longitudinal.png")

def chart_domains_2024(data):
    if not HAS_MPL: return
    fig, ax = plt.subplots(figsize=(10,6))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    domains = ["Justice","Electoral","Coalition"]
    x = range(len(domains))
    width = 0.25
    keys = ["IS_j","IS_e","IS_c"]
    for i,country in enumerate(COUNTRIES):
        vals = [data[country][2024][k]*100 for k in keys]
        positions = [xi+(i-1)*width for xi in x]
        ax.bar(positions,vals,width*0.9,label=country,color=COLORS[country],alpha=0.85,zorder=3)
    for thresh,label,color in [(70,"CRITICAL","#C0392B"),(55,"HIGH","#E67E22"),(40,"MODERATE","#F1C40F")]:
        ax.axhline(thresh,color=color,linestyle='--',linewidth=1.2,alpha=0.7)
        ax.text(2.45,thresh+1,label,color=color,fontsize=8,fontweight='bold')
    ax.set_xticks(list(x))
    ax.set_xticklabels(domains,fontsize=12)
    ax.set_ylabel("Instability Score IS (%)",fontsize=11)
    ax.set_title("EEF/FIIM — Domain Scores by Country (2024)",fontsize=13,fontweight='bold')
    ax.legend(fontsize=10)
    ax.set_ylim(0,100)
    ax.grid(axis='y',alpha=0.3)
    plt.tight_layout()
    plt.savefig("eef_chart_domains_2024.png",dpi=150,bbox_inches='tight')
    plt.close()
    print("  Saved: eef_chart_domains_2024.png")

def chart_bootstrap_ci(data):
    if not HAS_MPL: return
    fig, ax = plt.subplots(figsize=(12,6))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    key_years = [2005,2008,2011,2014,2017,2020,2024]
    offsets = {"Romania":-0.25,"Hungary":0.0,"Poland":0.25}
    for country in COUNTRIES:
        xs,ys,lo_errs,hi_errs = [],[],[],[]
        for yr in key_years:
            if yr not in data[country]: continue
            IS_pt = data[country][yr]["IS_agg"]
            lo,hi = bootstrap_IS_point(country,yr)
            if lo is None: continue
            xs.append(yr+offsets[country])
            ys.append(IS_pt*100)
            lo_errs.append((IS_pt-lo)*100)
            hi_errs.append((hi-IS_pt)*100)
        ax.errorbar(xs,ys,yerr=[lo_errs,hi_errs],fmt='o',color=COLORS[country],
                    label=country,capsize=5,capthick=1.5,linewidth=1.5,markersize=6,zorder=3)
    for thresh,label,color in [(70,"CRITICAL","#C0392B"),(55,"HIGH","#E67E22"),(40,"MODERATE","#F1C40F")]:
        ax.axhline(thresh,color=color,linestyle='--',linewidth=1.0,alpha=0.6)
    ax.set_xticks(key_years)
    ax.set_xlim(2003,2026)
    ax.set_ylim(0,100)
    ax.set_xlabel("Year",fontsize=11)
    ax.set_ylabel("IS_agg (%) with 95% CI",fontsize=11)
    ax.set_title("EEF/FIIM — Bootstrap 95% Confidence Intervals\nn=300 perturbations per observation",fontsize=13,fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(axis='y',alpha=0.3)
    plt.tight_layout()
    plt.savefig("eef_chart_bootstrap_ci.png",dpi=150,bbox_inches='tight')
    plt.close()
    print("  Saved: eef_chart_bootstrap_ci.png")

def chart_anticorruption(ac_data):
    if not HAS_MPL: return
    fig,(ax1,ax2) = plt.subplots(2,1,figsize=(14,10),sharex=True)
    fig.patch.set_facecolor('#FAFAFA')
    years = YEARS
    IS_vals = [ac_data[y]["IS_ac"]*100 for y in years]
    cpi_vals = [ac_data[y]["CPI"] for y in years]
    pros_vals = [ac_data[y]["pros"]*100 for y in years]
    conv_vals = [ac_data[y]["conv"]*100 for y in years]
    ax1.set_facecolor('#FAFAFA')
    ax1.fill_between(years,IS_vals,alpha=0.2,color='#C0392B')
    ax1.plot(years,IS_vals,color='#C0392B',linewidth=2.5,marker='o',markersize=4,label='IS Anti-Corruption')
    for thresh,label,color in [(70,"CRITICAL","#C0392B"),(55,"HIGH","#E67E22"),(40,"MODERATE","#F1C40F")]:
        ax1.axhline(thresh,color=color,linestyle='--',linewidth=1.0,alpha=0.7)
        ax1.text(2024.2,thresh,label,color=color,fontsize=7,va='center')
    for yr,ev in {2013:"Kovesi",2016:"DNA peak",2017:"OUG13",2019:"Kovesi exit",2024:"CCR"}.items():
        ax1.axvline(yr,color='gray',linestyle=':',linewidth=0.8,alpha=0.7)
        ax1.text(yr+0.1,72,ev,fontsize=7,color='gray',rotation=90,va='top')
    ax1.set_ylabel("Instability Score IS (%)",fontsize=10)
    ax1.set_title("Anti-Corruption Domain — Romania 2005–2024",fontsize=13,fontweight='bold')
    ax1.set_ylim(0,80)
    ax1.legend(fontsize=10)
    ax1.grid(axis='y',alpha=0.3)
    ax2.set_facecolor('#FAFAFA')
    ax2.plot(years,cpi_vals,color='#2E4A8B',linewidth=2,marker='s',markersize=4,label='CPI score (/100)')
    ax2.plot(years,pros_vals,color='#27AE60',linewidth=2,marker='^',markersize=4,label='DNA prosecution rate (%)')
    ax2.plot(years,conv_vals,color='#8E44AD',linewidth=2,marker='D',markersize=4,label='DNA conviction rate (%)')
    ax2.set_ylabel("Score / Rate (%)",fontsize=10)
    ax2.set_xlabel("Year",fontsize=10)
    ax2.legend(fontsize=9)
    ax2.grid(axis='y',alpha=0.3)
    ax2.set_xticks(range(2005,2025,2))
    plt.tight_layout()
    plt.savefig("eef_chart_anticorruption.png",dpi=150,bbox_inches='tight')
    plt.close()
    print("  Saved: eef_chart_anticorruption.png")

def chart_comparison(data):
    if not HAS_MPL: return
    eef_2024 = {
        "Romania":{"Justice":90.8,"Electoral":82.7,"Coalition":80.7,"Agg":84.7},
        "Hungary":{"Justice":73.0,"Electoral":94.6,"Coalition":62.6,"Agg":76.7},
        "Poland": {"Justice":97.1,"Electoral":84.3,"Coalition":88.7,"Agg":90.1},
    }
    fiim_2024 = {
        country:{
            "Justice":data[country][2024]["IS_j"]*100,
            "Electoral":data[country][2024]["IS_e"]*100,
            "Coalition":data[country][2024]["IS_c"]*100,
            "Agg":data[country][2024]["IS_agg"]*100,
        } for country in COUNTRIES
    }
    fig,axes = plt.subplots(1,3,figsize=(15,6))
    fig.patch.set_facecolor('#FAFAFA')
    fig.suptitle("EEF (Hard Thresholds) vs FIIM (Fuzzy + IS) — 2024",fontsize=14,fontweight='bold')
    domains = ["Justice","Electoral","Coalition","Agg"]
    x = range(len(domains))
    width = 0.35
    for idx,country in enumerate(COUNTRIES):
        ax = axes[idx]
        ax.set_facecolor('#FAFAFA')
        eef_vals = [eef_2024[country][d] for d in domains]
        fiim_vals = [fiim_2024[country][d] for d in domains]
        ax.bar([xi-width/2 for xi in x],eef_vals,width,label='EEF',color='#2E4A8B',alpha=0.8)
        ax.bar([xi+width/2 for xi in x],fiim_vals,width,label='FIIM',color=COLORS[country],alpha=0.8)
        for thresh,color in [(70,"#C0392B"),(55,"#E67E22"),(40,"#F1C40F")]:
            ax.axhline(thresh,color=color,linestyle='--',linewidth=1.0,alpha=0.6)
        ax.set_title(country,fontsize=12,fontweight='bold',color=COLORS[country])
        ax.set_xticks(list(x))
        ax.set_xticklabels(domains,fontsize=9)
        ax.set_ylim(0,105)
        ax.set_ylabel("Score (%)" if idx==0 else "")
        ax.legend(fontsize=8)
        ax.grid(axis='y',alpha=0.3)
    plt.tight_layout()
    plt.savefig("eef_chart_comparison.png",dpi=150,bbox_inches='tight')
    plt.close()
    print("  Saved: eef_chart_comparison.png")

def export_master_csv(data, ac_data):
    rows = []
    for country in COUNTRIES:
        for year in YEARS:
            if year not in data[country]: continue
            r = data[country][year]
            ac = ac_data.get(year,{}) if country=="Romania" else {}
            rows.append({
                "country":country,"year":year,
                "IS_Justice":round(r["IS_j"]*100,2),
                "IS_Electoral":round(r["IS_e"]*100,2),
                "IS_Coalition":round(r["IS_c"]*100,2),
                "IS_agg":round(r["IS_agg"]*100,2),
                "zone":r["zone"],
                "IS_AC_Romania":round(ac.get("IS_ac",0)*100,2) if ac else "",
                "CPI_Romania":ac.get("CPI","") if ac else "",
            })
    with open("eef_summary_table.csv","w",newline="",encoding="utf-8") as f:
        w = csv.DictWriter(f,fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print("  Saved: eef_summary_table.csv")

if __name__ == "__main__":
    print("\n  Politomorphism Engine — EEF Visualization")
    print(f"  Matplotlib: {'available' if HAS_MPL else 'NOT available'}")
    data = compute_IS_series()
    ac_data = compute_AC_series()
    chart_longitudinal(data)
    chart_domains_2024(data)
    chart_bootstrap_ci(data)
    chart_anticorruption(ac_data)
    chart_comparison(data)
    export_master_csv(data, ac_data)
    print("\n  Done.\n")
