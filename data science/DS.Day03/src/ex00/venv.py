#!/usr/bin/env python3
import os
def virtual_env():
    env_path = os.environ.get('VIRTUAL_ENV')
    if env_path:
        print(f"Your current virtual env is {env_path}")
    else:
        print("No virtual environment activated")

if __name__ == "__main__":
    virtual_env()