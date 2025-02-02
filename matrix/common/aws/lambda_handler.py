from enum import Enum
import json
import os

import boto3


class LambdaName(Enum):
    """
    Lambda function resource names used during matrix service request.
    """
    DRIVER_V0 = os.getenv("LAMBDA_DRIVER_V0_FUNCTION_NAME")
    DRIVER_V1 = os.getenv("LAMBDA_DRIVER_V1_FUNCTION_NAME")
    NOTIFICATION = os.getenv("LAMBDA_NOTIFICATION_FUNCTION_NAME")


class LambdaHandler:
    def __init__(self):

        self._client = boto3.client("lambda", region_name=os.environ['AWS_DEFAULT_REGION'])

    def invoke(self, fn_name: LambdaName, payload: dict):
        """
        Invokes a Lambda function.

        :param fn_name: The LambdaName of the function to be invoked
        :param payload: Data passed to invoked lambda
        """
        self._client.invoke(
            FunctionName=fn_name.value,
            InvocationType="Event",
            Payload=json.dumps(payload).encode(),
        )
