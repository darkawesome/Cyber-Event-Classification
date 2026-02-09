# Cyber Event Classifier and RSS Data Aggregator

### *Disclaimer*
### In making this tool there was some vibe coding at points

## Project Overview

This project is an automated system for collecting, classifying, and analyzing cybersecurity-related news articles using machine learning. The system performs the following key functions:

1. **RSS Feed Scraping**: Collects cybersecurity news from multiple sources
2. **Text Classification**: Uses machine learning to categorize news articles
3. **Data Aggregation**: Stores classified information in a structured CSV format


![Summary](https://github.com/darkawesome/blog/blob/main/content/img/CyberClassifi/SysMap.png?raw=true)

## Components

The project consists of four main Python scripts:

- `bleepinScrap.py`: RSS feed scraper
- `RandomFore.py`: Machine learning model trainer
- `Fontend.py`: Prediction and data processing script
- `Conductor.py`: Orchestration script to tie everything together

## Prerequisites

- Python 3.8+
- Required Python Libraries:
  ```
  pandas
  scikit-learn
  joblib
  numpy
  scipy
  feedparser
  ```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cyber-event-classifier.git
   cd cyber-event-classifier
   ```

2. Create a virtual environment (recommended):
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Setup and Training

### 1. Train the Machine Learning Model

Before first use, you need to train the Random Forest classifier:

```
python RandomFore.py
```

This script will:
- Process your input CSV
- Create TF-IDF vectorization
- Train Random Forest models
- Save trained models and encoders

### 2. Configuration

- Ensure you have an input CSV file with cybersecurity event data
- Update file paths in the scripts if necessary

## Usage

Run the main conductor script:

```
python Conductor.py
```

This will:
1. Scrape RSS feeds from cybersecurity news sources
2. Filter for cyber-attack related articles
3. Use the trained ML model to classify articles
4. Output results to `output.csv`

## Output

The `output.csv` will contain the following columns:
- slug
- year
- month
- actor
- actor_type
- organization
- industry_code
- industry
- motive
- event_type
- event_subtype
- description
- source_url
- country
- actor_country

## Notes

- The system requires an initial training dataset
- The initail training run does take some time. I added code comments to let you know what stage in the process you are in


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


MIT
