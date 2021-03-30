# ahapy

[![PyPI version](https://badge.fury.io/py/ahapy.svg)](https://badge.fury.io/py/ahapy)


A small Aha.io API client. The package handles authentication and pagination, giving the user exactly the information they seek.

This is in no way associated with Aha.io. For Aha.io API documentation, please visit [aha.io/api](https://www.aha.io/api).


## Install
```commandline
pip install ahapy
```


## Usage

After importing the library, create an instance of AhaV1 by providing your subdomain from https://[my-subdomain].aha.io/ and your API key.
```python
from ahapy import AhaV1

aha = AhaV1('<your-sub-domain>', '<your-api-key>')
```

Create a simple query by running the query method, giving the method the desired endpoint.
```python
data = aha.query('initiatives')

for i in data:
    print(i)
```

While using the query method, you can specify page size and customize the fields to be returned.
```python
data = aha.query('initiatives', per_page=200, fields='name,id')

for i in data:
    print(i)
```

After running a query, you can check if the number of record receieved is the number that was expected.

```python
data = aha.query('initiatives')

if len(data) == aha.count:
    print('Records returned matches expectation.')
```