FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY your_python_program.py .

CMD ["python", "your_python_program.py"]
