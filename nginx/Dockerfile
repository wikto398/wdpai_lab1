FROM nginx:alpine

# Remove the default Nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom Nginx configuration file
COPY config/default.conf /etc/nginx/conf.d/

# Copy your HTML file into the Nginx web directory
COPY ui_app/* /usr/share/nginx/html/
