import os
import shutil
import zipfile
import requests
from typing import List
from paths import DATA_DIR
from langchain_core.tools import tool


@tool
def download_and_extract_repo(repo_url: str) -> str:
    """Download a Git repository and extract it to a local directory.

    This tool downloads a Git repository as a ZIP file from GitHub or similar
    platforms and extracts it to a './data/repo' directory. It handles both 'main'
    and 'master' branch repositories automatically. If the repo directory
    already exists, it will be removed and replaced with the new download.

    Args:
        repo_url: The complete URL of the Git repository (e.g., https://github.com/user/repo)

    Returns:
        The path to the extracted repository directory if successful, or False if failed
    """
    output_dir = os.path.join(DATA_DIR, "repo")
    try:
        if os.path.exists(output_dir):
            print(f"Repository already exists in {output_dir}, removing it")
            shutil.rmtree(output_dir)

        # Create target directory
        os.makedirs(output_dir, exist_ok=True)

        # Convert repo URL to zip download URL
        if repo_url.endswith(".git"):
            repo_url = repo_url[:-4]
        if repo_url.endswith("/"):
            repo_url = repo_url[:-1]

        download_url = f"{repo_url}/archive/refs/heads/main.zip"

        print(f"Downloading repository from {download_url}")

        retires = 3
        i = 0
        while i < retires:
            response = requests.get(download_url, stream=True)
            if response.status_code == 404:
                download_url = f"{repo_url}/archive/refs/heads/master.zip"
                response = requests.get(download_url, stream=True)

            if response.status_code != 200:
                print(f"Failed to download repository: {response.status_code}")
                i += 1
                continue

            response.raise_for_status()
            break

        temp_dir = os.path.join(output_dir, "_temp_extract")
        os.makedirs(temp_dir, exist_ok=True)

        temp_zip = os.path.join(temp_dir, "repo.zip")
        with open(temp_zip, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        with zipfile.ZipFile(temp_zip, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        # Find the nested directory (it's usually named 'repo-name-main')
        nested_dirs = [
            d for d in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, d))
        ]
        if nested_dirs:
            nested_dir = os.path.join(temp_dir, nested_dirs[0])

            for item in os.listdir(nested_dir):
                source = os.path.join(nested_dir, item)
                destination = os.path.join(output_dir, item)
                if os.path.isdir(source):
                    shutil.copytree(source, destination)
                else:
                    shutil.copy2(source, destination)

        shutil.rmtree(temp_dir)

        return output_dir

    except requests.exceptions.RequestException as e:
        print(f"Failed to download repository: {str(e)}")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        return False

    except zipfile.BadZipFile as e:
        print(f"Invalid zip file: {str(e)}")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        return False

    except OSError as e:
        print(f"OS error occurred: {str(e)}")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        return False

    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        return False


@tool
def env_content(dir_path: str) -> str:
    """Read and return the content of a .env file from a specified directory.

    This tool searches through the given directory path and its subdirectories
    to find a .env file and returns its complete content. Useful for examining
    environment variables and configuration settings.

    Args:
        dir_path: The directory path to search for .env file (must be a local path, not URL)

    Returns:
        The complete content of the .env file as a string, or None if not found
    """
    for dir, _, files in os.walk(dir_path):
        for file in files:
            if file == ".env":
                with open(os.path.join(dir, file), "r") as f:
                    return f.read()
    return None

@tool
def weather_forecast(user_destination: str, user_departure: str) -> str:
    """Fetch and return the current weather forecast for departure and destination cities.

    This tool uses the OpenWeatherMap API to retrieve the current weather
    conditions for both the departure and destination cities. It formats the weather 
    data into a readable string that includes temperature, humidity, weather 
    description, wind speed, and more.

    Args:
        user_departure: The name of the departure city
        user_destination: The name of the destination city for which to fetch the weather forecast

    Returns:
        A formatted string containing weather information for both cities
    """
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    
    if not api_key:
        return "Error: OPENWEATHER_API_KEY not found in environment variables"
    
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    weather_data = {}
    
    # Fetch weather for departure city
    try:
        params = {
            "q": user_departure,
            "appid": api_key,
            "units": "metric"
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        departure_weather = response.json()
        weather_data["departure"] = {
            "city": user_departure,
            "temperature": departure_weather["main"]["temp"],
            "feels_like": departure_weather["main"]["feels_like"],
            "humidity": departure_weather["main"]["humidity"],
            "pressure": departure_weather["main"]["pressure"],
            "weather": departure_weather["weather"][0]["description"],
            "wind_speed": departure_weather["wind"]["speed"],
            "clouds": departure_weather["clouds"]["all"]
        }
    except requests.exceptions.RequestException as e:
        weather_data["departure"] = f"Error fetching weather for {user_departure}: {str(e)}"
    
    # Fetch weather for destination city
    try:
        params = {
            "q": user_destination,
            "appid": api_key,
            "units": "metric"
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        destination_weather = response.json()
        weather_data["destination"] = {
            "city": user_destination,
            "temperature": destination_weather["main"]["temp"],
            "feels_like": destination_weather["main"]["feels_like"],
            "humidity": destination_weather["main"]["humidity"],
            "pressure": destination_weather["main"]["pressure"],
            "weather": destination_weather["weather"][0]["description"],
            "wind_speed": destination_weather["wind"]["speed"],
            "clouds": destination_weather["clouds"]["all"]
        }
    except requests.exceptions.RequestException as e:
        weather_data["destination"] = f"Error fetching weather for {user_destination}: {str(e)}"
    
    # Format the response
    formatted_response = "Weather Information:\n"
    formatted_response += "=" * 50 + "\n"
    
    # Departure weather
    if isinstance(weather_data.get("departure"), dict):
        dep = weather_data["departure"]
        formatted_response += f"\n📍 Departure: {dep['city']}\n"
        formatted_response += f"   Temperature: {dep['temperature']}°C (feels like {dep['feels_like']}°C)\n"
        formatted_response += f"   Condition: {dep['weather'].capitalize()}\n"
        formatted_response += f"   Humidity: {dep['humidity']}%\n"
        formatted_response += f"   Wind Speed: {dep['wind_speed']} m/s\n"
        formatted_response += f"   Cloud Coverage: {dep['clouds']}%\n"
    else:
        formatted_response += f"\n📍 Departure: {weather_data['departure']}\n"
    
    # Destination weather
    if isinstance(weather_data.get("destination"), dict):
        dest = weather_data["destination"]
        formatted_response += f"\n📍 Destination: {dest['city']}\n"
        formatted_response += f"   Temperature: {dest['temperature']}°C (feels like {dest['feels_like']}°C)\n"
        formatted_response += f"   Condition: {dest['weather'].capitalize()}\n"
        formatted_response += f"   Humidity: {dest['humidity']}%\n"
        formatted_response += f"   Wind Speed: {dest['wind_speed']} m/s\n"
        formatted_response += f"   Cloud Coverage: {dest['clouds']}%\n"
    else:
        formatted_response += f"\n📍 Destination: {weather_data['destination']}\n"
    
    formatted_response += "\n" + "=" * 50
    
    return formatted_response

def get_all_tools() -> List:
    """Return a list of all available tools."""
    return [
        weather_forecast,
    ]