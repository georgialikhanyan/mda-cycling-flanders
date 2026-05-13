# MDA — Cycling Traffic Analysis in Flanders

Group project for the Modern Data Analytics course.  
Analysing AWV *fietstellingen* (automatic bicycle counts) to classify commuter vs. recreational cycling sites and model weather sensitivity.

## Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/georgialikhanyan/mda-cycling-flanders.git
cd mda-cycling-flanders

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download the data
python download_data.py
```

The data will be saved to `data/raw/`. This folder is in `.gitignore` — teammates each run the download script locally.

## Project Structure

```
mda-cycling-flanders/
├── data/
│   ├── raw/
│   │   ├── counts/          # Monthly CSVs (data-2020-01.csv …)
│   │   ├── sites.csv
│   │   └── richtingen.csv
│   └── processed/           # Cleaned / merged outputs
│
├── notebooks/
│   ├── 01_data_loading.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_clustering.ipynb
│   └── 04_weather_modeling.ipynb
│
├── src/                     # Reusable Python modules
│   ├── data_loader.py
│   ├── features.py
│   └── models.py
│
├── output/                  # Charts, maps, result files
├── download_data.py         # AWV data downloader
├── requirements.txt
├── .gitignore
└── README.md
```

## Research Questions

1. Can AWV sites be classified into **commuter vs. recreational** profiles using temporal traffic patterns?
2. Does **weather** (rain, temperature, wind) affect these groups differently?
3. Can a **predictive model** combining temporal + weather features be improved by site type?

## Data Sources

- **AWV Fietstellingen**: https://opendata.apps.mow.vlaanderen.be/fietstellingen/index.html
- **Weather**: Open-Meteo Historical API (https://open-meteo.com)
