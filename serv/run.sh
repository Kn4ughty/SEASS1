#!/bin/sh

gunicorn -w 2 server -b 127.0.0.1:5000