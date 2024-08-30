#!/bin/sh
pip install -r requirements.txt && \
python3 jira_export_features.py && \
unzip -u -o -d features ~/snap/firefox/common/tmp/downloads/FeatureBundle.zip && \
ls -l features

