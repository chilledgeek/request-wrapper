# requests-wrapper
This repo is a wrapper programme based python's requests package, 
adding a simple API key management capability.

It is designed to:
- Enable calling API endpoints using multiple API keys
- So that different API keys can be used for each consecutive call
- This can potentially benefit in cases where each API key is rate limiting
- When the rate limit is specified, this wrapper will automatically sleep accordingly until 
  the API key can be used again, reducing the chance of getting 
  a bad `429 Too Many Requests` error code

## Installation
```pip install git+https://github.com/chilledgeek/requests-wrapper.git```

## Example
``` python
from requests_wrapper.requests_wrapper import RequestsWrapper

# Load API keys and rate limit when constructing the class instance
requests_wrapper = RequestsWrapper(
    api_keys=["<api_key1>", "<api_key2>"],
    call_limit_per_second=2
)

queries = ["search_term1", "search_term2", "search_term3"]
responses = []

for query in queries:

    # Calling this is almost the same as calling requests, 
    # with the addition of specifying http_method and api_key_header 
    response = requests_wrapper.call(
        http_method="get",
        api_key_header="Authorization",
        url="<my_url>",
        params={"q": "<my_query_term>"}
    )

    responses.append(response)
```