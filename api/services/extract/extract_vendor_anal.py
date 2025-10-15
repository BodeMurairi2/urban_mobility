#!/usr/bin python3
import pandas as pd
from clean_data import clean_dataset
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# load the data
data = pd.read_parquet("../data/data_file/yellow_tripdata.parquet")

clean_data = clean_dataset(data=data)

def get_data_vendor_2():
    """Filter for Vendor 2"""
    vendor2_data = clean_data[clean_data['VendorID'] == 2]

    trip_counts = vendor2_data.groupby(['PULocationID', 'DOLocationID']).size().reset_index(name='trip_count')

    trip = trip_counts.sort_values("trip_count", ascending=False)
    return trip.head(10)

def get_predictions():
    """Get total price for vendor id
    PULocation = 186
    DOLocation = 230"""
    
    specific_trips = clean_data[
        (clean_data['PULocationID'] == 186) & 
        (clean_data['DOLocationID'] == 230)
    ].copy()

    if pd.api.types.is_timedelta64_dtype(specific_trips['duration']):
        specific_trips['duration_minutes'] = specific_trips['duration'].dt.total_seconds() / 60
    else:
        specific_trips['duration_minutes'] = specific_trips['duration']

    features = [
        'passenger_count', 'duration_minutes', 'fare_amount', 'extra', 'mta_tax', 
        'tolls_amount', 'improvement_surcharge', 'congestion_surcharge', 
        'Airport_fee', 'cbd_congestion_fee'
    ]
    X = specific_trips[features]
    y = specific_trips['total_amount']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    # evaluate
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)
    print(f"RMSE: {rmse:.2f}, R2 Score: {r2:.2f}")

    # Check coefficients
    coeff_df = pd.DataFrame({'Feature': features, 'Coefficient': model.coef_})
    print("\nFeature Coefficients:")
    print(coeff_df)

    # Create a DataFrame with actual and predicted prices
    predicted_prices = pd.DataFrame({
        'Actual Price': y_test.values,
        'Predicted Price': y_pred
    })

    # Round to 2 decimals for readability
    predicted_prices = predicted_prices.round(2)

    # Sort by Predicted Price from highest to lowest
    predicted_prices_sorted = predicted_prices.sort_values("Predicted Price", ascending=False)

    # Show the top 20
    return predicted_prices_sorted.head(5)

if __name__ == "__main__":
    get_data_vendor_2()
    get_predictions()