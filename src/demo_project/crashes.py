from prefect import flow


@flow
def boom_crash():
    raise SystemExit("Boom!")


if __name__ == "__main__":
    boom_crash()
