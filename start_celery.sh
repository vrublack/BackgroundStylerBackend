#!/bin/bash
celery -A main.celery worker -c 1
