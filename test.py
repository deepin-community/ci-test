import requests
import os

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization":"Bearer " + os.environ.get("GITHUB_TOKEN")
}
res = requests.patch(url="https://api.github.com/repos/deepin-community/ci-test/pulls/61",
headers=headers, json= {'state': 'closed'})
print(res.text)
print(res.status_code)