from fastapi import APIRouter, HTTPException, Response
from aiohttp import ClientSession
from env import env

router = APIRouter()

@router.get('/proxy/{asset_hash}')
async def proxy_file(asset_hash: str):
    if len(asset_hash) != 40:
        raise HTTPException(404)
    
    async with ClientSession(base_url=env.S3_PUBLIC_ENDPOINT) as client:
        async with client.get(asset_hash) as response:
            if response.status != 200:
                raise HTTPException(response.status)
            
            return Response(content=await response.content.read(), headers={
                'Content-Type': response.headers['Content-Type'],
                'Cache-Control': 'public, max-age=36000, immutable'
            })
        
@router.get('/static_proxy/{path:path}')
async def proxy_statis(path: str):
    async with ClientSession(base_url=env.S3_PUBLIC_ENDPOINT) as client:
        async with client.get(path) as response:
            if response.status != 200:
                raise HTTPException(response.status)
            
            return Response(content=await response.content.read(), headers={
                'Content-Type': response.headers['Content-Type'],
                'Cache-Control': 'public, max-age=36000, immutable'
            })