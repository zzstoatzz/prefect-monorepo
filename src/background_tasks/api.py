from fastapi import FastAPI, Body
from tasks import do_work

app = FastAPI()

@app.post("/background-task")
async def submit_work(data: str = Body(..., embed=True)):
    task_run = do_work.submit(data)
    print(f"Submitted task {task_run.id} with task key {task_run.task_key}")
    return {"message": "Work submitted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)