"""Charts for backends that cannot hold a native Office chart (docx, html).

Same exhibit data as the native path; matplotlib with all volatile metadata
stripped so the bytes repeat. Only bar and line here; add plates as needed and
declare them in the voice's plate_policy.
"""
import io

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

FMT = {"pct": lambda v, _: f"{v*100:.1f}%", "gbp": lambda v, _: f"£{v:.2f}", "num": lambda v, _: f"{v:,.1f}"}


def _figure(ex, pal, fonts, size=(7.2, 3.6)):
    plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Liberation Sans", "Arial", "DejaVu Sans"], "svg.hashsalt": "doc-studio"})
    fig, ax = plt.subplots(figsize=size, dpi=150)
    cats = ex["categories"]
    fmt = FMT[ex.get("y_format", "num")]
    for i, (name, vals) in enumerate(ex["values"].items()):
        col = "#" + (pal["accent"] if i == 0 else pal["muted"])
        if ex["plate"] == "line":
            ax.plot(cats, vals, color=col, linewidth=2.2, marker="o", label=name)
            for x, v in zip(cats, vals):
                ax.annotate(fmt(v, None), (x, v), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=8, color="#" + pal["structure"])
        else:
            bars = ax.bar(cats, vals, color=col, width=0.55, label=name)
            for b, v in zip(bars, vals):
                ax.annotate(fmt(v, None), (b.get_x() + b.get_width() / 2, v), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=8, color="#" + pal["structure"])
    ax.yaxis.set_major_formatter(FuncFormatter(fmt))
    ax.set_title(ex["label"], fontsize=9, color="#" + pal["muted"], loc="left")
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color("#" + pal["rule"])
    ax.tick_params(colors="#" + pal["muted"], labelsize=8)
    ax.yaxis.grid(True, color="#" + pal["rule"], linewidth=0.6)
    ax.set_axisbelow(True)
    if len(ex["values"]) > 1:
        ax.legend(frameon=False, fontsize=8)
    if ex["plate"] == "line":
        lo, hi = min(min(v) for v in ex["values"].values()), max(max(v) for v in ex["values"].values())
        pad = (hi - lo) * 0.35 or 1
        ax.set_ylim(lo - pad, hi + pad)
    fig.tight_layout()
    return fig


def chart_png(ex, pal, fonts):
    fig = _figure(ex, pal, fonts)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def chart_svg(ex, pal, fonts):
    fig = _figure(ex, pal, fonts)
    buf = io.BytesIO()
    fig.savefig(buf, format="svg", metadata={"Date": None, "Creator": None})
    plt.close(fig)
    return buf.getvalue().decode("utf-8")
