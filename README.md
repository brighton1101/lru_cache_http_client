# LRU Cache for HTTP Requests

### Python's requests library decorated with an LRU cache for similar GET requests. Supports an optional TTL policy.

### Usage:
```py
from lru_cache_http_client import get_caching_client
import time


def no_ttl_google():
    URL = "https://www.google.com"
    caching_client = get_caching_client(capacity=2)
    start = time.time()
    res1 = caching_client.get(URL)
    after_req_1 = time.time()
    res2 = caching_client.get(URL)
    finish = time.time()
    print("Time for initial request: {}".format(after_req_1 - start))
    print("Time for duplicate request: {}".format(finish - after_req_1))
    print("Total time: {}".format(finish - start))

def ttl_google():
    URL = "https://www.google.com"
    caching_client = get_caching_client(capacity=2, ttl_seconds=1)
    print("With TTL policy of 1 second")
    print("Issuing first req to google...")
    res1 = caching_client.get(URL)
    print("Now sleeping for two seconds")
    time.sleep(2)
    start = time.time()
    print("Issuing second req to google...")
    res2 = caching_client.get(URL)
    finish = time.time()
    # `res1` will be different than `res2` because
    # a second request will be issued.
    # `res1` expires in the cache due to the ttl policy
    print(
        "Response object 1 vs 2 is {}".format(
            "different" if res1 != res2 else "the same"
        )
    )
    assert res1 != res2
```
- See [requests api for get requests](https://requests.readthedocs.io/en/latest/_modules/requests/api/#get) for valid parameters
- Note that it is possible to write your own HTTP client if using `requests` is not a possibility for your project

### Use cases:
- Web scraping
- Duplicate requests to sources with rarely changing data

### Thread safety:
- Implementation uses `functools.lru_cache` from Python's standard library
- See [here](https://github.com/python/cpython/blob/a75c4c924de102e48faef5538eade764289915ab/Lib/functools.py#L470) 

### Features:
- Avoid issuing duplicate requests to static data sources
- Single dependency! (`requests`)
- Specify a max caching capacity
- Specify an optional TTL policy for cache (in seconds)
- Extensible - add your own `HttpClient` or `Hasher` implementation for full control

### Setting up development environment:
```bash
# From root directory where `setup.py` is located
chmod u+x init.bash
./init.bash
source venv/bin/activate
```