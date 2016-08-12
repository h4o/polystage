FROM python:3.5.2

RUN pip install openpyxl
RUN pip install PyYaml
RUN pip install requests
RUN pip install six

ENV PYTHONSTARTUP "python/shell.py"

WORKDIR /usr/src/Atlassian