# IMPORT LIBRARIES

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scrfft import scrfft


# LOAD DATASETS

df_2019 = pd.read_csv("2019data8.csv")
df_2022 = pd.read_csv("2022data8.csv")

print(df_2019.head())
print(df_2022.head())

# PREPARE 2019 DATA

df_2019['Date'] = pd.to_datetime(df_2019['Date'], format='%Y-%m-%d')
df_2019 = df_2019.set_index('Date')

# Total passengers per day
df_2019['bus_total']  = df_2019['Bus pax number peak']  +( 
    df_2019['Bus pax number offpeak'])
df_2019['tram_total'] = df_2019['Tram pax number peak'] +(
    df_2019['Tram pax number offpeak'])
df_2019['metro_total']= df_2019['Metro pax number peak']+(
    df_2019['Metro pax number offpeak'])

df_2019['total_pax'] = df_2019['bus_total'] + df_2019['tram_total'] +(
    df_2019['metro_total'])

# Revenue (X,Y,Z)
df_2019['bus_revenue'] = (
    df_2019['Bus pax number peak'] * df_2019['Bus price peak'] +
    df_2019['Bus pax number offpeak'] * df_2019['Bus price offpeak']
)

df_2019['tram_revenue'] = (
    df_2019['Tram pax number peak'] * df_2019['Tram price peak'] +
    df_2019['Tram pax number offpeak'] * df_2019['Tram price offpeak']
)

df_2019['metro_revenue'] = (
    df_2019['Metro pax number peak'] * df_2019['Metro price peak'] +
    df_2019['Metro pax number offpeak'] * df_2019['Metro price offpeak']
)

df_2019['Weekday'] = df_2019.index.day_name()


# PREPARE 2022 DATA — RECONSTRUCT TRUE PASSENGERS

df_2022['DateTime'] = pd.to_datetime(df_2022['Date and time'], 
                                     format='%Y-%m-%d %H:%M')
df_2022['Date'] = df_2022['DateTime'].dt.date
df_2022['Weekday'] = df_2022['DateTime'].dt.day_name()

# Count sample journeys per day
df_2022_daily = df_2022.groupby('Date').size().to_frame(name='sample_count')

# TRUE total for dataset 2022data8.csv from the table:
true_total_2022 = 266_107_756 + 344_481_229 + 458_859_118  # = 1,069,448,103

sample_total_2022 = len(df_2022)

scale_factor = true_total_2022 / sample_total_2022
print("Scale factor for 2022:", scale_factor)

# Estimate true daily passenger numbers
df_2022_daily['estimated_total_pax'] = ( 
    df_2022_daily['sample_count'] * scale_factor)


# FOURIER SMOOTHING FUNCTION

def fourier_smooth(y, terms=8):
    
    y = np.asarray(y)
    N = len(y)
    t = np.arange(N)

    # Use scrfft: we need an x array (0..N-1)
    x = np.arange(N)
    f, a, b = scrfft(x, y)

    
    smooth = np.ones(N) * a[0]

    # Reconstruct series using first `terms`
    for n in range(1, terms + 1):
        if n < len(a):  
            smooth += (
                a[n] * np.cos(2 * np.pi * n * t / N) +
                b[n] * np.sin(2 * np.pi * n * t / N)
            )

    return smooth
# FIGURE 1 — DAILY PASSENGERS + FOURIER (NO NORMALISATION)

y2019 = df_2019['total_pax'].values
y2022 = df_2022_daily['estimated_total_pax'].values

# Smooth using Fourier (now uses scrfft internally)
smooth2019 = fourier_smooth(y2019, terms=8)
smooth2022 = fourier_smooth(y2022, terms=8)

# Time axes
t2019 = np.arange(len(y2019))
t2022 = np.arange(len(y2022))

fig1, ax1 = plt.subplots(figsize=(12, 6), dpi=150)

ax1.scatter(t2019, y2019, s=10, alpha=0.5, label="2019 Daily Passengers")
ax1.scatter(t2022, y2022, s=10, alpha=0.5, 
            label="2022 Daily Passengers (Estimated)")

ax1.plot(t2019, smooth2019, linewidth=2, label="2019 Fourier (8 terms)")
ax1.plot(t2022, smooth2022, linewidth=2, label="2022 Fourier (8 terms)")

ax1.set_xlabel("Day of Year (1–365)")
ax1.set_ylabel("Number of Passengers")
ax1.set_title(
    "Figure 1: Daily Public Transport Usage with 8-Term Fourier Smoothing")

ax1.ticklabel_format(style='plain', axis='y')

ax1.text(0.02, 0.95, "Student ID: 24143189", transform=ax1.transAxes)

ax1.legend()
plt.tight_layout()
plt.show()



# FIGURE 2 — WEEKDAY COMPARISON + REVENUE

weekday_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"
                 ,"Sunday"]

avg_2019 = df_2019.groupby("Weekday")["total_pax"].mean().reindex(
    weekday_order)
avg_2022 = df_2022_daily.groupby(
    df_2022_daily.index.map(lambda d: pd.to_datetime(d).day_name())
    )['estimated_total_pax'].mean().reindex(weekday_order)
        

# Revenues X,Y,Z
X = df_2019['bus_revenue'].sum()
Y = df_2019['tram_revenue'].sum()
Z = df_2019['metro_revenue'].sum()

fig2, ax2 = plt.subplots(figsize=(12, 6), dpi=150)

x = np.arange(len(weekday_order))
bw = 0.35

ax2.bar(x - bw/2, avg_2019, width=bw, label="2019 Average")
ax2.bar(x + bw/2, avg_2022, width=bw, label="2022 Estimated Average")

ax2.set_xticks(x)
ax2.set_xticklabels(weekday_order, rotation=45)
ax2.set_ylabel("Average Daily Passengers")
ax2.set_title(
    "Figure 2: Weekday Passenger Comparison (2019 vs Estimated 2022)")



ax2.ticklabel_format(style='plain', axis='y')

ax2.text(0.02, 0.95, "Student ID: 24143189", transform=ax2.transAxes)

ax2.text(0.02, 0.95, "Student ID: 24143189", transform=ax2.transAxes)

ax2.text(0.02, 0.90, f"X = {X:,.0f}", transform=ax2.transAxes)
ax2.text(0.02, 0.85, f"Y = {Y:,.0f}", transform=ax2.transAxes)
ax2.text(0.02, 0.80, f"Z = {Z:,.0f}", transform=ax2.transAxes) 

ax2.legend()
plt.tight_layout()
plt.show()

# FIGURE 3 — METRO PRICE vs DISTANCE + LINEAR FIT

df_metro = df_2022[df_2022["Mode"] == "Metro"]

x = df_metro['Distance'].values
y = df_metro['Price'].values

coef = np.polyfit(x, y, 1)
slope, intercept = coef
y_pred = slope * x + intercept

fig3, ax3 = plt.subplots(figsize=(10, 6))

ax3.scatter(x, y, s=12, alpha=0.6, label="Metro Journeys (2022)")
ax3.plot(x, y_pred, color='red', linewidth=2, label="Linear Fit")

ax3.set_xlabel("Distance (km)")
ax3.set_ylabel("Price (€)")
ax3.set_title("Figure 3: Metro Price vs Distance (2022)")
ax3.text(0.05, 0.95, "Student ID: 24143189", transform=ax3.transAxes)

ax3.text(
    0.05, 0.90, #
    f"Price = {slope:.4f} × Distance + {intercept:.4f}", 
    transform=ax3.transAxes,
    color="red"
)

ax3.legend()
plt.tight_layout()
plt.show()


# FIGURE 4 — DISTANCE vs DURATION (ALL MODES)

dist = df_2022['Distance'].values
dur = df_2022['Duration'].values

fig4, ax4 = plt.subplots(figsize=(10, 6))

ax4.scatter(dist, dur, s=12, alpha=0.6)
ax4.set_xlabel("Distance (km)")
ax4.set_ylabel("Duration (minutes)")
ax4.set_title("Figure 4: Journey Distance vs Duration (2022)")

ax4.text(0.05, 0.95, "Student ID: 24143189", transform=ax4.transAxes)

plt.tight_layout()
plt.show()

# PRINT REVENUES

print("\nRevenue Values:")
print("X (Bus Revenue 2019):", X)
print("Y (Tram Revenue 2019):", Y)
print("Z (Metro Revenue 2019):", Z)