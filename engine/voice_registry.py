"""Voice registry for VoiceForge 2762 — built-in + cloned voices.

Voice IDs are Pocket TTS's built-in voice prompts. Cloned voices are
stored in data/config.json with their state files under data/cloned/.
"""
import json
from pathlib import Path
from threading import RLock

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_FILE = DATA_DIR / "config.json"
CLONED_DIR = DATA_DIR / "cloned"

BUILTIN_VOICES = [
    {"id": "alba", "name": "Alba", "gender": "female", "language": "en",
     "description": "Clear, versatile female voice", "tags": ["versatile", "clear"]},
    {"id": "cosette", "name": "Cosette", "gender": "female", "language": "en",
     "description": "Soft, gentle female voice", "tags": ["soft", "warm"]},
    {"id": "fantine", "name": "Fantine", "gender": "female", "language": "en",
     "description": "Expressive female voice", "tags": ["expressive", "emotional"]},
    {"id": "eponine", "name": "Eponine", "gender": "female", "language": "en",
     "description": "Bright, energetic female voice", "tags": ["bright", "energetic"]},
    {"id": "azelma", "name": "Azelma", "gender": "female", "language": "en",
     "description": "Light, cheerful female voice", "tags": ["cheerful", "casual"]},
    {"id": "anna", "name": "Anna", "gender": "female", "language": "en",
     "description": "Calm, professional female voice", "tags": ["calm", "professional"]},
    {"id": "vera", "name": "Vera", "gender": "female", "language": "en",
     "description": "Rich, mature female voice", "tags": ["rich", "confident"]},
    {"id": "mary", "name": "Mary", "gender": "female", "language": "en",
     "description": "Friendly female voice", "tags": ["friendly", "podcast"]},
    {"id": "jane", "name": "Jane", "gender": "female", "language": "en",
     "description": "Natural female voice", "tags": ["natural", "smooth"]},
    {"id": "eve", "name": "Eve", "gender": "female", "language": "en",
     "description": "Elegant female voice", "tags": ["elegant", "modern"]},
    {"id": "caro_davy", "name": "Caro Davy", "gender": "female", "language": "en",
     "description": "Distinctive female voice", "tags": ["distinctive", "warm"]},
    {"id": "lola", "name": "Lola", "gender": "female", "language": "en",
     "description": "Vibrant female voice", "tags": ["vibrant", "dynamic"]},
    {"id": "estelle", "name": "Estelle", "gender": "female", "language": "en",
     "description": "Graceful female voice", "tags": ["graceful", "melodic"]},
    {"id": "marius", "name": "Marius", "gender": "male", "language": "en",
     "description": "Strong male voice", "tags": ["strong", "authoritative"]},
    {"id": "javert", "name": "Javert", "gender": "male", "language": "en",
     "description": "Deep male voice — best for dark voiceovers", "tags": ["deep", "commanding"]},
    {"id": "jean", "name": "Jean", "gender": "male", "language": "en",
     "description": "Warm male voice", "tags": ["warm", "trustworthy"]},
    {"id": "charles", "name": "Charles", "gender": "male", "language": "en",
     "description": "Refined male voice", "tags": ["refined", "eloquent"]},
    {"id": "paul", "name": "Paul", "gender": "male", "language": "en",
     "description": "Casual male voice", "tags": ["casual", "friendly"]},
    {"id": "george", "name": "George", "gender": "male", "language": "en",
     "description": "Steady male voice", "tags": ["steady", "audiobook"]},
    {"id": "michael", "name": "Michael", "gender": "male", "language": "en",
     "description": "Dynamic male voice", "tags": ["dynamic", "energetic"]},
    {"id": "bill_boerst", "name": "Bill Boerst", "gender": "male", "language": "en",
     "description": "Classic male voice", "tags": ["classic", "broadcast"]},
    {"id": "peter_yearsley", "name": "Peter Yearsley", "gender": "male", "language": "en",
     "description": "Distinguished British male voice", "tags": ["british", "distinguished"]},
    {"id": "stuart_bell", "name": "Stuart Bell", "gender": "male", "language": "en",
     "description": "Clear male voice", "tags": ["clear", "versatile"]},
    {"id": "giovanni", "name": "Giovanni", "gender": "male", "language": "en",
     "description": "Charismatic male voice", "tags": ["charismatic", "expressive"]},
    {"id": "juergen", "name": "Juergen", "gender": "male", "language": "en",
     "description": "Precise male voice", "tags": ["precise", "articulate"]},
    {"id": "rafael", "name": "Rafael", "gender": "male", "language": "en",
     "description": "Natural male voice", "tags": ["natural", "conversational"]},
]

# Style characters: named presets built ONLY from Pocket TTS's own voices.
# A style character is not a new voice model and not a clone of anyone
# else's voice — it is a built-in base voice plus a pitch/speed preset,
# so generation stays on Pocket TTS (free, unlimited). This is how
# ElevenLabs-style characters (e.g. a deep professional voice in the
# style of ElevenLabs' Henry) are offered without cloning ElevenLabs'
# stock voices, which belong to their voice actors.
# Six style presets. Every built-in voice x every preset = one character,
# so the library grows to 26 base voices + 3 hero characters + 156
# style characters = 185 selectable characters, all generated on
# Pocket TTS. A preset only changes pitch/speed — the voice itself is
# always one of the 26 built-in Pocket TTS voices.
STYLE_PRESETS = [
    ("deep", "Deep", 0.85, 0.95),
    ("warm", "Warm", 0.95, 0.95),
    ("bright", "Bright", 1.12, 1.05),
    ("energetic", "Energetic", 1.15, 1.12),
    ("calm", "Calm", 0.92, 0.85),
    ("soft", "Soft", 1.05, 0.88),
]

STYLE_CHARACTERS = [
    {"id": "deep-pro", "name": "Deep Pro (Henry Style)", "gender": "male",
     "language": "en",
     "description": "Deep, professional male narration in the style of ElevenLabs' Henry — built from Pocket TTS",
     "tags": ["featured", "deep", "professional", "narration"], "is_style": True,
     "base_voice": "charles", "pitch": 0.95, "speed": 0.95},
    {"id": "warm-storyteller", "name": "Warm Storyteller", "gender": "female",
     "language": "en",
     "description": "Warm, mature female voice for stories and audiobooks",
     "tags": ["featured", "warm", "storytelling", "audiobook"], "is_style": True,
     "base_voice": "caro_davy", "pitch": 0.95, "speed": 0.95},
    {"id": "energetic-host", "name": "Energetic Host", "gender": "male",
     "language": "en",
     "description": "Bright, dynamic male voice for hosting and upbeat videos",
     "tags": ["featured", "energetic", "host", "dynamic"], "is_style": True,
     "base_voice": "michael", "pitch": 1.08, "speed": 1.08},
] + [
    {"id": f"{base['id']}-{slug}",
     "name": f"{base['name']} — {label}",
     "gender": base["gender"], "language": "en",
     "description": f"{label} version of {base['name']}",
     "tags": [slug, base["gender"]], "is_style": True,
     "base_voice": base["id"], "pitch": pitch, "speed": speed}
    for base in BUILTIN_VOICES
    for (slug, label, pitch, speed) in STYLE_PRESETS
]


class VoiceRegistry:
    def __init__(self):
        self._lock = RLock()
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        CLONED_DIR.mkdir(parents=True, exist_ok=True)
        if not CONFIG_FILE.exists():
            CONFIG_FILE.write_text(
                json.dumps({"verified": False, "cloned_voices": []}, indent=2),
                encoding="utf-8",
            )

    def _read_config(self):
        try:
            value = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            if isinstance(value, dict):
                return value
        except (OSError, json.JSONDecodeError):
            pass
        return {"verified": False, "cloned_voices": []}

    def _write_config(self, config):
        temp = CONFIG_FILE.with_suffix(".tmp")
        temp.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
        temp.replace(CONFIG_FILE)

    def get_all_voices(self, gender=None, language=None, search=None):
        with self._lock:
            config = self._read_config()
            voices = list(BUILTIN_VOICES) + list(STYLE_CHARACTERS)
            for item in config.get("cloned_voices", []):
                if isinstance(item, dict) and item.get("id"):
                    voices.append(item)
            if gender:
                voices = [v for v in voices if v.get("gender") == gender]
            if language:
                voices = [v for v in voices if v.get("language", "en") == language]
            if search:
                q = search.casefold()
                voices = [
                    v for v in voices
                    if q in (v.get("name", "") + " " + v.get("description", "")).casefold()
                ]
            return voices

    def get_voice(self, voice_id):
        return next((v for v in self.get_all_voices() if v.get("id") == voice_id), None)

    def get_languages(self):
        return sorted({v.get("language", "en") for v in self.get_all_voices()})

    def is_verified(self):
        return bool(self._read_config().get("verified", False))

    def set_verified(self, verified=True):
        with self._lock:
            config = self._read_config()
            config["verified"] = bool(verified)
            self._write_config(config)

    def add_cloned_voice(self, voice_id, name, state_path, language="en"):
        voice = {
            "id": voice_id, "name": name, "gender": "other",
            "language": language or "en", "description": "User-cloned voice",
            "is_cloned": True, "state_path": state_path, "tags": ["cloned"],
        }
        with self._lock:
            config = self._read_config()
            cloned = [v for v in config.get("cloned_voices", []) if v.get("id") != voice_id]
            cloned.append(voice)
            config["cloned_voices"] = cloned
            self._write_config(config)
        return voice

    def remove_cloned_voice(self, voice_id):
        with self._lock:
            config = self._read_config()
            cloned = config.get("cloned_voices", [])
            match = next((v for v in cloned if v.get("id") == voice_id), None)
            if match is None:
                return False
            config["cloned_voices"] = [v for v in cloned if v.get("id") != voice_id]
            self._write_config(config)
            for suffix in (".safetensors", "_reference.wav"):
                try:
                    (CLONED_DIR / f"{voice_id}{suffix}").unlink(missing_ok=True)
                except OSError:
                    pass
            return True
