# Cyber Event Classifier and RSS Data Aggregator

## Project Overview

This project is an automated system for collecting, classifying, and analyzing cybersecurity-related news articles using machine learning. The system performs the following key functions:

1. **RSS Feed Scraping**: Collects cybersecurity news from multiple sources
2. **Text Classification**: Uses machine learning to categorize news articles
3. **Data Aggregation**: Stores classified information in a structured CSV format

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

## Customization

- Modify `rss_feed_urls` in `Conductor.py` to add or remove news sources
- Adjust the machine learning model parameters in `RandomFore.py`
- Add custom filtering in `bleepinScrap.py`

## Notes

- The system requires an initial training dataset
- Performance improves with more training data
- Periodically retrain the model to maintain accuracy

## Limitations

- Accuracy depends on the quality and diversity of training data
- May not capture all nuanced cybersecurity events
- Requires manual verification of predictions

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

MIT
