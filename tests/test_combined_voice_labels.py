"""Integration guards for localized voice labels without changing wire IDs."""
import json
import subprocess
from pathlib import Path

import pytest

SOURCE = Path(__file__).resolve().parents[1] / 'desktop/plugin.js'


@pytest.mark.parametrize('locale, hint', [
    ('de-DE', 'regionale Ausrichtung'),
    ('es-ES', 'orientación regional'),
    ('fr-FR', 'regional focus'),
])
def test_voice_labels_keep_language_without_per_option_warning(locale, hint):
    source = SOURCE.read_text()
    # Evaluate the real declarations, without React, networking or microphone access.
    start = source.index('const VOICES = ')
    end = source.index('\n// A POST ', start)
    script = 'const navigator = {language: ' + json.dumps(locale) + '};\n'
    script += source[start:end]
    script += '\nconsole.log(JSON.stringify({label: voiceOptionLabel("miko"), id: effVoiceFor("codex", "miko"), hint: voiceLanguageHint()}));'
    result = subprocess.run(['node', '-e', script], text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data['label'] == 'Miko · Deutsch'
    assert data['id'] == 'miko'
    assert hint in data['hint']


@pytest.mark.parametrize('locale, expected', [('de-DE', 'Woche'), ('en-US', 'Weekly'), ('es-ES', 'Semanal')])
def test_backend_weekly_window_label_is_localized(locale, expected):
    source = SOURCE.read_text()
    start = source.index('const VOICES = ')
    end = source.index('\n// A POST ', start)
    script = 'const navigator = {language: ' + json.dumps(locale) + '};\n' + source[start:end]
    script += '\nconsole.log(JSON.stringify([usageWindowLabel("semanal"), usageWindowLabel("5h"), usageWindowLabel("custom")]));'
    result = subprocess.run(['node', '-e', script], text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == [expected, '5h', 'custom']
