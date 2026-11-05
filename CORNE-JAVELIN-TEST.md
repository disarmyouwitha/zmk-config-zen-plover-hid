# Corne / nice!nano v2 onboard Javelin test

This branch targets a standard 42-key Corne with nice!nano v2 controllers, no external flash and no display support in this first test. Main and Sym+Num bindings are copied from the user's Zen Plover HID keymap. Only the steno behavior changes to onboard Javelin translation.

## Dictionary and test

Four ordinary Plover JSON entries:

| Stroke | Translation |
|---|---|
| `TP` | `if` |
| `-T` | `the` |
| `KAT` | `cat` |
| `S` | `is` |

Enter Steno by tapping the outer right thumb from Main. In an empty text editor, release each chord fully before the next:

`TP` → `-T` → `KAT` → `S` → `-T` → `KAT`

Expected translated text: `if the cat is the cat`. No host Plover process is required for this path. The thumb left of A returns to Main. Star invokes Javelin undo. Unknown strokes are not included in this small dictionary.

The JSON compiles to a 142-byte JSC4 fixture with ARM linker relocations. The module pins the June 2026 engine ABI; updating its engine independently can break the binary format. The dictionary compiler's stroke masks, inclusive hash-rank base and relocatable embedding were corrected for this test. Host checks verify all four lookups, the phrase, an absent entry, and a larger collision/multi-stroke fixture. This is not hardware proof of translation.

## Firmware

- Left / central: `corne_javelin_tiny_left`.
- Right / peripheral: `corne_javelin_tiny_right`.
- Target: `nice_nano//zmk` (nice!nano v2 default revision in the pinned ZMK).
- The central links the Javelin engine and tiny dictionary. The peripheral forwards central-locality bindings.
- Full Plover/Lapwing downloads are disabled. No external flash mapping is used.
- Writable/persistent user dictionary is disabled for this read-only test.
- Existing Zen-specific files are retained as reference and are not the targets in this branch's build matrix.

After a successful build, flash the corresponding UF2 to each half's bootloader volume. Do not flash these to an original Corne-ish Zen: its board target and pinout differ. Keep the currently working Corne UF2 files for rollback. Settings reset is not part of the build or flash procedure.

## Status

See GitHub Actions for actual compilation status. Do not treat this document as confirmation of a successful build or successful on-device translation; those results are reported separately.
