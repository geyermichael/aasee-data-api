FROM python

WORKDIR /usr/src/

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && rm requirements.txt

COPY . .

CMD python app.py