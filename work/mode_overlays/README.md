# Mode overlays (base-5.1)

Authoring fragments for stamped system prompts.

```text
messages[0].content = CORE.md + "\n\n" + <mode>.md
```

`{{mode}}` in CORE is replaced with the mode name.

## Assemble

From repo root:

```bash
# Write overlays into the base-5.1 SNAPSHOT folder only (not base-5/)
python3 scripts/assemble_mode_prompts.py --base 5.1
python3 scripts/export_base_text.py --from v2/base/base-5.1/min --base 5.1 --out v2/base/base-5.1 --no-set-base-id
python3 scripts/new_base.py --refresh-manifest --base 5.1
python3 scripts/verify_base_pack.py --base 5.1
python3 scripts/diff_modes.py --base 5.1 --fail-if-clone
# Diff: Inspector base-5 vs base-5.1 (or diff -ru v2/base/base-5 v2/base/base-5.1)
```

## Files

| File | Role |
| --- | --- |
| CORE.md | Shared discipline + Layer A |
| analytics.md … custom.md | MODE_OVERLAY per mode |
| BASELINE_REPORT.md | Optional clone baseline |

See [docs/MODE.md](../../docs/MODE.md) · [work/RECREATE_MODE.md](../RECREATE_MODE.md) · ROADMAP **base-5.1**.
