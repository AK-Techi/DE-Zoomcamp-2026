# Start with python slim image
FROM python:3.13.11-slim
# Copy uv image from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set working directory
WORKDIR /app

# Add virtual environment path to PATH to keep all installed packages isolated
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files
COPY pyproject.toml .python-version uv.lock ./

# Install uv dependencies from lock file to keep same dependencies as local dev environment
RUN uv sync --locked
# Install all dependencies(used to test with just pandas and pyarrow with pip)
# RUN pip install pandas pyarrow

# Used it to test the COPY command from local repo to docker image
COPY pipeline/pipeline.py .

# Set entry point to run the pipeline
ENTRYPOINT ["python", "pipeline.py"]