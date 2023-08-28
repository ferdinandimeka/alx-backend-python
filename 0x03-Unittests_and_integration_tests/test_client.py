#!/usr/bin/env python3
"""Unittests for client module
"""
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock
from parameterized import parameterized, parameterized_class
from requests import HTTPError
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from typing import Dict


class TestGithubOrgClient(unittest.TestCase):
    """GithubOrgClient class unitests
    """
    @parameterized.expand([
        ("google", {'login': 'google'}),
        ("abc", {'login': 'abc'}),
    ])
    @patch('client.get_json')
    def test_org(self, org: str, resp: Dict, mocked_fxn: MagicMock) -> None:
        """Test that GithubOrgClient.org returns the correct value
        """
        mocked_fxn.return_value = MagicMock(return_value=resp)
        client = GithubOrgClient(org)
        self.assertEqual(client.org(), resp)
        mocked_fxn.assert_called_once_with(
            'https://api.github.com/orgs/{}'.format(org)
        )

    def test_public_repos_url(self) -> None:
        """Test that the result of _public_repos_url is the expected one
        """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mocked_org:
            mocked_org.return_value = {
                'repos_url': 'https://api.github.com/users/google/repos'
                }
            client = GithubOrgClient('test')
            self.assertEqual(
                client._public_repos_url,
                'https://api.github.com/users/google/repos'
                )
            mocked_org.assert_called_once_with()

    @patch('client.GithubOrgClient')
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Test that the list of repos is what you expect from the
            chosen payload. Test that the mocked property and method
            were called once.
        """
        test_payload = {
            'repos_url': "https://api.github.com/users/google/repos",
            'repos': [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/episodes.dart",
                    "created_at": "2013-01-19T00:31:37Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "has_issues": True,
                    "forks": 22,
                    "default_branch": "master",
                },
                {
                    "id": 8566972,
                    "name": "kratu",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/kratu",
                    "created_at": "2013-03-04T22:52:33Z",
                    "updated_at": "2019-11-15T22:22:16Z",
                    "has_issues": True,
                    "forks": 32,
                    "default_branch": "master",
                },
            ]
        }
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mocked_public_repos_url:
            mocked_public_repos_url.return_value = test_payload['repos_url']
            self.assertEqual(
                GithubOrgClient('google').public_repos(),
                ['episodes.dart', 'kratu']
            )
            mocked_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({'license': {'key': 'bsd-3-clause'}}, 'bsd-3-clause', True),
        ({'license': {'key': 'bs1-1.0'}}, 'bsd-3-clause', False),
    ])
    def test_has_license(
        self,
        repo: Dict,
        license_key: str,
        expected: bool
    ) -> None:
        """Test that the result of _public_repos_url is the expected one
        """
        gh_org_client = GithubOrgClient("google")
        client_has_licence = gh_org_client.has_license(repo, license_key)
        self.assertEqual(client_has_licence, expected)

    @parameterized_class([
        {
            'org_payload': TEST_PAYLOAD[0][0],
            'repos_payload': TEST_PAYLOAD[0][1],
            'expected_payload': TEST_PAYLOAD[0][2],
            'apache2_repos': TEST_PAYLOAD[0][3],
        },
    ])
    class TestIntegrationGithubOrgClient(unittest.TestCase):
        """Perform integration test for the GithubOrgClient class
        """
        @classmethod
        def setUpClass(cls) -> None:
            """Prepare for testing. set up class fixtures before running tests
            """
            route_payload = {
                'https://api.github.com/orgs/google': cls.org_payload,
                'https://api.github.com/orgs/google/repos': cls.repos_payload,
            }

            def get_payload(url):
                if url in route_payload:
                    return Mock(**{'json.return_value': route_payload[url]})
                return HTTPError

            cls.get_patcher = patch('requests.get', side_effect=get_payload)
            cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Test that the list of repos is what
            you expect from the chosen payload.
        """
        self.assertEqual(
            GithubOrgClient('google').public_repos(),
            self.expected_repos
        )

    def test_public_repos_with_license(self) -> None:
        """Test that the list of repos is what
            you expect from the chosen payload.
        """
        self.assertEqual(
            GithubOrgClient('google').public_repos('apache-2.0'),
            self.apache2_repos
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down class fixtures after running tests
        """
        return cls.get_patcher.stop()
