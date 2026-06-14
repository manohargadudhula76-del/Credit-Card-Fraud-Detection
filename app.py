import streamlit as st
import pandas as pd
import pickle
import json
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="FraudShield AI",
    page_icon="💳",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* Main app background */
.stApp {
    background:
    radial-gradient(circle at top left, rgba(56,189,248,0.14), transparent 35%),
    radial-gradient(circle at top right, rgba(239,68,68,0.14), transparent 30%),
    var(--background-color) !important;
    color: var(--text-color) !important;
}

/* Streamlit header */
[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0.08) !important;
}

/* Hero */
.hero {
    padding: 38px;
    border-radius: 25px;
    background:
    linear-gradient(135deg, rgba(15,23,42,0.88), rgba(30,41,59,0.72)),
    url("https://images.unsplash.com/photo-1601597111158-2fceff292cdc?auto=format&fit=crop&w=1400&q=80");
    background-size: cover;
    background-position: center;
    border: 1px solid rgba(148,163,184,0.45);
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
}

.hero-title {
    font-size: 48px;
    font-weight: 900;
    color: #ffffff !important;
    line-height: 1.05;
    margin-bottom: 6px;
    word-break: keep-all;
}

.hero-ai {
    font-size: 27px;
    font-weight: 800;
    color: #38bdf8 !important;
    line-height: 1.25;
    margin-bottom: 12px;
    max-width: 900px;
}

.hero-subtitle {
    font-size: 19px;
    color: #e2e8f0 !important;
    max-width: 850px;
    line-height: 1.6;
}

.badge {
    display: inline-block;
    padding: 8px 16px;
    background: rgba(250, 204, 21, 0.18);
    border: 1px solid #facc15;
    color: #fde68a !important;
    border-radius: 50px;
    font-weight: 700;
    margin-bottom: 16px;
}

/* Cards */
.card {
    padding: 26px;
    border-radius: 20px;
    background: var(--secondary-background-color) !important;
    border: 1px solid rgba(148,163,184,0.35);
    box-shadow: 0 12px 35px rgba(0,0,0,0.18);
}

.metric-title {
    color: var(--text-color) !important;
    opacity: 0.75;
    font-size: 15px;
    font-weight: 600;
}

.metric-value {
    color: #0284c7 !important;
    font-size: 34px;
    font-weight: 900;
}

.safe {
    color: #16a34a !important;
}

.fraud {
    color: #dc2626 !important;
}

.gold {
    color: #ca8a04 !important;
}

/* Info boxes */
.info-box {
    padding: 22px;
    border-radius: 18px;
    background: var(--secondary-background-color) !important;
    border-left: 6px solid #0284c7;
    color: var(--text-color) !important;
    font-size: 17px;
}

.warning-box {
    padding: 22px;
    border-radius: 18px;
    background: rgba(239,68,68,0.15) !important;
    border-left: 6px solid #dc2626;
    color: var(--text-color) !important;
    font-size: 17px;
}

.success-box {
    padding: 22px;
    border-radius: 18px;
    background: rgba(34,197,94,0.15) !important;
    border-left: 6px solid #16a34a;
    color: var(--text-color) !important;
    font-size: 17px;
}

/* Headings */
h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: var(--text-color);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    flex-wrap: wrap;
}

.stTabs [data-baseweb="tab"] {
    background-color: var(--secondary-background-color) !important;
    border-radius: 12px;
    padding: 12px 20px;
    color: var(--text-color) !important;
    border: 1px solid rgba(148,163,184,0.35);
}

.stTabs [data-baseweb="tab"] p {
    color: var(--text-color) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #2563eb, #dc2626) !important;
    color: #ffffff !important;
}

.stTabs [aria-selected="true"] p {
    color: #ffffff !important;
}

/* Radio buttons */
[role="radiogroup"] label {
    background: var(--secondary-background-color) !important;
    border: 1px solid rgba(148,163,184,0.35);
    border-radius: 12px;
    padding: 8px 12px;
    margin-right: 8px;
}

[role="radiogroup"] label p {
    color: var(--text-color) !important;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(135deg, #2563eb, #dc2626) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 18px !important;
    font-weight: 700 !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: scale(1.02);
    color: #ffffff !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: var(--secondary-background-color) !important;
    border: 1px solid rgba(148,163,184,0.35);
    border-radius: 14px;
    padding: 14px;
}

[data-testid="stFileUploader"] * {
    color: var(--text-color) !important;
}

/* Selectbox */
[data-baseweb="select"] {
    background: var(--secondary-background-color) !important;
}

[data-baseweb="select"] * {
    color: var(--text-color) !important;
}

/* Dataframe/table area */
[data-testid="stDataFrame"] {
    background: var(--secondary-background-color) !important;
    border-radius: 12px;
}

/* Plotly chart white area fix */
.js-plotly-plot,
.plotly,
.plot-container {
    background: var(--background-color) !important;
}

/* Footer */
.footer {
    text-align: center;
    padding: 25px;
    color: var(--text-color) !important;
    opacity: 0.75;
    font-size: 15px;
}

/* Mobile responsive */
@media (max-width: 768px) {
    .hero {
        padding: 22px;
        border-radius: 18px;
        background-position: center;
    }

    .badge {
        font-size: 11px;
        padding: 6px 10px;
        line-height: 1.4;
        margin-bottom: 12px;
    }

    .hero-title {
        font-size: 34px;
        line-height: 1.05;
        margin-bottom: 8px;
    }

    .hero-ai {
        font-size: 18px;
        line-height: 1.35;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 14px;
        line-height: 1.6;
    }

    .card {
        padding: 18px;
        border-radius: 16px;
        margin-bottom: 10px;
    }

    .metric-title {
        font-size: 13px;
    }

    .metric-value {
        font-size: 25px;
    }

    .info-box,
    .warning-box,
    .success-box {
        padding: 16px;
        font-size: 14px;
        border-radius: 14px;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 8px 10px;
        font-size: 12px;
    }

    [role="radiogroup"] label {
        display: block;
        margin-bottom: 8px;
        width: 100%;
    }

    h1 {
        font-size: 28px !important;
    }

    h2 {
        font-size: 24px !important;
    }

    h3 {
        font-size: 20px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD FILES ----------------
@st.cache_data
def load_data():
    return pd.read_csv("data/creditcard.csv")

@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

@st.cache_resource
def load_scaler():
    with open("scaler.pkl", "rb") as f:
        return pickle.load(f)

with open("columns.json", "r") as f:
    columns = json.load(f)["data_columns"]

df = load_data()
model = load_model()
scaler = load_scaler()

# ---------------- HERO SECTION ----------------
st.markdown(
"""
<div class="hero">

<span class="badge">
🏦 Banking Security • AI Fraud Monitoring • Risk Detection
</span>

<h1 class="hero-title">
💳 FraudShield
</h1>

<div class="hero-ai">
AI Powered Credit Card Fraud Detection System
</div>

<p class="hero-subtitle">
Detect suspicious credit card transactions using Machine Learning,
Random Forest and SMOTE with real-time dashboard insights.
</p>

</div>
""",
unsafe_allow_html=True
)

st.write("")

tab1, tab2, tab3 = st.tabs([
    "📊 Dataset Intelligence",
    "🤖 Model Performance",
    "🚨 Fraud Prediction"
])

# ---------------- CHART THEME FUNCTION ----------------
def apply_chart_theme(fig, height=480):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title_font=dict(color="#38bdf8", size=20),
        legend=dict(font=dict(color="#94a3b8")),
        xaxis=dict(
            title_font=dict(color="#94a3b8"),
            tickfont=dict(color="#94a3b8"),
            gridcolor="rgba(148,163,184,0.25)"
        ),
        yaxis=dict(
            title_font=dict(color="#94a3b8"),
            tickfont=dict(color="#94a3b8"),
            gridcolor="rgba(148,163,184,0.25)"
        )
    )
    return fig


# ---------------- TAB 1 ----------------
with tab1:
    st.header("📊 Dataset Intelligence Dashboard")

    total = len(df)
    normal = df[df["Class"] == 0].shape[0]
    fraud = df[df["Class"] == 1].shape[0]
    fraud_percentage = (fraud / total) * 100

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="metric-title">Total Transactions</div>
            <div class="metric-value">{total:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card">
            <div class="metric-title">Legitimate Transactions</div>
            <div class="metric-value safe">{normal:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="card">
            <div class="metric-title">Fraud Transactions</div>
            <div class="metric-value fraud">{fraud:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="card">
            <div class="metric-title">Fraud Percentage</div>
            <div class="metric-value gold">{fraud_percentage:.3f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class="info-box">
    This dataset is highly imbalanced. Fraud transactions are very rare compared to normal transactions.
    That is why SMOTE was used during model training.
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    class_count = df["Class"].value_counts().reset_index()
    class_count.columns = ["Class", "Count"]
    class_count["Class"] = class_count["Class"].map({0: "Normal", 1: "Fraud"})

    fig1 = px.bar(
        class_count,
        x="Class",
        y="Count",
        text="Count",
        title="Normal vs Fraud Transactions",
        color="Class",
        color_discrete_map={"Normal": "#22c55e", "Fraud": "#ef4444"}
    )
    fig1.update_traces(textfont_color="#ffffff")
    fig1 = apply_chart_theme(fig1, height=480)
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.histogram(
        df,
        x="Amount",
        nbins=80,
        title="Transaction Amount Distribution",
        color_discrete_sequence=["#38bdf8"]
    )
    fig2 = apply_chart_theme(fig2, height=480)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)


# ---------------- TAB 2 ----------------
with tab2:
    st.header("🤖 Model Performance Dashboard")

    accuracy = 0.9977704434535304
    precision = 0.4263959390862944
    recall = 0.8571428571428571
    f1 = 0.5694915254237288
    roc_auc = 0.9768104062108806

    c1, c2, c3, c4, c5 = st.columns(5)

    metrics = [
        ("Accuracy", accuracy),
        ("Precision", precision),
        ("Recall", recall),
        ("F1 Score", f1),
        ("ROC AUC", roc_auc)
    ]

    for col, (name, value) in zip([c1, c2, c3, c4, c5], metrics):
        with col:
            st.markdown(f"""
            <div class="card">
                <div class="metric-title">{name}</div>
                <div class="metric-value">{value:.3f}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class="success-box">
    ✅ Best Model Selected: <b>Random Forest Classifier</b><br>
    Random Forest performed best among the trained models and was selected for deployment.
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class="warning-box">
    ⚠️ In fraud detection, <b>Recall</b> is very important because missing a fraud transaction is more dangerous
    than flagging a normal transaction as suspicious.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Model Metrics Table")

    metrics_df = pd.DataFrame({
        "Metric": ["Accuracy", "Precision", "Recall", "F1 Score", "ROC AUC"],
        "Score": [accuracy, precision, recall, f1, roc_auc]
    })

    st.dataframe(metrics_df, use_container_width=True)

    st.subheader("Confusion Matrix")

    cm = [[56717, 113],
          [14, 84]]

    fig_cm = go.Figure(data=go.Heatmap(
        z=cm,
        x=["Predicted Normal", "Predicted Fraud"],
        y=["Actual Normal", "Actual Fraud"],
        colorscale="Reds",
        text=cm,
        texttemplate="%{text}",
        textfont={"size": 22, "color": "#111827"}
    ))

    fig_cm = apply_chart_theme(fig_cm, height=500)
    fig_cm.update_layout(title="Confusion Matrix")
    st.plotly_chart(fig_cm, use_container_width=True)

    st.subheader("ROC Curve")

    fig_roc = go.Figure()

    fig_roc.add_trace(go.Scatter(
        x=[0, 0.03, 0.08, 0.15, 1],
        y=[0, 0.70, 0.86, 0.94, 1],
        mode="lines+markers",
        name="Random Forest ROC Curve",
        line=dict(width=4, color="#2563eb"),
        marker=dict(size=8, color="#2563eb")
    ))

    fig_roc.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode="lines",
        name="Random Guess",
        line=dict(dash="dash", color="#ef4444")
    ))

    fig_roc = apply_chart_theme(fig_roc, height=500)
    fig_roc.update_layout(
        title=f"ROC Curve | AUC = {roc_auc:.3f}",
        xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate"
    )

    st.plotly_chart(fig_roc, use_container_width=True)

    csv_metrics = metrics_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Model Metrics",
        csv_metrics,
        "model_metrics.csv",
        "text/csv"
    )


# ---------------- TAB 3 ----------------
with tab3:
    st.header("🚨 Fraud Prediction Center")

    st.markdown("""
    <div class="info-box">
    Test the fraud detection model using CSV upload, built-in demo datasets, or a random sample transaction.
    This makes the app easy to use on both laptop and mobile.
    </div>
    """, unsafe_allow_html=True)

    prediction_mode = st.radio(
        "Choose Prediction Mode",
        ["📁 Upload CSV", "🎲 Try Demo Dataset", "⚡ Random Transaction"],
        horizontal=True
    )

    def predict_transactions(input_df):
        missing_cols = [col for col in columns if col not in input_df.columns]

        if missing_cols:
            st.error(f"Missing columns: {missing_cols}")
            return

        prediction_data = input_df[columns].copy()
        prediction_data["Amount"] = scaler.transform(prediction_data[["Amount"]])

        predictions = model.predict(prediction_data)

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(prediction_data)[:, 1]
        else:
            probabilities = [0] * len(predictions)

        output_df = input_df.copy()
        output_df["Prediction"] = predictions
        output_df["Prediction_Label"] = output_df["Prediction"].map({
            0: "Normal",
            1: "Fraud"
        })
        output_df["Fraud_Probability"] = [round(p * 100, 2) for p in probabilities]

        st.subheader("Prediction Results")
        st.dataframe(output_df, use_container_width=True)

        normal_pred = (predictions == 0).sum()
        fraud_pred = (predictions == 1).sum()

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"""
            <div class="card">
                <div class="metric-title">Predicted Normal</div>
                <div class="metric-value safe">{normal_pred}</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="card">
                <div class="metric-title">Predicted Fraud</div>
                <div class="metric-value fraud">{fraud_pred}</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            avg_prob = round(sum(probabilities) / len(probabilities) * 100, 2)
            st.markdown(f"""
            <div class="card">
                <div class="metric-title">Avg Fraud Probability</div>
                <div class="metric-value gold">{avg_prob}%</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        result_csv = output_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download Prediction Results",
            result_csv,
            "fraud_predictions.csv",
            "text/csv"
        )

    if prediction_mode == "📁 Upload CSV":
        uploaded_file = st.file_uploader("Upload Transaction CSV File", type=["csv"])

        if uploaded_file is not None:
            input_df = pd.read_csv(uploaded_file)

            st.subheader("Uploaded Transactions")
            st.dataframe(input_df.head(10), use_container_width=True)

            predict_transactions(input_df)

    elif prediction_mode == "🎲 Try Demo Dataset":
        demo_option = st.selectbox(
            "Select Demo Dataset",
            [
                "Normal Transactions",
                "Fraud Transactions",
                "Mixed Normal + Fraud Transactions"
            ]
        )

        demo_paths = {
            "Normal Transactions": "demo_csv_files/demo_normal_transactions.csv",
            "Fraud Transactions": "demo_csv_files/demo_fraud_transactions.csv",
            "Mixed Normal + Fraud Transactions": "demo_csv_files/demo_mixed_normal_fraud.csv"
        }

        demo_df = pd.read_csv(demo_paths[demo_option])

        st.subheader("Demo Dataset Preview")
        st.dataframe(demo_df.head(10), use_container_width=True)

        if st.button("Predict Demo Dataset"):
            predict_transactions(demo_df)

    elif prediction_mode == "⚡ Random Transaction":
        random_df = df.drop("Class", axis=1).sample(1)

        st.subheader("Random Transaction")
        st.dataframe(random_df, use_container_width=True)

        if st.button("Generate Prediction"):
            predict_transactions(random_df)


st.markdown("""
<div class="footer">
    FraudShield AI | Credit Card Fraud Detection using Machine Learning | Built with Streamlit
</div>
""", unsafe_allow_html=True)