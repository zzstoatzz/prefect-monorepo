import time
import httpx

if __name__ == "__main__":
    with httpx.Client() as client:
        while True:
            response = client.post(
                "http://localhost:8001/background-task",
                json={"data": "some data"}
            )
            print(response.json())
            time.sleep(5)