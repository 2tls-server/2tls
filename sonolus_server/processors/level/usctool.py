# Based on https://github.com/sevenc-nanashi/usctool, licensed under MIT.

from pydantic import BaseModel, field_validator, Field
from typing import Literal

type number = int | float

class BaseUSCObject(BaseModel):
    beat: number
    timeScaleGroup: number

class USCBpmChange(BaseUSCObject):
    timeScaleGroup: None = Field(None, exclude=True)
    type: Literal['bpm']
    bpm: number

class USCTimeScaleChangeChanges(BaseModel):
    beat: number
    timeScale: number

class USCTimeScaleChange(BaseModel):
    type: Literal['timeScaleGroup']
    changes: list[USCTimeScaleChangeChanges]

class BaseUSCNote(BaseUSCObject):
    lane: number
    size: number

class USCSingleNote(BaseUSCNote):
    type: Literal['single'] = 'single'
    critical: bool
    trace: bool
    direction: Literal['left', 'up', 'right', 'none', None] = None

class USCDamageNote(BaseUSCNote):
    type: Literal['damage'] = 'damage'

class USCConnectionStartNote(BaseUSCNote):
    type: Literal['start'] = 'start'
    critical: bool
    ease: Literal['out', 'linear', 'in', 'inout', 'outin'] # fixed ig?
    judgeType: Literal['normal', 'trace', 'none']

class USCConnectionTickNote(BaseUSCNote):
    type: Literal['tick'] = 'tick'
    critical: bool | None = None
    ease: Literal['out', 'linear', 'in', 'inout', 'outin'] # fixed ig?

class USCConnectionAttachNote(BaseUSCObject):
    type: Literal['attach'] = 'attach'
    critical: bool | None = None
    timeScaleGroup: number | None = None

class USCConnectionEndNote(BaseUSCNote):
    type: Literal['end'] = 'end'
    critical: bool
    direction: Literal['left', 'up', 'right', None] = None
    judgeType: Literal['normal', 'trace', 'none']

class USCSlideNote(BaseModel):
    type: Literal['slide'] = 'slide'
    critical: bool
    connections: list[USCConnectionStartNote | USCConnectionTickNote | USCConnectionAttachNote | USCConnectionEndNote]

    @field_validator('connections')
    def check_connections(cls, v):
        if not v:
            return
        
        if not isinstance(v[0], USCConnectionStartNote):
            raise ValueError
        if not isinstance(v[-1], USCConnectionEndNote):
            raise ValueError
        for mid in v[1:-1]:
            if not isinstance(mid, (USCConnectionTickNote, USCConnectionAttachNote)):
                raise ValueError
            
USC_COLORS = {
    'neutral': 0,
    'red': 1,
    'green': 2,
    'blue': 3,
    'yellow': 4,
    'purple': 5,
    'cyan': 6,
    'black': 7
}
type USCColor = Literal['neutral', 'red', 'green', 'blue', 'yellow', 'purple', 'cyan', 'black']

USC_FADES = {
    'in': 2,
    'out': 0,
    'none': 1
}
type USCFade = Literal['in', 'out', 'fade']

class USCGuideMidpointNote(BaseUSCNote):
    ease: Literal['out', 'linear', 'in', 'inout', 'outin'] # fixed ig?

class USCGuideNote(BaseModel):
    type: Literal['guide']
    color: USCColor
    fade: USCFade
    midpoints: list[USCGuideMidpointNote]

type USCObject = USCBpmChange | USCTimeScaleChange | USCSingleNote | USCSlideNote | USCGuideNote | USCDamageNote

class USC(BaseModel):
    offset: number
    objects: list[USCObject]