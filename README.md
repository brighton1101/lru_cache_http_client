# LRU Cache for HTTP Requests

### Python's requests library decorated with an LRU cache for similar GET requests. Supports an optional TTL policy.

### Use cases:
- Web scraping
- Duplicate requests to sources with rarely changing data

### Thread safety:
- Implementation uses `functools.lru_cache` from Python's standard library
- See [here](https://github.com/python/cpython/blob/a75c4c924de102e48faef5538eade764289915ab/Lib/functools.py#L470) for 

### Features:
- Avoid issuing duplicate requests to static data sources
- Single dependency! (`requests`)
- Specify a max caching capacity
- Specify an optional TTL policy for cache (in seconds)
- Extensible - add your own `HttpClient` or `Hasher` implementation for full control

### Setting up development environment:
```bash
# From root directory where `setup.py` is located
python3 -m venv venv
pip3 install -e .
pip3 install pytest # for testing via pytest
```