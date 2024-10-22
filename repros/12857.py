import aiohttp
from prefect import flow, task


@flow
def my_flow():
    for url in ["https://www.google.com", "https://www.microsoft.com"]:
        data = download_file.submit(url)
        do_something_with_data.submit(data)


@task()
async def download_file(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            assert resp.status == 200
            return await resp.read()


@task()
def do_something_with_data(data): ...


if __name__ == "__main__":
    my_flow()
