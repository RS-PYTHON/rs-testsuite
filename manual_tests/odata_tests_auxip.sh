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


# Tests performed to check OData compliance, see https://pforge-exchange2.astrium.eads.net/confluence/pages/viewpage.action?pageId=505564386

# Following secrets must be defined in the environment:

#  export ADGS_URL="xxx"
#  export ADGS_TOKEN_URL="xxx"
#  export ADGS_SCOPE="xxx"
#  export ADGS_CLIENT_ID="xxx"
#  export ADGS_CLIENT_SECRET="xxx"
#  export ADGS_USERNAME="xxx"
#  export ADGS_PASSWORD="xxx"

############################
# TESTS AUXIP
############################

AUTHBEAR="Authorization: Bearer"
AFIELD=".value[0].Name"

set -o pipefail
declare -A URL
declare -A TOKEN

URL['ADGS']=${ADGS_URL}

# Refresh tokens
TOKEN['ADGS']=$(curl -s -f -k -u "${ADGS_CLIENT_ID}:${ADGS_CLIENT_SECRET}" --data-urlencode grant_type=password --data-urlencode username="${ADGS_USERNAME}" --data-urlencode password="${ADGS_PASSWORD}" --data-urlencode scope="${ADGS_SCOPE}" "${ADGS_TOKEN_URL}" | jq -r .access_token)

# Basic check
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# eq
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ContentType%20eq%20'application/octet-stream'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# ne
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ContentType%20ne%20'application/zip'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=PublicationDate%20ne%202026-03-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=Name%20ne%20'foo'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# gt
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=PublicationDate%20gt%202026-02-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# ge
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=PublicationDate%20ge%202026-02-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# lt
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=PublicationDate%20lt%202026-02-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# le
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=PublicationDate%20le%202026-02-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# in
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ContentType%20in%20('application/octet-stream','foo')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# and
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ContentType%20eq%20'application/octet-stream'%20and%20PublicationDate%20lt%202026-01-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# or
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ContentType%20eq%20'application/octet-stream'%20or%20ContentType%20eq%20'foo'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# not
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=not%20endswith(Name,'p')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=not(ContentType%20eq%20'application/zip')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=not%20(ContentType%20eq%20'application/zip')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# ()
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ContentType%20eq%20'application/octet-stream'%20and%20(contains(Name,'2000')%20or%20contains(Name,'3000'))&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# concat
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=concat(ContentType,'Z')%20eq%20'application/octet-streamZ'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# contains
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=contains(Name,'2000')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# endswith
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=endswith(Name,'p')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# indexof
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=indexof(ContentType,'p')%20eq%201&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# length
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=length(ContentType)%20eq%2024&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# startswith
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=startswith(Name,'S1A')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# substring
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=substring(ContentType,23)%20eq%20'm'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# matchesPattern
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=matchesPattern(ContentType,'%5Eapplication/.*m\$')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# tolower
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=tolower(ContentType)%20eq%20'application/octet-stream'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# toupper
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=toupper(ContentType)%20eq%20'APPLICATION/OCTET-STREAM'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
# trim
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=trim(ContentType)%20eq%20'application/octet-stream'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done # NOSONAR
