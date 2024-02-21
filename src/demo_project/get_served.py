from prefect import flow


@flow(log_prints=True)
def foo(x: str | None = "oof") -> int:
    print(f"foo got {x=}")

if __name__ == "__main__":
    foo.serve("foo")