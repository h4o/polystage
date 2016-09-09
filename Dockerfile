FROM python:3.5.2

RUN pip install openpyxl
RUN pip install PyYaml
RUN pip install requests
RUN pip install six
RUN pip install gitpython

RUN git config --global http.sslVerify "false"

ENV PYTHONSTARTUP "python/shell.py"

WORKDIR /usr/src/Atlassian