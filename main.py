import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main():
    BASE_URL = "https://github.com/datascienceunibo/dialab2024/raw/main/Preprocessing_con_pandas"
    SALES_URL = f"{BASE_URL}/rossmann-sales.csv"
    STORES_URL = f"{BASE_URL}/rossmann-stores.csv"
    
    sales_data = pd.read_csv(
        SALES_URL,
        dtype={
            "Open": bool,
            "Promo": bool,
            "StateHoliday": "category",
            "SchoolHoliday": bool
        },
        parse_dates=["Date"]
    )
    
    stores_data = pd.read_csv(
        STORES_URL,
        index_col="Store",
        dtype={
            "StoreType": "category",
            "Assortment": "category",
            "Promo2": bool,
            "PromoInterval": "category",
        },
    )
    
    sales = pd.merge(sales_data, stores_data, left_on="Store", right_index=True)
    sales = sales.loc[sales["Open"]].drop(columns=["Open"])
    sales = sales.sort_values(["Date", "Store"])
    
    index_to_day_of_week = {
        1: "Mon",
        2: "Tue",
        3: "Wed",
        4: "Thu",
        5: "Fri",
        6: "Sat",
        7: "Sun"
    }
    
    sales["DaysOfWeek"] = sales["DaysOfWeek"].map(index_to_day_of_week).astype("categorys")

if __name__ == "__main__":
    
    main()