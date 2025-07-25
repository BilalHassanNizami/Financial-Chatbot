#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import re
import plotly.express as px
import gradio as gr

# Load data
try:
    df = pd.read_csv("chatbot_cleaned.csv")
except FileNotFoundError:
    raise FileNotFoundError("Could not find 'chatbot_cleaned.csv'. Ensure the file is in the root directory.")

# Metric cleaning
metrics_list = df['Metric'].str.lower().unique()
all_years = [2022, 2023, 2024]
default_companies = ["tesla", "apple", "microsoft"]

# Aliases (cleaned to remove duplicates)
alias_dict = {
    "revenue": "total revenue",
    "sales": "total revenue",
    "profit": "net income",
    "earnings": "net income",
    "earned": "net income",
    "earned more": "net income",
    "made profit": "net income",
    "made money": "net income",
    "make money": "net income",
    "made more": "net income",
    "make more": "net income",
    "who earned more": "net income",
    "which company earned more": "net income",
    "which earned": "net income",
    "op income": "operating income",
    "operating income": "operating income",
    "r&d": "r&d expense",
    "rnd": "r&d expense",
    "research": "r&d expense",
    "research and development": "r&d expense",
    "r&d est": "r&d expense (est.)",
    "r&d estimate": "r&d expense (est.)",
    "assets": "total assets",
    "liabilities": "total liabilities",
    "debt": "total liabilities",
    "equity": "shareholders' equity",
    "shareholder equity": "shareholders' equity",
    "cash equivalent": "cash & cash equivalents",
    "cash equivalents": "cash & cash equivalents",
    "cash eq": "cash & cash equivalents",
    "cash equi": "cash & cash equivalents",
    "cash equiv": "cash & cash equivalents",
    "operating cash": "operating cash flow",
    "op cash": "operating cash flow",
    "operating cash flow": "operating cash flow",
    "ocf": "operating cash flow",
    "capex": "capital expenditures",
    "capital expense": "capital expenditures",
    "cap exp": "capital expenditures",
    "cap expenditure": "capital expenditures",
    "capital expenditure": "capital expenditures",
    "free cash flow": "free cash flow (est.)",
    "cash flow": "free cash flow (est.)",
    "estimated free cash": "free cash flow (est.)",
    "free cash flow est": "free cash flow (est.)",
    "est free cash flow": "free cash flow (est.)",
    "fcf": "free cash flow (est.)",
    "eps bas": "eps (basic)",
    "eps basic": "eps (basic)",
    "eps diluted": "eps (diluted)",
    "eps dil": "eps (diluted)",
    "cloud": "cloud revenue",
    "cloud revenue": "cloud revenue",
}

# Enhanced year phrase mapping
def extract_years(message):
    years = []
    message = message.lower()

    # Regex year detection
    year_matches = re.findall(r"\b(2022|2023|2024)\b", message)
    years.extend([int(y) for y in year_matches])

    # Phrase-based mappings
    if any(phrase in message for phrase in ["all years", "last 3 years", "since 2022", "past 3 years"]):
        return [2022, 2023, 2024]
    if any(phrase in message for phrase in ["last two years", "last 2 years", "past 2 years", "since 2023", "second and third year", "2nd and 3rd year", "second and last year"]):
        return [2023, 2024]
    if any(phrase in message for phrase in ["first and last year", "1st and 3rd year"]):
        return [2022, 2024]
    if any(phrase in message for phrase in ["first two years", "first 2 years", "1st and 2nd year", "first and second year"]):
        return [2022, 2023]
    if any(phrase in message for phrase in ["second year", "2nd year"]):
        return [2023]
    if any(phrase in message for phrase in ["first year", "1st year"]):
        return [2022]
    if any(phrase in message for phrase in ["third year", "3rd year", "latest year", "last year", "2024"]):
        return [2024]

    return sorted(list(set(years))) if years else all_years

# Chart functions
def plot_bar_chart(company_df, metric, year):
    fig = px.bar(company_df, x='Company', y=str(year), title=f"{metric.title()} by Company in {year}", text=str(year))
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(template='plotly_white', uniformtext_minsize=8, uniformtext_mode='show')
    return fig

def plot_comparison_chart(metric, years):
    chart_data = []
    for _, row in df[df['Metric'].str.lower() == metric].iterrows():
        company = row["Company"]
        for year in years:
            val = row.get(str(year))
            if pd.notna(val):
                chart_data.append({
                    "Company": company,
                    "Year": year,
                    "Value": val
                })
    if not chart_data:
        return None
    chart_df = pd.DataFrame(chart_data)
    fig = px.bar(
        chart_df,
        x="Year",
        y="Value",
        color="Company",
        barmode="group",
        title=f"{metric.title()} Comparison ({', '.join(map(str, years))})",
        text="Value"
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(template='plotly_white')
    return fig

# Chatbot core
def handle_message(message, history):
    if not message:
        return history, "Please enter a question.", None

    message = message.lower()

    # Companies
    companies = re.findall(r"\b(tesla|apple|microsoft)\b", message)
    if not companies or any(phrase in message for phrase in ["all companies", "compare companies"]):
        companies = default_companies

    # Years
    years = extract_years(message)

    # Metric
    metric_match = [m for m in metrics_list if m in message]
    if not metric_match:
        for alias, standard in alias_dict.items():
            if re.search(rf"\b{re.escape(alias)}\b", message):
                metric_match = [standard]
                break
    metric = metric_match[0] if metric_match else None

    if not metric:
        reply = "❌ Please mention a valid financial metric (e.g., revenue, EPS, R&D)."
        return history + [{"role": "user", "content": message}, {"role": "assistant", "content": reply}], "", None

    # Filter Data
    filtered_df = df[
        (df['Metric'].str.lower() == metric) &
        (df['Company'].str.lower().isin(companies))
    ]

    if filtered_df.empty:
        reply = "❌ No matching data found for the given metric and companies."
        return history + [{"role": "user", "content": message}, {"role": "assistant", "content": reply}], "", None

    # Text Reply
    lines = [f"📊 **{metric.title()} Comparison**:"]
    for company in companies:
        sub = filtered_df[filtered_df["Company"].str.lower() == company]
        if sub.empty:
            continue
        lines.append(f"\n**{company.title()} – {metric.title()}**")
        for year in years:
            if str(year) in sub.columns:
                val = sub[str(year)].values[0] if not sub[str(year)].empty else None
                if pd.notna(val):
                    lines.append(f"{year}: ${val:,.0f}")
                else:
                    lines.append(f"{year}: Data not available")
            else:
                lines.append(f"{year}: Data not available")

    reply = "\n".join(lines)

    # Chart
    chart = plot_comparison_chart(metric, years)

    # Final Output
    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply}
    ]
    return history, "", chart

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown(
        """
        # 💬 Financial Chatbot  
        👨‍💻 Developed by: **📊 Bilal Hassan Nizami**  

        Ask about Tesla, Apple, or Microsoft (Annual Financial Reports filed with US SEC, 2022–2024).  

        #### 📌 Example Questions:
        - *Compare R&D expenses for all companies*
        - *Tesla operating income all years*
        - *Apple vs Microsoft revenue since 2022*
        - *Who earned more in 1st and 3rd year?*
        """,
        elem_id="title"
    )

    with gr.Row():
        with gr.Column():
            msg = gr.Textbox(label="Ask your question:")
            btn = gr.Button("Submit")
            chatbot_output = gr.Chatbot(type="messages", label="Conversation")
        chart_output = gr.Plot(label="Chart")

    btn.click(
        fn=handle_message,
        inputs=[msg, chatbot_output],
        outputs=[chatbot_output, msg, chart_output],
    ).then(
        lambda chart: gr.update(visible=chart is not None),
        inputs=[chart_output],
        outputs=[chart_output],
    )

# Launch
demo.launch(share=True)


# In[ ]:




