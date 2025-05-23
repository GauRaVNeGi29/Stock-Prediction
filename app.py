import streamlit as st 
import pandas as pd
import yfinance as yf
from ta.volatility import BollingerBands
from ta.trend import MACD, EMAIndicator, SMAIndicator
from ta.momentum import RSIIndicator
import datetime
from datetime import date
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import r2_score, mean_absolute_error

image = './public/image.jpg'

# st.title('Stock Price Predictions')
st.sidebar.info('Welcome to the Stock Price Prediction App. Choose your options below')
# st.sidebar.info("Created and designed by [Gaurav Negi](https://www.linkedin.com/in/)")


def main():
    option = st.sidebar.selectbox('Make a choice', ['Select','Recent Data', 'Predict'],index=0)
    if option == 'Recent Data':
        dataframe(data)
    # elif option == 'Visualize':
    #     tech_indicators(data)
    elif option == 'Predict':
        predict()
    else:
        front()



@st.cache_resource
def download_data(op, start_date, end_date):
    df = yf.download(op, start=start_date, end=end_date, progress=False)
    return df



option = st.sidebar.text_input('Enter a Stock Symbol', value='AAPL')
option = option.upper()
today = datetime.date.today()
duration = st.sidebar.number_input('Enter the duration', value=365)
before = today - datetime.timedelta(days=duration)
start_date = st.sidebar.date_input('Start Date', value=before)
end_date = st.sidebar.date_input('End date', today)
# if st.sidebar.button('Send'):
#     if start_date < end_date:
#         st.sidebar.success('Start date: `%s`\n\nEnd date: `%s`' %(start_date, end_date))
#         download_data(option, start_date, end_date)
#     else:
#         st.sidebar.error('Error: End date must fall after start date')



data = download_data(option, start_date, end_date)
scaler = StandardScaler()

def tech_indicators(data):
    st.header('Technical Indicators')
    option = st.radio('Choose a Technical Indicator to Visualize', ['Close', 'BB', 'MACD', 'RSI', 'SMA', 'EMA'])

    bb_indicator = BollingerBands(data['Close'])
    bb = data
    bb['bb_h'] = bb_indicator.bollinger_hband()
    bb['bb_l'] = bb_indicator.bollinger_lband()
    bb = bb[['Close', 'bb_h', 'bb_l']]
    
    macd = MACD(data['Close']).macd()
    
    rsi = RSIIndicator(data['Close']).rsi()
    # SMA
    sma = SMAIndicator(data['Close'], window=14).sma_indicator()
    # EMA
    ema = EMAIndicator(data['Close']).ema_indicator()

    if option == 'Close':
        st.write('Close Price')
        st.line_chart(data['Close'])
    elif option == 'BB':
        st.write('BollingerBands')
        st.line_chart(bb)
    elif option == 'MACD':
        st.write('Moving Average Convergence Divergence')
        st.line_chart(macd)
    elif option == 'RSI':
        st.write('Relative Strength Indicator')
        st.line_chart(rsi)
    elif option == 'SMA':
        st.write('Simple Moving Average')
        st.line_chart(sma)
    else:
        st.write('Expoenetial Moving Average')
        st.line_chart(ema)


def dataframe(data):
    st.header('Recent Data')
    
    num = st.number_input('\nHow many days of data?', value=5)
    num = int(num)
    st.dataframe(data.tail(num))



def predict():
    model = st.radio('Choose a model', ['LinearRegression', 'RandomForestRegressor', 'ExtraTreesRegressor', 'KNeighborsRegressor', 'XGBoostRegressor'])
    num = st.number_input('How many days forecast?', value=5)
    num = int(num)
    if st.button('Predict'):
        if model == 'LinearRegression':
            engine = LinearRegression()
            model_engine(engine, num)
        elif model == 'RandomForestRegressor':
            engine = RandomForestRegressor()
            model_engine(engine, num)
        elif model == 'ExtraTreesRegressor':
            engine = ExtraTreesRegressor()
            model_engine(engine, num)
        elif model == 'KNeighborsRegressor':
            engine = KNeighborsRegressor()
            model_engine(engine, num)
        else:
            engine = XGBRegressor()
            model_engine(engine, num)


def model_engine(model, num):
    df = data['Close']
    df['preds'] = data['Close'].shift(-num)
    x = df.drop(['preds'], axis=1).values
    x = scaler.fit_transform(x)
    x_forecast = x[-num:]
    x = x[:-num]
    y = df.preds.values
    y = y[:-num]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.2, random_state=7)
    model.fit(x_train, y_train)
    preds = model.predict(x_test)
    st.text(f'r2_score: {r2_score(y_test, preds)} \
            \n\nMAE: {mean_absolute_error(y_test, preds)}')
    forecast_pred = model.predict(x_forecast)
    day = 1
    for i in forecast_pred:
        st.text(f'Day {day}: {i}')
        day += 1

def front():
    st.title('Stock Price Prediction')
    st.subheader('Predict Stock Prices Based on Historical Data')
    st.image(image, caption='Stock Market', use_container_width=True)
    st.info("""

    This app predicts the stock price based on historical data. 

    You can select options from the sidebar to get predictions.
    
    The app uses advanced algorithms to analyze historical stock data and provide predictions for future prices.

    """)
    if st.button('Get Started'):
        st.write('Please select the stock symbol and prediction period from the sidebar.')

    st.markdown("""
    ---

    **Contact Us:**

    - Email: abc@gmail.com

    - Phone: +91 98765433210


    **Follow Us:**

    - [Twitter](https://twitter.com/)

    - [LinkedIn](https://linkedin.com/in/)

    - [GitHub](https://github.com/)


    **Disclaimer:** This app is for educational purposes only. 

    Please do your own research before making any investment decisions.

    """)

if __name__ == '__main__':
    main()
