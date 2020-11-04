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
```

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