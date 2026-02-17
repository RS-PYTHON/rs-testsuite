import json
import logging
import os

import requests
from behave import then, use_step_matcher
from requests import Response

logger = logging.getLogger(__name__)


def rs_server_http_call(
    context,
    verb: str,
    url: str,
    statuses: list[int] | None = None,
    parameter: str | None = None,
) -> Response:
    assert context.apikey is not None, "API-KEY is not set."
    assert os.getenv("RS_SERVER_URL") is not None, "RS_SERVER_URL is not set."

    if statuses is None:
        statuses = [200]

    # Push API-KEY and argument on the header
    headers = {"x-api-key": f"{context.apikey}", "Content-Type": "application/json"}

    with requests.Session() as session:
        rs_server_url = os.environ["RS_SERVER_URL"]
        full_url = rs_server_url + (
            url[1:] if rs_server_url.endswith("/") and url.startswith("/") else url
        )
        logger.info("%s %s", verb, full_url)
        if parameter:
            logger.info("%s implement parameter %s", verb, parameter)
        response = session.request(verb, full_url, headers=headers, json=parameter)
        assert (
            response.status_code in statuses
        ), f"status for {verb} {url} is {response.status_code} and not in {statuses}: {response.text}"
        return response


@then("rs-server get {url} ends with status {status:d}")
def rs_server_get(context, url: str, status: int = 200) -> Response:
    """
    Perform a GET call to the catalog and send back the response
    """
    return rs_server_http_call(context, "GET", url, [status])


@then("rs-server post {url} ends with status {status:d}")
def rs_server_post(context, url: str, parameter: json, status: int = 200) -> Response:
    """
    Perform a POST call to the catalog and send back the response
    """
    return rs_server_http_call(context, "POST", url, [status], parameter)


use_step_matcher("cfparse")


@then("rs-server post {url} ends with status in {statuses:d+}")
def rs_server_post_ex(
    context,
    url: str,
    parameter: json,
    statuses: list[int] | None = None,
) -> Response:
    """
    Perform a POST call to the catalog and send back the response
    """
    return rs_server_http_call(context, "POST", url, statuses, parameter)


use_step_matcher("parse")


@then("rs-server put {url} ends with status {status:d}")
def rs_server_put(context, url: str, parameter: json, status: int = 200) -> Response:
    """
    Perform a PUT call to the catalog and send back the response
    """
    return rs_server_http_call(context, "PUT", url, [status], parameter)


@then("rs-server patch {url} ends with status {status:d}")
def rs_server_patch(context, url: str, parameter: json, status: int = 200) -> Response:
    """
    Perform a PATCH call to the catalog and send back the response
    """
    return rs_server_http_call(context, "PATCH", url, [status], parameter)


@then("rs-server options {url} ends with status {status:d}")
def rs_server_options(
    context,
    url: str,
    parameter: json,
    status: int = 200,
) -> Response:
    """
    Perform a OPTIONS call to the catalog and send back the response
    """
    return rs_server_http_call(context, "OPTIONS", url, [status], parameter)


@then("rs-server delete {url} ends with status {status:d}")
def rs_server_delete(context, url: str, status: int = 200) -> Response:
    """
    Perform a DELETE call to the catalog and send back the response
    """
    return rs_server_http_call(context, "DELETE", url, [status])
