from prefect import flow


@flow(log_prints=True)
def foo(
    x: int,
    y: int = 42,
    z: str | None = None,
) -> int:
    print(x, y, z)

if __name__ == "__main__":
    foo.serve("foo")