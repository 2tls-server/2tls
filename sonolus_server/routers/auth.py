from fastapi import APIRouter, Header, Request, HTTPException
from asyncio import to_thread
from ..models import *
from time import time

from .. import database
from sqlmodel import select, update

router = APIRouter()

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
import base64

import secrets
from env import env

PUBLIC_KEY = {
    "kty": "EC",
    "x": "d2B14ZAn-zDsqY42rHofst8rw3XB90-a5lT80NFdXo0",
    "y": "Hxzi9DHrlJ4CVSJVRnydxFWBZAgkFxZXbyxPSa8SJQw",
    "crv": "P-256"
}

def make_public_key(jwk: dict):
    x_bytes = base64.urlsafe_b64decode(jwk['x'] + "==")
    y_bytes = base64.urlsafe_b64decode(jwk['y'] + "==")
    return ec.EllipticCurvePublicKey.from_encoded_point(
        ec.SECP256R1(), 
        b"\x04" + x_bytes + y_bytes
    )

public_key = make_public_key(PUBLIC_KEY)

def verify_signature(body: bytes, signature_b64: str) -> bool:
    try:
        sig_raw = base64.b64decode(signature_b64)
        if len(sig_raw) != 64:
            return False

        r = int.from_bytes(sig_raw[:32], "big")
        s = int.from_bytes(sig_raw[32:], "big")
        sig_der = encode_dss_signature(r, s)

        public_key.verify(sig_der, body, ec.ECDSA(hashes.SHA256()))
        return True
    except Exception:
        return False

MINUTES_30 = 30 * 60

@router.post('/authenticate', response_model=ServerAuthenticateResponse)
async def auth(auth_request: ServerAuthenticateRequest, request: Request, signature: str=Header('', alias='Sonolus-Signature')):    
    if auth_request.type != 'authenticateServer':
        raise HTTPException(418, 'Not authentication request')
    
    if auth_request.address not in env.FINAL_HOST_LINKS:
        raise HTTPException(418, 'Invalid server address')
    
    if auth_request.time / 1000 - time() > 60:
        raise HTTPException(401, 'Request expired')

    raw_body = await request.body()

    if not signature or not await to_thread(verify_signature, raw_body, signature):
        return HTTPException(418, 'Invalid signature')
    
    session_id = secrets.token_urlsafe(32)
    
    async with database.get_session() as session:
        db_user = (await session.execute(select(User).where(User.id == auth_request.userProfile.id))).scalar_one_or_none()

        if not db_user:
            user = User(**auth_request.userProfile.model_dump(include=User.model_fields.keys()))
            anonymous_user = AnonymousUser(user=user)
            user.anonymous_user = anonymous_user

            session.add_all([user, anonymous_user])
            await session.commit()

            await session.refresh(user)
            await session.refresh(anonymous_user)

            user.anonymous_user = anonymous_user # for good measure
            new_user = user
        else:
            if (req_user := auth_request.userProfile.model_dump(include=User.model_fields.keys())) != db_user.model_dump(include=ServiceUserProfile.model_fields.keys()):
                await session.execute((
                    update(User)
                    .where(User.id == auth_request.userProfile.id)
                    .values(**req_user)
                ))

                await session.commit()
            
            new_user = User(**req_user)
            new_user.anonymous_user = (await session.execute(select(AnonymousUser).where(AnonymousUser.user_id == new_user.id))).scalar_one()

    async with database.redis_client.client() as redis:
        await redis.setex(f'{env.PROJECT_NAME}:session:{session_id}', MINUTES_30, new_user.id)
        await redis.setex(f'{env.PROJECT_NAME}:user:{new_user.id}', MINUTES_30, new_user.model_dump_json())

    return ServerAuthenticateResponse(
        session=session_id,
        expiration=(int(time()) + MINUTES_30) * 1000
    )