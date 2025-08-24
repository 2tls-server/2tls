# I really tried to rewrite usc2leveldata to python but uhh

# from .processor import uscToLevelData, USC
from .usctool import USC
from pydantic import BaseModel
from typing import Literal
from gzip import compress
import quickjs

class USCFile(BaseModel):
    usc: USC
    version: Literal[2]

def uscToLevelData(usc: USC):
    ctx = quickjs.Context()
    ctx.eval(JS_CODE)

    return ctx.get('uscToLevelData')(usc.model_dump_json()).json()

def process_level(data: bytes) -> bytes:
    data = data.decode()

    model = USCFile.model_validate_json(data, strict=True)
    return compress(uscToLevelData(usc=model.usc).encode()) # TODO: Support for USCv1 and chs/mmws/sus

JS_CODE = '''
// MIT License

// Copyright (c) 2023 sevenc-nanashi

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

// MIT License

// Copyright (c) 2023 Nanashi.

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

// ---- Original License ----

// MIT License

// Copyright (c) 2023 NonSpicyBurrito

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

// MIT License

// Copyright (c) 2021 NonSpicyBurrito

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

// Code from following repos:
// https://github.com/sevenc-nanashi/sonolus-pjsekai-engine-extended
// https://github.com/sevenc-nanashi/usctool
// https://github.com/Sonolus/sonolus-core/

// uscToLevelData = USCFade = USCColor = EngineArchetypeName = EngineArchetypeDataName = void 0;
EngineArchetypeDataName = {
    Beat: '#BEAT',
    Bpm: '#BPM',
    TimeScale: '#TIMESCALE',
    Judgment: '#JUDGMENT',
    Accuracy: '#ACCURACY',
};
EngineArchetypeName = {
    BpmChange: '#BPM_CHANGE',
    TimeScaleChange: '#TIMESCALE_CHANGE',
};
USCColor = {
    neutral: 0,
    red: 1,
    green: 2,
    blue: 3,
    yellow: 4,
    purple: 5,
    cyan: 6,
    black: 7,
};
USCFade = {
    in: 2,
    out: 0,
    none: 1,
};
function uscToLevelData (uscjson, offset = 0) {
    const usc = JSON.parse(uscjson);

    const entities = [];
    const timeToIntermediates = new Map();
    const intermediateToRef = new Map();
    const intermediateToEntity = new Map();
    let i = 0;
    const getRef = (intermediate) => {
        let ref = intermediateToRef.get(intermediate);
        if (ref)
            return ref;
        ref = (i++).toString(36);
        intermediateToRef.set(intermediate, ref);
        const entity = intermediateToEntity.get(intermediate);
        if (entity)
            entity.name = ref;
        return ref;
    };
    const append = (intermediate) => {
        const entity = {
            archetype: intermediate.archetype,
            data: [],
        };
        if (intermediate.sim) {
            const beat = intermediate.data[EngineArchetypeDataName.Beat];
            if (typeof beat !== "number")
                throw new Error("Unexpected beat");
            const intermediates = timeToIntermediates.get(beat);
            if (intermediates) {
                intermediates.push(intermediate);
            }
            else {
                timeToIntermediates.set(beat, [intermediate]);
            }
        }
        const ref = intermediateToRef.get(intermediate);
        if (ref)
            entity.name = ref;
        intermediateToEntity.set(intermediate, entity);
        entities.push(entity);
        for (const [name, value] of Object.entries(intermediate.data)) {
            if (typeof value === "number") {
                entity.data.push({
                    name,
                    value,
                });
            }
            else if (typeof value === "boolean") {
                entity.data.push({
                    name,
                    value: value ? 1 : 0,
                });
            }
            else if (typeof value === "string") {
                entity.data.push({
                    name,
                    ref: value,
                });
            }
            else {
                entity.data.push({
                    name,
                    ref: getRef(value),
                });
            }
        }
        if ("timeScaleGroup" in intermediate) {
            entity.data.push({
                name: "timeScaleGroup",
                ref: `tsg:${intermediate.timeScaleGroup ?? 0}`,
            });
        }
    };
    append({
        archetype: "Initialization",
        data: {},
        sim: false,
    });
    append({
        archetype: "InputManager",
        data: {},
        sim: false,
    });
    append({
        archetype: "Stage",
        data: {},
        sim: false,
    });
    let tsGroupIndex = -1;
    const tsGroupEntities = [];
    const tsChangeEntities = [];
    for (const tsGroup of usc.objects) {
        if (tsGroup.type !== "timeScaleGroup")
            continue;
        tsGroupIndex++;
        const changes = [...tsGroup.changes];
        changes.sort((a, b) => a.beat - b.beat);
        for (const [index, change] of Object.entries(changes)) {
            tsChangeEntities.push({
                archetype: "TimeScaleChange",
                data: [
                    {
                        name: EngineArchetypeDataName.Beat,
                        value: change.beat,
                    },
                    {
                        name: "timeScale",
                        value: change.timeScale === 0 ? 0.000001 : change.timeScale,
                    },
                    tsGroup.changes[+index + 1] === undefined
                        ? {
                            name: "next",
                            value: -1,
                        }
                        : {
                            name: "next",
                            ref: `tsc:${tsGroupIndex}:${+index + 1}`,
                        },
                ],
                name: `tsc:${tsGroupIndex}:${index}`,
            });
        }
        tsGroupEntities.push({
            archetype: "TimeScaleGroup",
            data: [
                {
                    name: "first",
                    ref: `tsc:${tsGroupIndex}:0`,
                },
                {
                    name: "length",
                    value: tsGroup.changes.length,
                },
                tsGroupIndex === tsGroup.changes.length - 1
                    ? {
                        name: "next",
                        value: -1,
                    }
                    : {
                        name: "next",
                        ref: `tsg:${tsGroupIndex + 1}`,
                    },
            ],
            name: `tsg:${tsGroupIndex}`,
        });
    }
    if (tsGroupIndex === -1) {
        entities.push({
            archetype: "TimeScaleGroup",
            data: [
                {
                    name: "first",
                    ref: "tsc:0:0",
                },
                {
                    name: "length",
                    value: 0,
                },
            ],
            name: "tsg:0",
        });
        entities.push({
            archetype: "TimeScaleChange",
            data: [
                {
                    name: EngineArchetypeDataName.Beat,
                    value: 0,
                },
                {
                    name: "timeScale",
                    value: 1,
                },
                {
                    name: "timeScaleGroup",
                    ref: "trg:0",
                },
            ],
            name: "tsc:0:0",
        });
    }
    else {
        entities.push(...tsGroupEntities);
        entities.push(...tsChangeEntities);
    }
    for (const object of usc.objects) {
        handlers[object.type](object, append);
    }
    for (const intermediates of timeToIntermediates.values()) {
        for (let i = 1; i < intermediates.length; i++) {
            append({
                archetype: "SimLine",
                data: {
                    a: intermediates[i - 1],
                    b: intermediates[i],
                },
                sim: false,
            });
        }
    }
    return {
        bgmOffset: usc.offset + offset,
        entities,
    };
};
// uscToLevelData = uscToLevelData;
const directions = {
    left: -1,
    up: 0,
    right: 1,
};
const eases = {
    outin: -2,
    out: -1,
    linear: 0,
    in: 1,
    inout: 2,
};
const slideStarts = {
    tap: 0,
    trace: 1,
    none: 2,
};
const bpm = (object, append) => {
    append({
        archetype: EngineArchetypeName.BpmChange,
        data: {
            [EngineArchetypeDataName.Beat]: object.beat,
            [EngineArchetypeDataName.Bpm]: object.bpm,
        },
        sim: false,
    });
};
const timeScaleGroup = () => undefined;
const single = (object, append) => {
    const intermediate = {
        archetype: object.critical ? "CriticalTapNote" : "NormalTapNote",
        data: {
            [EngineArchetypeDataName.Beat]: object.beat,
            lane: object.lane,
            size: object.size,
        },
        timeScaleGroup: object.timeScaleGroup,
        sim: true,
    };
    if (object.trace) {
        intermediate.archetype = object.critical
            ? "CriticalTraceNote"
            : "NormalTraceNote";
        if (object.direction) {
            if (object.direction === "none") {
                intermediate.archetype = "NonDirectionalTraceFlickNote";
            }
            else {
                intermediate.archetype = object.critical
                    ? "CriticalTraceFlickNote"
                    : "NormalTraceFlickNote";
                intermediate.data.direction = directions[object.direction];
            }
        }
    }
    else {
        if (object.direction) {
            intermediate.archetype = object.critical
                ? "CriticalFlickNote"
                : "NormalFlickNote";
            if (object.direction === "none") {
                return;
            }
            intermediate.data.direction = directions[object.direction];
        }
    }
    append(intermediate);
};
const damage = (object, append) => {
    const intermediate = {
        archetype: "DamageNote",
        data: {
            [EngineArchetypeDataName.Beat]: object.beat,
            lane: object.lane,
            size: object.size,
        },
        sim: false,
        timeScaleGroup: object.timeScaleGroup,
    };
    append(intermediate);
};
const slide = (object, append) => {
    const cis = [];
    const joints = [];
    const attaches = [];
    const ends = [];
    let startType = "tap";
    const connections = getConnections(object);
    for (const [i, connection] of connections.entries()) {
        if (i === 0) {
            if (connection.type !== "start")
                continue;
            let archetype;
            let sim = true;
            if (connection.judgeType === "none") {
                archetype = "HiddenSlideStartNote";
                sim = false;
                startType = "none";
            }
            else if (connection.judgeType === "trace") {
                if (connection.critical) {
                    archetype = "CriticalTraceSlideStartNote";
                }
                else {
                    archetype = "NormalTraceSlideStartNote";
                }
                startType = "trace";
            }
            else {
                if (connection.critical) {
                    archetype = "CriticalSlideStartNote";
                }
                else {
                    archetype = "NormalSlideStartNote";
                }
                startType = "tap";
            }
            const ci = {
                archetype,
                data: {
                    [EngineArchetypeDataName.Beat]: connection.beat,
                    lane: connection.lane,
                    size: connection.size,
                },
                sim,
                ease: connection.ease,
                timeScaleGroup: connection.timeScaleGroup,
            };
            cis.push(ci);
            joints.push(ci);
            continue;
        }
        if (i === connections.length - 1) {
            if (connection.type !== "end")
                continue;
            let ci;
            if (connection.judgeType === "none") {
                ci = {
                    archetype: "HiddenSlideTickNote",
                    data: {
                        [EngineArchetypeDataName.Beat]: connection.beat,
                        lane: connection.lane,
                        size: connection.size,
                    },
                    sim: false,
                    timeScaleGroup: connection.timeScaleGroup,
                };
            }
            else {
                let archetype;
                if (connection.judgeType === "trace") {
                    if (connection.critical) {
                        archetype = "CriticalTraceSlideEndNote";
                    }
                    else {
                        archetype = "NormalTraceSlideEndNote";
                    }
                }
                else {
                    if (connection.critical) {
                        archetype = "CriticalSlideEndNote";
                    }
                    else {
                        archetype = "NormalSlideEndNote";
                    }
                }
                ci = {
                    archetype,
                    data: {
                        [EngineArchetypeDataName.Beat]: connection.beat,
                        lane: connection.lane,
                        size: connection.size,
                    },
                    sim: true,
                    timeScaleGroup: connection.timeScaleGroup,
                };
                if ("direction" in connection) {
                    ci.archetype = connection.critical
                        ? "CriticalSlideEndFlickNote"
                        : "NormalSlideEndFlickNote";
                    ci.data.direction = directions[connection.direction];
                }
            }
            cis.push(ci);
            joints.push(ci);
            ends.push(ci);
            continue;
        }
        switch (connection.type) {
            case "tick": {
                const ci = {
                    archetype: "HiddenSlideTickNote",
                    data: {
                        [EngineArchetypeDataName.Beat]: connection.beat,
                        lane: connection.lane,
                        size: connection.size,
                    },
                    sim: false,
                    ease: connection.ease,
                    timeScaleGroup: connection.timeScaleGroup,
                };
                if ("critical" in connection)
                    ci.archetype = connection.critical
                        ? "CriticalSlideTickNote"
                        : "NormalSlideTickNote";
                cis.push(ci);
                joints.push(ci);
                break;
            }
            case "attach": {
                const ci = {
                    archetype: "IgnoredSlideTickNote",
                    data: {
                        [EngineArchetypeDataName.Beat]: connection.beat,
                    },
                    sim: false,
                };
                if ("critical" in connection)
                    ci.archetype = connection.critical
                        ? "CriticalAttachedSlideTickNote"
                        : "NormalAttachedSlideTickNote";
                if ("timeScaleGroup" in connection)
                    ci.timeScaleGroup = connection.timeScaleGroup;
                cis.push(ci);
                attaches.push(ci);
                break;
            }
            case "start":
            case "end":
                throw new Error("Unexpected slide tick");
        }
    }
    const connectors = [];
    const start = cis[0];
    for (const [i, joint] of joints.entries()) {
        if (i === 0)
            continue;
        const head = joints[i - 1];
        if (!head.ease)
            throw new Error("Unexpected missing ease");
        const archetype = object.critical
            ? "CriticalSlideConnector"
            : "NormalSlideConnector";
        connectors.push({
            archetype,
            data: {
                start,
                end: ends[0],
                head,
                tail: joint,
                ease: eases[head.ease],
                startType: slideStarts[startType],
            },
            sim: false,
        });
    }
    for (const attach of attaches) {
        const index = cis.indexOf(attach);
        const tailIndex = joints.findIndex((c) => cis.indexOf(c) > index);
        attach.data.attach = connectors[tailIndex - 1];
    }
    for (const end of ends) {
        end.data.slide = connectors[connectors.length - 1];
    }
    for (const ci of cis) {
        append(ci);
    }
    for (const connector of connectors) {
        append(connector);
    }
};
const guide = (object, append) => {
    const start = object.midpoints[0];
    const end = object.midpoints[object.midpoints.length - 1];
    for (const [i, joint] of object.midpoints.entries()) {
        if (i === 0)
            continue;
        const head = object.midpoints[i - 1];
        if (!head.ease)
            throw new Error("Unexpected missing ease");
        append({
            archetype: "Guide",
            data: {
                color: USCColor[object.color],
                fade: USCFade[object.fade],
                ease: eases[head.ease],
                startLane: start.lane,
                startSize: start.size,
                startBeat: start.beat,
                startTimeScaleGroup: `tsg:${start.timeScaleGroup ?? 0}`,
                headLane: head.lane,
                headSize: head.size,
                headBeat: head.beat,
                headTimeScaleGroup: `tsg:${head.timeScaleGroup ?? 0}`,
                tailLane: joint.lane,
                tailSize: joint.size,
                tailBeat: joint.beat,
                tailTimeScaleGroup: `tsg:${joint.timeScaleGroup ?? 0}`,
                endLane: end.lane,
                endSize: end.size,
                endBeat: end.beat,
                endTimeScaleGroup: `tsg:${end.timeScaleGroup ?? 0}`,
            },
            sim: false,
        });
    }
};
const handlers = {
    bpm,
    single,
    timeScaleGroup,
    slide,
    guide,
    damage,
};
const getConnections = (object) => {
    const connections = [...object.connections];
    const beats = connections.map(({ beat }) => beat).sort((a, b) => a - b);
    const min = beats[0];
    const max = beats[beats.length - 1];
    const start = Math.max(Math.ceil(min / 0.5) * 0.5, Math.floor(min / 0.5 + 1) * 0.5);
    for (let beat = start; beat < max; beat += 0.5) {
        connections.push({
            type: "attach",
            beat,
        });
    }
    const startStep = connections.find(({ type }) => type === "start");
    const endStep = connections.find(({ type }) => type === "end");
    const steps = connections.filter(({ type }) => type === "tick" || type === "attach");
    steps.sort((a, b) => a.beat - b.beat);
    if (!startStep)
        throw "Missing start";
    if (!endStep)
        throw "Missing end";
    return [startStep, ...steps, endStep];
};
'''