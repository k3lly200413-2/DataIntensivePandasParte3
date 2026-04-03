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
    
    sales["DayOfWeek"] = sales["DayOfWeek"].map(index_to_day_of_week).astype("category")

    # print(sales.loc[sales["Customers"] > 4_000])
    
    # print(sales.loc[sales["DayOfWeek"] == "Sun", "Sales"].mean())
    
    # print(pd.notna(sales["CompetitionDistance"]).count())
    
    # print(sales["Date"].value_counts())
    
    sales = sales.set_index(["Date", "Store"])
    
    # print(sales.head(5))
    
    # print(sales.index)
    
    # print(sales.index.get_level_values("Date"))    # Or (0)
    
    # print(sales.loc[("2015-07-01", 1)])
    
    # print(sales.loc[("2015-07-01", 1), "Sales"])
    
    # print(sales.loc["2015-07-01"])

    # slice(None is like saying : to show that we start from 0 until the end, but we
    # Can't use : in ())
    
    # sales.loc[(slice(None), 1), :]
    
    # print(sales.loc[("2015-07-1", 42), "Customers"])
    
    # print(sales.loc[("2015-07-2", slice(None)), "Sales"].sum())
    
    # print(sales.loc[("2015-07-3", [2, 15, 18]), "Sales"].sum())
    
    # per ogni possibile valore distinto di giorno della settimana
    # for dow in sales["DayOfWeek"].unique():
    #     # estraggo i relativi valori di Sales dal frame e calcolo la media
    #     mean_sales_on_dow = sales.loc[sales["DayOfWeek"] == dow, "Sales"].mean()
    #     # stampo il giorno della settimana e la media
    #     # align right with width of 4
    #     print(f"{dow:>4}: {mean_sales_on_dow:6.2f}")
        
    # print(sales.groupby("DayOfWeek").ngroups)
    
    # print(list(sales.groupby("DayOfWeek").groups.keys()))
    
    # print(sales.groupby("DayOfWeek").mean(numeric_only=True))
    
    # print(sales.groupby("DayOfWeek")["Sales"].mean())
    
    # sales.groupby("DayOfWeek")["Sales"].describe()
    
    # sales.groupby("DayOfWeek")["Sales"].describe().T
    
    # print(sales.groupby("DayOfWeek")["Sales"].agg(["sum", "mean"]))
    
    # print(sales.groupby("DayOfWeek")[["Sales", "Customers"]].agg(["mean", "std"]))
    
    # print(pd.qcut(sales["CompetitionDistance"], 3))

    # print(sales.groupby(pd.qcut(sales["CompetitionDistance"], 3))[["Sales", "Customers"]].mean())

    # print(sales.groupby(["StoreType", "Assortment"])[["Sales", "Customers"]].mean())
    
    # print(sales.groupby(["DayOfWeek", "Promo"])["Customers"].mean())
    
    # print(sales.groupby(sales["DayOfWeek"].isin(["Sat", "Sun"]))[["Sales", "Customers"]].mean())
    
    # print(sales.groupby("Date")["Sales"].sum().idxmax())
    
    # print(sales.groupby(["StoreType", "Assortment"])["Sales"].mean())
    
    # `stack` sposta un livello dall'indice delle colonne a quello delle righe, 
    # per cui dati che prima erano affiancati vengono impilati (_stacked_) 
    # uno sopra l'altro.
    
    #`unstack` al contrario sposta un livello dall'indice delle righe 
    # a quello delle colonne, 
    # rendendo affiancati dati che prima erano impilati.
    
    mean_sales_by_categories = sales.groupby(["StoreType", "Assortment"])["Sales"].mean()
    mean_sales_by_categories.unstack()
    print(mean_sales_by_categories)
    # mean_sales_by_categories.unstack("StoreType")  # oppure unstack(0)
    # mean_sales_by_categories.dropna()
    # mean_sales_by_categories.dropna().unstack()
    
    means_by_categories = sales.groupby(["StoreType", "Assortment"])[["Sales", "Customers"]].agg(["sum", "mean"])
    print(means_by_categories.unstack("Assortment"))
    print(means_by_categories.stack(1))
    # reorder_levels takes the index of the original columns
    means_by_categories.stack(1).reorder_levels([2, 0, 1], axis=0)
    # sorts the index so first all means then all sums
    means_by_categories.stack(1).reorder_levels([2, 0, 1], axis=0).sort_index()
    
    sales.pivot_table(
        values=["Sales", "Customers"],      # ricavi e numero clienti
        index=["StoreType", "Assortment"],  # per tipologia di negozio
        columns=[],
        aggfunc=["sum", "mean"],            # totali e medi giornalieri
    )
    
    sales.pivot_table(
        values=["Sales"],       # ricavi giornalieri
        index=["DayOfWeek"],    # per giorno della settimana
        columns=["StoreType"],  # per tipologia di negozio
        aggfunc=["mean"],       # medi
    )
    
    sales.pivot_table(
        values=["Sales"],       # ricavi giornalieri
        index=["DayOfWeek"],    # per giorno della settimana
        columns=["StoreType"],  # per tipologia di negozio
        aggfunc=["mean"],       # medi
        margins=True,
        margins_name="Tutti",
    )
    
    print(sales.groupby(["DayOfWeek", "Promo"])["Customers"])
    
if __name__ == "__main__":
    
    main()