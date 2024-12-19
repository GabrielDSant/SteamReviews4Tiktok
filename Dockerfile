FROM python:3.10.14

RUN apt update && apt-get install -y ffmpeg python3-pip curl

WORKDIR /

RUN pip install playwright
RUN python -m playwright install
RUN python -m playwright install-deps
RUN pip install ffmpeg-python moviepy
RUN pip install git+https://github.com/openai/whisper.git
RUN pip install openai==0.28.0

# Define o script como ENTRYPOINT
CMD ["bash"]
