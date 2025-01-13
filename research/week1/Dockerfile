FROM httpd:2.4

RUN echo "ServerName localhost" >> /usr/local/apache2/conf/httpd.conf

RUN sed -i 's/Listen 80/Listen 8061/' /usr/local/apache2/conf/httpd.conf

RUN echo "<h1>Hello from Apache running in Kubernetes!</h1>" > /usr/local/apache2/htdocs/index.html

EXPOSE 8061

CMD ["httpd-foreground"]
