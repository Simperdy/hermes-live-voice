"""Integration guards for localized voice labels without changing wire IDs."""
import json
import subprocess
from pathlib import Path

import pytest

SOURCE = Path(__file__).resolve().parents[1] / 'desktop/plugin.js'


@pytest.mark.parametrize('locale, warning, hint', [
    ('de-DE', 'Experimentell — nicht verifiziert', 'regionale Ausrichtung'),
    ('es-ES', 'Experimental — sin verificar', 'orientación regional'),
    ('fr-FR', 'Experimental — not verified', 'regional focus'),
])
def test_localized_voice_labels_and_language_hint(locale, warning, hint):
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
    assert data['label'] == 'Miko · Deutsch (' + warning + ')'
    assert data['id'] == 'miko'
    assert hint in data['hint']
