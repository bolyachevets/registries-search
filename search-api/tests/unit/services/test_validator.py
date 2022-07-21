# Copyright © 2022 Province of British Columbia
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

"""Tests to verify the validator is working as expected."""

import copy

import pytest
from flask import current_app

from search_api.services import authz
from search_api.services.validator import RequestValidator
from tests.unit.services.utils import helper_create_jwt


MOCK_URL_NO_KEY = 'https://bcregistry-bcregistry-mock.apigee.net/mockTarget/auth/api/v1/'
MOCK_URL = 'https://bcregistry-bcregistry-mock.apigee.net/auth/api/v1/'

DOCUMENT_ACCESS_REQUEST_TEMPLATE = {
    "documentAccessRequest":{
        "documents": [
            {
                "type": "BUSINESS_SUMMARY_FILING_HISTORY"
            }
        ]
    }
}

USERS_ORG =  {
  "orgs": [
    {
      "accessType": "REGULAR",
      "id": 2617,
      "name": "Test",
      "orgStatus": "ACTIVE",
      "orgType": "PREMIUM",
      "statusCode": "ACTIVE"
    }
  ]
}

def test_document_access_request_valid(client, session, jwt, requests_mock):
    """Assert that a auth-api user orgs request works as expected with the mock service endpoint."""
    # setup
    current_app.config.update(AUTH_SVC_URL=MOCK_URL_NO_KEY)
    token = helper_create_jwt(jwt, [authz.PPR_ROLE])
    org = USERS_ORG['orgs'][0]
    requests_mock.get(f"{current_app.config.get('AUTH_SVC_URL')}users/orgs", json=USERS_ORG)
    requests_mock.get(f"{current_app.config.get('AUTH_SVC_URL')}orgs/{org['id']}", json=org)

    err =RequestValidator.validate_document_access_request(DOCUMENT_ACCESS_REQUEST_TEMPLATE, org['id'], token, 'basic')
    # check

    assert org['orgType'] == 'PREMIUM'
    assert org['id']

    assert err is None


def test_document_access_request_invalid_basic_account(client, session, jwt, requests_mock):
    """Assert that a auth-api user orgs request works as expected with the mock service endpoint."""
    # setup
    current_app.config.update(AUTH_SVC_URL=MOCK_URL_NO_KEY)
    token = helper_create_jwt(jwt, [authz.PPR_ROLE])
    USERS_ORG_COPY = copy.deepcopy(USERS_ORG)
    USERS_ORG_COPY['orgs'][0]['orgType'] = 'BASIC'
    org = USERS_ORG_COPY['orgs'][0]
    requests_mock.get(f"{current_app.config.get('AUTH_SVC_URL')}users/orgs", json=USERS_ORG_COPY)
    requests_mock.get(f"{current_app.config.get('AUTH_SVC_URL')}orgs/{org['id']}", json=org)

    err =RequestValidator.validate_document_access_request(DOCUMENT_ACCESS_REQUEST_TEMPLATE, org['id'], token, 'basic')
    # check

    assert err[0]['error'] == 'Document Access Request can be created only by a premium account user'


@pytest.mark.parametrize('test_name, error_message', [
    ('no_documents', 'Document list must contain atleast one document type'),
    ('invalid_document_type', 'Invalid Document Type')
])
def test_document_access_request_invalid(client, session, jwt, requests_mock, test_name, error_message):
    """Assert that a auth-api user orgs request works as expected with the mock service endpoint."""
    # setup
    current_app.config.update(AUTH_SVC_URL=MOCK_URL_NO_KEY)
    token = helper_create_jwt(jwt, [authz.PPR_ROLE])
    org = USERS_ORG['orgs'][0]
    requests_mock.get(f"{current_app.config.get('AUTH_SVC_URL')}users/orgs", json=USERS_ORG)
    requests_mock.get(f"{current_app.config.get('AUTH_SVC_URL')}orgs/{org['id']}", json=org)

    request_template_copy = copy.deepcopy(DOCUMENT_ACCESS_REQUEST_TEMPLATE)
    if test_name == 'no_documents':
        del request_template_copy['documentAccessRequest']['documents']
    if test_name == 'invalid_document_type':
        request_template_copy['documentAccessRequest']['documents'][0]['type'] = 'test'

    err =RequestValidator.validate_document_access_request(request_template_copy, org['id'], token, 'basic')
    # check

    assert err[0]['error'] == error_message
