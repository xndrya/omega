FROM python:3.7.7-alpine3.11
COPY web_check_availability.py /
CMD [ "python", "./check_availability.py" ]