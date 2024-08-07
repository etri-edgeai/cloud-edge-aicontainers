FROM alpine:latest

# Install necessary packages
RUN apk update && apk add --no-cache \
    bash \
    curl \
    lm_sensors \
    util-linux

# Copy scripts into the image
COPY beacon.sh /usr/local/bin/beacon.sh

# Make scripts executable
RUN chmod +x /usr/local/bin/beacon.sh

# Set entrypoint
ENTRYPOINT ["/bin/bash", "/usr/local/bin/beacon.sh"]