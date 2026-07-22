from fastapi import FastAPI

app = FastAPI(title="Task API", 
              version="1.0"
              )


# Stage 0 - Hello Server
@app.get("/")
async def root():
    data = {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }
    return data

# Stage 1 - Health Check
@app.get("/health")
async def health():
    return {
        "status": "ok"
    }