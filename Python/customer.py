# Step 1: Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Step 2: Create Sample Dataset (You can replace with CSV)
data = {
    'Age': [22,35,41,29,50,31,27,45,38,26,33,40,28,52,37],
    'Tenure': [6,24,12,36,48,8,18,60,10,15,5,30,9,72,20],
    'MonthlyCharges': [450,1200,850,1500,2000,600,950,2500,700,800,500,1400,650,3000,1000],
    'ContractType': ['Month-to-Month','One Year','Month-to-Month','Two Year','Two Year',
                     'Month-to-Month','One Year','Two Year','Month-to-Month','One Year',
                     'Month-to-Month','Two Year','Month-to-Month','Two Year','One Year'],
    'SupportCalls': [3,1,4,0,0,5,1,0,4,2,6,1,3,0,1],
    'Churn': ['Yes','No','Yes','No','No','Yes','No','No','Yes','No','Yes','No','Yes','No','No']
}

df = pd.DataFrame(data)

# Step 3: Encode Categorical Data
le = LabelEncoder()
df['ContractType'] = le.fit_transform(df['ContractType'])
df['Churn'] = le.fit_transform(df['Churn'])

# Step 4: Define X and y
X = df.drop('Churn', axis=1)
y = df['Churn']

# Step 5: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 6: Model Training
model = LogisticRegression()
model.fit(X_train, y_train)

# Step 7: Prediction
y_pred = model.predict(X_test)

# Step 8: Evaluation
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
