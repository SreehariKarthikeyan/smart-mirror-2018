import requests
import json
import datetime
import tkinter as tk
import random

def get_stock_price(symbol):
# https://site.financialmodelingprep.com/developer/docs 
    stock_url = f'https://financialmodelingprep.com/api/v3/stock/real-time-price/{symbol}'
    response = requests.get(stock_url)
    data = response.json()
    return data['price']

def get_weather_info(city):
    # https://publicapi.dev/meta-weather-api
    weather_url = f'https://www.metaweather.com/api/location/search/?query={city}'
    response = requests.get(weather_url)
    data = response.json()
    if data:
        woeid = data[0]['woeid']
        weather_url = f'https://www.metaweather.com/api/location/{woeid}/'
        response = requests.get(weather_url)
        data = response.json()
        return data['consolidated_weather'][0]['the_temp'], data['consolidated_weather'][0]['weather_state_name']
    else:
        return 'N/A', 'N/A'

def get_holidays(year):
    # Using date.nager.at public holidays API
    holidays_url = f'https://date.nager.at/api/v2/publicholidays/{year}/us'
    response = requests.get(holidays_url)
    holidays = response.json()
    return holidays

def get_random_message():
    messages = ["You look good!", "You look amazing!", "You look sexy!", "Have a fantastic day!"]
    return random.choice(messages)

def get_news(api_key):
    # Using News API (replace 'YOUR_NEWS_API_KEY' with your actual key)  https://newsapi.org/
    news_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    response = requests.get(news_url)
    news_data = response.json()
    headlines = [article['title'] for article in news_data.get('articles', [])]
    return headlines


def update_display():

    now = datetime.datetime.now()
    year = now.year
    stock_price = get_stock_price('AAPL')  
    stock_price = get_stock_price('MSFT')  
    stock_price = get_stock_price('GOOGL')  
    stock_price = get_stock_price('NVDA')  
    weather_temp, weather_condition = get_weather_info('Chennai')  
    holidays = get_holidays(year)
    
    holiday_names = [holiday['localName'] for holiday in holidays if holiday['date'] == now.strftime('%Y-%m-%d')]
    holiday_text = f'Holidays: {", ".join(holiday_names)}' if holiday_names else 'No holidays today'
    
    random_message = get_random_message()
    display_text.set(f'Stock: ${stock_price}  |  Weather: {weather_temp}°C, {weather_condition}  |  {holiday_text}  |  {random_message}')
    
    # Remind to take an umbrella if it might rain
    if "rain" in weather_condition.lower():
        remind_umbrella()
    #    Display news 
    news_api_key = 'YOUR_NEWS_API_KEY'  # Replace with your News API key
    news_headlines = get_news(news_api_key)
    
    if news_headlines:
        news_text.set('\n'.join(news_headlines))
    else:
        news_text.set('No news updates available')

def remind_umbrella():
    reminder_window = tk.Toplevel(root)
    reminder_window.title('Reminder')
    reminder_label = tk.Label(reminder_window, text='Don\'t forget to take an umbrella!', font=('Helvetica', 14), padx=10, pady=10)
    reminder_label.pack()

root = tk.Tk()
root.title('Smart Mirror')

display_text = tk.StringVar()
label = tk.Label(root, textvariable=display_text, font=('Helvetica', 18))
label.pack(pady=20)

news_text = tk.StringVar()
news_label = tk.Label(root, textvariable=news_text, font=('Helvetica', 14), wraplength=500, justify='left', anchor='w')
news_label.pack(pady=20)
update_display()


root.after(300000, update_display)

root.mainloop()
