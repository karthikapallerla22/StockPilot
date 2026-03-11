import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# ----------------------------------
# Page Configuration
# ----------------------------------
st.set_page_config(page_title="StockPilot Dashboard", layout="wide")

st.title("📊 StockPilot - Stock Market Analysis Dashboard")
# ----------------------------------
# Custom Gradient Background
# ----------------------------------

page_bg = """
<style>

/* ---------------- MAIN BACKGROUND ---------------- */
[data-testid="stAppViewContainer"]{
background: radial-gradient(circle at 20% 90%, #C84A9A 0%, transparent 40%),
            linear-gradient(135deg,#061A3A,#0B2A5B,#1F3F8A,#6A3FA0);
background-attachment: fixed;
}

/* ---------------- SIDEBAR ---------------- */
[data-testid="stSidebar"]{
background: linear-gradient(180deg,#061A3A,#0B2A5B);
}

/* SIDEBAR TITLE */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3{
color:white !important;
}

/* ---------------- TEXT ---------------- */
h1,h2,h3,h4,h5,h6{
color:#ffffff;
}

p,span,label{
color:#e6e6e6;
}

/* ---------------- BUTTONS ---------------- */
.stButton>button{
background: linear-gradient(135deg,#ff7ac6,#c84a9a);
color:white;
border-radius:8px;
border:none;
font-weight:600;
transition:0.3s;
}

.stButton>button:hover{
background: linear-gradient(135deg,#ff9bd6,#d86ab0);
}

/* ---------------- INPUT BOXES ---------------- */
.stTextInput>div>div>input{
background-color:rgba(255,255,255,0.9);
color:#061A3A;
border-radius:6px;
}

/* ---------------- SELECT BOX ---------------- */
.stSelectbox>div>div{
background-color:rgba(255,255,255,0.9);
color:#061A3A;
}

/* ---------------- SLIDER ---------------- */
.stSlider>div>div{
color:white;
}

/* ---------------- DATAFRAME ---------------- */
[data-testid="stDataFrame"]{
background-color:rgba(255,255,255,0.95);
border-radius:10px;
}

/* ---------------- METRIC CARDS ---------------- */
[data-testid="stMetric"]{
background:rgba(255,255,255,0.08);
padding:12px;
border-radius:10px;
}

/* ---------------- CHATBOT AREA ---------------- */

/* remove black strip behind chatbot */
[data-testid="stBottom"]{
background: radial-gradient(circle at 20% 90%, #C84A9A 0%, transparent 40%),
            linear-gradient(135deg,#061A3A,#0B2A5B,#1F3F8A,#6A3FA0) !important;
}

/* remove inner dark container */
[data-testid="stBottom"] > div{
background: transparent !important;
}

/* glass style chat input */
[data-testid="stChatInput"]{
background: rgba(255,255,255,0.08) !important;
backdrop-filter: blur(12px);
-webkit-backdrop-filter: blur(12px);
border: 1px solid rgba(255,255,255,0.2);
border-radius: 12px;
padding: 8px;
}

/* chat text area */
[data-testid="stChatInput"] textarea{
background: transparent !important;
color: white !important;
}

/* placeholder */
[data-testid="stChatInput"] textarea::placeholder{
color: rgba(255,255,255,0.6);
}

/* send button */
[data-testid="stChatInput"] button{
background: rgba(255,255,255,0.15);
border-radius: 8px;
border: none;
color: white;
}

/* ---------------- TOOLBAR ---------------- */

/* deploy button */
[data-testid="stToolbar"] button{
color:black !important;
}

/* hamburger menu */
[data-testid="stMainMenu"] svg{
fill:black !important;
}

</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)
# ----------------------------------
# Ticker List
# ----------------------------------
tickers = [
    "AAPL","MSFT","TSLA","AMZN","NVDA","GOOGL","META","NFLX",
    "RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS","WIPRO.NS","SBIN.NS"
]

# ----------------------------------
# Sidebar Settings
# ----------------------------------
st.sidebar.header("Stock Settings")

ticker = st.sidebar.text_input(
    "Enter Stock Symbol",
    "AAPL"
)

period = st.sidebar.selectbox(
    "Select Time Period",
    ["6mo","1y","2y","5y"]
)

sma_short = st.sidebar.slider(
    "Short SMA Window",
    5,50,20
)

sma_long = st.sidebar.slider(
    "Long SMA Window",
    20,200,50
)

rsi_period = st.sidebar.slider(
    "RSI Period",
    7,30,14
)
# -------------------------------
# Wishlist Feature
# -------------------------------

st.sidebar.subheader("⭐ Wishlist")

# Initialize wishlist
if "wishlist" not in st.session_state:
    st.session_state.wishlist = []

# Input for ticker
ticker_input = st.sidebar.text_input("Add Stock (Ticker)")

# Add stock
if st.sidebar.button("Add Stock"):
    if ticker_input:
        ticker = ticker_input.upper()
        if ticker not in st.session_state.wishlist:
            st.session_state.wishlist.append(ticker)
        else:
            st.sidebar.warning("Stock already added")

st.sidebar.write("### Saved Stocks")

# Function to get stock data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    if not data.empty:
        price = data["Close"].iloc[-1]
        open_price = data["Open"].iloc[-1]
        change = ((price - open_price) / open_price) * 100
        return price, change
    return None, None

# Display wishlist
for i, stock in enumerate(st.session_state.wishlist):

    col1, col2, col3 = st.sidebar.columns([3,2,1])

    price, change = get_stock_data(stock)

    if price:
        if change > 0:
            col1.markdown(f"**{stock}** 🟢")
            col2.write(f"${price:.2f} (+{change:.2f}%)")
        else:
            col1.markdown(f"**{stock}** 🔴")
            col2.write(f"${price:.2f} ({change:.2f}%)")
    else:
        col1.write(stock)

    # Remove button
    if col3.button("✕", key=f"remove_{i}"):
        st.session_state.watchlist.pop(i)
        st.rerun()

# Clear wishlist
if st.sidebar.button("Clear Wishlist"):
    st.session_state.wishlist = []
    st.rerun()
# ----------------------------------
# Comparison Section
# ----------------------------------
st.sidebar.markdown("---")
st.sidebar.header("Compare Two Stocks")

stock1 = st.sidebar.selectbox(
    "First Stock Ticker",
    tickers
)

stock2 = st.sidebar.selectbox(
    "Second Stock Ticker",
    tickers,
    index=1
)

compare_btn = st.sidebar.button("Compare Stocks")

# ----------------------------------
# Load Data
# ----------------------------------
@st.cache_data
def load_data(ticker, period):
    df = yf.download(ticker, period=period)
    df.dropna(inplace=True)
    return df

try:
    df = load_data(ticker, period)
except:
    st.error("Unable to fetch stock data.")
    st.stop()

# ----------------------------------
# Indicators
# ----------------------------------
df["SMA_Short"] = df["Close"].rolling(sma_short).mean()
df["SMA_Long"] = df["Close"].rolling(sma_long).mean()

# RSI Calculation
delta = df["Close"].diff()

gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(rsi_period).mean()
avg_loss = loss.rolling(rsi_period).mean()

rs = avg_gain / avg_loss

df["RSI"] = 100 - (100 / (1 + rs))

# ----------------------------------
# Trading Signals
# ----------------------------------
df["Signal"] = 0
df.loc[df["SMA_Short"] > df["SMA_Long"], "Signal"] = 1
df.loc[df["SMA_Short"] < df["SMA_Long"], "Signal"] = -1

# ----------------------------------
# Backtesting
# ----------------------------------
df["Returns"] = df["Close"].pct_change()

df["Strategy_Returns"] = df["Returns"] * df["Signal"].shift(1)

market_returns = (1 + df["Returns"]).cumprod()
strategy_returns = (1 + df["Strategy_Returns"]).cumprod()

# ----------------------------------
# Data Preview
# ----------------------------------
st.subheader(f"Latest Stock Data ({ticker})")
st.dataframe(df.tail())

# ----------------------------------
# Interactive Candlestick Chart
# ----------------------------------
st.subheader("Interactive Stock Chart")

fig = go.Figure()

fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Price"
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["SMA_Short"],
        mode="lines",
        name=f"SMA {sma_short}"
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["SMA_Long"],
        mode="lines",
        name=f"SMA {sma_long}"
    )
)

fig.update_layout(
    title=f"{ticker} Stock Price",
    xaxis_title="Date",
    yaxis_title="Price",
    template="plotly_dark",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# RSI Indicator (Interactive)
# ----------------------------------
st.subheader("RSI Indicator")

fig_rsi = go.Figure()

fig_rsi.add_trace(
    go.Scatter(
        x=df.index,
        y=df["RSI"],
        mode="lines",
        name="RSI"
    )
)

fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")

fig_rsi.update_layout(
    title="Relative Strength Index (RSI)",
    xaxis_title="Date",
    yaxis_title="RSI Value",
    template="plotly_dark",
    hovermode="x unified"
)

st.plotly_chart(fig_rsi, use_container_width=True)
# ----------------------------------
# Strategy Backtesting (Interactive)
# ----------------------------------
st.subheader("Strategy Backtesting")

fig_backtest = go.Figure()

fig_backtest.add_trace(
    go.Scatter(
        x=df.index,
        y=market_returns,
        mode="lines",
        name="Market Returns"
    )
)

fig_backtest.add_trace(
    go.Scatter(
        x=df.index,
        y=strategy_returns,
        mode="lines",
        name="Strategy Returns"
    )
)

fig_backtest.update_layout(
    title="Strategy vs Market Performance",
    xaxis_title="Date",
    yaxis_title="Growth",
    template="plotly_dark",
    hovermode="x unified"
)

st.plotly_chart(fig_backtest, use_container_width=True)
# ----------------------------------
# Performance Metrics
# ----------------------------------
st.subheader("Performance")

market_return = (market_returns.iloc[-1] - 1) * 100
strategy_return = (strategy_returns.iloc[-1] - 1) * 100

col1, col2 = st.columns(2)

col1.metric("Market Return", f"{market_return:.2f}%")
col2.metric("Strategy Return", f"{strategy_return:.2f}%")

# ----------------------------------
# Latest Trading Signal
# ----------------------------------
st.subheader("Trading Signal")

signal = df["Signal"].iloc[-1]

if signal == 1:
    text = "📈 BUY SIGNAL"
    color = "#00ff9d"

elif signal == -1:
    text = "📉 SELL SIGNAL"
    color = "#ff4b4b"

else:
    text = "⚖ HOLD SIGNAL"
    color = "#ffd166"


st.markdown(f"""
<div style="
backdrop-filter: blur(12px);
background: rgba(255,255,255,0.08);
border: 1px solid rgba(255,255,255,0.2);
padding: 25px;
border-radius: 15px;
text-align:center;
font-size:26px;
font-weight:600;
color:{color};
box-shadow: 0 8px 32px rgba(0,0,0,0.3);
">
{text}
</div>
""", unsafe_allow_html=True)
# ----------------------------------
# Risk Analysis
# ----------------------------------

st.subheader("⚠ Risk Analysis")

daily_returns = df["Returns"].dropna()

# Volatility
volatility = daily_returns.std() * np.sqrt(252)

# Sharpe Ratio
sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252)

# Maximum Drawdown
close = df["Close"].squeeze()   # ensure Series

rolling_max = close.cummax()
drawdown = (close - rolling_max) / rolling_max
drawdown = drawdown.fillna(0)   # prevent blank graph

max_drawdown = float(drawdown.min())

col1, col2, col3 = st.columns(3)

col1.metric("Volatility (Risk)", f"{volatility*100:.2f}%")
col2.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
col3.metric("Max Drawdown", f"{max_drawdown*100:.2f}%")

# -------------------------
# Drawdown Chart
# -------------------------

st.subheader("📉 Drawdown Chart")

fig_drawdown = go.Figure()

fig_drawdown.add_trace(
    go.Scatter(
        x=drawdown.index,
        y=drawdown.values,
        mode="lines",
        name="Drawdown"
    )
)

fig_drawdown.add_hline(y=0, line_dash="dash")  # reference line

fig_drawdown.update_layout(
    title="Maximum Drawdown Over Time",
    xaxis_title="Date",
    yaxis_title="Drawdown",
    template="plotly_dark"
)

st.plotly_chart(fig_drawdown, use_container_width=True)
# ----------------------------------
# Stock Comparison
# ----------------------------------
if compare_btn:

    st.subheader(f"📊 {stock1} vs {stock2} Comparison")

    data1 = yf.download(stock1, period="6mo")
    data2 = yf.download(stock2, period="6mo")

    if data1.empty or data2.empty:
        st.error("Stock data not available")

    else:

        close1 = data1["Close"].squeeze()
        close2 = data2["Close"].squeeze()

        fig_compare = go.Figure()

        # Stock 1 Line
        fig_compare.add_trace(
            go.Scatter(
                x=data1.index,
                y=close1,
                mode="lines",
                name=stock1,
                customdata=data1[["Open","High","Low"]].values,
                hovertemplate=
                "Date: %{x}<br>" +
                "Open: %{customdata[0]:.2f}<br>" +
                "High: %{customdata[1]:.2f}<br>" +
                "Low: %{customdata[2]:.2f}<br>" +
                "Close: %{y:.2f}<extra></extra>"
            )
        )

        # Stock 2 Line
        fig_compare.add_trace(
            go.Scatter(
                x=data2.index,
                y=close2,
                mode="lines",
                name=stock2,
                customdata=data2[["Open","High","Low"]].values,
                hovertemplate=
                "Date: %{x}<br>" +
                "Open: %{customdata[0]:.2f}<br>" +
                "High: %{customdata[1]:.2f}<br>" +
                "Low: %{customdata[2]:.2f}<br>" +
                "Close: %{y:.2f}<extra></extra>"
            )
        )

        fig_compare.update_layout(
            title="Stock Price Comparison",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_dark",
            hovermode="closest"
        )

        st.plotly_chart(fig_compare, use_container_width=True)

        # Latest Prices
        price1 = float(close1.iloc[-1])
        price2 = float(close2.iloc[-1])

        # Starting Prices
        start1 = float(close1.iloc[0])
        start2 = float(close2.iloc[0])

        # Returns
        return1 = ((price1 - start1) / start1) * 100
        return2 = ((price2 - start2) / start2) * 100

        col1, col2 = st.columns(2)

        col1.metric(stock1, f"${price1:.2f}", f"{return1:.2f}%")
        col2.metric(stock2, f"${price2:.2f}", f"{return2:.2f}%")

        # Show best performing stock only if returns are available
if 'return1' in locals() and 'return2' in locals():

    st.markdown("### 🏆 Best Performing Stock")

    if return1 > return2:
        text = f"{stock1} performed better with {return1:.2f}% return"
    elif return2 > return1:
        text = f"{stock2} performed better with {return2:.2f}% return"
    else:
        text = "Both stocks performed equally"

    st.markdown(f"""
    <div style="
    background: linear-gradient(135deg,#00c853,#43a047,#1b5e20);
    padding:20px;
    border-radius:14px;
    text-align:left;
    font-size:20px;
    font-weight:400;
    color:white;
    box-shadow:0 4px 16px rgba(0,0,0,0.35);
    ">
    🏆 {text}
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------
# STOCK CHATBOT
# ----------------------------------

st.subheader("AI Stock Assistant 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Chat input (part of dashboard, not footer)
user_input = st.text_input("Ask about RSI, SMA, trading signals...", key="chatbox")

if user_input:

    prompt = user_input
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    question = prompt.lower()

    # Smart responses
    if "rsi" in question:
        reply = """
RSI (Relative Strength Index) measures momentum.

• Above 70 → Stock may be overbought  
• Below 30 → Stock may be oversold  
• Between 30–70 → Neutral trend
"""

    elif "sma" in question or "moving average" in question:
        reply = """
SMA (Simple Moving Average) smooths price data.

Short SMA crossing above Long SMA → BUY signal  
Short SMA crossing below Long SMA → SELL signal
"""

    elif "buy" in question:
        reply = "A BUY signal happens when the short moving average crosses above the long moving average."

    elif "sell" in question:
        reply = "A SELL signal happens when the short moving average crosses below the long moving average."

    elif "stock" in question:
        reply = "You can analyze stocks by entering their ticker symbol in the sidebar."

    else:
        reply = "I can help explain RSI, SMA, trading signals, and stock analysis."

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.write(reply)