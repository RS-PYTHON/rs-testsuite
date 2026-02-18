#!/bin/sh

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
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# eq
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ContentType%20eq%20'application/octet-stream'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# ne
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ContentType%20ne%20'application/octet-stream'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# gt
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=PublicationDate%20gt%202026-02-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# ge
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=PublicationDate%20ge%202026-02-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# lt
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=PublicationDate%20lt%202026-02-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# le
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=PublicationDate%20le%202026-02-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# in
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ContentType%20in%20('application/octet-stream','foo')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# and
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ContentType%20eq%20'application/octet-stream'%20and%20PublicationDate%20lt%202026-01-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# or
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ContentType%20eq%20'application/octet-stream'%20or%20ContentType%20eq%20'foo'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# not
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=not%20endswith(Name,'p')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=not(ContentType%20eq%20'application/zip')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=not%20(ContentType%20eq%20'application/zip')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# ()
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=ContentType%20eq%20'application/octet-stream'%20and%20(contains(Name,'2000')%20or%20contains(Name,'3000'))&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# concat
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=concat(ContentType,'Z')%20eq%20'application/octet-streamZ'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# contains
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=contains(Name,'2000')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# endswith
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=endswith(Name,'p')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# indexof
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=indexof(ContentType,'p')%20eq%201&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# length
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=length(ContentType)%20eq%2024&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# startswith
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=startswith(Name,'S1A')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# substring
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=substring(ContentType,23)%20eq%20'm'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# matchesPattern
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=matchesPattern(ContentType,'%5Eapplication/.*m\$')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# tolower
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=tolower(ContentType)%20eq%20'application/octet-stream'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# toupper
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=toupper(ContentType)%20eq%20'APPLICATION/OCTET-STREAM'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
# trim
for sys in ADGS ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Products?\$filter=trim(ContentType)%20eq%20'application/octet-stream'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${AFIELD}" || echo "ERROR" ; done
