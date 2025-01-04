import pyttsx3        #pip install pyttsx3
import datetime
import wikipedia      #pip install wikipedia
import speech_recognition as sr  #pip install speechRecognition
import webbrowser
import os
import smtplib
import requests       #pip install requests
import calendar



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id) 
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
        
    else:
        speak("Good Evening!") 
        
    speak("I am Jarvis, Please tell me how can i help you")
    
def takeCommand():
    # it takes microphone input from the user and returns the string output
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)
        
    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        
    except Exception as e:
        #print(e)
        
        print("Say that again please....")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 465)
    server.ehlo()
    server.starttls()
    server.login('your e-mail id', 'password')
    server.sendmail('your e-mail-id', to, content)
    server.close()
    

def getWeather(city):
    api_key = "1df67b1752b9338457e1a8bed3eb0476"  # Replace with your actual OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        main = data["main"]
        weather = data["weather"][0]

        temperature = main["temp"]
        humidity = main["humidity"]
        description = weather["description"]

        weather_report = f"The current temperature in {city} is {temperature} degrees Celsius with {description}. The humidity is {humidity}%."
        print(weather_report)
        speak(weather_report)

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        speak("Sorry, I couldn't connect to the weather service.")
    except (KeyError, ValueError) as e:
        print(f"Error processing weather data: {e}")
        speak("Sorry, I couldn't find weather information for that city.")



def show_calendar():
    year = 2025
    
    # Create and format calendar
    cal = calendar.TextCalendar(calendar.SUNDAY)
    calendar_text = ""
    
    for month in range(1, 13):
        calendar_text += cal.formatmonth(year, month) + "\n"
    
    print(calendar_text)
    speak(f"Showing calendar for {year}")

    
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
       
        #Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia....')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
            
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            
        elif 'open brave' in query:
            brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
            try:
                os.startfile(brave_path)
                #speak("Opening Brave browser")
            except FileNotFoundError:
                speak("Brave browser path not found. Please check the installation")
            
        elif 'open google' in query:
            webbrowser.open("google.com")
            
        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
            
        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs' #Replace with your music directory
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0])) #starts from the first music in the directory
            
            
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"The time is {strTime}")
            
        elif 'open code' in query:
            codePath = "C:\\Users\\smrit\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
            
        elif 'email to (your e-mail id)' in query:
            try:
                speak("What should i say?")
                content = takeCommand()
                to = "your e-mail id"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry , Iam not able to send this e-mail")
                
        elif 'weather' in query:
            speak("Which city's weather would you like to know?")
            city = takeCommand().lower()
            getWeather(city)
            
        elif 'calendar' in query or 'show calendar' in query:
            show_calendar()
            
        elif 'exit' in query or 'quit' in query or 'goodbye' in query:
            speak("Byebye! Have a great day!")
            exit()
            
        