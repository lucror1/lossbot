FROM nginx:mainline-alpine

WORKDIR /data

# Copy files over
COPY nginx.conf /etc/nginx/nginx.conf
COPY --chmod=644 secrets/public.crt /data/cert/
COPY --chmod=600 secrets/private.key /data/cert/
COPY static static