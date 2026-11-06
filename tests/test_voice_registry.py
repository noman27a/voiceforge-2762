"""Tests for the VoiceForge 2762 voice registry."""
import sys
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "engine"))

from voice_registry import VoiceRegistry, BUILTIN_VOICES


@pytest.fixture()
def registry(tmp_path, monkeypatch):
    """Registry pointed at a temp data dir so tests never touch real data."""
    import voice_registry as vr

    monkeypatch.setattr(vr, "DATA_DIR", tmp_path / "data")
    monkeypatch.setattr(vr, "CONFIG_FILE", tmp_path / "data" / "config.json")
    monkeypatch.setattr(vr, "CLONED_DIR", tmp_path / "data" / "cloned")
    return VoiceRegistry()


def test_builtin_voices_present(registry):
    voices = registry.get_all_voices()
    assert len(voices) == len(BUILTIN_VOICES)
    ids = {v["id"] for v in voices}
    assert "alba" in ids and "javert" in ids


def test_gender_filter(registry):
    female = registry.get_all_voices(gender="female")
    assert female and all(v["gender"] == "female" for v in female)
    male = registry.get_all_voices(gender="male")
    assert male and all(v["gender"] == "male" for v in male)


def test_search(registry):
    found = registry.get_all_voices(search="deep")
    assert any(v["id"] == "javert" for v in found)


def test_get_voice_missing(registry):
    assert registry.get_voice("no_such_voice") is None


def test_add_and_remove_cloned_voice(registry):
    voice = registry.add_cloned_voice("cloned_abc123", "My Voice", "/tmp/x.safetensors")
    assert voice["is_cloned"] is True
    assert registry.get_voice("cloned_abc123") is not None
    assert registry.remove_cloned_voice("cloned_abc123") is True
    assert registry.get_voice("cloned_abc123") is None
    assert registry.remove_cloned_voice("cloned_abc123") is False


def test_verification_flag(registry):
    assert registry.is_verified() is False
    registry.set_verified(True)
    assert registry.is_verified() is True
