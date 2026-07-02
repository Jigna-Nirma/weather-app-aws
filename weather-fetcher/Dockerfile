FROM public.ecr.aws/lambda/python:3.12

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Install dependencies
RUN pip install boto3

# Set the handler
CMD ["lambda_function.lambda_handler"]