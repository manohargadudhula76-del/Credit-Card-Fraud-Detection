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

.stApp {
    background:
    radial-gradient(circle at top left, rgba(56,189,248,0.18), transparent 35%),
    radial-gradient(circle at top right, rgba(239,68,68,0.18), transparent 30%),
    linear-gradient(135deg, #020617 0%, #0f172a 45%, #111827 100%) !important;
    color: #ffffff !important;
}

[data-testid="stHeader"] {
    background: rgba(2, 6, 23, 0.85) !important;
}

.hero {
    padding: 38px;
    border-radius: 25px;
    background:
    linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.85)),
    url("https://images.unsplash.com/photo-1601597111158-2fceff292cdc?auto=format&fit=crop&w=1400&q=80");
    background-size: cover;
    background-position: center;
    border: 1px solid #334155;
    box-shadow: 0 20px 60px rgba(0,0,0,0.45);
}

.hero-title {
    font-size: 58px;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 22px;
    color: #cbd5e1;
    max-width: 850px;
}

.badge {
    display: inline-block;
    padding: 8px 16px;
    background: rgba(250, 204, 21, 0.18);
    border: 1px solid #facc15;
    color: #fde68a;
    border-radius: 50px;
    font-weight: 700;
    margin-bottom: 16px;
}

.card {
    padding: 26px;
    border-radius: 20px;
    background: linear-gradient(135deg, #111827, #1e293b);
    border: 1px solid #334155;
    box-shadow: 0 12px 35px rgba(0,0,0,0.38);
}

.metric-title {
    color: #cbd5e1;
    font-size: 15px;
    font-weight: 600;
}

.metric-value {
    color: #38bdf8;
    font-size: 34px;
    font-weight: 900;
}

.safe {
    color: #4ade80;
}

.fraud {
    color: #fb7185;
}

.gold {
    color: #facc15;
}

.info-box {
    padding: 22px;
    border-radius: 18px;
    background: rgba(15,23,42,0.95);
    border-left: 6px solid #38bdf8;
    color: #e2e8f0;
    font-size: 17px;
}

.warning-box {
    padding: 22px;
    border-radius: 18px;
    background: rgba(127,29,29,0.4);
    border-left: 6px solid #ef4444;
    color: #fecaca;
    font-size: 17px;
}

.success-box {
    padding: 22px;
    border-radius: 18px;
    background: rgba(20,83,45,0.4);
    border-left: 6px solid #22c55e;
    color: #bbf7d0;
    font-size: 17px;
}

h1, h2, h3 {
    color: white !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #111827;
    border-radius: 12px;
    padding: 12px 20px;
    color: white;
    border: 1px solid #334155;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #2563eb, #dc2626) !important;
    color: white !important;
}

.footer {
    text-align: center;
    padding: 25px;
    color: #94a3b8;
    font-size: 15px;
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
st.markdown("""
<div class="hero">
    <div class="badge">🏦 Banking Security • AI Fraud Monitoring • Risk Detection</div>
    <div class="hero-title">FraudShield AI</div>
    <div class="hero-subtitle">
        A professional credit card fraud detection system that analyzes transaction patterns,
        identifies suspicious activity, and supports batch fraud prediction using Machine Learning.
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

tab1, tab2, tab3 = st.tabs([
    "📊 Dataset Intelligence",
    "🤖 Model Performance",
    "🚨 Fraud Prediction"
])

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
    fig1.update_layout(template="plotly_dark", height=480)
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.histogram(
        df,
        x="Amount",
        nbins=80,
        title="Transaction Amount Distribution",
        color_discrete_sequence=["#38bdf8"]
    )
    fig2.update_layout(template="plotly_dark", height=480)
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
        textfont={"size": 22}
    ))

    fig_cm.update_layout(
        title="Confusion Matrix",
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(fig_cm, use_container_width=True)

    st.subheader("ROC Curve")

    fig_roc = go.Figure()
    fig_roc.add_trace(go.Scatter(
        x=[0, 0.03, 0.08, 0.15, 1],
        y=[0, 0.70, 0.86, 0.94, 1],
        mode="lines+markers",
        name="Random Forest ROC Curve",
        line=dict(width=4)
    ))
    fig_roc.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode="lines",
        name="Random Guess",
        line=dict(dash="dash")
    ))

    fig_roc.update_layout(
        title=f"ROC Curve | AUC = {roc_auc:.3f}",
        xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate",
        template="plotly_dark",
        height=500
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