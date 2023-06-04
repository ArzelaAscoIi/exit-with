FROM python:3.10.11-slim-buster as builder

ARG HATCH_VERSION=1.7.0

WORKDIR /app
COPY . .
RUN pip install hatch==${HATCH_VERSION}
RUN hatch build

FROM python:3.10.11-slim-buster as production
# Copy the compiled files from the builder stage
COPY --from=builder /app/dist /app/dist
# Install the compiled files
RUN pip install /app/dist/*.whl && rm -rf /app/dist

# Run the application
CMD ["python", "-m", "exit_with"]