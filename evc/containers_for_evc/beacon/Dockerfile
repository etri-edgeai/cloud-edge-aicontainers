# Dockerfile
FROM alpine:latest

# Copy scripts into the image
COPY beacon_arm.sh /usr/local/bin/beacon_arm.sh
COPY beacon_x86.sh /usr/local/bin/beacon_x86.sh

# Make scripts executable
RUN chmod +x /usr/local/bin/beacon_arm.sh /usr/local/bin/beacon_x86.sh

# Set entrypoint based on the architecture
CMD ["/usr/bin/bash", "-c", "if [ $(uname -m) = 'x86_64' ]; then /usr/local/bin/beacon_x86.sh; else /usr/local/bin/beacon_arm.sh; fi"]
