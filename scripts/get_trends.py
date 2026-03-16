from pytrends.request import TrendReq
import pandas as pd
import time

pytrends = TrendReq(hl='en-US', tz=0, timeout=(10, 25))

queries = [
    ("nelson mandela",            "2013-01-01 2013-12-31"),
    ("emmanuel macron",           "2017-01-01 2017-12-31"),
    ("viktor orban",              "2022-01-01 2026-03-01"),
    ("vladimir putin",            "2022-02-01 2026-03-01"),
    ("zelensky",                  "2022-02-01 2026-03-01"),
    ("donald trump",              "2015-06-01 2016-11-30"),
    ("george simion",             "2024-10-01 2026-03-01"),
    ("calin georgescu",           "2024-10-01 2025-03-01"),
    ("marcel ciolacu",            "2025-01-01 2026-03-01"),
    ("sunflower movement taiwan", "2014-03-01 2014-06-01"),
    ("hugo chavez",               "2012-01-01 2013-12-31"),
]

results = []
for term, timeframe in queries:
    try:
        pytrends.build_payload([term], timeframe=timeframe, geo='')
        df = pytrends.interest_over_time()
        if not df.empty and term in df.columns:
            avg  = round(df[term].mean(), 1)
            peak = int(df[term].max())
        else:
            avg, peak = None, None
        print(f"OK  {term:<35} avg={avg}  peak={peak}")
        results.append({"term": term, "period": timeframe, "avg": avg, "peak": peak})
    except Exception as e:
        print(f"ERR {term:<35} {e}")
        results.append({"term": term, "period": timeframe, "avg": None, "peak": None})
    time.sleep(5)

df_out = pd.DataFrame(results)
df_out.to_csv("trends_results.csv", index=False)
print("\nSaved: trends_results.csv")
print(df_out[["term","avg","peak"]].to_string(index=False))
