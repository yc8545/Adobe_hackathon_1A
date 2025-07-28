# 🐍 Use lightweight base image
FROM python:3.9-slim

# 👩‍💻 Set working directory inside the container
WORKDIR /app

# 🗂️ Copy files
COPY . /app

# 🧪 Install dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    libasound2-dev \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 🔊 Default command to run your CLI extractor
CMD ["python", "extractor.py", "sample.pdf"]
