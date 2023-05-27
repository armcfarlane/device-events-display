ARG PYTHON_VERSION
ARG EVENTS_DISPLAY_ROOT_DIRECTORY_PATH

# Stage 1: Build and run unit tests
FROM python:${PYTHON_VERSION}-slim AS builder

WORKDIR $EVENTS_DISPLAY_ROOT_DIRECTORY_PATH

COPY test/unit/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run unit tests
RUN pytest test/unit

# Install necessary packages.
RUN apt-get update && apt-get --reinstall install -y bash

# Stage 2: Build the final image
FROM python:${PYTHON_VERSION}-slim

# Copy the python application code.
COPY --from=builder $EVENTS_DISPLAY_ROOT_DIRECTORY_PATH $EVENTS_DISPLAY_ROOT_DIRECTORY_PATH

# Copy the necessary packages that were installed during the builder stage.
COPY --from=builder /bin/bash /bin/bash

# Install production dependencies
RUN pip install --no-cache-dir -r $EVENTS_DISPLAY_ROOT_DIRECTORY_PATH/build/requirements.txt

# Copy the application startup script
COPY --from=builder application_startup.sh $EVENTS_DISPLAY_ROOT_DIRECTORY_PATH/

ENV PATH=/:${EVENTS_DISPLAY_ROOT_PATH}:/bin:/sbin:/usr/local/bin:/usr/local/sbin:.

# Set the PYTHONPATH environment variable so that the modules
# can be imported correctly.
ENV PYTHONPATH=${EVENTS_DISPLAY_ROOT_DIRECTORY_PATH}:.

WORKDIR $EVENTS_DISPLAY_ROOT_DIRECTORY_PATH

EXPOSE $EVENTS_DISPLAY_SERVICE_PORT
EXPOSE $EVENTS_DISPLAY_METRICS_PORT

# Start the FastAPI application
CMD ["application_startup.sh"]

