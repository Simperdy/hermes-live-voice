# Experimental Codex Live voices: Miko and Sonna

This branch makes **Miko** (`miko`) and **Sonna** (`sonna`) manually selectable for the Codex Live engine. They are marked “experimental — not verified” in the voice picker. Existing voices and the `cove` fallback remain unchanged. The plugin does not change the Codex model slug or realtime protocol version.

## Evidence and limits

- OpenAI's [ChatGPT Voice help page](https://help.openai.com/en/articles/20001274-chatgpt-voice) lists Miko and Sonna as German Live voices and says availability can vary by account/region.
- The installed Codex CLI 0.163.0 app-server schema generated locally with `codex app-server generate-ts --experimental` contains the IDs `miko` and `sonna` in `RealtimeVoice` and types `thread/realtime/start`'s optional `voice` field as that enum.
- The [current Codex app-server RealtimeVoice schema](https://github.com/openai/codex/blob/main/codex-rs/app-server-protocol/schema/typescript/RealtimeVoice.ts) also contains both IDs.
- These facts validate the names and request field against the schema, **not** end-to-end support of either voice by every Codex/app-server or GPT-Live rollout. No authenticated session was started here and no audio was generated.

## Manual Mac test

1. Use a separate reviewed copy of this branch in the Hermes Desktop environment that runs the Codex app-server; do not replace the stable install until you intentionally choose to test it.
2. Open Live Voice settings, keep the Codex engine selected, and choose `miko (experimental — not verified)` or `sonna (experimental — not verified)`.
3. Start a session and speak German. Confirm the requested voice actually sounds distinct and the transcript remains responsive; switching the language alone does not validate the voice identity.
4. If Codex rejects the ID or the session fails, keep the displayed error and Codex version for diagnosis. The plugin surfaces startup errors rather than retrying with `cove`.
5. Re-select any stable voice to return to the established path. Do not publish or deploy based only on schema acceptance; record whether both voices work on the Mac/tower setup first.
