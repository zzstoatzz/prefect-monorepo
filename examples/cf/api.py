import asyncio
from typing import Annotated

import controlflow as cf
from fastapi import FastAPI
from prefect import flow
from pydantic import Field

app = FastAPI()


@flow(log_prints=True)
async def handle_message(message: str):
    result = await cf.run_async(
        message, result_type=Annotated[str, Field(description="sPoNgEbOb MoCkInG tExT")]
    )
    print(result)


@app.post("/chat")
async def chat(message: str):
    asyncio.create_task(handle_message(message))
    return {"message": "Message received"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
