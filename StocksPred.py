import streamlit as st
import pandas as pd
from tradingview_ta import TA_Handler, Interval
import plotly.graph_objs as go

def get_technical_analysis(symbol):
    handler = TA_Handler(
        symbol=symbol,
        exchange="NSE",
        screener="india",
        interval=Interval.INTERVAL_1_DAY,
        timeout=10
    )
    return handler.get_analysis()

def main():
    st.title('TradeView Analytics')

    symbol = st.text_input('Enter Stock Symbol')

    if not symbol:
        st.warning("Please enter a stock symbol.")
        return

    try:
        analysis = get_technical_analysis(symbol)
        st.subheader('Technical Analysis')
        st.write(f"*Symbol:* {symbol}")

        # Summary chart
        st.subheader('Summary Chart')
        summary_data = {
            'Timestamp': list(analysis.summary.keys()),
            'Value': list(analysis.summary.values())
        }
        summary_df = pd.DataFrame(summary_data)
        fig = go.Figure(data=go.Scatter(x=summary_df['Timestamp'], y=summary_df['Value'], mode='lines', name='Summary'))
        st.plotly_chart(fig)

        # Moving averages table and chart
        st.subheader('Moving Averages')
        ma_data = {
            'Moving Average': list(analysis.moving_averages.keys()),
            'Value': list(analysis.moving_averages.values())
        }
        ma_df = pd.DataFrame(ma_data)
        st.write(ma_df)

        st.subheader('Moving Averages Chart')
        ma_chart = go.Figure()
        for ma, value in analysis.moving_averages.items():
            ma_chart.add_trace(go.Scatter(x=summary_df['Timestamp'], y=[value]*len(summary_df), mode='lines', name=ma))
        st.plotly_chart(ma_chart)

        # Indicators table and chart
        st.subheader('Indicators')
        indicators_data = {
            'Indicator': list(analysis.indicators.keys()),
            'Value': list(analysis.indicators.values())
        }
        indicators_df = pd.DataFrame(indicators_data)
        st.write(indicators_df)

        st.subheader('Indicators Chart')
        indicators_chart = go.Figure()
        for indicator, value in analysis.indicators.items():
            indicators_chart.add_trace(go.Scatter(x=summary_df['Timestamp'], y=[value]*len(summary_df), mode='lines', name=indicator))
        st.plotly_chart(indicators_chart)

    except Exception as e:
        st.error(f"Error fetching technical analysis data: {str(e)}")

if _name_ == '_main_':
    main()
