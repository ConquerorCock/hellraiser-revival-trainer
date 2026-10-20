# Security Policy

## Scope

`hellraiser-revival-trainer` is an external memory trainer. It requires
`PROCESS_ALL_ACCESS` on `HellraiserRevival.exe` and, for hotkey capture,
`RegisterHotKey` on the interactive desktop. It does **not** install drivers,
hook the kernel, or persist beyond the running Python process.

## Reporting a vulnerability

If you find an issue outside the known limitations below, open a private
security advisory on GitHub with:

- Affected module (`ingest`, `processors`, `drivers`, `utils`)
- Reproduction steps
- Windows build + Python version

## Known limitations (not vulnerabilities)

- Trainer requires an elevated shell to write to a protected process.
- Anti-cheat EAC / BattlEye are **not** bypassed by design; the trainer is
  intended for offline / single-player use only.
- Overlay uses tkinter and will not render over exclusive fullscreen; use
  borderless windowed.
- Offsets break on every game update. That is expected — see CONTRIBUTING.

## Disclosure timeline

We aim to acknowledge reports within 72 hours and ship a patch within 14 days
for confirmed issues affecting the trainer's own attack surface.