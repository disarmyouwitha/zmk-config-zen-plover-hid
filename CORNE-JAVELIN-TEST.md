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

The JSON compiles to a 142-byte JSC4 fixture with ARM linker relocations. The module pins the June 2026 engine ABI; updating its engine independently can break the binary format. The dictionary compiler's stroke masks, inclusive hash-rank base and relocatable embedding were corrected for this test. Host checks verify all four lookups, the phrase, an absent entry, and a larger collision/multi-stroke fixture. These host checks are supplemented by the successful physical test recorded below.

## Firmware

- Left / central: `corne_javelin_tiny_left`.
- Right / peripheral: `corne_javelin_tiny_right`.
- Target: `nice_nano//zmk` (nice!nano v2 default revision in the pinned ZMK).
- The central links the Javelin engine and tiny dictionary. The peripheral forwards central-locality bindings.
- Full Plover/Lapwing downloads are disabled. No external flash mapping is used.
- Writable/persistent user dictionary is disabled for this read-only test.
- Existing Zen-specific files are retained as reference and are not the targets in this branch's build matrix.

After a successful build, flash the corresponding UF2 to each half's bootloader volume. Do not flash these to an original Corne-ish Zen: its board target and pinout differ. Keep the currently working Corne UF2 files for rollback. Settings reset is not part of the build or flash procedure.

## Verified on-device result — November 4, 2026

**PASS:** user confirmed `TP` types `if`, then confirmed the exact six-stroke phrase **if the cat is the cat** on the physical Corne. Normal typing remains available on the other layers. Both nice!nano v2 halves use ZMK; no external flash or host Plover was used for translation.

- Successful paired CI: https://github.com/disarmyouwitha/zmk-config-zen-plover-hid/actions/runs/41970438534
- Tested configuration source: `d653188` (documentation updates after this do not change the firmware).
- Tested Javelin module: `995fa19` on `disarmyouwitha/zmk-javelin-steno`.
- Pinned engine: `22726675b2dcf3b8b6ba1e20898f25e324b2260a`.
- Corrected diagnostic left UF2: 465,664 payload bytes, with the 142-byte dictionary at address `0x75f00`.
- Actual device log passed all four native dictionary lookups and showed emitted i/f HID events; the user confirmed visible output and the full phrase.
- Raw USB logs are kept locally rather than committed because they also contain normal typing events.

The installed left firmware is a diagnostic build with USB logging enabled. Right firmware did not require reflashing for the dictionary-pointer fix. No settings reset was performed.

## Resume when external flash arrives

The four-entry internal-flash proof is complete. Full Plover/Lapwing dictionaries, external QSPI wiring/mapping, dictionary programming, persistent user dictionaries, and long-term reliability are not implemented or validated by this test. Before wiring the 16 MB flash, select available nice!nano GPIOs, verify the exact flash component and supply voltage, and implement/test the Zephyr QSPI mapped-read/partition path. Preserve this working tiny-dictionary build as a baseline. Remove diagnostic logging after hardware debugging is complete.

## First on-device test: failure and corrected table pointer

The initial firmware typed normally but hung after the first steno chord. Investigation found that the compiler pointed the stroke-definition array one entry before its first entry, while the native engine's CreateStrokeCache copies the first entry and subtracts one from its RAM pointer itself. This double adjustment made the engine interpret dictionary-name bytes as pointers. The first Python/UF2 checks shared that incorrect assumption, so their success did not validate the constructor path. Both checks are now corrected, with a malformed-pointer regression.

The diagnostic central build enables USB logging, uses an 8 KB workqueue stack, and performs all four dictionary lookups through the native engine before enabling translation. Its log records each init phase, key event, and emitted HID event. USB serial logs and the physical phrase test subsequently confirmed the fix, as recorded above. The original peripheral can remain installed because the split key bindings/protocol are unchanged.
