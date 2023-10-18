from urllib.request import urlopen
from urllib.error import HTTPError 
import json

def fetch_json(url: str) -> str:
    try:
        response = urlopen(url)
        if response.getcode() == 200:
            return response.read()
        else:
            raise HTTPError(url, response.getcode(), "HTTP request failed", None, None)
    except HTTPError as e:
        print(f"HTTP error: {e}")
        raise e
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
    
def tokenize(input: str):
    return "".join(ch.lower() if ch.isalpha() else " " for ch in input).split()

def num_url(num: int) -> str:
    assert num > 0
    return "https://xkcd.com/" + str(num) + "/info.0.json"

def update_dict(num, words, data):
    for word in words:
        if word not in data:
            data[word] = {num}
        else:
            data[word].add(num)

def index(max: int):
    data = {}
    for num in range(1, max + 1):
        print(f"Starting to index {num}")
        url = num_url(num)
        try:
            json_data = fetch_json(url)
        except Exception:
            continue

        obj = json.loads(json_data)
        for key in ("transcript", "alt", "title"):
            try:
                words = tokenize(obj[key])
            except Exception as e:
                continue
            update_dict(num, words, data)
        print(f"Finished indexing {num}")
    
    for key in data:
        data[key] = list(data[key])
    
    with open("index.json", "w") as f:
        f.write(json.dumps(data))

def search(key: str):
    try:
        f = open("index.json", "r")
    except FileNotFoundError:
        index(2842)
        f = open("index.json", "r")

    data = json.loads(f.read())

    if key in data:
        print(f"xkcd comics with the keyword \"{key}\":")
        for num in data[key]:
            print("https://xkcd.com/" + str(num))
    else:
        print("Not found")

## Edit keyword here
if __name__ == "__main__":
    search("python")