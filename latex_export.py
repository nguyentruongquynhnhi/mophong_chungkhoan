import os
from data_service import monthly_table, quarterly_table, abnormal_days


def _sach(t):
    """Bỏ dấu gạch dưới trong tên cột/chỉ mục để LaTeX không báo lỗi."""
    t = t.copy()
    t.columns = [c.replace("_", " ").replace("%", r"\%") for c in t.columns]
    t.index.name = (t.index.name or "").replace("_", " ")
    return t


def export_tables(df, folder="report/tables"):
    os.makedirs(folder, exist_ok=True)
    _sach(monthly_table(df)).to_latex(f"{folder}/thang.tex", float_format="%.0f")
    _sach(quarterly_table(df)).to_latex(f"{folder}/quy.tex", float_format="%.1f")
    ab = abnormal_days(df)
    ab = ab.assign(date=ab["date"].dt.strftime("%d/%m/%Y"))
    cols = ["date", "ref", "floor", "ceil", "close", "dong_cua_san", "dong_cua_tran"]
    _sach(ab[cols].head(15)).to_latex(f"{folder}/batthuong.tex", index=False, float_format="%.0f")