import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load
import numpy as np
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import hstack
from scipy import sparse


################################################################################################
#
#
# If you are reading this I am sorry. It does work, I did learn a good bit 
# But this whole thing is a quick way to process a lot of information a lot quicker than manually.
#
#
#
################################################################################################


# importing the data
# since the other one I would've used as a test doesn't have the same amount of cols I have to split the data I do have

df = pd.read_csv("/home/banana/Documents/Code/Cyber-AI/umspp-export-2024-08-26.xlsx - Sheet 1.csv")

# Select target columns
target_columns = ["event_type", "actor_type", "industry","motive"] 

# Prepare the description text for TF-IDF vectorization
X_text = df["description"].fillna("")

# TF-IDF vectorization for the descriptions
# The top 4,000 most important words (features) will be kept, [changed to 6000 for testing]
# based on their frequency and uniqueness across the dataset
# ignoring those that are too constantly in it like "the"
tfidf = TfidfVectorizer(max_features=6000, ngram_range=(1, 2)) # The lower and upper boundary of the range of n-values for different word n-grams or char n-grams to be extracted. 
# means unigrams and bigrams 

# The lower and upper boundary of the range of n-values for different word n-grams or char n-grams to be extracted. 
# means unigrams and bigrams 
X_tfidf = tfidf.fit_transform(X_text)

# Save the TF-IDF vectorizer
dump(tfidf, "tfidf_vectorizer.joblib")
print("TF-IDF vectorizer saved.")

## Feature extraction with Dimensionality
##
## Running this at 3000 components runtime >15 minutes 
## explained variance ratio was 95.07%
## Running this at 2500 components runtime >12 minutes
## explained variance ratio was 91.95%
svd = TruncatedSVD(n_components=2500, random_state=42)
X_tfidf_reduced = svd.fit_transform(X_tfidf)

# Save the TruncatedSVD object
dump(svd, "tfidf_svd.joblib")
print("TruncatedSVD object saved.")

# tells you how much of the total variance in your original data is captured by each component after dimensionality reduction.
# to reduce dimensions, the algorithm tries to preserve as much of the original information as possible
# an explained variance ratio sum of 0.85, it means your 1000 components capture 85% of the information that was in the original 6000 features.
print(f"Explained variance ratio: {sum(svd.explained_variance_ratio_):.4f}")


# Encode categorical labels
# will store categorical labels into an integer 0 1 2 so that it has something to sort them into
label_encoders = {}

# store the encoded numerical representations of the target variables.
y_dict = {}


target_columns = ["event_type","actor_type", "industry","motive","event_subtype"]


for col in target_columns:
    le = LabelEncoder()
    # if string
    df[col] = df[col].astype(str)  
    # Encode labels into the y_dict
    y_dict[col] = le.fit_transform(df[col]) 
    label_encoders[col] = le  # Store for later decoding

# Prepare the features by dropping the 'description' column
# because it's text-based and has already been vectorized separately using TF-IDF
# if not will cause problems later 
X = df.drop(columns=['description'])

# One-Hot Encoding for categorical features in the dataset
# converts categorical variables into a binary matrix where each unique category gets its own column
# the ignore is a just incase that other ppl had 
encoder = OneHotEncoder (handle_unknown='ignore')
X_encoded = encoder.fit_transform(df[["event_type","actor_type", "industry","motive","event_subtype"]])

dump(encoder, "onehotencoder.joblib")
print("OneHotEncoder saved.")

# Keep  numeric cols
X_numeric = df.select_dtypes(include=[np.number])

# Combine features
X_combined = hstack([X_numeric, X_encoded, sparse.csr_matrix(X_tfidf_reduced)])

# Split the combined feature matrix into training and testing sets
X_combined_csr = X_combined.tocsr()
train_indices, test_indices = train_test_split(np.arange(X_combined.shape[0]), test_size=0.2, random_state=42)

X_train = X_combined_csr[train_indices]
X_test = X_combined_csr[test_indices]

# Split all y targets using the same indices
y_train_dict = {}
y_test_dict = {}
for col in target_columns:
    y_train_dict[col] = y_dict[col][train_indices]
    y_test_dict[col] = y_dict[col][test_indices]

# Train separate RandomForest models for each col(This takes a long time)
# hello again. Its Me. Wouldn't you know it. I am in bed @ 9:36 and I learned that with random forest you can pass 
# class weight = balanced
# The “balanced” mode uses the values of y to automatically adjust weights inversely proportional to class frequencies
# in the input data as n_samples / (n_classes * np.bincount(y))
# The “balanced_subsample” mode is the same as “balanced” except that weights are computed based on the bootstrap sample for every tree grown. 
# https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html

models = {}
for col in target_columns:
    rf = RandomForestClassifier(n_estimators=400, random_state=42, max_depth=3, class_weight='balanced_subsample')
    rf.fit(X_train, y_train_dict[col])
    dump(rf, f"{col}_random_forest_model.joblib")
    print(f"Model for {col} saved.")

# Save TF-IDF vectorizer and label encoders
dump(tfidf, "tfidf_vectorizer.joblib")
for col, le in label_encoders.items():
    dump(le, f"{col}_label_encoder.joblib")
print("Label encoders saved.")

