import requests
import json
import tkinter as tk
from datetime import datetime
from itertools import cycle
import random
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Constants for API keys and credentials file
OPENWEATHERMAP_API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'
NEWS_API_KEY = 'YOUR_NEWS_API_KEY'
TASKS_CREDENTIALS_FILE = 'tasks_credentials.json'
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']

def get_stock_price(symbol):
    stock_url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=demo'
    response = requests.get(stock_url)
    data = response.json()
    return data['Global Quote']['05. price']

def get_weather_info(city):
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}'
    response = requests.get(weather_url)
    data = response.json()
    return data['main']['temp'], data['weather'][0]['main']

def get_holidays(country_code):
    year = datetime.now().year
    holidays_url = f'https://date.nager.at/api/v2/PublicHolidays/{year}/{country_code}'
    response = requests.get(holidays_url)
    data = response.json()
    return [holiday['name'] for holiday in data]

def get_news():
    news_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'
    response = requests.get(news_url)
    data = response.json()
    headlines = [article['title'] for article in data['articles']]
    return cycle(headlines)

def get_random_thought():
    thoughts = [
        "Every day is a new beginning.",
        "Embrace the glorious mess that you are.",
        "You are capable of amazing things.",
        "Be kind to yourself today.",
        "Your attitude determines your direction."
    ]
    return random.choice(thoughts)

def get_compliment():
    compliments = [
        "Looking good!",
        "You're amazing!",
        "You've got this!",
        "You're a star!",
        "You're beautiful inside and out!"
    ]
    return random.choice(compliments)

def authenticate_google_tasks():
    creds = None
    if os.path.exists('tasks_token.json'):
        creds = Credentials.from_authorized_user_file('tasks_token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                TASKS_CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('tasks_token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_google_tasks():
    creds = authenticate_google_tasks()
    service = build('tasks', 'v1', credentials=creds)
    results = service.tasklists().list().execute()
    tasklists = results.get('items', [])

    if not tasklists:
        return []

    tasks_result = service.tasks().list(tasklist=tasklists[0]['id']).execute()
    tasks = tasks_result.get('items', [])

    return [task['title'] for task in tasks]

def create_label(root, text, font=('Helvetica', 12), wraplength=600, justify="left", fg="black"):
    label = tk.Label(root, text=text, font=font, wraplength=wraplength, justify=justify, fg=fg)
    label.pack(pady=10)
    return label

def update_checklist(checklist_label):
    tasks = get_google_tasks()
    checklist_label.config(text='\n'.join(tasks))

def update_display(root, weather_label, reminder_label, news_text, thought_label, compliment_label, checklist_label):
    stock_price = get_stock_price('AAPL')
    weather_temp, weather_condition = get_weather_info('New York')
    holidays = get_holidays('US')

    weather_label.config(text=f'Wealth: ${stock_price}  |  Weather: {weather_temp}°C ({weather_condition})  |  Holidays: {", ".join(holidays)}')

    if 'rain' in weather_condition.lower():
        reminder_label.config(text="Don't forget to take an umbrella!", fg="red")
    else:
        reminder_label.config(text="")

    news_headline = next(news_cycle)
    news_text.set(news_headline)

    thought_label.config(text=get_random_thought())
    compliment_label.config(text=get_compliment())

    update_checklist(checklist_label)

    root.after(300000, lambda: update_display(root, weather_label, reminder_label, news_text, thought_label, compliment_label, checklist_label))

# GUI setup
root = tk.Tk()
root.title('Smart Mirror')

weather_label = create_label(root, "", font=('Helvetica', 18))
reminder_label = create_label(root, "", font=('Helvetica', 14), fg="red")
news_text = tk.StringVar()
news_label = create_label(root, textvariable=news_text, font=('Helvetica', 14), wraplength=600, justify="left")
thought_label = create_label(root, get_random_thought(), font=('Helvetica', 12), wraplength=600, justify="left", fg="blue")
compliment_label = create_label(root, get_compliment(), font=('Helvetica', 12), wraplength=600, justify="left", fg="green")
checklist_label = create_label(root, "", font=('Helvetica', 12), wraplength=600, justify="left", fg="brown")


news_cycle = get_news()

# Initial display update
update_display(root, weather_label, reminder_label, news_text, thought_label, compliment_label, checklist_label)


root.mainloop() 