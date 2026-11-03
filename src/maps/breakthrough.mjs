// Exact approved geometry: 026fb7a / planning/r3-geometry/map.json.
export const BREAKTHROUGH=Object.freeze({
  "bounds": {
    "left": 192,
    "right": 576,
    "top": 0,
    "bottom": 768
  },
  "exit": {
    "left": 320,
    "right": 448,
    "top": 0,
    "bottom": 192
  },
  "tank": {
    "x": 512,
    "y": 704,
    "facing": "up"
  },
  "truck": {
    "x": 272,
    "y": 688,
    "heading": 1
  },
  "deadline": 90,
  "speed": 48,
  "body": [
    128,
    56
  ],
  "margin": 4,
  "turnRadius": 76,
  "turnSeconds": 0.35,
  "spacing": 16
});
const CELLS=[
  {
    "id": "U0",
    "x": 320,
    "y": 128,
    "kind": "brick"
  },
  {
    "id": "U1",
    "x": 384,
    "y": 128,
    "kind": "brick"
  },
  {
    "id": "US0",
    "x": 320,
    "y": 192,
    "kind": "steel"
  },
  {
    "id": "US1",
    "x": 384,
    "y": 192,
    "kind": "steel"
  },
  {
    "id": "P",
    "x": 480,
    "y": 256,
    "kind": "steel"
  },
  {
    "id": "L0",
    "x": 288,
    "y": 480,
    "kind": "brick"
  },
  {
    "id": "LS0",
    "x": 352,
    "y": 480,
    "kind": "steel"
  },
  {
    "id": "L1",
    "x": 288,
    "y": 544,
    "kind": "brick"
  },
  {
    "id": "LS1",
    "x": 352,
    "y": 544,
    "kind": "steel"
  }
];
export function missionWalls(){return CELLS.map(w=>({...w,width:64,height:64}));}
