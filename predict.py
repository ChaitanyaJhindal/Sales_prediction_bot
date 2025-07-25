import pandas as pd
import joblib
from datetime import datetime
import numpy as np
import argparse
import os

def predict_sales(mapped_item_id, date_str):
    """
    Loads a trained model and data to predict sales for a single item-date pair.
    """
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Define file paths relative to the script's location
        model_path = os.path.join(script_dir, 'xgb_sales_model_v3.pkl')
        data_path = os.path.join(script_dir, 'sales_data_with_mapped_ids_v3.csv')

        # Check if all required files exist
        for f in [model_path, data_path]:
            if not os.path.exists(f):
                return f"Error: Required file not found - '{f}'. Make sure it's in the same directory as the script."

        # Load the model and the data file
        model = joblib.load(model_path)
        df = pd.read_csv(data_path)
        df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE']).dt.date
    except Exception as e:
        return f"An error occurred during file loading: {e}"

    # Convert input date string to a date object for comparison
    try:
        input_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return "Error: Invalid date format. Please use 'YYYY-MM-DD'."

    # Find the specific row in the dataframe that matches the input
    target_row = df[(df['ITEMID_Mapped'] == mapped_item_id) & (df['ORDERDATE'] == input_date)]

    if target_row.empty:
        return f"No historical data found for Mapped ITEMID {mapped_item_id} on {date_str}."

    # Get the actual value from this row
    actual_value = target_row['TOTAL_ITEMSOLD'].iloc[0]

    # The feature vector for the model is already pre-calculated in the CSV
    features_for_prediction = [
        target_row['ITEMID_Mapped'].iloc[0],
        target_row['DAY'].iloc[0],
        target_row['MONTH'].iloc[0],
        target_row['YEAR'].iloc[0],
        target_row['DAY_NUM'].iloc[0],
        target_row['IS_WEEKEND'].iloc[0],
        target_row['FESTIVAL_ENC'].iloc[0],
        target_row['ROLLING_3DAY_AVG'].iloc[0]
    ]

    # Predict and round the result
    predicted_value_float = model.predict([features_for_prediction])[0]
    predicted_value = int(round(predicted_value_float))

    return f"Actual: {int(actual_value)}, Predicted: {predicted_value}"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Predict sales for a given mapped item ID and date.")
    parser.add_argument("mapped_id", type=int, help="The mapped ITEMID (e.g., 3).")
    parser.add_argument("date", type=str, help="The date in YYYY-MM-DD format (e.g., 2024-05-01).")
    
    args = parser.parse_args()
    result = predict_sales(args.mapped_id, args.date)
    print(result)