import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
from PIL import Image
import io
import base64

st.set_page_config(
    page_title="📊 Analytiq — AI-Powered Business Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        footer {visibility: hidden;}
        .block-container {padding-top: 1rem;}
        h1 {color: #2E86C1;}
    </style>
""", unsafe_allow_html=True)

st.title("📊 Analytiq — AI-Powered Business Intelligence Platform")
st.write("Upload CSV, Excel, or a Chart Image — ask questions in plain English.")

# ── GROQ SETUP ──────────────────────────────────────────────
@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_client()

def ask_ai(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"

def ask_ai_vision(image_bytes: bytes, question: str) -> str:
    try:
        image_data = base64.b64encode(image_bytes).decode("utf-8")
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Vision Error: {str(e)}"

# ── TABS ────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📁 Data Analysis",
    "🤖 Chat with Data",
    "👁️ AI Vision"
])

# ══════════════════════════════════════════════
# TAB 1 — DATA ANALYSIS
# ══════════════════════════════════════════════
with tab1:
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file:
        # Load file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(f"✅ Loaded {df.shape[0]} rows × {df.shape[1]} columns")

        # ── Smart column detection ──
        date_cols = []
        for col in df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    date_cols.append(col)
                except:
                    pass

        num_cols = df.select_dtypes(include='number').columns.tolist()
        cat_cols = df.select_dtypes(include='object').columns.tolist()

        # ── Sidebar Filters ──
        st.sidebar.header("🔍 Filters")

        if date_cols:
            date_col = st.sidebar.selectbox("Date column", date_cols)
            df = df.dropna(subset=[date_col])
            min_date = df[date_col].min().date()
            max_date = df[date_col].max().date()
            date_range = st.sidebar.date_input(
                "Date Range",
                [min_date, max_date]
            )
            if len(date_range) == 2:
                df = df[
                    (df[date_col] >= pd.to_datetime(date_range[0])) &
                    (df[date_col] <= pd.to_datetime(date_range[1]))
                ]

        for col in cat_cols[:2]:
            options = df[col].unique().tolist()
            selected = st.sidebar.multiselect(f"{col}", options, default=options)
            if selected:
                df = df[df[col].isin(selected)]

        # ── Preview ──
        st.subheader("📁 Data Preview")
        st.dataframe(df, width="stretch")

        # ── Smart KPIs ──
        st.subheader("📌 Key Metrics")
        if num_cols:
            cols = st.columns(min(len(num_cols), 4))
            for i, col in enumerate(num_cols[:4]):
                cols[i].metric(f"Σ {col}", f"{df[col].sum():,.0f}")

        # ── Charts ──
        if num_cols and cat_cols:
            st.subheader("🥧 Category Distribution")
            fig = px.pie(
                df, names=cat_cols[0], values=num_cols[0],
                title=f"{num_cols[0]} by {cat_cols[0]}"
            )
            st.plotly_chart(fig, width="stretch")

        if date_cols and num_cols:
            st.subheader("📈 Trend Over Time")
            fig2 = px.line(
                df, x=date_cols[0], y=num_cols[0],
                title=f"{num_cols[0]} over time"
            )
            st.plotly_chart(fig2, width="stretch")

        if num_cols and date_cols:
            st.subheader("📊 Monthly Bar Chart")
            df['Month'] = pd.to_datetime(df[date_cols[0]]).dt.to_period('M').astype(str)
            monthly = df.groupby('Month')[num_cols[0]].sum().reset_index()
            fig3 = px.bar(
                monthly, x='Month', y=num_cols[0],
                title=f"Monthly {num_cols[0]}"
            )
            st.plotly_chart(fig3, width="stretch")

        # ── AI Auto Insight ──
        st.subheader("🤖 AI Data Insight")
        if st.button("✨ Generate AI Insight"):
            summary = df[num_cols].describe().to_string() if num_cols else "No numeric data"
            prompt = f"""
You are a business analyst. Here is the dataset summary:
Columns: {list(df.columns)}
Total rows: {len(df)}
Statistics: {summary}

Give 3 clear business insights in simple language.
Be specific with numbers. End with 1 actionable recommendation.
"""
            with st.spinner("Analyzing your data..."):
                insight = ask_ai(prompt)
            st.success(insight)

        # Save for Tab 2
        st.session_state['df'] = df
        st.session_state['num_cols'] = num_cols

    else:
        st.info("👈 Upload a CSV or Excel file to get started.")

# ══════════════════════════════════════════════
# TAB 2 — CHAT WITH YOUR DATA
# ══════════════════════════════════════════════
with tab2:
    st.subheader("🤖 Chat with Your Data")
    st.write("Ask anything about your uploaded data in plain English.")

    if 'df' not in st.session_state:
        st.warning("⚠️ Please upload a file in the Data Analysis tab first.")
    else:
        df = st.session_state['df']

        st.markdown("**💡 Try asking:**")
        col1, col2 = st.columns(2)
        with col1:
            st.code("Which category has highest total?")
            st.code("What is the average value?")
        with col2:
            st.code("Are there any unusual spikes?")
            st.code("Give me a profit summary")

        question = st.text_input("Ask a question about your data:")

        if question and st.button("Ask AI 🤖"):
            prompt = f"""
You are a data analyst assistant.
Dataset shape: {df.shape}
Columns: {list(df.columns)}
Data types: {df.dtypes.to_dict()}
First 5 rows: {df.head().to_string()}
Statistics: {df.describe().to_string()}

User question: {question}

Answer clearly and specifically using the data provided.
If you can calculate something, show the calculation.
"""
            with st.spinner("Thinking..."):
                answer = ask_ai(prompt)
            st.markdown("### 💬 Answer")
            st.success(answer)

# ══════════════════════════════════════════════
# TAB 3 — AI VISION
# ══════════════════════════════════════════════
with tab3:
    st.subheader("👁️ AI Vision — Analyze Any Chart or Image")
    st.write("Upload a chart, graph, or business screenshot — AI will explain it.")

    image_file = st.file_uploader(
        "Upload chart image (PNG, JPG)",
        type=["png", "jpg", "jpeg"]
    )

    if image_file:
        st.image(image_file, caption="Uploaded Image", width="stretch")

        vision_question = st.text_input(
            "What do you want to know?",
            placeholder="e.g. What trend does this chart show? Any anomalies?"
        )

        if st.button("🔍 Analyze with AI Vision"):
            image_bytes = image_file.read()
            question = vision_question if vision_question else (
                "Analyze this chart. Tell me: "
                "1) Main insight 2) Any trends or anomalies "
                "3) What business decision this data supports"
            )
            with st.spinner("AI is reading the image..."):
                result = ask_ai_vision(image_bytes, question)
            st.markdown("### 🧠 AI Vision Analysis")
            st.success(result)

    st.markdown("---")
    st.markdown("**💡 What you can upload:**")
    c1, c2, c3 = st.columns(3)
    c1.info("📊 Any chart or graph screenshot")
    c2.info("📄 PDF report screenshot")
    c3.info("🖥️ Dashboard screenshot")
