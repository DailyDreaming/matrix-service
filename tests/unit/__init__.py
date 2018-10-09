import os
import unittest

from moto import mock_dynamodb2

# TODO: set DEPLOYMENT_STAGE=test when test env exists
os.environ['DEPLOYMENT_STAGE'] = "dev"
os.environ['AWS_DEFAULT_REGION'] = "us-east-1"
os.environ['AWS_ACCESS_KEY_ID'] = "ak"
os.environ['AWS_SECRET_ACCESS_KEY'] = "sk"
os.environ['LAMBDA_DRIVER_FUNCTION_NAME'] = f"dcp-matrix-service-driver-{os.environ['DEPLOYMENT_STAGE']}"
os.environ['DYNAMO_STATE_TABLE_NAME'] = f"dcp-matrix-service-state-table-{os.environ['DEPLOYMENT_STAGE']}"
os.environ['DYNAMO_OUTPUT_TABLE_NAME'] = f"dcp-matrix-service-output-table-{os.environ['DEPLOYMENT_STAGE']}"


class MatrixTestCaseUsingMockAWS(unittest.TestCase):
    def setUp(self):
        self.dynamo_mock = mock_dynamodb2()
        self.dynamo_mock.start()

    def tearDown(self):
        self.dynamo_mock.stop()

    @staticmethod
    def create_test_state_table(dynamo):
        dynamo.create_table(
            TableName=os.environ['DYNAMO_STATE_TABLE_NAME'],
            KeySchema=[
                {
                    'AttributeName': "RequestId",
                    'KeyType': "HASH",
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': "RequestId",
                    'AttributeType': "S",
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 25,
                'WriteCapacityUnits': 25,
            },
        )

    @staticmethod
    def create_test_output_table(dynamo):
        dynamo.create_table(
            TableName=os.environ['DYNAMO_OUTPUT_TABLE_NAME'],
            KeySchema=[
                {
                    'AttributeName': "RequestId",
                    'KeyType': "HASH",
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': "RequestId",
                    'AttributeType': "S",
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 15,
                'WriteCapacityUnits': 15,
            },
        )
