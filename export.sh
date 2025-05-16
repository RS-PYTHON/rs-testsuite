#!/bin/sh
BUNDLE="$HOME/snap/firefox/common/tmp/downloads/FeatureBundle.zip"

pip install -r requirements.txt && \
rm -f $BUNDLE && \
python3 jira_export_features.py && \
rm -f features/*.feature && \
unzip -u -o -d features $BUNDLE && \
rm -f $BUNDLE && \
ls -l features
