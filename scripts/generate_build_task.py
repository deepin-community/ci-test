#!/bin/env python3

import yaml
import os
import logging

logging.basicConfig(level=logging.INFO)
maxSize = os.environ.get("MAX_TASKS", 10)

def read_intergration():
    with open("intergration.yml", "r+") as intergration_file:
        return yaml.safe_load(intergration_file)

def main():
    try:
        allRepos = [{"order": j,"data":{"payload": []}} for j in range(maxSize)]
        data = read_intergration()
        message = data.get("message", "")
        print("::set-output name=message::" + message)
        for repo in data.get("repos"):
            order = int(repo.get("order",0))
            if order >= maxSize: order = maxSize - 1
            elif order < 0: order = 0
            allRepos[order].get("data").get("payload").append(repo)
        for order in allRepos:
            if len(order.get("data").get("payload")) > 0:
                print("::set-output name=build_matrix_" + str(order['order']) + "::" + str(order.get("data")))
    except BaseException as e:
        logging.error(e)
        exit(-10)

if __name__ == "__main__":
    exit(main())
