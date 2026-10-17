import matplotlib.pyplot as plt
THANG = [f"T{i}" for i in range(1, 13)]
def bar_monthly_mean(t, path="out/bar_thang.png"):
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(THANG, t["gia_tb"], color="tab:blue")
    ax.set(title="Giá trung bình mỗi tháng", xlabel="Tháng", ylabel="VND")
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)
def box_monthly(df, path="out/box_thang.png"):
    data = [df.loc[df["month"] == m, "avg"] for m in range(1, 13)]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.boxplot(data, tick_labels=THANG)
    ax.set(title="Phân bố giá mỗi tháng (boxplot)", xlabel="Tháng", ylabel="VND")
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)
def hist_half_years(df, cols, path="out/hist_nua_nam.png"):
    dau = df.loc[df["quarter"] <= 2, cols].to_numpy().ravel()
    cuoi = df.loc[df["quarter"] >= 3, cols].to_numpy().ravel()
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    axes[0].hist(dau, bins=30, color="tab:green", edgecolor="white")
    axes[0].set(title="Quý 1–2", xlabel="Giá (VND)", ylabel="Số quan sát")
    axes[1].hist(cuoi, bins=30, color="tab:red", edgecolor="white")
    axes[1].set(title="Quý 3–4", xlabel="Giá (VND)")
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)