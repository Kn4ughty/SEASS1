#!/bin/sh

gunicorn -w 2 server -b 0.0.0.0:5000