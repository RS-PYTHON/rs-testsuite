from behave import given, when, then
from behave import use_step_matcher

import os
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urljoin


@given ('the flow {flow} is defined on the github url {url}')
def step_check_github_entry(context: str, flow:str, url:str):
    """
    Check Github entry
    """
    
    