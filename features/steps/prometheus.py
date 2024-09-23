from behave import given, when, then
from behave import use_step_matcher
import json
import re
from endpoints import step_request_service, is_valid_json

container_tab = [
    ('prefect',                 ('.*prefect-server.*',          '',                           ':(\d+\.\d+\.\d+)-')   ),
    ('rs-server-frontend',      ('.*rs-server-frontend.*',      '',                           ':([0-9a-zA-Z.]+)$')   ),
    ('rs-server-adgs',          ('.*rs-server-adgs.*',          '',                           ':([0-9a-zA-Z.]+)$')   ),
    ('rs-server-cadip',         ('.*rs-server-cadip.*',         '',                           ':([0-9a-zA-Z.]+)$')   ),
    ('rs-server-staging',       ('.*rs-server-staging.*',       '',                           ':([0-9a-zA-Z.]+)$')   ),
    ('rs-server-catalog',       ('.*server-catalog.*',          '.*server-catalog-db.*',      ':([0-9a-zA-Z.]+)$')   ),
    ('pgstac',                  ('.*server-catalog-db.*',       '',                           'v(\d+\.\d+\.\d+)')   )
    ]



# Call Prometheus query
@when('we call the prometheus query {query}')
def step_request_prometheus(context: str, query: str):
    step_request_service(context, 'monitoring', 'prometheus/api/v1/query?query=' + query)


# Check that the Prometheus query send back almost one item
@then('almost one prometheus result is provided')
def step_check_prometheus_result(context: str):
    step_check_json_prometheus_is_not_null(context, 'data', 'result')



# Specific check: Ensure the response is in JSON format and that the path level1.level2 contains at least one element.
@then('the answer is a json with almost one element on the path {level1}.{level2}')
def step_check_json_prometheus_is_not_null(context: str, level1: str, level2: str):
    assert context.response_status_code == 200
    assert is_valid_json(context.response.text) == True

    data = json.loads(context.response.text)
    assert len(data[level1][level2]) > 0


use_step_matcher("re")

# Check the version of a specific container
@given ('the container (?P<container>prefect|rs-server-frontend|rs-server-adgs|rs-server-cadip|rs-server-staging|rs-server-catalog|pgstac) has got version (?P<version>[^"]+)')
@then  ('the container (?P<container>prefect|rs-server-frontend|rs-server-adgs|rs-server-cadip|rs-server-staging|rs-server-catalog|pgstac) has got version (?P<version>[^"]+)')
def step_check_container_version(context: str, container: str, version: str):
    # Retrieve the configuration for the specified container from container_tab
    configuration = next((valeurs for key, valeurs in container_tab if key == container), None)
    
    # Get container information from Prometheus
    query = f'kube_pod_container_info{{  pod=~"{configuration[0]}", pod!~"{configuration[1]}"  }}'
    response = step_request_service(context, 'monitoring', 'prometheus/api/v1/query?query=' + query)

    # Get the image value from the response data
    data = json.loads(response.text)
    image_value = (data['data']['result'][0]['metric']['image'])
    
    # Use regex to find the version in the image value
    match = re.search(fr'{configuration[2]}', image_value)
    version_extracted = match.group(1)
    
    # Assert that the extracted version matches the expected version
    assert (version_extracted == version)


