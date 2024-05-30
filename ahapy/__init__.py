import requests
import re


class BaseAPI(object):
    def __init__(self, sub_domain, api_key):
        self.sub_domain = sub_domain
        self.api_key = api_key

        self.url = 'https://{}.aha.io/api'.format(self.sub_domain)

        self.session = requests.Session()
        self.session.headers.update({'Authorization': 'Bearer ' + api_key})


class AhaV1(BaseAPI):
    def __init__(self, sub_domain, api_key):
        self.sub_domain = sub_domain
        self.api_key = api_key
        self.version = '/v1/'
        self.page = 1
        self.total_pages = 0
        self.count = 0
        self.endpoint = ''

        super(AhaV1, self).__init__(sub_domain, api_key)

    def _count(self, endpoint, **options):
        url = self.url + self.version + endpoint
        response = self.session.get(url, params=options)
        r = response.json()
        self.count = r['pagination']['total_records']
        return self.count

    def _parse_endpoint_arg(self, endpoint_arg):
        s = re.split('/', endpoint_arg)
        if re.match('[a-z]', s[-1]):
            return s[-1]
        else:
            return s[-2]

    def _pagination(self, json_response):
        """
        Extracts pagination information from a JSON response dictionary.

        Parameters:
            json_response (dict): A dictionary containing the JSON response data.

        Returns:
            The first element of the 'pagination' list in the json_response dictionary,
            if it exists. If 'pagination' is not a list, it is returned as-is. If 'pagination'
            does not exist in the json_response dictionary, None is returned.
        """
        if 'pagination' in json_response:
            pagination = json_response['pagination']
            if isinstance(pagination, list):
                if len(pagination) > 0:
                    return pagination[0]
                else:
                    return None
            else:
                return pagination
        else:
            return None


    def query(self, endpoint, **options):
        """
        Query for Aha.io V1 endpoint
        """
        self.endpoint = self._parse_endpoint_arg(endpoint)

        while True:
            url = self.url + self.version + endpoint
            if self.page <= self.total_pages:
                url = url + '?page=' + str(self.page)
                response = self.session.get(url, params=options)
            else:
                response = self.session.get(url, params=options)
                r = response.json()
                pagination = self._pagination(r)
                if pagination is not None:
                    self.count = pagination['total_records']

            if not response.ok:
                print("Response status code: " + str(response.status_code))
                print("Response text: " + response.text)

            r = response.json()
            pagination = self._pagination(r)
            if pagination is not None:
                self.total_pages = pagination['total_pages']
                self.page = pagination['current_page'] + 1
            else:
                # trim pluralization from endpoint as this is 
                # singular in response body if no pagination
                # this is used as a check later to make sure 
                # response body matches expectations
                self.endpoint = self.endpoint[:-1]

            if self.endpoint in r.keys():
                for i in r[self.endpoint]:
                    yield i
            elif self.endpoint == 'custom_pivots':
                # custom_pivots response does not follow the same pattern as the other endpoints
                # so we need to give it special handling
                result = r.copy()
                if 'pagination' in result:
                    del result['pagination']
                    yield result

            if self.page > self.total_pages:
                break
