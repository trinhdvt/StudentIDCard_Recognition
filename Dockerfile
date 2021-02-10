FROM python:3.8

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt --no-cache-dir

RUN pip3 install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html --no-cache-dir

RUN pip3 uninstall opencv-python -y

RUN pip3 install opencv-python-headless

CMD ["python3", "server.py"]

