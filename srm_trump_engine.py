import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

try:
    # 1. Load Trump data (handling quotes and separators)
    df = pd.read_csv('TRUMP+DATA.csv', quotechar='"', skipinitialspace=True)
    if len(df.columns) == 1:
        df = pd.read_csv('TRUMP+DATA.csv', sep=',', quotechar='"')
    
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    # 2. SRM Variables (Trump Case Study)
    V, A, D, N = 0.90, 0.72, 0.25, 0.95
    srm_score = V * A * np.exp(-2 * D) * N

    # 3. Export English Report
    with open('trump_srm_report.json', 'w') as f:
        json.dump({"symbol": "Donald Trump", "srm_score": round(srm_score, 4), "status": "Success"}, f, indent=4)

    # 4. Export Chart
    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['ratio'], color='red', label='Trump Visibility')
    plt.title('SRM Validation: Donald Trump (US 2015-2016)')
    plt.grid(True, alpha=0.3)
    plt.savefig('trump_srm_chart.png')
    print("Files created successfully.")

except Exception as e:
    print(f"Error occurred: {e}")
