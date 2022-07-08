import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.api import meta_data
from app.api.routes import raw_data, results
load_dotenv()
env = os.getenv('ENV')

# create application
app = FastAPI(
    title=meta_data.title, 
    description=meta_data.description, 
    version=meta_data.version, 
    openapi_tags=meta_data.tags_metadata)

# just the root endpoint
@app.get("/", tags=['👋 Welcome'])
def welcome():
    return {"message": f"Hello from the {meta_data.title}", "api_base_url": meta_data.api_base_url, "api_doc": meta_data.api_docs_url}
       
# use fastapi router an add endpoints       
app.include_router(raw_data.router, prefix=meta_data.api_path) # see api/raw-data.py
app.include_router(results.router, prefix=meta_data.api_path) # see api/resutls.py

print(meta_data.console_output)





