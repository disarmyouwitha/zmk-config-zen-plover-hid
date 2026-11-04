# Zen V2 — Voyager layout for Mac

Three layers, 42 keys per layer. In MAIN, `tap / hold` shows the two actions.
Hold actions use a 200 ms tapping term. MAIN ⇢ STENO is the bottom-right key;
STENO ⇢ MAIN is the bottom-left key. Hold the middle left thumb for SYM+NUM.

## MAIN

```text
 LEFT HALF                                                       RIGHT HALF
 Tab/Esc  Q/[    W/]    E/{    R/}    T/'           Y/-   U/&   I/*    O/⌘F   P/⌘⇧4    Delete
 Ctrl     A/⌘A   S/⌘S   D/(    F/)    G/"           H/_   J/!   K/#    L/~    ;/Enter  Enter
 Shift    Z/⌘Z   X/⌘X   C/⌘C   V/⌘V   B/`           N/=   M/@   ,/$    ./^    / / \    STENO
                ⌘     Hold SYM+NUM  Backspace       Space  Space  Sticky Shift
```

Ctrl+A/S/Z/X/C/V/F editing shortcuts become Command+A/S/Z/X/C/V/F.
P's hold becomes Command+Shift+4. Semicolon's hold is ordinary Enter.
Control, Shift, symbols and Shift+Left retain their meanings.

## SYM+NUM

```text
 LEFT HALF                                                       RIGHT HALF
 ⌘⌥Esc   BT1    BT2    Up     BT clear  —          KP+    7    8    9    Backspace  Backspace
 —        —     Left   Down   Right     —           -     4    5    6    Enter      Enter
 ⇧Left    —      —     Space    —       —           =     1    2    3    .           —
                  ⌘   (held)  Backspace            —     0    Sticky Shift
```

BT1/BT2 select ZMK profiles 0/1. BT clear removes the selected profile's host
bond; forget it on the host too before re-pairing. These replace unused Voyager
LED positions Q/W/R; all other LED controls are omitted. The extra Zen thumb
keys retain Command and sticky Shift. Plus sends keypad Plus; digits use the
ordinary number row, as in the reference's unlabeled digit keys.

## STENO — Plover HID

```text
 LEFT HALF                                                       RIGHT HALF
 #C     #1     #2     #3     #4     #5             #6     #7     #8     #9     #A     #B
 —      S1-    T-     P-     H-     *1             *3     -F     -P     -L     -T     -D
 MAIN   S2-    K-     W-     R-     *2             *4     -R     -B     -G     -S     -Z
                  —    A     O                     E      U      —
```

All 38 steno keys have distinct Plover HID indices. This matches the reference's
consonant/star positions and all twelve number-bar keys. The extra outer Zen
thumb keys are disabled in STENO. All steno actions are immediate plain presses;
none uses hold-tap or ordinary keyboard letters.
