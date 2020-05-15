FROM terrillo/python3flask:latest

WORKDIR /client

ENV STATIC_URL ./
ENV STATIC_PATH /static

# Place your flask application on the server
COPY . .


# Install requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# NGINX setup
COPY ./nginx.sh /nginx.sh
COPY ./cert.pem /etc/nginx/cert.pem
COPY ./key.pem /etc/nginx/key.pem
RUN chmod +x /nginx.sh

ENV PYTHONPATH=./

ENTRYPOINT ["/nginx.sh"]

# Start Server
CMD ["/start.sh"]

EXPOSE 443