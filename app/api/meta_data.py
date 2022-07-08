import os
from dotenv import load_dotenv
load_dotenv()
env = os.getenv('ENV')

base_url = 'http://0.0.0.0:8000'
if env == 'dev':
    base_url = 'http://0.0.0.0:8042'  
api_path = '/api/v1'
api_base_url = base_url + api_path
api_docs_url = base_url + '/docs'

version = "1.0.0"

title = "Aasee Data API"

description = """
## About
This application is part of the [Data Science Management](https://www.hnu.de/studium/studiengaenge/bachelorstudiengaenge/data-science-management-bsc) study programm and the final project of the Data Science Ecosystem course.

We created a [dockerized](https://www.docker.com/) Web-API for the [Aasee](https://www.stadt-muenster.de/tourismus/sehenswertes/aasee.html) using [FastApi](https://fastapi.tiangolo.com/) and a [MySQL](https://www.mysql.com/de/) database.

One feature is the prediction of the water temperature for a future day by a given outdoor temperature on that day.

#### Authors
- Andreas Geyer (Docker, make)
- Michael Geyer (MySQL, FastAPI)
- Tim Werner (Data Analytics)

 🙈 *Only half of programming is coding. The other 90% is debugging. - Unknown* <br>
 🤓 *Measuring programming progress by lines of code is like measuring aircraft building progress by weight. - Bill Gates*
"""


tags_metadata = [
{
    "name": "👋 Welcome",
    "description": "Just the welcome endpoint"
},     
{
    "name": "💿 Raw Data",
    "description": "All endpoint for the raw data"
}, 
{
    "name": "📊 Analytics Results",
    "description": "All endpoint for the analytics results"
}]

output_command = 'make app-prod-init'
if env == 'dev':
    output_command = 'make app-dev-init'

console_output = f"""
👋  {title}

💻  Mode: {env}
🎉  Version: {version}
📄  Docs URL: {api_docs_url}

❗️  Please use following command in a new terminal to setup the database.\n
    {output_command} 
"""