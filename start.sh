#!/bin/sh
source venv/bin/activate
pip install -r requirements.txt

pytest

cd switchPatrol
python main.py