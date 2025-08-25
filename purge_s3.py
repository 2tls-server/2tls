from sys import exit

action = input('Are you ABSOLUTELY sure you want to purge the S3 Bucket? [yes]')

if action != 'yes':
    print('Aborting...')
    exit(0)

from aiobotocore.session import get_session
from env import env
from asyncio import run

async def main():
    async with get_session().create_client(
        's3',
        endpoint_url=env.S3_API_ENDPOINT,
        aws_access_key_id=env.S3_ACCESS_KEY,
        aws_secret_access_key=env.S3_SECRET_KEY,
    ) as s3:
        paginator = s3.get_paginator('list_objects_v2')

        async for page in paginator.paginate(Bucket=env.S3_BUCKET_NAME):
            objs = []

            if 'Contents' in page:
                for obj in page['Contents']:
                    objs.append({'Key': obj['Key']})

            for chunk_offset in range(0, len(objs), 1000):
                chunk = objs[chunk_offset:chunk_offset + 1000]
                if chunk:
                    await s3.delete_objects(
                        Bucket=env.S3_BUCKET_NAME,
                        Delete={'Objects': chunk}
                    )

run(main())