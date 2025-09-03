FROM python:3.12-slim
EXPOSE 5000
WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT [ "/src/entrypoint.sh" ]