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

#  export S1A_URL='xxx'
#  export S1A_TOKEN_URL='xxx'
#  export S1A_GRANT_TYPE='xxx'
#  export S1A_AUTHORIZATION='xxx'
#  export S1A_CLIENT_ID='xxx'
#  export S1A_CLIENT_SECRET='xxx'
#  export S1A_USERNAME='xxx'
#  export S1A_PASSWORD='xxx'

#  export S1C_URL='xxx'
#  export S1C_TOKEN_URL='xxx'
#  export S1C_AUTHORIZATION='xxx'
#  export S1C_GRANT_TYPE='xxx'
#  export S1C_SCOPE='xxx'
#  export S1C_CLIENT_ID='xxx'
#  export S1C_CLIENT_SECRET='xxx'
#  export S1C_USERNAME='xxx'
#  export S1C_PASSWORD='xxx'

#  export S1D_URL='xxx'
#  export S1D_TOKEN_URL='xxx'
#  export S1D_AUTHORIZATION='xxx'
#  export S1D_GRANT_TYPE='xxx'
#  export S1D_SCOPE='xxx'
#  export S1D_CLIENT_ID='xxx'
#  export S1D_CLIENT_SECRET='xxx'
#  export S1D_USERNAME='xxx'
#  export S1D_PASSWORD='xxx'

#  export S2C_URL='xxx'
#  export S2C_TOKEN_URL='xxx'
#  export S2C_AUTHORIZATION='xxx'
#  export S2C_GRANT_TYPE='xxx'
#  export S2C_SCOPE='xxx'
#  export S2C_USERNAME='xxx'
#  export S2C_PASSWORD='xxx'

#  export S2B_URL='xxx'
#  export S2B_TOKEN_URL='xxx'
#  export S2B_AUTHORIZATION='xxx'
#  export S2B_GRANT_TYPE='xxx'
#  export S2B_CLIENT_ID='xxx'
#  export S2B_CLIENT_SECRET='xxx'
#  export S2B_USERNAME='xxx'
#  export S2B_PASSWORD='xxx'

#  export S3A_URL='xxx'
#  export S3A_TOKEN_URL='xxx'
#  export S3A_GRANT_TYPE='xxx'
#  export S3A_AUTHORIZATION='xxx'
#  export S3A_CLIENT_ID='xxx'
#  export S3A_USERNAME='xxx'
#  export S3A_PASSWORD='xxx'

#  export S3B_URL='xxx'
#  export S3B_TOKEN_URL='xxx'
#  export S3B_AUTHORIZATION='xxx'
#  export S3B_GRANT_TYPE='xxx'
#  export S3B_SCOPE='xxx'
#  export S3B_CLIENT_ID='xxx'
#  export S3B_CLIENT_SECRET='xxx'
#  export S3B_USERNAME='xxx'
#  export S3B_PASSWORD='xxx'

############################
# TESTS PRIP
############################

AUTHBEAR="Authorization: Bearer"
PFIELD=".value[0].Name"

set -o pipefail
declare -A URL
declare -A TOKEN

URL['S1A']=${S1A_URL}
URL['S1C']=${S1C_URL}
URL['S1D']=${S1D_URL}
URL['S2A']=${S2C_URL}
URL['S2B']=${S2B_URL}
URL['S3A']=${S3A_URL}
URL['S3B']=${S3B_URL}

# Refresh tokens
TOKEN['S1A']=$(curl -s -f -k --location -H "Content-Type: application/x-www-form-urlencoded" --data-urlencode grant_type="${S1A_GRANT_TYPE}" --data-urlencode username="${S1A_USERNAME}" --data-urlencode password="${S1A_PASSWORD}" --data-urlencode client_id="${S1A_CLIENT_ID}" --data-urlencode client_secret="${S1A_CLIENT_SECRET}" "${S1A_TOKEN_URL}" | jq -r .access_token)
TOKEN['S1C']=$(curl -s -f -k --location -H "Content-Type: application/x-www-form-urlencoded" --data-urlencode grant_type="${S1C_GRANT_TYPE}" --data-urlencode username="${S1C_USERNAME}" --data-urlencode password="${S1C_PASSWORD}" --data-urlencode client_id="${S1C_CLIENT_ID}" --data-urlencode client_secret="${S1C_CLIENT_SECRET}" --data-urlencode scope="${S1C_SCOPE}" "${S1C_TOKEN_URL}" | jq -r .access_token)
TOKEN['S1D']=$(curl -s -f -k --location -H "Content-Type: application/x-www-form-urlencoded" --data-urlencode grant_type="${S1D_GRANT_TYPE}" --data-urlencode username="${S1D_USERNAME}" --data-urlencode password="${S1D_PASSWORD}" --data-urlencode client_id="${S1D_CLIENT_ID}" --data-urlencode client_secret="${S1D_CLIENT_SECRET}" "${S1D_TOKEN_URL}" | jq -r .access_token)
TOKEN['S2A']=$(curl -s -f -k --location -H "Content-Type: application/x-www-form-urlencoded" -H "Authorization: ${S2C_AUTHORIZATION}" --data-urlencode grant_type="${S2C_GRANT_TYPE}" --data-urlencode username="${S2C_USERNAME}" --data-urlencode password="${S2C_PASSWORD}" --data-urlencode scope="${S2C_SCOPE}" "${S2C_TOKEN_URL}" | jq -r .access_token)
TOKEN['S2B']=$(curl -s -f -k --location -H "Content-Type: application/x-www-form-urlencoded" -H "Authorization: ${S2B_AUTHORIZATION}" --data-urlencode grant_type="${S2B_GRANT_TYPE}" --data-urlencode username="${S2B_USERNAME}" --data-urlencode password="${S2B_PASSWORD}" --data-urlencode client_id="${S2B_CLIENT_ID}" --data-urlencode client_secret="${S2B_CLIENT_SECRET}" "${S2B_TOKEN_URL}" | jq -r .access_token)
TOKEN['S3A']=$(curl -s -f -k --location -H "Content-Type: application/x-www-form-urlencoded" -H "Authorization: ${S3A_AUTHORIZATION}" --data-urlencode grant_type="${S3A_GRANT_TYPE}" --data-urlencode username="${S3A_USERNAME}" --data-urlencode password="${S3A_PASSWORD}" --data-urlencode client_id="${S3A_CLIENT_ID}" "${S3A_TOKEN_URL}" | jq -r .access_token)
TOKEN['S3B']=$(curl -s -f -k --location -H "Content-Type: application/x-www-form-urlencoded" -H "Authorization: ${S3B_AUTHORIZATION}" --data-urlencode grant_type="${S3B_GRANT_TYPE}" --data-urlencode username="${S3B_USERNAME}" --data-urlencode password="${S3B_PASSWORD}" --data-urlencode client_id="${S3B_CLIENT_ID}" --data-urlencode client_secret="${S3B_CLIENT_SECRET}" "${S3B_TOKEN_URL}" | jq -r .access_token)

# Basic check
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR # NOSONAR
# eq
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ContentLength%20eq%200&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
#for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=Checksum%5B0%5D%2FAlgorithm%20eq%20'MD5'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ContentType%20eq%20'application/octet-stream'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ProductionType%20eq%20OData.CSC.ProductionType'systematic_production'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=Attributes/OData.CSC.StringAttribute/any(att:att/Name%20eq%20'orbitDirection'%20and%20att/OData.CSC.StringAttribute/Value%20in%20('ASCENDING','ascending','DESCENDING','descending'))&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# ne
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ContentLength%20ne%200&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ContentType%20ne%20'application/octet-stream'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ProductionType%20ne%20OData.CSC.ProductionType'systematic_production'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=Attributes/OData.CSC.StringAttribute/any(att:att/Name%20eq%20'orbitDirection'%20and%20att/OData.CSC.StringAttribute/Value%20ne%20'DESCENDING')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# gt
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=PublicationDate%20gt%202026-02-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# ge
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=PublicationDate%20ge%202026-02-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# lt
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=PublicationDate%20lt%202026-12-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# le
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=PublicationDate%20le%202026-12-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# in
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ContentType%20in%20('application/octet-stream','application/zip')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ProductionType%20in%20(OData.CSC.ProductionType'systematic_production',OData.CSC.ProductionType'on-demand default')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=Attributes/OData.CSC.StringAttribute/any(att:att/Name%20eq%20'orbitDirection'%20and%20att/OData.CSC.StringAttribute/Value%20in%20('ASCENDING','ascending','DESCENDING','descending'))&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# and
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=PublicationDate%20gt%202026-02-01T00:00:00.000Z%20and%20PublicationDate%20lt%202026-12-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# or
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=PublicationDate%20gt%202026-02-01T00:00:00.000Z%20or%20PublicationDate%20lt%202026-12-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# not
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=not%20endswith(Name,'l')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# ()
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=PublicationDate%20gt%202026-02-01T00:00:00.000Z%20and%20(contains(Name,'2000')%20or%20contains(Name,'3000'))&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# concat
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=concat(ContentType,'Z')%20eq%20'application/octet-streamZ'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# contains
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=contains(Name,'2000')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# endswith
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=endswith(Name,'p')%20or%20endswith(Name,'r')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# indexof
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=indexof(Name,'.')%20gt%201&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# length
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=length(ContentType)%20gt%2010&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# startswith
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=startswith(Name,'S')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# substring
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=substring(ContentType,23)%20eq%20'm'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# matchesPattern
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=matchesPattern(ContentType,'%5Eapplication/.*m\$')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# tolower
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=tolower(ContentType)%20eq%20'application/octet-stream'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# toupper
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=toupper(ContentType)%20eq%20'APPLICATION/OCTET-STREAM'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
# trim
for sys in S1A S1C S1D S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=trim(ContentType)%20eq%20'application/octet-stream'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR

# smallest public SAFE product
PFIELD='.value[0] | "\(.Name) \(.ContentLength)"'
for sys in S1A S1D; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=not%20(contains(Name,'WV_RAW'))%20and%20endswith(Name,'SAFE.zip')&\$top=1&\$orderby=ContentLength%20asc" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
for sys in S1C S2A S2B S3A S3B ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=not%20(contains(Name,'HKM2'))%20and%20not%20(contains(Name,'SR_1_LAN_RD'))%20and%20not%20(contains(Name,'WV_RAW'))%20and%20not%20(contains(Name,'DO_0_'))%20and%20not%20(contains(Name,'_CAL_'))%20and%20not%20(contains(Name,'_AI_'))%20and%20not%20(contains(Name,'AX'))%20and%20not%20(contains(Name,'AUX'))%20and%20(endswith(Name,'SAFE.zip')%20or%20endswith(Name,'.tar')%20or%20endswith(Name,'SEN3.zip'))&\$top=1&\$orderby=ContentLength%20asc" | jq "${PFIELD}" || echo "ERROR" ; done # NOSONAR
