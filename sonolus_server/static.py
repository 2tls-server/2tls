'''
NOTE: I gotta host these myselves. After all, some time will pass and I will need to change this

I have no idea how I will do it, but hey, there's a first time for everything

Also TODO, calculate the hashes
'''

from .models import *
from env import env

background = BackgroundItem(
    name=f'{env.PROJECT_NAME}-chcy-background',
    source='Chart Cyanvas',
    title='Live V3',
    subtitle='プロジェクトセカイ カラフルステージ!',
    author='Burrito (from Nanashi\'s github)',
    tags=[],
    thumbnail=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/blob/main/backend/assets/backgrounds/v3_thumbnail.png?raw=true'),
    data=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/raw/refs/heads/main/backend/assets/backgrounds/data.json.gz'),
    image=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/blob/main/backend/assets/backgrounds/v3.png?raw=true'),
    configuration=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/raw/refs/heads/main/backend/assets/backgrounds/configuration.json.gz')
)

effect = EffectItem(
    name=f'{env.PROJECT_NAME}-chcy-effect',
    source='Chart Cyanvas',
    title='SFX',
    subtitle='PJSekai + Trace notes',
    author='Sonolus (from Nanashi\'s github)',
    tags=[],
    thumbnail=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/raw/refs/heads/main/backend/assets/effects/EffectThumbnail'),
    data=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/raw/refs/heads/main/backend/assets/effects/EffectData'),
    audio=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/raw/refs/heads/main/backend/assets/effects/EffectAudio')
)

particle = ParticleItem(
    name=f'{env.PROJECT_NAME}-chcy-particle',
    source='Chart Cyanvas',
    title='PJSekai / v3',
    subtitle='From: https://canary.discord.com/channels/696599620259807242/696608361235611720/1192891297162330265',
    author='Hyeon2 (from Nanashi\'s github)',
    tags=[],
    thumbnail=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/blob/main/backend/assets/particles/thumbnail.png?raw=true'),
    data=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/raw/refs/heads/main/backend/assets/particles/v3.json.gz'),
    texture=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/blob/main/backend/assets/particles/v3.png?raw=true')
)

skin_old = SkinItem(
    name=f'{env.PROJECT_NAME}-chcy-skin-01',
    source='Chart Cyanvas',
    title='PJSekai+ / Type 1',
    subtitle='PjSekai + Trace notes, Type 1',
    author='Sonolus + Nanashi.',
    tags=[],
    thumbnail=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/blob/main/backend/assets/skins/01_thumbnail.png?raw=true'),
    data=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/raw/refs/heads/main/backend/assets/skins/01_data.json.gz'),
    texture=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/blob/main/backend/assets/skins/01_texture.png?raw=true')
)

skin_new = SkinItem(
    name=f'{env.PROJECT_NAME}-chcy-skin-02',
    source='Chart Cyanvas',
    title='PjSekai+ / Type 2',
    subtitle='PjSekai + Trace notes, Type 2',
    author='Sonolus + Nanashi.',
    tags=[],
    thumbnail=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/blob/main/backend/assets/skins/02_thumbnail.png?raw=true'),
    data=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/raw/refs/heads/main/backend/assets/skins/02_data.json.gz'),
    texture=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/blob/main/backend/assets/skins/02_texture.png?raw=true')
)

engine = EngineItem(
    name=f'{env.PROJECT_NAME}-chcy-pjsekai-extended',
    source='Chart Cyanvas',
    title='PJSekai+',
    subtitle='sevenc-nanashi/sonolus-pjsekai-engine-extended',
    author='Nanashi. <sevenc7c.com> (Forked from NonSpicyBurrito/sonolus-pjsekai-engine)',
    tags=[],
    skin=skin_new,
    background=background,
    effect=effect,
    particle=particle,
    thumbnail=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/raw/refs/heads/main/backend/assets/engines/EngineThumbnail'),
    playData=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/raw/refs/heads/main/backend/assets/engines/EnginePlayData'),
    watchData=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/raw/refs/heads/main/backend/assets/engines/EngineWatchData'),
    previewData=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/raw/refs/heads/main/backend/assets/engines/EnginePreviewData'),
    tutorialData=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/raw/refs/heads/main/backend/assets/engines/EngineTutorialData'),
    configuration=Srl(url='https://github.com/sevenc-nanashi/chart_cyanvas/raw/refs/heads/main/backend/assets/engines/EngineConfiguration')
)