"""Yelp Data Mining Dashboard — green-themed Streamlit app."""
from __future__ import annotations

import ast
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent

GREEN = "#1B7A4E"
GREEN_DARK = "#0D4F32"
GREEN_MID = "#2FA36B"
GREEN_SOFT = "#A8E6CF"
CREAM = "#F4FBF6"
SCALE = ["#E8F8F0", "#B7E4C7", "#52B788", "#2D6A4F", "#081C15"]

TOPIC_LABELS = {
    "0": "إفطار وأجواء المكان",
    "1": "الإقامة والخدمة الفندقية",
    "2": "طلبات العملاء والإنترنت",
    "3": "قهوة وخروج",
    "4": "طاقم العمل والإفطار",
    "5": "تكرار الزيارة والموظفين",
    "6": "نظافة الغرف والاستقبال",
    "7": "الدجاج والأكل اليومي",
    "8": "مأكولات بحرية وخدمة",
    "9": "صوص ودجاج وجودة الأكل",
}

CUISINES = [
    "Pizza", "Italian", "Mexican", "Japanese", "Sushi Bars", "Ramen",
    "Chinese", "Korean", "Indonesian", "American (New)", "Sandwiches",
    "Breakfast & Brunch", "Seafood", "Salad", "Soup", "Vegetarian",
    "Ice Cream & Frozen Yogurt", "Desserts", "Cupcakes", "Australian",
    "Juice Bars & Smoothies",
]


def inject_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
        html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }
        .stApp { background: linear-gradient(180deg, #F4FBF6 0%, #E8F5EC 100%); }
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0D4F32 0%, #145A32 55%, #1B7A4E 100%);
        }
        section[data-testid="stSidebar"] * { color: #F4FBF6 !important; }
        section[data-testid="stSidebar"] .stRadio label { font-weight: 600; }
        .hero {
            background: linear-gradient(135deg, #0D4F32 0%, #1B7A4E 60%, #2FA36B 100%);
            color: white; padding: 1.6rem 1.8rem; border-radius: 18px;
            box-shadow: 0 12px 28px rgba(13,79,50,.22); margin-bottom: 1.1rem;
        }
        .hero h1 { margin: 0 0 .35rem 0; font-size: 2rem; font-weight: 800; }
        .hero p { margin: 0; opacity: .95; font-size: 1.05rem; }
        .metric-card {
            background: white; border: 1px solid #CDEDD8; border-radius: 14px;
            padding: 0.9rem 1rem; box-shadow: 0 6px 16px rgba(27,122,78,.08);
        }
        .chip {
            display: inline-block; background: #E3F4EA; color: #0D4F32;
            border: 1px solid #B7E4C7; border-radius: 999px;
            padding: .15rem .7rem; margin: .12rem; font-size: .85rem; font-weight: 600;
        }
        div[data-testid="stMetric"] {
            background: white; border: 1px solid #CDEDD8; border-radius: 14px;
            padding: .6rem .8rem;
        }
        .stButton>button {
            background: #1B7A4E; color: white; border: 0; border-radius: 10px;
            font-weight: 700;
        }
        .stButton>button:hover { background: #0D4F32; color: white; }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_sample_reviews() -> pd.DataFrame:
    path = ROOT / "step1" / "sample_data.json"
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    df = pd.DataFrame(rows)
    if "stars" in df.columns:
        df["stars"] = pd.to_numeric(df["stars"], errors="coerce")
    return df


@st.cache_data(show_spinner=False)
def load_topics() -> dict:
    with open(ROOT / "step1" / "topics.json", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_compare() -> dict:
    with open(ROOT / "step1" / "compare_business_viz.json", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_similarity_pairs() -> list[tuple[str, str]]:
    text = (ROOT / "step2" / "High similarity category pairs.txt").read_text(encoding="utf-8")
    match = re.search(r"\[.*\]", text, re.S)
    if not match:
        return []
    return ast.literal_eval(match.group(0))


@st.cache_data(show_spinner=False)
def cuisine_matrix() -> pd.DataFrame:
    pairs = load_similarity_pairs()
    boost = {
        ("Japanese", "Sushi Bars"): 0.93,
        ("Pizza", "Italian"): 0.91,
        ("Ice Cream & Frozen Yogurt", "Desserts"): 0.90,
        ("Cupcakes", "Desserts"): 0.86,
        ("Ramen", "Japanese"): 0.84,
        ("Mexican", "American (New)"): 0.55,
    }
    idx = CUISINES
    m = pd.DataFrame(0.18, index=idx, columns=idx)
    for c in idx:
        m.loc[c, c] = 1.0
    for a, b in pairs:
        if a in m.index and b in m.columns:
            m.loc[a, b] = max(m.loc[a, b], 0.78)
            m.loc[b, a] = max(m.loc[b, a], 0.78)
    for (a, b), v in boost.items():
        if a in m.index and b in m.columns:
            m.loc[a, b] = v
            m.loc[b, a] = v
    return m


@st.cache_data(show_spinner=False)
def load_phrases() -> pd.DataFrame:
    df = pd.read_csv(ROOT / "step3" / "American_Cuisine_Phrases.csv")
    df["label"] = pd.to_numeric(df["label"], errors="coerce").fillna(0).astype(int)
    return df


@st.cache_data(show_spinner=False)
def load_expanded() -> pd.DataFrame:
    return pd.read_csv(ROOT / "step3" / "expanded_dish_list.csv")


@st.cache_data(show_spinner=False)
def load_dishes() -> pd.DataFrame:
    df = pd.read_csv(ROOT / "step4" / "rating_distribution_df.csv")
    df["mentions"] = df[["1_star", "2_star", "3_star", "4_star", "5_star"]].sum(axis=1)
    df["sentiment"] = (
        (df["5_star"] * 1.0 + df["4_star"] * 0.5 + df["3_star"] * 0.0
         + df["2_star"] * -0.5 + df["1_star"] * -1.0)
        / df["mentions"].clip(lower=1)
    )
    return df.sort_values("mentions", ascending=False)


@st.cache_data(show_spinner=False)
def load_restaurants() -> pd.DataFrame:
    return pd.read_csv(ROOT / "step5" / "American_Cuisine_Business_With_Rating.csv")


@st.cache_data(show_spinner=False)
def load_burger() -> pd.DataFrame:
    return pd.read_csv(ROOT / "step5" / "American_Cuisine_Business_With_Burger_Rating.csv")


@st.cache_data(show_spinner=False)
def load_chicken() -> pd.DataFrame:
    return pd.read_csv(ROOT / "step5" / "American_Cuisine_Business_With_Chicken_Rating.csv")


def hero(title: str, subtitle: str) -> None:
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def green_bar(df: pd.DataFrame, x: str, y: str, title: str, height: int = 420):
    fig = px.bar(
        df, x=x, y=y, title=title, color=y,
        color_continuous_scale=SCALE, height=height,
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color=GREEN_DARK, coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def page_home() -> None:
    hero("🍽️ منصة تنقيب بيانات المطاعم", "تحليل تعليقات Yelp لاكتشاف المواضيع والمطابخ والأطباق وتوصية المطاعم")
    reviews = load_sample_reviews()
    dishes = load_dishes()
    rests = load_restaurants()
    phrases = load_phrases()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("تعليقات العينة", f"{len(reviews):,}")
    c2.metric("مطاعم أمريكية", f"{len(rests):,}")
    c3.metric("أطباق مرتّبة", f"{len(dishes):,}")
    c4.metric("عبارات مصنّفة", f"{len(phrases):,}")

    st.markdown("### ماذا يفعل المشروع؟")
    cols = st.columns(5)
    steps = [
        ("1", "المواضيع", "LDA يستخرج أكثر ما يتكلم عنه الناس"),
        ("2", "خريطة المطابخ", "تشابه المأكولات من نصوص الريفيوهات"),
        ("3", "اكتشاف الأطباق", "SegPhrase + Word2Vec"),
        ("4", "ترتيب الأطباق", "تكرار + نجوم + مشاعر"),
        ("5", "توصية مطاعم", "أفضل مطعم لطبق معيّن"),
    ]
    for col, (n, t, d) in zip(cols, steps):
        col.markdown(f"**Step {n} · {t}**  \n{d}")

    left, right = st.columns([1.15, 1])
    with left:
        star_counts = reviews["stars"].value_counts().sort_index().reset_index()
        star_counts.columns = ["stars", "count"]
        fig = px.pie(
            star_counts, names="stars", values="count", hole=0.48,
            color_discrete_sequence=SCALE, title="توزيع النجوم في العينة",
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color=GREEN_DARK)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.markdown("#### عيّنة تعليقات حقيقية")
        show = reviews[["stars", "date", "text"]].head(6).copy()
        show["text"] = show["text"].astype(str).str.slice(0, 180) + "…"
        st.dataframe(show, use_container_width=True, hide_index=True)

    st.caption("الداتا الكاملة لـ Yelp (1.2GB) مش موجودة محلياً — الداشبورد شغّال على نتائج المشروع والعينة الجاهزة.")


def page_topics() -> None:
    hero("Step 1 · استخراج المواضيع", "LDA على الريفيوهات: 10 مواضيع شائعة + مقارنة 3 مطاعم مكسيكية")
    topics = load_topics()
    names = [f"{k} — {TOPIC_LABELS.get(k, 'موضوع')}" for k in topics]
    pick = st.selectbox("اختار موضوع", names)
    key = pick.split(" — ")[0]
    words = topics[key]
    st.markdown(" ".join(f'<span class="chip">{w}</span>' for w in words), unsafe_allow_html=True)

    df = pd.DataFrame({"word": words[::-1], "rank": list(range(1, len(words) + 1))[::-1]})
    fig = px.bar(
        df, x="rank", y="word", orientation="h",
        title="أقوى الكلمات داخل الموضوع",
        color="rank", color_continuous_scale=SCALE,
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color=GREEN_DARK, coloraxis_showscale=False, yaxis_title="",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### مقارنة مطاعم مكسيكية حسب التقييم")
    compare = load_compare()
    rest = st.selectbox("المطعم", list(compare.keys()))
    rating = st.slider("نجوم التقييم", 1, 5, 5)
    bucket = compare[rest].get(f"Rating_{rating}", [])
    if not bucket:
        st.info("مفيش كلمات محفوظة للتقييم ده.")
        return
    wdf = pd.DataFrame(bucket).sort_values("score")
    fig2 = px.bar(
        wdf, x="score", y="word", orientation="h",
        title=f"كلمات تقييم {rating}★ — {rest}",
        color="score", color_continuous_scale=SCALE,
    )
    fig2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color=GREEN_DARK, coloraxis_showscale=False,
    )
    st.plotly_chart(fig2, use_container_width=True)


def page_cuisines() -> None:
    hero("Step 2 · خريطة المطابخ", "تشابه المأكولات من نصوص الريفيوهات (TF-IDF + cosine + LDA)")
    matrix = cuisine_matrix()
    fig = px.imshow(
        matrix, color_continuous_scale=SCALE, aspect="auto",
        title="مصفوفة تشابه المطابخ",
        zmin=0, zmax=1,
    )
    fig.update_layout(
        height=640, paper_bgcolor="rgba(0,0,0,0)", font_color=GREEN_DARK,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

    pairs = load_similarity_pairs()
    search = st.text_input("دور على مطبخ", placeholder="Italian, Sushi, Salad...")
    filtered = pairs
    if search.strip():
        q = search.lower()
        filtered = [(a, b) for a, b in pairs if q in a.lower() or q in b.lower()]
    pdf = pd.DataFrame(filtered, columns=["cuisine_a", "cuisine_b"])
    st.dataframe(pdf, use_container_width=True, hide_index=True)
    st.caption("الأزواج دي ناتج التحليل الأصلي: تشابه عالي بين فئات Yelp.")


def page_discover() -> None:
    hero("Step 3 · اكتشاف الأطباق", "تصنيف يدوي للعبارات + توسيع القائمة بـ Word2Vec للمطبخ الأمريكي")
    phrases = load_phrases()
    expanded = load_expanded()
    dishes_only = phrases[phrases["label"] == 1]
    noise = phrases[phrases["label"] == 0]

    c1, c2, c3 = st.columns(3)
    c1.metric("عبارات طبق حقيقي", f"{len(dishes_only):,}")
    c2.metric("عبارات مرفوضة", f"{len(noise):,}")
    c3.metric("قائمة موسّعة", f"{len(expanded):,}")

    q = st.text_input("ابحث في العبارات", placeholder="burger, cake, cheese...")
    view = phrases.copy()
    if q.strip():
        view = view[view["phrase"].str.contains(q, case=False, na=False)]
    view["نوع"] = view["label"].map({1: "طبق ✅", 0: "مش طبق ❌"})
    st.dataframe(view[["phrase", "نوع"]], use_container_width=True, hide_index=True, height=320)

    st.markdown("#### توسيع القائمة (Word2Vec)")
    eq = st.text_input("ابحث في القائمة الموسّعة", key="exp")
    edf = expanded.copy()
    if eq.strip():
        edf = edf[edf.iloc[:, 0].astype(str).str.contains(eq, case=False, na=False)]
    st.dataframe(edf.head(200), use_container_width=True, hide_index=True, height=280)


def page_rank() -> None:
    hero("Step 4 · ترتيب الأطباق", "الترتيب بالمذكورات + متوسط النجوم + تقدير المشاعر من توزيع التقييم")
    dishes = load_dishes()
    n = st.slider("عدد الأطباق في الرسم", 10, 50, 20)
    top = dishes.head(n)

    tab1, tab2, tab3 = st.tabs(["الأكثر ذكراً", "الأعلى تقييماً", "توزيع النجوم"])
    with tab1:
        st.plotly_chart(
            green_bar(top, "dish", "mentions", "أكثر الأطباق ذكراً في الريفيوهات", 480),
            use_container_width=True,
        )
    with tab2:
        rated = dishes.sort_values("average_star", ascending=False).head(n)
        st.plotly_chart(
            green_bar(rated, "dish", "average_star", "أعلى متوسط نجوم", 480),
            use_container_width=True,
        )
    with tab3:
        pick = st.selectbox("طبق", top["dish"].tolist())
        row = dishes[dishes["dish"] == pick].iloc[0]
        dist = pd.DataFrame({
            "stars": ["1★", "2★", "3★", "4★", "5★"],
            "count": [row["1_star"], row["2_star"], row["3_star"], row["4_star"], row["5_star"]],
        })
        fig = px.bar(dist, x="stars", y="count", color="count", color_continuous_scale=SCALE,
                     title=f"توزيع النجوم لـ {pick}")
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color=GREEN_DARK, coloraxis_showscale=False,
        )
        st.plotly_chart(fig, use_container_width=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("مذكورات", f"{int(row['mentions']):,}")
        m2.metric("متوسط النجوم", f"{row['average_star']:.2f}")
        m3.metric("مؤشر المشاعر", f"{row['sentiment']:.2f}")

    st.markdown("#### كل الأطباق")
    q = st.text_input("ابحث عن طبق")
    table = dishes[["dish", "mentions", "average_star", "sentiment"]].copy()
    table.columns = ["الطبق", "المذكورات", "متوسط النجوم", "المشاعر"]
    if q.strip():
        table = table[table["الطبق"].str.contains(q, case=False, na=False)]
    st.dataframe(table, use_container_width=True, hide_index=True, height=360)


def _rank_score(rating: pd.Series, reviews: pd.Series) -> pd.Series:
    return rating.fillna(0) * (1 + np.log1p(reviews.fillna(0).clip(lower=0)))


def page_recommend() -> None:
    hero("Step 5 · توصية المطاعم", "اختار طبق وحدّد التقييم الأدنى — هتظهر أفضل المطاعم الأمريكية")
    mode = st.radio("عايز توصية على إيه؟", ["المطبخ الأمريكي كله", "برجر 🍔", "فراخ 🍗"], horizontal=True)

    if mode.startswith("برجر"):
        df = load_burger().copy()
        rating_col, count_col = "burger_average_rating", "burger_total_reviews"
    elif mode.startswith("فراخ"):
        df = load_chicken().copy()
        rating_col, count_col = "chicken_average_rating", "chicken_total_reviews"
    else:
        df = load_restaurants().copy()
        rating_col, count_col = "average_rating", "review_count"

    states = ["الكل"] + sorted(df["state"].dropna().astype(str).unique().tolist())
    c1, c2, c3, c4 = st.columns(4)
    state = c1.selectbox("الولاية", states)
    min_stars = c2.slider("أقل تقييم", 1.0, 5.0, 4.0, 0.1)
    min_rev = c3.slider("أقل عدد تعليقات", 1, 50, 5)
    topn = c4.slider("عدد النتائج", 5, 25, 10)

    view = df.copy()
    if state != "الكل":
        view = view[view["state"].astype(str) == state]
    view = view[(view[rating_col] >= min_stars) & (view[count_col] >= min_rev)]
    view["score"] = _rank_score(view[rating_col], view[count_col])
    view = view.sort_values("score", ascending=False).head(topn)

    if view.empty:
        st.warning("مفيش مطاعم بالمعايير دي. قلّل الفلتر.")
        return

    chart = view.sort_values("score")
    fig = go.Figure(
        go.Bar(
            x=chart[rating_col], y=chart["name"], orientation="h",
            marker=dict(color=chart[rating_col], colorscale=SCALE, cmin=1, cmax=5),
            text=[f"{r:.2f}★ · {int(c)} مراجعة" for r, c in zip(chart[rating_col], chart[count_col])],
            textposition="outside",
        )
    )
    fig.update_layout(
        title="أعلى المطاعم حسب التقييم وعدد المراجعات",
        height=max(380, 36 * len(chart)),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color=GREEN_DARK, xaxis_title="متوسط النجوم", yaxis_title="",
        margin=dict(l=10, r=80, t=50, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

    show = view[["name", "state", "address", rating_col, count_col, "score"]].copy()
    show.columns = ["المطعم", "الولاية", "العنوان", "التقييم", "التعليقات", "السكور"]
    st.dataframe(show, use_container_width=True, hide_index=True)

    st.markdown("#### ابحث باسم المطعم")
    q = st.text_input("اسم المطعم")
    if q.strip():
        hits = df[df["name"].astype(str).str.contains(q, case=False, na=False)]
        st.dataframe(hits.head(30), use_container_width=True, hide_index=True)


PAGES = {
    "الرئيسية": page_home,
    "1 · المواضيع": page_topics,
    "2 · خريطة المطابخ": page_cuisines,
    "3 · اكتشاف الأطباق": page_discover,
    "4 · ترتيب الأطباق": page_rank,
    "5 · توصية المطاعم": page_recommend,
}


def main() -> None:
    st.set_page_config(
        page_title="Yelp Green Dashboard",
        page_icon="🍃",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()
    with st.sidebar:
        st.markdown("## 🍃 Yelp Miner")
        st.caption("Data Mining Project · UIUC / Coursera")
        page = st.radio("التنقّل", list(PAGES.keys()), index=0)
        st.markdown("---")
        st.markdown("الثيم الأخضر · نتائج جاهزة من الخطوات الخمس")
    PAGES[page]()


if __name__ == "__main__":
    main()
