# train_model.py
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, 'training_data.csv')


df = pd.read_csv(csv_path)

# Encode fight_result into integers
result_map = {'NOT_OVER': 0, 'P1_WIN': 1, 'P2_WIN': 2}
df['fight_result_enc'] = df['fight_result'].map(result_map).fillna(0).astype(int)


feature_cols = [
    # player1 
    'player1_id','player1_health','player1_x_coord','player1_y_coord',
    'player1_is_jumping','player1_is_crouching','player1_in_move','player1_move_id',
    # player2 
    'player2_id','player2_health','player2_x_coord','player2_y_coord',
    'player2_is_jumping','player2_is_crouching','player2_in_move','player2_move_id',
    # global
    'timer','fight_result_enc','has_round_started','is_round_over'
]

#Define target columns (buttons), matching your CSV exactly
button_cols = [
    # player1 buttons
    'player1_A','player1_B','player1_X','player1_Y',
    'player1_L','player1_R','player1_Up','player1_Down',
    'player1_Left','player1_Right','player1_Start','player1_Select',
    # player2 buttons
    'player2_A','player2_B','player2_X','player2_Y',
    'player2_L','player2_R','player2_Up','player2_Down',
    'player2_Left','player2_Right','player2_Start','player2_Select'
]

#Extract features & labels    
X = df[feature_cols].values
y = df[button_cols].astype(int).values  # ensure 0/1

# Train/validation split
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.1, random_state=42
)

#Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled   = scaler.transform(X_val)

#Train a multi-output Random Forest with fewer
base_clf = RandomForestClassifier(
    n_estimators=20,      
    max_depth=8,        
    min_samples_leaf=5,   
    random_state=42,
    n_jobs=1              # single-threaded to avoid thread overhead
)
model = MultiOutputClassifier(base_clf, n_jobs=1)
model.fit(X_train_scaled, y_train)


val_score = model.score(X_val_scaled, y_val)
print(f"Validation multi-output accuracy: {val_score:.3f}")


joblib.dump(scaler, 'scaler.pkl')
joblib.dump(model,  'bot_model.pkl')
print("Training complete. Saved scaler.pkl and bot_model.pkl.")
