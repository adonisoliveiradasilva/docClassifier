import uvicorn

if __name__ == "__main__":
    uvicorn.run("api.src.main.main:app", host="localhost", port=8000, reload=True, log_level="info")
