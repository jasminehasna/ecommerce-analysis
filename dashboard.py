from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

sns.set_theme(style="whitegrid")
st.set_page_config(page_title="Brazilian E-Commerce Dashboard", layout="wide")

DATA_PATH = Path(__file__).with_name("main_data.csv")
SEGMENT_ORDER = ["Champions", "Loyal Customers", "Potential Loyalists", "At Risk", "Lost"]
SEGMENT_COLORS = ["#1565C0", "#2E7D32", "#F57F17", "#C62828", "#6A1B9A"]


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    if "order_delivered_customer_date" in df.columns:
        df["order_delivered_customer_date"] = pd.to_datetime(
            df["order_delivered_customer_date"], errors="coerce"
        )
    return df


def create_monthly_orders_df(df):
    monthly = (
        df.resample("ME", on="order_purchase_timestamp")
        .agg(order_count=("order_id", "nunique"), revenue=("payment_value", "sum"))
        .reset_index()
    )
    monthly["period"] = monthly["order_purchase_timestamp"].dt.strftime("%Y-%m")
    return monthly


def safe_score_series(series, reverse=False):
    if series.empty:
        return pd.Series(dtype=int)

    if series.nunique(dropna=False) <= 1:
        return pd.Series(3, index=series.index, dtype=int)

    ranked = series.rank(method="average", ascending=not reverse)
    scaled = ((ranked - 1) / (len(series) - 1) * 4).round().astype(int) + 1
    return scaled.clip(1, 5)


def create_rfm_df(df):
    reference_date = df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
    rfm = (
        df.groupby("customer_unique_id")
        .agg(
            recency=("order_purchase_timestamp", lambda x: (reference_date - x.max()).days),
            frequency=("order_id", "nunique"),
            monetary=("payment_value", "sum"),
        )
        .reset_index()
    )
    rfm["R_score"] = safe_score_series(rfm["recency"], reverse=True)
    rfm["F_score"] = safe_score_series(rfm["frequency"])
    rfm["M_score"] = safe_score_series(rfm["monetary"])
    rfm["RFM_total"] = (
        rfm["R_score"].astype(int) + rfm["F_score"].astype(int) + rfm["M_score"].astype(int)
    )

    def segment_customer(score):
        if score >= 13:
            return "Champions"
        if score >= 10:
            return "Loyal Customers"
        if score >= 7:
            return "Potential Loyalists"
        if score >= 5:
            return "At Risk"
        return "Lost"

    rfm["Segment"] = rfm["RFM_total"].apply(segment_customer)
    return rfm


def main():
    st.title("Brazilian E-Commerce Dashboard")
    st.caption("Analisis perilaku pelanggan dan performa kategori produk")

    df = load_data()

    min_date = df["order_purchase_timestamp"].min().date()
    max_date = df["order_purchase_timestamp"].max().date()

    with st.sidebar:
        st.header("Filter")
        selected_dates = st.date_input(
            "Rentang Waktu",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

    if isinstance(selected_dates, tuple):
        if len(selected_dates) >= 2:
            start_date, end_date = selected_dates[0], selected_dates[1]
        elif len(selected_dates) == 1:
            start_date = end_date = selected_dates[0]
        else:
            start_date, end_date = min_date, max_date
    else:
        start_date = end_date = selected_dates or min_date

    if start_date is None:
        start_date = min_date
    if end_date is None:
        end_date = start_date
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    filtered = df[
        (df["order_purchase_timestamp"].dt.date >= start_date)
        & (df["order_purchase_timestamp"].dt.date <= end_date)
    ].copy()

    if filtered.empty:
        st.warning("Tidak ada data pada rentang tanggal yang dipilih.")
        st.stop()

    total_orders = filtered["order_id"].nunique()
    total_revenue = filtered["payment_value"].sum()
    total_customers = filtered["customer_unique_id"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Orders", f"{total_orders:,}")
    col2.metric("Total Revenue", f"R$ {total_revenue:,.2f}")
    col3.metric("Unique Customers", f"{total_customers:,}")

    monthly = create_monthly_orders_df(filtered)
    top_categories = (
        filtered.groupby("product_category_name_english")["order_id"]
        .nunique()
        .sort_values(ascending=False)
        .head(10)
        .reset_index(name="order_count")
    )
    rfm = create_rfm_df(filtered)
    seg_summary = (
        rfm.groupby("Segment")
        .agg(jumlah=("customer_unique_id", "count"), avg_monetary=("monetary", "mean"))
        .reindex(SEGMENT_ORDER)
        .fillna(0)
        .reset_index()
    )

    left, right = st.columns(2)

    with left:
        st.subheader("Tren Order Bulanan")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(monthly["period"], monthly["order_count"], marker="o", color="#1565C0", linewidth=2)
        ax.set_xlabel("Periode")
        ax.set_ylabel("Jumlah Order")
        ax.tick_params(axis="x", rotation=45)
        st.pyplot(fig)

    with right:
        st.subheader("Top 10 Kategori Produk")
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.barplot(
            data=top_categories,
            x="order_count",
            y="product_category_name_english",
            palette="Blues_r",
            ax=ax,
        )
        ax.set_xlabel("Jumlah Order")
        ax.set_ylabel("Kategori")
        st.pyplot(fig)

    st.subheader("Ringkasan Segmentasi RFM")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(data=seg_summary, x="Segment", y="jumlah", palette=SEGMENT_COLORS, ax=ax, order=SEGMENT_ORDER)
    ax.set_xlabel("Segmen")
    ax.set_ylabel("Jumlah Pelanggan")
    ax.tick_params(axis="x", rotation=20)
    st.pyplot(fig)

    st.dataframe(
        seg_summary.rename(
            columns={"jumlah": "Jumlah Pelanggan", "avg_monetary": "Rata-rata Monetary"}
        )
    )


if __name__ == "__main__":
    main()
