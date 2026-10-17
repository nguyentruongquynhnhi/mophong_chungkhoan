import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from data_service import COLS

XANH, DO, VANG, DUONG, TIM = "#00c800", "#ff2020", "#ffd800", "#1e90ff", "#b040ff"


def mau(price, ref, floor, ceil, tol=1e-6):
    """Màu theo quy ước: so với giá tham chiếu của ngày."""
    if abs(price - ceil) < tol:
        return TIM
    if abs(price - floor) < tol:
        return DUONG
    if abs(price - ref) < tol:
        return VANG
    return XANH if price > ref else DO


def make_animation(df, path="out/abc.mp4", fps=21, max_days=None, dpi=100, step=1):
    n = len(df) if max_days is None else max_days
    P = df[COLS].to_numpy()
    cummax = df["high"].cummax().to_numpy()      # đỉnh giá tính đến từng ngày
    d_peak, d_low = int(df["high"].idxmax()), int(df["low"].idxmin())

    plt.style.use("dark_background")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7))
    for ax in (ax1, ax2):
        ax.set(xlim=(-2, 370), ylim=(0, 15000), ylabel="VND")
    ax2.set_xlabel("Ngày")
    title = ax1.set_title("", color="white")

    # --- nến từng ngày (ẩn sẵn, bật dần) ---
    wicks, bodies = [], []
    for d in range(n):
        c = mau(df["close"].iloc[d], df["ref"].iloc[d], df["floor"].iloc[d], df["ceil"].iloc[d])
        (w,) = ax1.plot([d, d], [0, 0], color=c, lw=1, visible=False)
        r = Rectangle((d - 0.35, 0), 0.7, 0, color=c, visible=False)
        ax1.add_patch(r)
        wicks.append(w); bodies.append(r)

    # --- đường giá + 3 đường mốc ---
    (line,) = ax2.plot([], [], color="orange", lw=1)
    (l_ref,) = ax2.plot([], [], color=VANG, ls=":", lw=1)
    (l_flo,) = ax2.plot([], [], color=DUONG, ls=":", lw=1)
    (l_cei,) = ax2.plot([], [], color=TIM, ls=":", lw=1)
    t_now = ax2.text(0, 0, "", fontsize=9)
    xs, ys = [], []

    # --- (9a) chú thích màu ---
    ax2.legend(
        handles=[Line2D([], [], color=c, ls=":", label=s) for c, s in
                 ((TIM, "Giá trần"), (VANG, "Giá tham chiếu"), (DUONG, "Giá sàn"))],
        loc="upper left", fontsize=8, frameon=False)

    # --- (9b) ghi chú đỉnh / đáy, hiện khi video chạy tới ngày đó ---
    note_peak = ax2.annotate(
        f"ĐỈNH {df['high'].max():,.0f}", xy=(d_peak, df["high"].max()),
        xytext=(d_peak - 60, df["high"].max() * 0.9), color="white",
        arrowprops=dict(arrowstyle="->", color="white"), visible=False)
    note_low = ax2.annotate(
        f"ĐÁY {df['low'].min():,.0f}", xy=(d_low, df["low"].min()),
        xytext=(d_low + 15, df["low"].min() + 4000), color="white",
        arrowprops=dict(arrowstyle="->", color="white"), visible=False)

    # --- (9c) nhãn quý và nhãn kịch trần / kịch sàn ---
    t_quy = ax1.text(0.02, 0.88, "", transform=ax1.transAxes, fontsize=14, color="white")
    t_ke = ax1.text(0.98, 0.88, "", transform=ax1.transAxes, fontsize=14,
                    ha="right", fontweight="bold")

    def update(t):
        d, k = divmod(t, 7)
        row, ref = P[d], df["ref"].iloc[d]
        flo, cei = df["floor"].iloc[d], df["ceil"].iloc[d]
        p = row[k]
        xs.append(d + k / 7); ys.append(p)
        line.set_data(xs, ys)
        for l, v in ((l_ref, ref), (l_flo, flo), (l_cei, cei)):
            l.set_data([d, 365], [v, v])
        t_now.set_position((d + 3, p)); t_now.set_text(f"{p:,.0f}")
        t_now.set_color(mau(p, ref, flo, cei))

        # trục y tự co giãn theo đỉnh giá đã đạt tới
        ymax = max(cummax[d] * 1.25, 5000)
        ax1.set_ylim(0, ymax); ax2.set_ylim(0, ymax)

        seen = row[: k + 1]
        c = mau(p, ref, flo, cei)
        wicks[d].set_data([d, d], [seen.min(), seen.max()])
        bodies[d].set_xy((d - 0.35, min(row[0], p)))
        bodies[d].set_height(abs(p - row[0]) or 1)
        for a in (wicks[d], bodies[d]):
            a.set_visible(True); a.set_color(c)

        title.set_text(f"MÔ PHỎNG CHỨNG KHOÁN ABC – ngày {d + 1}/365 – ({df['date'].iloc[d]:%d/%m/%Y})")
        t_quy.set_text(f"Quý {df['quarter'].iloc[d]}")
        if c == TIM:
            t_ke.set_text("KỊCH TRẦN"); t_ke.set_color(TIM)
        elif c == DUONG:
            t_ke.set_text("KỊCH SÀN"); t_ke.set_color(DUONG)
        else:
            t_ke.set_text("")
        note_peak.set_visible(d >= d_peak)
        note_low.set_visible(d >= d_low)
        return []

    anim = animation.FuncAnimation(
        fig, update, frames=range(0, n * 7, step), blit=False, repeat=False)
    writer = (animation.PillowWriter(fps=fps) if path.endswith(".gif")
              else animation.FFMpegWriter(fps=fps))
    anim.save(path, writer=writer, dpi=dpi)
    plt.close(fig)
