import os
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime, timedelta
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.models import Order

# Load environment variables
load_dotenv()

API_KEY = os.getenv("APCA_API_KEY_ID")
SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
BASE_URL = os.getenv("APCA_API_BASE_URL")

# Initialize client
trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)

st.set_page_config(page_title="Alpaca Trading Dashboard", layout="wide")
st.title("📈 Alpaca Streamlit Trading Dashboard")

menu = ["📊 Trade Stocks", "📜 Order History"]
choice = st.sidebar.radio("Select Page", menu)

if choice == "📊 Trade Stocks":
    st.subheader("🛒 Place an Order")
    with st.form("order_form"):
        symbol = st.text_input("Symbol (e.g. AAPL)", value="MSFT").upper()
        qty = st.number_input("Quantity", min_value=1, value=1)
        side = st.selectbox("Order Side", options=["buy", "sell"])
        order_type = st.selectbox("Order Type", options=["market"])
        time_in_force = st.selectbox("Time in Force", options=["gtc", "day"])

        submitted = st.form_submit_button("Submit Order")
        if submitted:
            try:
                order_data = MarketOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=OrderSide(side),
                    time_in_force=TimeInForce(time_in_force)
                )
                order = trading_client.submit_order(order_data)
                st.success(f"✅ Order submitted: ID {order.id}")
            except Exception as e:
                st.error(f"❌ Error submitting order: {e}")

elif choice == "📜 Order History":
    st.subheader("📜 Order History")
    try:
        orders = trading_client.get_orders()
        if not orders:
            st.info("No orders found.")
        else:
            for order in orders:
                st.json({
                    "symbol": order.symbol,
                    "qty": order.qty,
                    "side": str(order.side),
                    "type": str(order.order_type),
                    "status": str(order.status),
                    "submitted_at": str(order.submitted_at),
                    "filled_qty": order.filled_qty
                })
    except Exception as e:
        st.error(f"Error retrieving orders: {e}")
