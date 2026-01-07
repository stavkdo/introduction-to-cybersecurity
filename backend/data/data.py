import pandas as pd
import matplotlib.pyplot as plt
import json
import glob
import os
import matplotlib as mpl

# --- הגדרות נתיב ---
LOGS_FOLDER = 'backend/data' 

# 1. טעינה ואיחוד
all_files = glob.glob(os.path.join(LOGS_FOLDER, "*.log"))
if not all_files:
    print("No logs found!")
    exit()

li = []
for filename in all_files:
    scenario_name = os.path.basename(filename).replace('.log', '')
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    data = json.loads(line)
                    data['scenario'] = scenario_name
                    li.append(data)
                except: continue

df = pd.DataFrame(li)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 2. עיצוב וצבעים
scenarios = sorted(df['scenario'].unique())
cmap = mpl.colormaps.get_cmap('tab10')
color_dict = {scenario: cmap(i % 10) for i, scenario in enumerate(scenarios)}

# 3. בניית הדאשבורד
fig = plt.figure(figsize=(18, 18))
gs = fig.add_gridspec(4, 1, height_ratios=[1, 1, 1, 1.2])

# --- שורה 1: Latency ---
sub_gs0 = gs[0].subgridspec(1, 2, wspace=0.3)
ax1 = fig.add_subplot(sub_gs0[0])
ax2 = fig.add_subplot(sub_gs0[1])

stats = df.groupby('scenario')['latency_ms'].agg(['mean', 'median'])
for i, scenario in enumerate(stats.index):
    ax1.bar(i - 0.2, stats.loc[scenario, 'mean'], width=0.4, color=color_dict[scenario])
    ax1.bar(i + 0.2, stats.loc[scenario, 'median'], width=0.4, color=color_dict[scenario], alpha=0.5)
ax1.set_xticks(range(len(stats)))
ax1.set_xticklabels(stats.index, rotation=20, ha='right', fontsize=9)
ax1.set_title('Avg vs Median Latency', fontsize=12, pad=10) # כותרת קטנה יותר

# --- שורה 2: Throughput ---
for scenario in scenarios:
    subset = df[df['scenario'] == scenario].resample('1s', on='timestamp').count()
    ax2.plot(subset.index, subset['username'], label=scenario, color=color_dict[scenario])
ax2.set_title('Throughput (Requests/Sec)', fontsize=12, pad=10)
ax2.legend(fontsize='8', ncol=2)

# --- שורה 3: Rolling Trend ---
ax3 = fig.add_subplot(gs[1])
df_sorted = df.sort_values('timestamp').set_index('timestamp')
for scenario in scenarios:
    group = df_sorted[df_sorted['scenario'] == scenario]
    group['latency_ms'].rolling(window='5s').mean().plot(ax=ax3, label=scenario, color=color_dict[scenario], linewidth=2)
ax3.set_title('Performance Trend (5s Smoothed)', fontsize=12, pad=10)
ax3.set_ylabel('ms', fontsize=10)
ax3.tick_params(labelsize=9)

# --- שורה 4: טבלה ---
ax4 = fig.add_subplot(gs[2])
ax4.axis('off')

success_df = df[df['result'] == 'success']
if not success_df.empty:
    summary = success_df.groupby('scenario').agg({
        'result': 'count',
        'latency_ms': 'mean',
        'username': lambda x: ", ".join(x.unique()[:3]) + ("..." if len(x.unique()) > 3 else "")
    }).reset_index()
    summary.columns = ['Scenario', 'Successes', 'Avg Latency', 'Involved Users']
    summary['Avg Latency'] = summary['Avg Latency'].map('{:.2f} ms'.format)

    table = ax4.table(cellText=summary.values, colLabels=summary.columns, loc='center', cellLoc='left')
    table.auto_set_font_size(False)
    table.set_fontsize(10) # גופן טבלה קטן יותר
    table.scale(1, 2.2) 

    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold')
            cell.set_facecolor('#f0f0f0')
else:
    ax4.text(0.5, 0.5, "No success records found", ha='center')

# פקודת הרווחים המאוזנת
plt.subplots_adjust(top=0.92, bottom=0.08, hspace=0.6, left=0.1, right=0.95)
plt.show()