#!/bin/bash

set -eu

pip install pipenv

pipenv install --three

pipenv run test
