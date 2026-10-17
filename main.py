import os
import charts
import pandas as pd
import data_service
pd.set_option("display.width",200)
pd.set_option("display.max_columns",None)
from data_service import load_data, monthly_table, quarterly_table
df = load_data()
ab = data_service.abnormal_days(df)
print(len(ab), "ngày bất thường")
print(ab.head(10))
print(ab[["dong_cua_san", "dong_cua_tran", "dong_cua_bang_tc", "ca_phien_san", "ca_phien_tran"]].sum())
os.makedirs("out", exist_ok=True)
print(quarterly_table(df))
t = monthly_table(df)
charts.bar_monthly_mean(t)
charts.box_monthly(df)
print(t)
print("Tháng biên độ lớn nhất:", t["bien_do"].idxmax())
from data_service import COLS
charts.hist_half_years(df, COLS)
i = df["high"].idxmax(); j = df["low"].idxmin()
print("Đỉnh", df.loc[i, "high"], df.loc[i, "date"].date(), "| Đáy", df.loc[j, "low"], df.loc[j, "date"].date())
r = df["high"] - df["low"]; k = r.idxmax()
print("Biên độ trong ngày lớn nhất", r[k], df.loc[k, "date"].date())
