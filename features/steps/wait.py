from behave import when
import time


@when('i wait for {seconds:d} seconds')
def step_impl(context, seconds: int):
    time.sleep(seconds)
