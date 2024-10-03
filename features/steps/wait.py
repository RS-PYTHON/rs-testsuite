from behave import when
import time


@when('i wait for {seconds:d} seconds')
def step_sleep(context, seconds: int):
    time.sleep(seconds)
