#!/bin/env python3

import requests
import yaml
import os
import logging

maxSize = os.environ.get("MAX_TASKS", 10)
illegal_tags = []

header = {
    "Accept": "application/vnd.github+json",
    "Authorization":"Bearer " + os.environ.get("GITHUB_TOKEN")
}

def read_intergration():
    with open("intergration.yml", "r+") as intergration_file:
        return yaml.safe_load(intergration_file)

def check_tag_exsist(repo, tag):
    res = requests.get("https://api.github.com/repos/deepin-community/{repo}/git/ref/tags/{tag}".format(repo=repo, tag=tag), headers=header)
    if res.status_code != 200:
        illegal_tags.append({"repo": repo, "tag": tag})

try:
    allRepos = [{"order": j,"data":{"payload": []}} for j in range(maxSize)]
    data = read_intergration()
    message = data.get("message", "")
    print("::set-output name=message::" + message)
    for repo in data.get("repos"):
        order = int(repo.get("order",0))
        order = max(0, order) and min(order , maxSize - 1)
        check_tag_exsist(repo.get('repo'), repo.get('tag'))
        allRepos[order].get("data").get("payload").append(repo)
    if len(illegal_tags) > 0:
        print("::set-output name=illegal_tags::" + str(illegal_tags))
    for order in allRepos:
        if len(order.get("data").get("payload")) > 0:
            print("::set-output name=build_matrix_" + str(order['order']) + "::" + str(order.get("data")))
except BaseException as e:
    logging.error(e)
    exit(-10)
