#!/bin/sh
# Copyright 2023-2026 Airbus
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

BUNDLE="$HOME/snap/firefox/common/tmp/downloads/FeatureBundle.zip"

pip install -r requirements.txt && \
rm -f $BUNDLE && \
python3 jira_export_features.py && \
rm -f features/*.feature && \
unzip -u -o -d features $BUNDLE && \
rm -f $BUNDLE && \
ls -l features
