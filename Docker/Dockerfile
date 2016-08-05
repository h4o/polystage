FROM python:3.5.2

RUN pip install openpyxl
RUN pip install PyYaml
RUN pip install requests
RUN pip install six

WORKDIR /usr/src/Atlassian
CMD [ "python", "-i", "init.py" ]