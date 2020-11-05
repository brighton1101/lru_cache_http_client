#!/usr/bin/env python3

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


def no_ttl_multiple():
    URLS = ["https://www.google.com/", "https://www.wikipedia.org/"]
    caching_client = get_caching_client(capacity=1)
    start = time.time()
    res1 = caching_client.get(URLS[0])
    after_req_1 = time.time()
    res2 = caching_client.get(URLS[1])
    after_req_2 = time.time()
    res3 = caching_client.get(URLS[1])
    after_req_3 = time.time()
    res4 = caching_client.get(URLS[0])
    finish = time.time()
    print("NO TTL POLICY:")
    print("Time is in seconds")
    print("First request to google: {}".format(after_req_1 - start))
    print("Cache is now at capacity with google")
    print("First request to wikipedia: {}".format(after_req_2 - after_req_1))
    print("Second request to wikipedia: {}".format(after_req_3 - after_req_2))
    print("Cache is now at capacity with wikipedia")
    print("Second request to google: {}".format(finish - after_req_3))
    print("\n")


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
    print(
        "Response object 1 vs 2 is {}".format(
            "different" if res1 != res2 else "the same"
        )
    )
    assert res1 != res2


if __name__ == "__main__":
    no_ttl_multiple()
    ttl_google()
