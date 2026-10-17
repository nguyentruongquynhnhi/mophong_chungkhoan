import numpy as np
import pandas as pd
COLS = ["open", "p1", "p2", "p3", "p4", "p5", "close"]
def load_data(path="data/abc-25.csv", start="2025-01-01", ref0=10000):
    df = pd.read_csv(path, header=None, names=COLS)
    df["date"] = pd.date_range(start, periods=len(df), freq="D")
    # giá tham chiếu = giá đóng cửa hôm trước (ngày đầu: ref0)
    df["ref"] = df["close"].shift(1).fillna(ref0)
    df["floor"] = df["ref"] * 0.9
    df["ceil"] = df["ref"] * 1.1
    df["avg"] = df[COLS].mean(axis=1)
    df["high"] = df[COLS].max(axis=1)
    df["low"] = df[COLS].min(axis=1)
    df["month"] = df["date"].dt.month
    df["quarter"] = df["date"].dt.quarter
    return df
def monthly_table(df):
    t = df.groupby("month").agg(
        gia_tb=("avg", "mean"), do_lech_chuan=("avg", "std"),
        cao_nhat=("high", "max"), thap_nhat=("low", "min"))
    t["bien_do"] = t["cao_nhat"] - t["thap_nhat"]
    return t.round(0)
def quarterly_table(df):
    t = df.groupby("quarter").agg(
        gia_tb=("avg", "mean"), do_lech_chuan=("avg", "std"),
        cao_nhat=("high", "max"), thap_nhat=("low", "min"),
        dong_cua_cuoi=("close", "last"))
    t["bien_do"] = t["cao_nhat"] - t["thap_nhat"]
    t["thay_doi_%"] = (t["dong_cua_cuoi"] / df.groupby("quarter")["ref"].first() - 1) * 100
    return t.round(1)

import numpy as np  # đã import ở đầu file
def abnormal_days(df, tol=1e-6):
    p = df[COLS].to_numpy()
    at_floor = np.isclose(p, df["floor"].to_numpy()[:, None], atol=tol)
    at_ceil = np.isclose(p, df["ceil"].to_numpy()[:, None], atol=tol)
    out = df.copy()
    out["dong_cua_san"] = at_floor[:, -1]
    out["dong_cua_tran"] = at_ceil[:, -1]
    out["dong_cua_bang_tc"] = np.isclose(df["close"], df["ref"], atol=tol)
    out["ca_phien_san"] = at_floor.all(axis=1)
    out["ca_phien_tran"] = at_ceil.all(axis=1)
    flags = ["dong_cua_san", "dong_cua_tran", "dong_cua_bang_tc", "ca_phien_san", "ca_phien_tran"]
    return out[out[flags].any(axis=1)][["date", "ref", "floor", "ceil", "close"] + flags]