FROM selenium/standalone-chrome:latest

# Set working directory
WORKDIR /filmmon

# Copy the requirements file and install dependencies
COPY main.py /filmmon
COPY requirements.txt /filmmon
RUN sudo apt update
RUN sudo apt install -y python3-venv
RUN sudo python3 -m venv .venv
RUN sudo .venv/bin/pip install -r requirements.txt

# Set the default command to run the application
ENTRYPOINT [".venv/bin/python3"]
CMD ["main.py"]