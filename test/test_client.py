import os
import re
import math
import json
import unittest
from ahapy import AhaV1

# To run tests, cd into package directory and the run the following:
# python -m unittest

AHA_KEY = os.environ.get('AHA_API_KEY')
assert AHA_KEY is not None, "Set AHA_API_KEY environment variable"

AHAPY_TEST_SUBDOMAIN = os.environ.get("AHAPY_TEST_SUBDOMAIN")
assert AHAPY_TEST_SUBDOMAIN is not None, "Set AHAPY_TEST_SUBDOMAIN environment variable"


class TestClient(unittest.TestCase):

    def test_v1_query(self):
        aha = AhaV1(AHAPY_TEST_SUBDOMAIN, AHA_KEY)
        data = aha.query('initiatives')
        self.assertIsNotNone(data)


    def test_v1_count(self):
        aha = AhaV1(AHAPY_TEST_SUBDOMAIN, AHA_KEY)
        count = aha._count('epics')
        self.assertGreater(count, -1)


    def test_v1_fields(self):
        aha = AhaV1(AHAPY_TEST_SUBDOMAIN, AHA_KEY)
        data = aha.query('initiatives', fields='name,id')
        for i in data:
            self.assertIsNotNone(i['name'])


    def test_v1_page(self):
        aha = AhaV1(AHAPY_TEST_SUBDOMAIN, AHA_KEY)
        aha.query('initiatives', per_page=200)
        expected_pages = math.ceil(aha.count / 200)
        self.assertEqual(expected_pages, aha.total_pages)


    def test_v1_endpoint_parse_1(self):
        aha = AhaV1(AHAPY_TEST_SUBDOMAIN, AHA_KEY)
        endpoint = aha._parse_endpoint_arg('initiatives/12345/epics')
        self.assertEqual('epics', endpoint)


    def test_v1_endpoint_parse_2(self):
        aha = AhaV1(AHAPY_TEST_SUBDOMAIN, AHA_KEY)
        endpoint = aha._parse_endpoint_arg('initiatives/12345')
        self.assertEqual('initiatives', endpoint)


    def test_v1_endpoint_parse_3(self):
        aha = AhaV1(AHAPY_TEST_SUBDOMAIN, AHA_KEY)
        endpoint = aha._parse_endpoint_arg('initiatives')
        self.assertEqual('initiatives', endpoint)

    def test_v1_endpoint_parse_4(self):
        aha = AhaV1(AHAPY_TEST_SUBDOMAIN, AHA_KEY)
        endpoint = aha._parse_endpoint_arg('bookmarks/custom_pivots/801750833?view=list')
        self.assertEqual('custom_pivots', endpoint)

    def test_v1_custom_pivot_list(self):
        aha = AhaV1(AHAPY_TEST_SUBDOMAIN, AHA_KEY)
        data = aha.query('bookmarks/custom_pivots/7216017113000441776', view='list')
        required_keys = ['columns','rows']
        for row in data:
            existing_keys = list((key in row for key in required_keys))
            self.assertTrue(all(existing_keys),
                            f"Missing keys: {[required_keys[i] for i,exist in enumerate(existing_keys) if not exist]}")
            break

    def test_pagination_with_list(self):
        # Test that it returns the first element of a non-empty pagination list
        aha = AhaV1(AHAPY_TEST_SUBDOMAIN, AHA_KEY)
        json_response = {'pagination': [{'page': 1, 'total_pages': 5}]}
        result = aha._pagination(json_response)
        self.assertEqual(result, {'page': 1, 'total_pages': 5})

    def test_pagination_with_non_list(self):
        # Test that it returns a non-list object as is
        aha = AhaV1(AHAPY_TEST_SUBDOMAIN, AHA_KEY)
        json_response = {'pagination': {'page': 1, 'total_pages': 5}}
        result = aha._pagination(json_response)
        self.assertEqual(result, {'page': 1, 'total_pages': 5})

    def test_pagination_missing(self):
        # Test that it returns None if pagination is missing
        aha = AhaV1(AHAPY_TEST_SUBDOMAIN, AHA_KEY)
        json_response = {'data': [1, 2, 3]}
        result = aha._pagination(json_response)
        self.assertIsNone(result)

    def test_pagination_with_empty_list(self):
        # Test that it returns None if pagination list is empty
        aha = AhaV1(AHAPY_TEST_SUBDOMAIN, AHA_KEY)
        json_response = {'pagination': []}
        result = aha._pagination(json_response)
        self.assertIsNone(result)
