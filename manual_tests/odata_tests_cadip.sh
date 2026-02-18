#!/bin/sh

# Tests performed to check OData compliance, see https://pforge-exchange2.astrium.eads.net/confluence/pages/viewpage.action?pageId=505564386

# Following secrets must be defined in the environment:

#  export MPS_URL='xxx'
#  export MPS_URL_TOKEN='xxx'
#  export MPS_CLIENT_ID='xxx'
#  export MPS_CLIENT_SECRET='xxx'
#  export MPS_USERNAME='xxx'
#  export MPS_PASSWORD='xxx'
#  export MPS_AUTHORIZATION='xxx'

#  export MTI_URL='xxx'
#  export MTI_TOKEN_URL='xxx'
#  export MTI_GRANT_TYPE='xxx'
#  export MTI_SCOPE='xxx'
#  export MTI_CLIENT_ID='xxx'
#  export MTI_CLIENT_SECRET='xxx'
#  export MTI_USERNAME='xxx'
#  export MTI_PASSWORD='xxx'

#  export NSG_URL='xxx'
#  export NSG_TOKEN_URL='xxx'
#  export NSG_GRANT_TYPE='xxx'
#  export NSG_CLIENT_ID='xxx'
#  export NSG_CLIENT_SECRET='xxx'
#  export NSG_USERNAME='xxx'
#  export NSG_PASSWORD='xxx'

#  export SGS_URL='xxx'
#  export SGS_TOKEN_URL='xxx'
#  export SGS_GRANT_TYPE='xxx'
#  export SGS_CLIENT_ID='xxx'
#  export SGS_CLIENT_SECRET='xxx'
#  export SGS_USERNAME='xxx'
#  export SGS_PASSWORD='xxx'

#  export SSC_URL='xxx'
#  export SSC_TOKEN_URL='xxx'
#  export SSC_GRANT_TYPE='xxx'
#  export SSC_CLIENT_ID='xxx'
#  export SSC_CLIENT_SECRET='xxx'
#  export SSC_USERNAME='xxx'
#  export SSC_PASSWORD='xxx'

############################
# TESTS CADIP
############################

AUTHBEAR="Authorization: Bearer"
CFIELD=".value[0].SessionId"

set -o pipefail
declare -A URL
declare -A TOKEN

URL['MPS']=${MPS_URL}
URL['MTI']=${MTI_URL}
URL['NSG']=${NSG_URL}
URL['SGS']=${SGS_URL}
URL['SSC']=${SSC_URL}

# Refresh tokens
TOKEN['MPS']=$(curl -s -f -k --location -H "Content-Type: application/x-www-form-urlencoded" -H "Authorization: ${MPS_AUTHORIZATION}" --data-urlencode grant_type=password --data-urlencode username="${MPS_USERNAME}" --data-urlencode password="${MPS_PASSWORD}" --data-urlencode client_id="${MPS_CLIENT_ID}" --data-urlencode client_secret="${MPS_CLIENT_SECRET}" "${MPS_URL_TOKEN}" | jq -r .access_token)
TOKEN['MTI']=$(curl -s -f -k --location -H "Content-Type: application/x-www-form-urlencoded" --data-urlencode grant_type="${MTI_GRANT_TYPE}" --data-urlencode username="${MTI_USERNAME}" --data-urlencode password="${MTI_PASSWORD}" --data-urlencode client_id="${MTI_CLIENT_ID}" --data-urlencode client_secret="${MTI_CLIENT_SECRET}" --data-urlencode scope="${MTI_SCOPE}" "${MTI_TOKEN_URL}" | jq -r .access_token)
TOKEN['NSG']=$(curl -s -f -k --location -H "Content-Type: application/x-www-form-urlencoded" --data-urlencode grant_type="${NSG_GRANT_TYPE}" --data-urlencode username="${NSG_USERNAME}" --data-urlencode password="${NSG_PASSWORD}" --data-urlencode client_id="${NSG_CLIENT_ID}" --data-urlencode client_secret="${NSG_CLIENT_SECRET}" "${NSG_TOKEN_URL}" | jq -r .access_token)
TOKEN['SGS']=$(curl -s -f -k --location -H "Content-Type: application/x-www-form-urlencoded" --data-urlencode grant_type="${SGS_GRANT_TYPE}" --data-urlencode username="${SGS_USERNAME}" --data-urlencode password="${SGS_PASSWORD}" --data-urlencode client_id="${SGS_CLIENT_ID}" --data-urlencode client_secret="${SGS_CLIENT_SECRET}" "${SGS_TOKEN_URL}" | jq -r .access_token)
TOKEN['SSC']=$(curl -s -f -k --location -H "Content-Type: application/x-www-form-urlencoded" --data-urlencode grant_type="${SSC_GRANT_TYPE}" --data-urlencode username="${SSC_USERNAME}" --data-urlencode password="${SSC_PASSWORD}" --data-urlencode client_id="${SSC_CLIENT_ID}" --data-urlencode client_secret="${SSC_CLIENT_SECRET}" "${SSC_TOKEN_URL}" | jq -r .access_token)

# Basic check
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$top=1" | jq "${FIELD}" || echo "ERROR" ; done
# eq
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=Satellite%20eq%20'S1A'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# ne
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=Satellite%20ne%20'S1A'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# gt
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=PublicationDate%20gt%202026-02-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# ge
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=PublicationDate%20ge%202026-02-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# lt
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=PublicationDate%20lt%202026-02-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# le
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=PublicationDate%20le%202026-02-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# in
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=Satellite%20in%20('S1A','S1C')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# and
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=Satellite%20eq%20'S1C'%20and%20PublicationDate%20lt%202026-01-01T00:00:00.000Z&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# or
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=Satellite%20eq%20'S1A'%20or%20Satellite%20eq%20'S1C'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# not
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=not%20endswith(SessionId,'0')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=not(Satellite%20eq%20'S1A')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=not%20(Satellite%20eq%20'S1A')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# ()
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=Satellite%20eq%20'S1A'%20and%20(contains(SessionId,'2000')%20or%20contains(SessionId,'3000'))&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# concat
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=concat(Satellite,'Z')%20eq%20'S1AZ'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# contains
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=contains(SessionId,'2000')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# endswith
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=endswith(SessionId,'0')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# indexof
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=indexof(Satellite,'A')%20eq%202&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# length
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=length(Satellite)%20eq%203&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# startswith
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=startswith(SessionId,'S1A')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# substring
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=substring(Satellite,1)%20eq%20'1A'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# matchesPattern
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=matchesPattern(Satellite,'%5ES.*A\$')&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# tolower
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=tolower(Satellite)%20eq%20's1a'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# toupper
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=toupper(Satellite)%20eq%20'S1A'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
# trim
for sys in MPS MTI NSG SGS SSC ; do echo -n "${sys}: " ; curl -sfkH "${AUTHBEAR} ${TOKEN[$sys]}" "${URL[$sys]}/Sessions?\$filter=trim(Satellite)%20eq%20'S1A'&\$orderby=PublicationDate%20desc&\$top=1" | jq "${CFIELD}" || echo "ERROR" ; done
