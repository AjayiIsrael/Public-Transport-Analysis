🚌 Public Transport Usage Analysis (2019 & 2022)
A data analysis project comparing public transport ridership, pricing, and revenue across two years using Fourier smoothing, linear regression, and custom revenue modelling on bus, tram, and metro datasets.

📁 Repository Structure
├── Transport.py          # Main Python analysis script
├── 2019data8.csv        # 2019 daily aggregated transport data
├── 2022data8.csv        # 2022 individual journey records
├── requirements.txt     # Python dependencies
├── .gitignore
└── README.md

📌 Project Overview
This project analyses two public transport datasets covering 2019 and 2022. The 2019 dataset contains aggregated daily totals for buses, trams, and metro — including passenger counts (peak/off-peak splits) and ticket prices. The 2022 dataset contains individual journey records with mode, distance (km), duration (minutes), and price (€).
Key questions explored:

How did daily and seasonal passenger patterns differ between 2019 and 2022?
Which days of the week see the highest ridership?
How does metro pricing scale with journey distance?
What is the relationship between journey distance and travel duration?
What were total revenues per transport mode in 2019?


📊 Figures & Analysis
Figure 1 — Daily Passengers with Fourier Smoothing
Raw daily passenger counts for both years are plotted as scatter points. An 8-term Fourier series is fitted to each year to reveal underlying seasonal structure and holiday peaks/valleys. 2022 usage is slightly higher overall, indicating post-disruption recovery and growth.
Fourier Series Formula:
S(t) = a₀ + Σ [ aₙ·cos(2πnt/N) + bₙ·sin(2πnt/N) ]   for n = 1 to 8
Where a₀, aₙ, bₙ are Fourier coefficients extracted via scrfft, t is the day of year, and N is the total number of data points.

Figure 2 — Weekday Passenger Comparison
Side-by-side bar charts compare average daily passengers by day of the week across both years. Fridays peak in both years, consistent with commuter and leisure travel overlap. Weekday averages are broadly higher in 2022.
2019 Total Mode Revenues:
ModeRevenue (€)Bus (X)563,481,750Tram (Y)675,640,502Metro (Z)2,196,392,565
Metro dominates revenue, consistent with its higher capacity and demand on rapid transit corridors.
Revenue Formula:
R_mode = (p_peak × c_peak) + (p_off × c_off)

Figure 3 — Metro Price vs Distance (Linear Regression)
A scatter plot of 2022 metro journeys with a linear regression fit. Price increases predictably with distance.
Price = 0.1364 × Distance + 5.4464

Base fare: ≈ €5.45
Per-km rate: ≈ €0.14/km


Figure 4 — Journey Distance vs Duration
Duration generally rises with distance across all 2022 modes, but variability increases for longer trips — likely due to routing differences, stop density, congestion, and delays. Distance alone is insufficient for reliable journey-time prediction.

🛠️ Technologies Used

Python 3
NumPy — array operations and Fourier reconstruction
Pandas — data loading, cleaning, and aggregation
Matplotlib — all visualisations
scrfft — custom FFT library for Fourier coefficient extraction


▶️ How to Run

Clone the repository

bash   git clone https://github.com/AjayiIsrael/Public-Transport-Analysis.git
   cd Public-Transport-Analysis

Install dependencies

bash   pip install -r requirements.txt

Ensure the data files are in the same directory

   2019data8.csv
   2022data8.csv

Run the script

bash   python 24143189.py
This will generate and display all four figures.

👤 Author
Israel Ajayi
Student ID: 24143189
