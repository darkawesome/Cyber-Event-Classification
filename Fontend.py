import csv
import os
import numpy as np
from joblib import load
from scipy.sparse import hstack, csr_matrix
from sklearn.preprocessing import OneHotEncoder

# Helper function to load models with error handling
def load_model(file_path):
    if not os.path.exists(file_path):
        print(f"Error: Model file '{file_path}' not found. Please train the model and save it.")
        return None
    return load(file_path)

def main_function():
    print("Loading pre-trained models...")

    # Load the saved models and components
    rf_event_type = load_model('event_type_random_forest_model.joblib')
    rf_actor_type = load_model('actor_type_random_forest_model.joblib')
    rf_industry = load_model('industry_random_forest_model.joblib')
    rf_motive = load_model('motive_random_forest_model.joblib')
    rf_event_subtype = load_model('event_subtype_random_forest_model.joblib')

    tfidf = load_model('tfidf_vectorizer.joblib')
    svd = load_model('tfidf_svd.joblib')
    
    # Check if required models are loaded
    required_models = [rf_event_type, rf_actor_type, rf_industry, rf_motive, rf_event_subtype, tfidf, svd]
    if None in required_models:
        print("One or more required models could not be loaded. Please make sure all model files exist.")
        return  # Exit the function but don't terminate the process with exit()

    encoder = load_model('onehotencoder.joblib')
    if encoder is None:
        print("OneHotEncoder not found, will handle categorical features differently.")
       

    label_encoder_event_type = load_model('event_type_label_encoder.joblib')
    label_encoder_actor_type = load_model('actor_type_label_encoder.joblib')
    label_encoder_industry = load_model('industry_label_encoder.joblib')
    label_encoder_motive = load_model('motive_label_encoder.joblib')
    label_encoder_event_subtype = load_model('event_subtype_label_encoder.joblib')

    
    new_description = input("Enter the description: ")
    
    # Process text with TF-IDF and SVD, same as in training
    X_new_tfidf = tfidf.transform([new_description])
    X_new_tfidf_reduced = svd.transform(X_new_tfidf)

   
    expected_features = rf_event_type.n_features_in_
    tfidf_reduced_features = X_new_tfidf_reduced.shape[1]  # Should be 2500
    
    # Calculate how many additional features we need (numeric + one-hot encoded)
    additional_features_needed = expected_features - tfidf_reduced_features
    
    # Create zero matrices for these additional features
    X_new_additional = csr_matrix((1, additional_features_needed))
    
    # Combine all features just like in training
    X_new_combined = hstack([X_new_additional, csr_matrix(X_new_tfidf_reduced)])
    
    print(f"Debug: Combined feature shape: {X_new_combined.shape}")
    print(f"Debug: Expected features: {expected_features}")

    # Now use X_new_combined for ALL predictions (just like models were trained)
    
    # Predict event type
    event_type_encoded = rf_event_type.predict(X_new_combined)
    event_type = label_encoder_event_type.inverse_transform(event_type_encoded)

    # Predict actor type (use same combined features)
    actor_type_encoded = rf_actor_type.predict(X_new_combined)
    actor_type = label_encoder_actor_type.inverse_transform(actor_type_encoded)

    # Predict industry (use same combined features)
    industry_encoded = rf_industry.predict(X_new_combined)
    industry = label_encoder_industry.inverse_transform(industry_encoded)

    # Predict motive (use same combined features)
    motive_encoded = rf_motive.predict(X_new_combined)
    motive = label_encoder_motive.inverse_transform(motive_encoded)

    # Predict event subtype (use same combined features)
    event_subtype_encoded = rf_event_subtype.predict(X_new_combined)
    event_subtype = label_encoder_event_subtype.inverse_transform(event_subtype_encoded)

    
    print(f"Predicted event type: {event_type[0]}")
    print(f"Predicted actor type: {actor_type[0]}")
    print(f"Predicted industry: {industry[0]}")
    print(f"Predicted motive: {motive[0]}")
    print(f"Predicted event subtype: {event_subtype[0]}")

    
    testpilot_file = "testpilot.csv"

    # Read the year and month from testpilot.csv
    def get_year_and_month_from_testpilot():
        try:
            with open(testpilot_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    
                    year = row.get('year', None)
                    month = row.get('month', None)
                    return year, month
        except FileNotFoundError:
            print(f"Error: {testpilot_file} not found.")
            return None, None

    
    new_data_year, new_data_month = get_year_and_month_from_testpilot()

    if not new_data_year or not new_data_month:
        print("Year and month could not be retrieved from testpilot.csv. Please check the file.")
        return

    new_data_event_type = event_type[0]
    new_data_actor_type = actor_type[0]
    new_data_industry = industry[0]
    new_data_motive = motive[0]
    new_data_event_subtype = event_subtype[0]

    # Function to get the key for a given industry
    industry_codes = {
        "Agriculture, Forestry, Fishing and Hunting": 11,
        "Mining,Quarring and Oil and Gas Extraction": 21,
        "Utilities": 22,
        "Construction": 23,
        "Manufacturing": "31-33",  # Fixed 
        "Wholesale Trade": 42,
        "Retail Trade": "44-45",    # Fixed 
        "Transportation and Warehousing": "48-49",  # Fixed 
        "Information": 51,
        "Finance and Insurance": 52,
        "Real Estate and Rental and Leasing": 53,
        "Professional, Scientific, and Technical Services": 54,
        "Management of Companies and Enterprises": 55,
        "Administrative and Support and Waste Management and Remediation Services": 56,
        "Educational Services": 61,
        "Health Care and Social Assistance": 62,
        "Arts, Entertainment, and Recreation": 71,
        "Accommodation and Food Services": 72,
        "Other Services (except Public Administration)": 81,
        "Public Administration": 92
    }

    def get_industry_key(industry):
        return industry_codes.get(industry, "Industry not found")

    new_data_industry_code = get_industry_key(new_data_industry)

    print(f"Are the following autocomplete variables correct? {new_data_actor_type}, {new_data_industry}, {new_data_motive}, {new_data_event_type}, {new_data_event_subtype}")
    confirm = input("Is this correct? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Please re-run the script and provide the correct values.")
        return
        
    new_data_slug = input("Enter the slug: ")
    new_data_actor = input("Enter the actor: ")
    new_data_organization = input("Enter the organization: ")
    new_data_source_url = input("Enter the source URL: ")
    new_data_country = input("Enter the country: ")
    new_data_actor_country = input("Enter the actor country: ")

    # Write the data to the CSV file
    output_file = "output.csv"
    try:
        # Check if the file exists and is empty
        file_is_empty = not os.path.exists(output_file) or os.stat(output_file).st_size == 0

        with open(output_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write the header only if the file is empty
            if file_is_empty:
                writer.writerow([
                    "slug", "year", "month", "actor", "actor_type", "organization",
                    "industry_code", "industry", "motive", "event_type", "event_subtype",
                    "description", "source_url", "country", "actor_country"
                ])

            # Write the data row
            writer.writerow([
                new_data_slug, new_data_year, new_data_month, new_data_actor, new_data_actor_type,
                new_data_organization, new_data_industry_code, new_data_industry, new_data_motive,
                new_data_event_type, new_data_event_subtype, new_description, new_data_source_url,
                new_data_country, new_data_actor_country
            ])
        print(f"Data written to {output_file} successfully.")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

# Allow the script to be run directly or imported
if __name__ == "__main__":
    main_function()
