import aioboto3
from os import getenv

class S3Client:
    def __init__(self):
        self.client = aioboto3.resource(service_name='s3',
                                                   endpoint_url=getenv('S3_ENDPOINT_URL'),
                                                   aws_access_key_id=getenv("AWS_ACCESS_KEY"),
                                                   aws_secret_access_key=getenv("AWS_SECRET_KEY"))

    async def write_image(self, image_bytes, image_path):
        await self.client.Object('logs', image_path).put(Body=image_bytes)


client = S3Client()
