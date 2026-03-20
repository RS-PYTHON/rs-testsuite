from behave import then
from rs_server import rs_server_get
from rs_server import rs_server_post
import logging

logger = logging.getLogger(__name__)


@then("staging get url succeeds")
def step_check_staging(context):
    """
    Check the staging url
    """
    rs_server_get(context, "processes/staging", 200)

@then("staging post url exists")
def step_check_staging_post(context):
    """
    Check the staging url
    """
    process_json = {}
    #logger.info("JSON use for POST Staging request : %s", process_json)
    rs_server_post(context, "processes/staging/execution", process_json, 422)
