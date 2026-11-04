#!/usr/bin/env python3
"""Regenerate README layer graphics from config/corneish_zen.keymap (stdlib only)."""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'config/corneish_zen.keymap'
OUTPUT = ROOT / 'docs/keymap'
LAYERS = [('main_layer', 'main', 'Main', '0', 'Hold the middle left thumb for Sym+Num · Tap outer right thumb for Steno'),
          ('sym_num_layer', 'sym-num', 'Sym+Num', '1', 'Release the middle left thumb to return to Main'),
          ('steno_layer', 'steno', 'Steno · Plover HID', '2', 'Tap the thumb left of A to return to Main · The key left of lower S is disabled')]
NAMES = {'TAB':'Tab', 'ESC':'Esc', 'LCTRL':'Ctrl', 'LSHIFT':'Shift', 'LCMD':'⌘',
         'SPACE':'Space', 'BSPC':'Bksp', 'RET':'Enter', 'DEL':'Del →', 'LBKT':'[', 'RBKT':']',
         'LBRC':'{', 'RBRC':'}', 'SQT':"'", 'DQT':'"', 'LPAR':'(', 'RPAR':')',
         'MINUS':'−', 'UNDER':'_', 'AMPS':'&', 'STAR':'*', 'EXCL':'!', 'HASH':'#',
         'TILDE':'~', 'GRAVE':'`', 'EQUAL':'=', 'AT':'@', 'DLLR':'$', 'CARET':'^',
         'BSLH':'\\', 'FSLH':'/', 'COMMA':',', 'DOT':'.', 'SEMI':';', 'UP':'↑',
         'DOWN':'↓', 'LEFT':'←', 'RIGHT':'→', 'KP_PLUS':'KP +', 'MAIN':'Main', 'STENO':'Steno'}
PLOVER = {'SL':'S1−', 'SL2':'S2−', 'TL':'T−', 'KL':'K−', 'PL':'P−', 'WL':'W−', 'HL':'H−', 'RL':'R−',
          'A':'A', 'O':'O', 'E':'E', 'U':'U', 'ST':'*1', 'ST2':'*2', 'ST3':'*3', 'ST4':'*4',
          'FR':'−F', 'RR':'−R', 'PR':'−P', 'BR':'−B', 'LR':'−L', 'GR':'−G', 'TR':'−T', 'SR':'−S',
          'DR':'−D', 'ZR':'−Z', 'NM':'#1', 'NM2':'#2', 'NM3':'#3', 'NM4':'#4', 'NM5':'#5',
          'NM6':'#6', 'NM7':'#7', 'NM8':'#8', 'NM9':'#9', 'NMA':'#A', 'NMB':'#B', 'NMC':'#C'}

def key_name(key):
    if key == 'LG(LS(N4))': return '⌘⇧4'
    if key == 'LG(LA(ESC))': return '⌘⌥Esc'
    if key == 'LS(LEFT)': return '⇧←'
    if key.startswith('LG('): return '⌘' + key_name(key[3:-1])
    if re.fullmatch(r'N[0-9]', key): return key[1:]
    return NAMES.get(key, key)

def parse_layers():
    source = re.sub(r'//[^\n]*', '', SOURCE.read_text())
    layers = dict(re.findall(r'(\w+_layer)\s*\{.*?bindings\s*=\s*<(.*?)>;', source, re.S))
    layers = {name: [re.sub(r'\s+', ' ', b).strip() for b in re.findall(r'&[^&]+', text)]
              for name, text in layers.items()}
    for name, bindings in layers.items():
        if len(bindings) != 42: raise ValueError(f'{name}: expected 42 bindings, got {len(bindings)}')
    return layers

def label(binding, index, layers):
    parts = binding.split()
    kind = parts[0]
    if kind == '&trans': return label(layers['main_layer'][index], index, layers)
    if kind == '&ht': return key_name(parts[2]), key_name(parts[1]), 'dual'
    if kind == '&kp': return key_name(parts[1]), '', 'plain'
    if kind == '&plv': return PLOVER[parts[1][4:]], '', 'steno'
    if kind == '&to': return key_name(parts[1]), 'tap to switch', 'layer'
    if kind == '&mo': return 'Layer 1', 'hold', 'layer'
    if kind == '&sk': return 'Shift', 'sticky', 'plain'
    if kind == '&bt':
        return ('Clear', 'BT bond', 'plain') if parts[1] == 'BT_CLR' else ('BT ' + str(int(parts[2])+1), 'profile', 'plain')
    if kind == '&none': return '—', '', 'disabled'
    raise ValueError(f'Unknown binding: {binding}')

def text(x, y, content, css=''):
    return f'<text x="{x}" y="{y}" class="{css}">{html.escape(content)}</text>'

def render(layer_key, filename, title, number, caption, layers):
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="540" viewBox="0 0 1120 540" role="img" aria-labelledby="title desc">',
           f'<title id="title">Zen V2 — {html.escape(title)} layer {number}</title>',
           '<desc id="desc">42-key split layout. For dual-action keys, tap is above the divider and hold is below. Thumb keys appear at the bottom. Disabled keys have a dash.</desc>',
           '''<style>
.bg{fill:#f6f7fb}.key{fill:#fff;stroke:#d5d9e4;stroke-width:1.2}.line{stroke:#e5e7ef;stroke-width:1}
text{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#202637;font-size:18px;text-anchor:middle;dominant-baseline:middle}
.title{font-size:27px;font-weight:600;text-anchor:start}.subtitle{font-size:14px;fill:#596477;text-anchor:start}.side{font-size:12px;letter-spacing:2px;fill:#596477;text-anchor:start}
.hold{fill:#5f4aad;font-size:16px}.meta{fill:#596477;font-size:12px}.disabled .key{fill:#eceef4;stroke:#e0e3eb}.disabled text{fill:#8e98aa}
.layer .key{fill:#ebe5fb;stroke:#c5b4eb}.steno .key{fill:#edf5fb;stroke:#c4d9ea}.footer{font-size:14px;fill:#596477;text-anchor:start}
@media(prefers-color-scheme:dark){.bg{fill:#151922}.key{fill:#222936;stroke:#414b5e}.line{stroke:#414b5e}text{fill:#ecf0f7}.subtitle,.side,.meta,.footer{fill:#b3bdcd}.hold{fill:#c2aaff}.disabled .key{fill:#1b202b;stroke:#303746}.disabled text{fill:#77849a}.layer .key{fill:#35294e;stroke:#71578e}.steno .key{fill:#203448;stroke:#3f617c}}
</style>''', '<rect class="bg" width="1120" height="540" rx="16"/>',
           text(32, 37, title + '  /  ' + number, 'title'),
           text(32, 69, 'CORNE-ISH ZEN V2     ·     VOYAGER LAYOUT FOR MAC', 'subtitle'),
           text(735, 37, 'Dual-action keys: tap above · hold below', 'subtitle'),
           text(735, 64, '⌘ Command     ⌥ Option     ⇧ Shift', 'subtitle')]
    for side in range(2):
        origin = 32 if side == 0 else 611
        svg.append(text(origin, 105, 'LEFT HALF' if side == 0 else 'RIGHT HALF', 'side'))
        stagger = [18,18,8,0,8,18] if side == 0 else [18,8,0,8,18,18]
        for local in range(21):
            if local < 18:
                row, col = divmod(local,6);idx=row*12+side*6+col
                x=origin+col*81;y=128+row*88+stagger[col]
            else:
                thumb=local-18;idx=36+side*3+thumb
                x=origin+((3+thumb) if side==0 else thumb)*81;y=412
            tap,hold,kind=label(layers[layer_key][idx],idx,layers)
            svg.append(f'<g class="{kind}" data-key-index="{idx}"><title>{html.escape(tap + (" / " + hold if hold else ""))}</title><rect class="key" x="{x}" y="{y}" width="72" height="76" rx="8"/>')
            if hold:
                svg.append(text(x+36,y+25,tap))
                if kind=='dual':svg.append(f'<line class="line" x1="{x+12}" x2="{x+60}" y1="{y+40}" y2="{y+40}"/>')
                svg.append(text(x+36,y+57,hold,'hold' if kind=='dual' else 'meta'))
            else: svg.append(text(x+36,y+38,tap))
            svg.append('</g>')
    svg += [text(32,516,caption,'footer'),'</svg>']
    target=OUTPUT/f'{filename}.svg';target.write_text('\n'.join(svg)+'\n');print(target.relative_to(ROOT))

if __name__ == '__main__':
    OUTPUT.mkdir(parents=True,exist_ok=True)
    layers=parse_layers()
    for args in LAYERS:render(*args,layers)
