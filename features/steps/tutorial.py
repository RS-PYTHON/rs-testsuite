"""xxx"""

from behave import given
from behave import when
from behave import then


@given('the ninja has a third level black-belt')
def step_impl1(context):
    """xxx"""
    pass


@when('attacked by Chuck Norris')
def step_impl2(context):
    """xxx"""
    assert True is not False


@then('the ninja should run for his life')
def step_impl3(context):
    """xxx"""
    assert context.failed is False
