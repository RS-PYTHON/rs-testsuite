from prefect import flow


@flow(log_prints=True, validate_parameters=True)
def data_life_cycle():
    print("start data life cycle")


if __name__ == "__main__":
    data_life_cycle()