from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from email_triage_env import EmailTriageEnv, Action
import os

app = FastAPI(title="Email Triage OpenEnv API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global env instance
env = None

@app.get("/")
async def root():
    return {"message": "Email Triage OpenEnv API", "status": "running"}

@app.on_event("startup")
async def startup_event():
    global env
    task = os.getenv("TASK", "easy")  # Default to easy
    env = EmailTriageEnv(task=task)

@app.post("/reset")
async def reset():
    global env
    if env is None:
        raise HTTPException(status_code=500, detail="Environment not initialized")
    obs = env.reset()
    return obs.dict()

@app.post("/step")
async def step(action_data: dict):
    global env
    if env is None:
        raise HTTPException(status_code=500, detail="Environment not initialized")
    try:
        action = Action(**action_data)
        obs, reward, done, info = env.step(action)
        return {
            "observation": obs.dict(),
            "reward": reward.dict(),
            "done": done,
            "info": info
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/state")
async def state():
    global env
    if env is None:
        raise HTTPException(status_code=500, detail="Environment not initialized")
    return env.state()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)