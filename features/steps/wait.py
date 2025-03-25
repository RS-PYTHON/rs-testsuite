import time

from behave import when


@when("I wait for {seconds:d} seconds")
def step_sleep(context, seconds: int):
    assert context is not None
    time.sleep(seconds)
