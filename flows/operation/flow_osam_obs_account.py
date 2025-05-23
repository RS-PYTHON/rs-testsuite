from prefect import flow


@flow (log_prints=True, validate_parameters=True)
def osam_obs_account(account_name: str = ""):
    print("start osam obs account")
    
    
if __name__ == "__main__":
    osam_obs_account()