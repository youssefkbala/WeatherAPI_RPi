import requests
from datetime import datetime
import RPi.GPIO as GPIO

# Defining the LEDs pins:

LED1 = 11
LED2 = 13
LED3 = 15

# Setting up the GPIO pins to be output...

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)

def led(option):
    global LED1, LED2, LED3
    #---------------------------------------------------------
    # In the led() function we will handle the LEDs states
    # depending on the weather id code retreived from the api
    #_________________________________________________________

    # 1st LED
    if int(option[0]) == 1:
        GPIO.output(LED1, True)
    else:
        GPIO.output(LED1, False)

    # 2nd LED
    if int(option[1]) == 1:
        GPIO.output(LED2, True)
    else:
        GPIO.output(LED2, False)

    # 3rd LED
    if int(option[2]) == 1:
        GPIO.output(LED3, True)
    else:
        GPIO.output(LED3, False)

# https://www.instructables.com/Control-LED-Using-Raspberry-Pi-GPIO/

# based on the information given in the api website :

#         https://openweathermap.org/weather-conditions

# each weather status have a specific id
# so we are going to declare a dictionary to store the id values
# with its corresponding code to turn on a different LED
# combination for each weather status :

#       id = 2xx --> Thunderstorm --> LED1 : OFF | LED2 : OFF | LED3 : ON
#       id = 3xx --> Drizzle      --> LED1 : OFF | LED2 : ON  | LED3 : OFF
#       id = 5xx --> Rain         --> LED1 : OFF | LED2 : ON  | LED3 : ON
#       id = 6xx --> Snow         --> LED1 : ON  | LED2 : OFF | LED3 : OFF
#       id = 7xx --> Atmosphere   --> LED1 : ON  | LED2 : OFF | LED3 : ON
#       id = 800 --> Clear        --> LED1 : ON  | LED2 : ON  | LED3 : OFF
#       id = 8xx --> Clouds       --> LED1 : ON  | LED2 : ON  | LED3 : ON


# the binary code for the three LEDs combination will be represented as a string
# of three digits, with ON state represented by 1 and OFF by 0
# and the first digit will handle the LED1, 2nd is LED2 and the 3rd digit is LED3

weather_bin_code = {
    2: "001", 3: "010", 5: "011",
    6: "100", 7: "101", 800: "110",
    8: "111"
}

# The api address from where we will get our weather data
api_adr = 'https://api.openweathermap.org/data/2.5/weather?appid=147f627e68540fe4a575f179ea69558e&q='

# At the end of the api address we should add the city name
# that's why we will ask the user to enter the city name
# then add it to the api address

city = input("Enter the city name : ")

# Now the URL is completed
url = api_adr + city

# Next we will send a request to the api with the given URL
# that will return all the weather data about the given city in json format

json_data = requests.get(url).json()

# In the first element in 'weather' block under the value 'main'
# we can find the weather status name :

weather_status = json_data['weather'][0]['main']

# And in the value 'id' we find the weather status id to be tested in our led() function

weather_id = json_data['weather'][0]['id']

# We will use the datetime,now() method to get the actual time
# and make it in HH / MM / SS form

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

print(weather_status)

# Next we will check the weather id from our dictionnary
# and call the led() function to handle LEDs state based on the given weather id

if weather_id == 800:
    led(weather_bin_code[800])  # Clear weather
else:
    led(weather_bin_code[weather_id // 100])