#!/usr/bin/env python3
"""
Listing of the Sumo Logic API endpoints as of 2022/07/16
"""

import sys
sys.dont_write_bytecode = True

OBJECTMAP = {}

OBJECTMAP['apps'] = '/v1/apps'
OBJECTMAP['connections'] = '/v1/connections'
OBJECTMAP['views'] = '/v1/scheduledViews'
OBJECTMAP['partitions'] = '/v1/partitions'
OBJECTMAP['fers'] = '/v1/extractionRules'
OBJECTMAP['dynamicrules'] = '/v1/dynamicParsingRules'
OBJECTMAP['fields'] = '/v1/fields'
OBJECTMAP['droppedfields'] = '/v1/fields/dropped'
OBJECTMAP['builtinfields'] = '/v1/fields/builtin'
OBJECTMAP['fieldsquota'] = '/v1/fields/quota'
OBJECTMAP['ingestbudgets'] = '/v1/ingestBudgets'
OBJECTMAP['users'] = '/v1/users'
OBJECTMAP['roles'] = '/v1/roles'
OBJECTMAP['personalfolders'] = '/v2/content/folders/personal'
OBJECTMAP['globalfolders'] = '/v2/content/folders/global'
OBJECTMAP['recommendedfolders'] = '/v2/content/folders/adminRecommended'
OBJECTMAP['transformrules'] = '/v1/transformationRules'
OBJECTMAP['account-owner'] = '/v1/account/accountOwner'
OBJECTMAP['account-status'] = '/v1/account/status'
OBJECTMAP['tokens'] = '/v1/tokens'
OBJECTMAP['accesskeys'] = '/v1/accessKeys'
OBJECTMAP['allowed-ips'] = '/v1/serviceAllowlist/addresses'
OBJECTMAP['allowed-status'] = '/v1/serviceAllowlist/status'
OBJECTMAP['policy-general-audit'] = '/v1/policies/audit'
OBJECTMAP['policy-search-audit'] = '/v1/policies/searchAudit'
OBJECTMAP['policy-sharedata'] = '/v1/policies/shareDashboardsOutsideOrganization'
OBJECTMAP['policy-dataccess'] = '/v1/policies/dataAccessLevel'
OBJECTMAP['policy-maxsessions'] = '/v1/policies/userConcurrentSessionsLimit'
OBJECTMAP['policy-timeout'] = '/v1/policies/maxUserSessionTimeout'
OBJECTMAP['account-events'] = '/v1/healthEvents'
OBJECTMAP['dashboards'] = '/v2/dashboards'
OBJECTMAP['policy-password'] = '/v1/passwordPolicy'
OBJECTMAP['fields-traces'] = '/v1/tracing/tracequery/fields'
OBJECTMAP['fields-spans'] = '/v1/tracing/spanquery/fields'
OBJECTMAP['account-servicemap'] = '/v1/tracing/serviceMap'
