import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="Chess.com Blitz Analytics",
    layout="wide"
)



# =========================
# Colors
# =========================

WIN_COLOR = "#2F80ED"
LOSS_COLOR = "#EB5757"
DRAW_COLOR = "#C4C9D1"
RATING_COLOR = "#2F80ED"


# =========================
# Load Data
# =========================

kpi = pd.read_csv("data/processed/01_kpi_summary.csv")
rating = pd.read_csv("data/processed/02_rating_trend.csv")
termination = pd.read_csv("data/processed/03_termination_performance.csv")
color = pd.read_csv("data/processed/04_color_performance.csv")
opening = pd.read_csv("data/processed/05_opening_performance.csv")
previous = pd.read_csv("data/processed/06_previous_game_performance.csv")
opponent_opening = pd.read_csv("data/processed/07_opponent_opening_performance.csv")


# =========================
# Prepare Data
# =========================

rating["played_at"] = pd.to_datetime(
    rating["played_at"],
    utc=True
)

rating["rating_rolling_50"] = (
    rating["focal_player_rating"]
    .rolling(50, center=True)
    .mean()
)

termination["termination_label"] = termination["termination_type"].replace({
    "checkmated": "Checkmate",
    "resigned": "Resignation",
    "timeout": "Timeout",
    "abandoned": "Abandonment",
})

termination_order = [
    "Resignation",
    "Checkmate",
    "Timeout",
    "Abandonment",
]

termination["termination_label"] = pd.Categorical(
    termination["termination_label"],
    categories=termination_order,
    ordered=True
)

termination = termination.sort_values(
    "termination_label"
)

color["focal_player_color"] = color["focal_player_color"].replace({
    "white": "White Pieces",
    "black": "Black Pieces",
})

opening = opening.sort_values(
    "win_percentage",
    ascending=True
)

opponent_opening = opponent_opening.sort_values(
    "win_percentage",
    ascending=True
)

previous_plot = pd.DataFrame({
    "previous_result": [
        "After a Win",
        "After a Loss"
    ],
    "win": [
        previous.loc[0, "win_percent_after_wins"],
        previous.loc[0, "win_percent_after_loss"],
    ],
    "loss": [
        previous.loc[0, "loss_percent_after_wins"],
        previous.loc[0, "loss_percent_after_loss"],
    ],
    "draw": [
        previous.loc[0, "draw_percent_after_wins"],
        previous.loc[0, "draw_percent_after_loss"],
    ],
})


# =========================
# Page Header
# =========================

st.title("Chess.com Blitz Analytics")



# =========================
# KPI Summary
# =========================

cols = st.columns(6)

cols[0].metric(
    "Games",
    f'{kpi.loc[0, "total_games"]:.0f}'
)

cols[1].metric(
    "Ending Rating",
    f'{kpi.loc[0, "current_rating"]:.0f}'
)

cols[2].metric(
    "Rating Change",
    f'{kpi.loc[0, "rating_change"]:+.0f}'
)

cols[3].metric(
    "Wins",
    f'{kpi.loc[0, "wins"]:.0f}'
)

cols[4].metric(
    "Losses",
    f'{kpi.loc[0, "losses"]:.0f}'
)

cols[5].metric(
    "Draws",
    f'{kpi.loc[0, "draws"]:.0f}'
)


# =========================
# Row 1
# Rating Progression + How Games End
# =========================

left, right = st.columns(2)

with left:
    fig_rating, ax_rating = plt.subplots(
        figsize=(6, 2.25),
        dpi=85
    )

    ax_rating.plot(
        rating["played_at"],
        rating["rating_rolling_50"],
        linewidth=2.5,
        color=RATING_COLOR,
        label="50-game rolling average",
    )

    ax_rating.plot(
        rating["played_at"],
        rating["focal_player_rating"],
        linewidth=0.8,
        alpha=0.4,
        color=RATING_COLOR,
        label="Raw rating",
    )

    ax_rating.set_title(
        "Rating Progression",
        fontsize=11,
        pad=8
    )

    ax_rating.set_ylabel(
        "Rating",
        fontsize=8
    )

    ax_rating.xaxis.set_major_formatter(
        mdates.DateFormatter("%b %Y")
    )

    ax_rating.set_ylim(700, 1300)
    ax_rating.grid(axis="y", alpha=0.25)
    ax_rating.set_axisbelow(True)

    ax_rating.spines["top"].set_visible(False)
    ax_rating.spines["right"].set_visible(False)

    ax_rating.legend(
        frameon=False,
        loc="upper left",
        fontsize=7,
    )

    ax_rating.tick_params(
        axis="both",
        labelsize=7
    )

    fig_rating.tight_layout()

    st.pyplot(fig_rating)
    plt.close(fig_rating)


with right:
    fig_end, ax_end = plt.subplots(
        figsize=(6, 2.25),
        dpi=85
    )

    x = list(range(len(termination)))
    width = 0.34

    win_x = [
        i - width / 2
        for i in x
    ]

    loss_x = [
        i + width / 2
        for i in x
    ]

    ax_end.bar(
        win_x,
        termination["won_by_count"],
        width=width,
        label="Wins",
        color=WIN_COLOR,
    )

    ax_end.bar(
        loss_x,
        termination["lost_by_count"],
        width=width,
        label="Losses",
        color=LOSS_COLOR,
    )

    ax_end.set_title(
        "How Games End",
        fontsize=11,
        pad=30
    )

    ax_end.set_xticks(x)

    ax_end.set_xticklabels(
        termination["termination_label"],
        fontsize=7
    )

    ax_end.set_ylabel(
        "Games",
        fontsize=8
    )

    ax_end.grid(
        axis="y",
        alpha=0.2
    )

    ax_end.set_axisbelow(True)

    ax_end.spines["top"].set_visible(False)
    ax_end.spines["right"].set_visible(False)

    ax_end.legend(
        frameon=False,
        fontsize=7,
        ncol=2,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.0),
    )

    ax_end.tick_params(
        axis="y",
        labelsize=7
    )

    fig_end.tight_layout()

    st.pyplot(fig_end)
    plt.close(fig_end)


# =========================
# Row 2
# Performance by Color + Previous Game Performance
# =========================

left, right = st.columns(2)

with left:
    fig_color, ax_color = plt.subplots(
        figsize=(6, 2.25),
        dpi=85
    )

    ax_color.barh(
        color["focal_player_color"],
        color["win_percentage"],
        color=WIN_COLOR,
        label="Win",
    )

    ax_color.barh(
        color["focal_player_color"],
        color["loss_percentage"],
        left=color["win_percentage"],
        color=LOSS_COLOR,
        label="Loss",
    )

    ax_color.barh(
        color["focal_player_color"],
        color["draw_percentage"],
        left=(
            color["win_percentage"]
            + color["loss_percentage"]
        ),
        color=DRAW_COLOR,
        label="Draw",
    )

    for i, row in color.reset_index(drop=True).iterrows():
        win = row["win_percentage"]
        loss = row["loss_percentage"]

        ax_color.text(
            win / 2,
            i,
            f"{win:.1f}%",
            ha="center",
            va="center",
            fontsize=7,
        )

        ax_color.text(
            win + loss / 2,
            i,
            f"{loss:.1f}%",
            ha="center",
            va="center",
            fontsize=7,
        )

    ax_color.set_title(
        "Performance by Color",
        fontsize=11,
        pad=30
    )

    ax_color.set_xlim(
        0,
        100
    )

    ax_color.set_ylabel("")

    ax_color.legend(
        ncol=3,
        frameon=False,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.0),
        fontsize=7,
    )

    ax_color.spines["top"].set_visible(False)
    ax_color.spines["right"].set_visible(False)
    ax_color.spines["left"].set_visible(False)

    ax_color.grid(
        axis="x",
        alpha=0.15
    )

    ax_color.set_axisbelow(True)

    ax_color.tick_params(
        axis="both",
        labelsize=7
    )

    fig_color.tight_layout()

    st.pyplot(fig_color)
    plt.close(fig_color)


with right:
    fig_previous, ax_previous = plt.subplots(
        figsize=(6, 2.25),
        dpi=85
    )

    ax_previous.barh(
        previous_plot["previous_result"],
        previous_plot["win"],
        label="Win",
        color=WIN_COLOR,
    )

    ax_previous.barh(
        previous_plot["previous_result"],
        previous_plot["loss"],
        left=previous_plot["win"],
        label="Loss",
        color=LOSS_COLOR,
    )

    ax_previous.barh(
        previous_plot["previous_result"],
        previous_plot["draw"],
        left=(
            previous_plot["win"]
            + previous_plot["loss"]
        ),
        label="Draw",
        color=DRAW_COLOR,
    )

    for i, row in previous_plot.reset_index(drop=True).iterrows():
        win = row["win"]
        loss = row["loss"]

        ax_previous.text(
            win / 2,
            i,
            f"{win:.1f}%",
            ha="center",
            va="center",
            fontsize=7,
        )

        ax_previous.text(
            win + loss / 2,
            i,
            f"{loss:.1f}%",
            ha="center",
            va="center",
            fontsize=7,
        )

    ax_previous.set_title(
        "Performance After a Win or Loss",
        fontsize=11,
        pad=30
    )

    ax_previous.set_xlim(
        0,
        100
    )

    ax_previous.set_ylabel("")

    ax_previous.legend(
        ncol=3,
        frameon=False,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.0),
        fontsize=7,
    )

    ax_previous.grid(
        axis="x",
        alpha=0.25
    )

    ax_previous.set_axisbelow(True)

    ax_previous.spines["top"].set_visible(False)
    ax_previous.spines["right"].set_visible(False)
    ax_previous.spines["left"].set_visible(False)

    ax_previous.invert_yaxis()

    ax_previous.tick_params(
        axis="both",
        labelsize=7
    )

    fig_previous.tight_layout()

    st.pyplot(fig_previous)
    plt.close(fig_previous)


# =========================
# Row 3
# Openings I Play + Openings I Face
# =========================

left, right = st.columns(2)

with left:
    fig_opening, ax_opening = plt.subplots(
        figsize=(6, 2.4),
        dpi=85
    )

    ax_opening.barh(
        opening["opening_family"],
        opening["win_percentage"],
        label="Win",
        color=WIN_COLOR,
    )

    ax_opening.barh(
        opening["opening_family"],
        opening["loss_percentage"],
        left=opening["win_percentage"],
        label="Loss",
        color=LOSS_COLOR,
    )

    ax_opening.barh(
        opening["opening_family"],
        opening["draw_percentage"],
        left=(
            opening["win_percentage"]
            + opening["loss_percentage"]
        ),
        label="Draw",
        color=DRAW_COLOR,
    )

    for i, row in opening.reset_index(drop=True).iterrows():
        win = row["win_percentage"]
        loss = row["loss_percentage"]

        ax_opening.text(
            win / 2,
            i,
            f"{win:.1f}%",
            ha="center",
            va="center",
            fontsize=6.5,
        )

        ax_opening.text(
            win + loss / 2,
            i,
            f"{loss:.1f}%",
            ha="center",
            va="center",
            fontsize=6.5,
        )

    ax_opening.set_title(
        "Openings I Play",
        fontsize=11,
        pad=34
    )

    ax_opening.set_xlim(
        0,
        100
    )

    ax_opening.set_ylabel("")

    ax_opening.legend(
        ncol=3,
        frameon=False,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.0),
        fontsize=7,
    )

    ax_opening.spines["top"].set_visible(False)
    ax_opening.spines["right"].set_visible(False)
    ax_opening.spines["left"].set_visible(False)

    ax_opening.grid(
        axis="x",
        alpha=0.15
    )

    ax_opening.set_axisbelow(True)

    ax_opening.tick_params(
        axis="both",
        labelsize=6.8
    )

    fig_opening.tight_layout()

    st.pyplot(fig_opening)
    plt.close(fig_opening)


with right:
    fig_opponent, ax_opponent = plt.subplots(
        figsize=(6, 2.4),
        dpi=85
    )

    ax_opponent.barh(
        opponent_opening["opening_family"],
        opponent_opening["win_percentage"],
        label="Win",
        color=WIN_COLOR,
    )

    ax_opponent.barh(
        opponent_opening["opening_family"],
        opponent_opening["loss_percentage"],
        left=opponent_opening["win_percentage"],
        label="Loss",
        color=LOSS_COLOR,
    )

    ax_opponent.barh(
        opponent_opening["opening_family"],
        opponent_opening["draw_percentage"],
        left=(
            opponent_opening["win_percentage"]
            + opponent_opening["loss_percentage"]
        ),
        label="Draw",
        color=DRAW_COLOR,
    )

    for i, row in opponent_opening.reset_index(drop=True).iterrows():
        win = row["win_percentage"]
        loss = row["loss_percentage"]

        ax_opponent.text(
            win / 2,
            i,
            f"{win:.1f}%",
            ha="center",
            va="center",
            fontsize=6.5,
        )

        ax_opponent.text(
            win + loss / 2,
            i,
            f"{loss:.1f}%",
            ha="center",
            va="center",
            fontsize=6.5,
        )

    ax_opponent.set_title(
        "Openings I Face",
        fontsize=11,
        pad=34
    )

    ax_opponent.set_xlim(
        0,
        100
    )

    ax_opponent.set_ylabel("")

    ax_opponent.legend(
        ncol=3,
        frameon=False,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.0),
        fontsize=7,
    )

    ax_opponent.spines["top"].set_visible(False)
    ax_opponent.spines["right"].set_visible(False)
    ax_opponent.spines["left"].set_visible(False)

    ax_opponent.grid(
        axis="x",
        alpha=0.15
    )

    ax_opponent.set_axisbelow(True)

    ax_opponent.tick_params(
        axis="both",
        labelsize=6.8
    )

    fig_opponent.tight_layout()

    st.pyplot(fig_opponent)
    plt.close(fig_opponent)


# =========================
# Key Findings + About
# =========================

left, right = st.columns(2)

with left:
    st.markdown("### Key Findings")

    st.markdown("""
- **Rating improved substantially** across the analysis period, despite several shorter periods of decline.
- **Timeouts are much more common in wins than losses**, suggesting that time management may be a relative strength in my blitz games.
- **Performance by opening varies more noticeably than performance by color**.
- **Previous-game result is associated with subsequent performance:** win rate rises to 52.6% after a win and falls to 47.4% after a loss.
""")

with right:
    st.markdown("### About the Analysis")

    st.write(
        """
        This dashboard analyzes 1,807 Chess.com blitz games from the account
        davidslone2000. Monthly Chess.com game archives were ingested with
        Python and stored in PostgreSQL, where SQL was used to clean,
        transform, and analyze the game data. Processed analytical datasets
        were then loaded with pandas and visualized using Matplotlib and
        Streamlit.
        """
    )
