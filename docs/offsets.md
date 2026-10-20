# Hellraiser: Revival — offset reference

Offsets are relative to the module base of `HellraiserRevival.exe`
(`TrainerConfig.module_base`).

| Field          | Offset  | Type  | Notes                          |
|----------------|---------|-------|--------------------------------|
| health         | 0x2A10  | int32 | player HP, 0 = death           |
| pins           | 0x2A14  | int32 | puzzle pins remaining          |
| cenobite_hp    | 0x4C80  | int32 | active cenobite encounter      |
| puzzle_state   | 0x51A8  | float | Lemarchand box rotation        |

## Build history

- **1.4.2 (2026-01)** — current, signatures in `processors/signatures.json`.
- **1.3.9 (2025-12)** — `cenobite_hp` moved from `0x4C60`.
- **1.3.0 (2025-11)** — initial public trainer support.