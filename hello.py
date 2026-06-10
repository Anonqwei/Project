
from flask import Flask, abort, redirect, render_template, request, url_for
from io import StringIO #
import json
import requests
app = Flask(__name__, template_folder='Template') #this will create a Flask application instance and specify the folder where the HTML templates are located. In this case, it is set to 'Template', which means the application will look for HTML files in the 'Template' directory when rendering templates.

@app.route('/', methods=['GET', 'POST']) #this will define the route for the home page of the web application. It will accept both GET and POST requests, which means it can handle both displaying the form for input and processing the submitted data when the user submits the form with latitude and longitude values.

def home():

    periods = None #these parameters set to none to prevent errors when the page is first loaded and prevent crash if API does not work or return unexpected data. By initializing these variables to None, the application can check if they have valid data before trying to access their properties, which helps to avoid errors and ensure that the application runs smoothly even when there are issues with the API response.
    current = None
    city = None
    state = None

    if request.method == 'POST':#this will check if the request method is POST, which means the user has submitted the form with the latitude and longitude values. If it is a POST request, it will execute the code inside this block to fetch the weather data based on the provided latitude and longitude.

        lat = request.form['lat']
        lon = request.form['lon']

        url = f'https://api.weather.gov/points/{lat},{lon}'

        response = requests.get(
            url,
            headers={"User-Agent": "MyWeatherApp"}
        )

        js = response.json()
        try: #in case property is not found in the JSON response, it will raise a KeyError and the except block will handle that error by setting periods to None, which will prevent the application from crashing and allow it to continue running even if the expected data is not available in the API response.
           forecast_url = js['properties']['forecast']
           city = js['properties']['relativeLocation']['properties']['city']
           state = js['properties']['relativeLocation']['properties']['state']
           forecast = requests.get(
           forecast_url,
                headers={"User-Agent": "MyWeatherApp"}
           ).json()
     
           periods = forecast['properties']['periods']
           current = periods[0]
        except KeyError:
            periods = None
    

    return render_template(
        'UI.html',
        state=state,
        city=city,
        periods=periods,
        current=current
    )


@app.errorhandler(KeyError) #this will make sure when there is a KeyError, it will call the handle_key_error function to handle the error and redirect the user to the home page instead of showing the default error page.
def handle_key_error(error):
    return redirect(url_for('home'))
@app.errorhandler(404) #this will make sure when there is 404 error, it will call the not_found_error function to handle the error and redirect the user to the home page instead of showing the default 404 error page.
def not_found_error(error): 
    return redirect(url_for('home'))


@app.errorhandler(requests.exceptions.RequestException) #this will make sure when there is a RequestException error, it will call the handle_request_error function to handle the error and return a JSON response with an error message and a 503 status code, indicating that the weather service is unavailable.
def handle_request_error(error):
    return {
        "error": "Weather service unavailable"
    }, 503  
if __name__ == "__main__": #this will check if the script is being run directly (as the main program) and if so, it will start the Flask development server with debug mode enabled. This allows you to run the web application locally and see any error messages or changes in real-time as you develop the application.
    app.run(debug=True)
