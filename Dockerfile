# first stage
FROM python:3.8 AS builder
COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN python3 -m pip install --user -r requirements.txt
# second unnamed stage
FROM python:3.8
WORKDIR /code

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY ./src .
RUN apt install curl
# update PATH environment variable
EXPOSE 5000
ENV PATH=/root/.local:$PATH
CMD [ "python", "./main.py" ]