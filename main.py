from fastapi import FastAPI

app = FastAPI(   
    title="AI Incidentt powered management system",
    description="web based application used for internal AI powered system",
    version="1.0.0")

@app.get("/health")
async def healthCheck():
    return{
        "status" : "200",
        "version" : "1.0.0",
        "condition" : "working"
    }