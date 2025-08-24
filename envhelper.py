from pydantic import BaseModel

class BaseEnv(BaseModel):
    REDIS_LINK: str
    DATABASE_LINK: str

    FINAL_HOST_LINKS: list[str] # At least one should be provided; first one will be used in strings
                                # don't forget scheme

    S3_API_ENDPOINT: str
    S3_BUCKET_NAME: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_PUBLIC_ENDPOINT: str # wont actually be sent to a client, but rather used by a server itself. Must end with /

    PROJECT_NAME: str = '2tls'
    IS_DEV: bool = True