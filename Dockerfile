FROM python:3.12 
# Or any preferred Python version.
ADD main.py .
RUN pip install "reactpy[flask]"
CMD [“python”, “./main.py”] 