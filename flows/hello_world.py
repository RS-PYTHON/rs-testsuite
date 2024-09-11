from prefect import flow


@flow
def my_flow() -> str:
    return "Hello, world!"
