FROM amazonlinux:2023

# Install Python and build dependencies
RUN dnf update -y && \
    dnf install -y python3.9 python3.9-pip zip && \
    dnf clean all

# Set working directory
WORKDIR /app

# Copy application files
COPY package/thumbnail_generator.py package/requirements.txt ./

# Install Python dependencies
RUN python3.9 -m pip install --no-cache-dir -r requirements.txt -t ./package

# Create Lambda deployment package
RUN cd package && \
    cp ../thumbnail_generator.py . && \
    zip -r ../thumbnail_lambda.zip .

# Optional: Set up entrypoint if needed
CMD ["/bin/bash"]