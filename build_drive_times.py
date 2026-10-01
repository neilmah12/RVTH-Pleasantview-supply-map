# =============================================================================
# Build script: River Valley Townhomes, straight-line vs drive distance.
# Writes public/drive-times.html, a single-purpose page designed to be
# screenshotted for marketing material. Separate from build_site.py; it does
# not touch the main supply map.
#
# Inputs:
#   data/river_valley_drive_times.json   (OpenRouteService driving routes,
#                                         produced in Colab; see README)
#   PROJECTS in build_site.py            (comp and subject coordinates)
# =============================================================================
import ast, json, os, re

with open("build_site.py", encoding="utf-8") as f:
    _src = f.read()
PROJECTS = ast.literal_eval(re.search(r"PROJECTS = (\[.*?\n\])", _src, re.S).group(1))
by_id = {p["id"]: p for p in PROJECTS}
subject = next(p for p in PROJECTS if p["name"] == "River Valley Townhomes")

with open("data/river_valley_drive_times.json", encoding="utf-8") as f:
    routes = json.load(f)

comps = []
for r in routes:
    p = by_id[r["id"]]
    assert p["name"] == r["name"], (p["name"], r["name"])
    comps.append({
        "id": r["id"], "name": r["name"], "lat": p["lat"], "lng": p["lng"],
        "straight_km": r["straight_km"], "drive_km": r["drive_km"],
        "detour": r["detour"], "route": r["route"],
    })
# Biggest detour first: the pin numbers on the map match the chart rows.
comps.sort(key=lambda c: -c["detour"])

DATA = {"subject": {"name": subject["name"], "lat": subject["lat"], "lng": subject["lng"]},
        "comps": comps}

_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>River Valley Townhomes: Straight-Line vs Drive Distance</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#f7f6f3;--surface:#fff;--border:#e8e5df;--border-light:#f0ede8;
  --text-primary:#1a1917;--text-secondary:#6b6760;--text-muted:#a09d99;
  --accent:#c8572a;--navy:#2a3f5f;
}
html,body{height:100%;font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text-primary)}
body{display:flex;overflow:hidden}
#map{flex:1;min-width:0;height:100%}
#panel{width:390px;flex-shrink:0;height:100%;background:var(--surface);border-left:1px solid var(--border);display:flex;flex-direction:column;padding:26px 24px 16px}
.eyebrow{font-size:10px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--navy)}
h1{font-size:19px;font-weight:600;line-height:1.25;margin-top:6px}
#headline{margin-top:18px;padding:14px 16px;border-radius:8px;background:#faf3ef;border:1px solid #f1ddd3}
#headline .big{font-size:34px;font-weight:600;color:var(--accent);line-height:1;font-variant-numeric:tabular-nums}
#headline .txt{font-size:12.5px;color:var(--text-secondary);margin-top:6px;line-height:1.4}
#headline .txt b{color:var(--text-primary);font-weight:600}
#legend{display:flex;gap:14px;margin-top:18px;font-size:10.5px;color:var(--text-secondary);align-items:center;flex-wrap:wrap}
#legend span{display:flex;align-items:center;gap:5px}
#chart{margin-top:6px;flex:1;min-height:0}
#chart svg{width:100%;height:auto;display:block}
.row{cursor:pointer}
.row .hit{fill:transparent}
.row:hover .hit,.row.on .hit{fill:rgba(200,87,42,.07)}
#foot{font-size:9.5px;color:var(--text-muted);line-height:1.45;border-top:1px solid var(--border-light);padding-top:9px}
.pin{width:22px;height:22px;border-radius:50%;background:var(--accent);border:2px solid #fff;color:#fff;font:600 11px 'DM Sans',sans-serif;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,.25)}
.pin.on{background:#1a1917;transform:scale(1.2)}
.spin{width:34px;height:34px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:var(--navy);border:3px solid #fff;box-shadow:0 3px 8px rgba(0,0,0,.3)}
.ring-label{font:500 10px 'DM Mono',monospace;color:#6b6760;background:rgba(255,255,255,.85);padding:1px 5px;border-radius:8px;white-space:nowrap}
.subj-tip{font:600 12px 'DM Sans',sans-serif;color:#fff;background:var(--navy);border:none;border-radius:6px;padding:4px 9px;box-shadow:0 2px 6px rgba(0,0,0,.25)}
.subj-tip:before{display:none}
body.clean .leaflet-control-zoom{display:none}
@media (max-width:900px){body{flex-direction:column;overflow:auto}#map{height:60vh;flex:none}#panel{width:100%;height:auto;border-left:none}}
</style>
</head>
<body>
<div id="map"></div>
<div id="panel">
  <div class="eyebrow">Existing townhome supply</div>
  <h1>Nearby comps are farther than they look</h1>
  <div id="headline"><div class="big" id="h-big"></div><div class="txt" id="h-txt"></div></div>
  <div id="legend">
    <span><svg width="22" height="8"><line x1="0" y1="4" x2="22" y2="4" stroke="#2a3f5f" stroke-width="1.6" stroke-dasharray="4 4"/></svg>Straight line</span>
    <span><svg width="22" height="8"><line x1="0" y1="4" x2="22" y2="4" stroke="#c8572a" stroke-width="2.6"/></svg>Driving route</span>
  </div>
  <div id="chart"></div>
  <div id="foot">Distances in km from River Valley Townhomes (4210 102 Ave NW). Drive distance is the shortest driving route. Routing: openrouteservice.org, &copy; OpenStreetMap contributors.</div>
</div>
<script>
const DATA = __DATA__;
const S = DATA.subject, C = DATA.comps;

if (/[?&]clean/.test(location.search)) document.body.classList.add('clean');

// ---------- map ----------
const map = L.map('map', {zoomControl: false, attributionControl: false, zoomSnap: 0.1});
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {maxZoom: 19}).addTo(map);
L.control.zoom({position: 'topleft'}).addTo(map);
L.control.attribution({position: 'bottomleft', prefix: false}).addAttribution('&copy; Esri &middot; OpenStreetMap contributors').addTo(map);

// straight-line reference rings
[1, 3, 5].forEach(function(km) {
  L.circle([S.lat, S.lng], {radius: km * 1000, color: '#2a3f5f', weight: 1, opacity: .35, fillOpacity: 0, dashArray: '2 6', interactive: false}).addTo(map);
  var north = L.latLng(S.lat, S.lng).toBounds(km * 2000).getNorth();
  L.marker([north, S.lng], {interactive: false, icon: L.divIcon({className: '', html: '<div class="ring-label">' + km + ' km</div>', iconSize: [0, 0], iconAnchor: [14, 8]})}).addTo(map);
});

const layers = {};
C.forEach(function(c, i) {
  var route = L.polyline(c.route.map(function(pt) { return [pt[1], pt[0]]; }), {color: '#c8572a', weight: 3, opacity: .4, lineJoin: 'round'}).addTo(map);
  var line = L.polyline([[S.lat, S.lng], [c.lat, c.lng]], {color: '#2a3f5f', weight: 1.6, opacity: .75, dashArray: '4 6'}).addTo(map);
  var pin = L.marker([c.lat, c.lng], {zIndexOffset: 500, icon: L.divIcon({className: '', html: '<div class="pin">' + (i + 1) + '</div>', iconSize: [22, 22], iconAnchor: [11, 11]})}).addTo(map);
  layers[i] = {route: route, line: line, pin: pin};
  pin.on('click', function() { focusRow(i); });
});

L.marker([S.lat, S.lng], {zIndexOffset: 1000, icon: L.divIcon({className: '', html: '<div class="spin"></div>', iconSize: [34, 34], iconAnchor: [17, 34]})})
  .bindTooltip('River Valley Townhomes', {permanent: true, direction: 'right', offset: [14, -16], className: 'subj-tip'}).addTo(map);

var all = [[S.lat, S.lng]];
var ring = L.latLng(S.lat, S.lng).toBounds(10000);  // keep the 5 km ring fully in frame
all.push([ring.getNorth(), ring.getEast()], [ring.getSouth(), ring.getWest()]);
C.forEach(function(c) { c.route.forEach(function(pt) { all.push([pt[1], pt[0]]); }); });
map.fitBounds(L.latLngBounds(all), {paddingTopLeft: [30, 30], paddingBottomRight: [30, 30]});

// ---------- headline ----------
var sumS = 0, sumD = 0;
C.forEach(function(c) { sumS += c.straight_km; sumD += c.drive_km; });
document.getElementById('h-big').textContent = (sumD / sumS).toFixed(1) + 'x';
document.getElementById('h-txt').innerHTML = 'Across the <b>' + C.length + ' comps</b> within 5 km straight-line, the drive averages <b>' + (sumD / sumS).toFixed(1) + 'x</b> the straight-line distance.';

// ---------- dumbbell chart ----------
var W = 350, ROW = 38, TOP = 24, X0 = 166, X1 = 290, MAX = 12;
function x(km) { return X0 + (km / MAX) * (X1 - X0); }
var H = TOP + C.length * ROW + 6;
var svg = '<svg viewBox="0 0 ' + W + ' ' + H + '" xmlns="http://www.w3.org/2000/svg" font-family="DM Sans,sans-serif">';
[0, 4, 8, 12].forEach(function(t) {
  svg += '<line x1="' + x(t) + '" y1="' + (TOP - 6) + '" x2="' + x(t) + '" y2="' + (H - 4) + '" stroke="#ece9e3" stroke-width="1"/>';
  svg += '<text x="' + x(t) + '" y="' + (TOP - 10) + '" font-size="9" fill="#a09d99" text-anchor="middle">' + t + (t === 12 ? ' km' : '') + '</text>';
});
C.forEach(function(c, i) {
  var y = TOP + i * ROW + ROW / 2;
  var name = c.name.replace(' Townhomes', '').replace(/ Nw$/, '');
  svg += '<g class="row" data-i="' + i + '">';
  svg += '<rect class="hit" x="0" y="' + (y - ROW / 2) + '" width="' + W + '" height="' + ROW + '" rx="4"/>';
  svg += '<circle cx="14" cy="' + y + '" r="9" fill="#c8572a"/><text x="14" y="' + (y + 3.6) + '" font-size="10.5" font-weight="600" fill="#fff" text-anchor="middle">' + (i + 1) + '</text>';
  svg += '<text x="29" y="' + (y + 3.8) + '" font-size="11" fill="#1a1917">' + name + '</text>';
  svg += '<line x1="' + x(c.straight_km) + '" y1="' + y + '" x2="' + x(c.drive_km) + '" y2="' + y + '" stroke="#e0c4b6" stroke-width="3" stroke-linecap="round"/>';
  svg += '<circle cx="' + x(c.straight_km) + '" cy="' + y + '" r="4.2" fill="#fff" stroke="#2a3f5f" stroke-width="1.8"/>';
  svg += '<circle cx="' + x(c.drive_km) + '" cy="' + y + '" r="4.6" fill="#c8572a"/>';
  svg += '<text x="' + (x(c.straight_km) - 8) + '" y="' + (y + 3.4) + '" font-size="10.5" fill="#2a3f5f" text-anchor="end" font-family="DM Mono,monospace">' + c.straight_km.toFixed(1) + '</text>';
  svg += '<text x="' + (x(c.drive_km) + 8) + '" y="' + (y + 3.4) + '" font-size="10.5" fill="#c8572a" font-weight="500" font-family="DM Mono,monospace">' + c.drive_km.toFixed(1) + '</text>';
  svg += '<text x="' + (W - 2) + '" y="' + (y + 3.8) + '" font-size="12.5" font-weight="600" fill="#1a1917" text-anchor="end">' + c.detour.toFixed(1) + 'x</text>';
  svg += '</g>';
});
svg += '</svg>';
document.getElementById('chart').innerHTML = svg;

// ---------- interaction: click a row (or pin) to highlight that route ----------
var active = null;
function focusRow(i) {
  if (active !== null) {
    layers[active].route.setStyle({opacity: .4, weight: 3});
    layers[active].line.setStyle({opacity: .75, weight: 1.6});
    layers[active].pin.getElement().firstChild.classList.remove('on');
    document.querySelector('.row[data-i="' + active + '"]').classList.remove('on');
  }
  if (active === i) { active = null; return; }
  active = i;
  layers[i].route.setStyle({opacity: 1, weight: 5}).bringToFront();
  layers[i].line.setStyle({opacity: 1, weight: 2.2}).bringToFront();
  layers[i].pin.getElement().firstChild.classList.add('on');
  document.querySelector('.row[data-i="' + i + '"]').classList.add('on');
}
document.querySelectorAll('.row').forEach(function(el) {
  el.addEventListener('click', function() { focusRow(+el.getAttribute('data-i')); });
});
</script>
</body>
</html>"""

os.makedirs("public", exist_ok=True)
_out = "public/drive-times.html"
with open(_out, "w", encoding="utf-8") as f:
    f.write(_HTML.replace("__DATA__", json.dumps(DATA, separators=(",", ":"))))
print("Saved:", _out)
print(f"Comps: {len(comps)} | avg detour: {sum(c['drive_km'] for c in comps)/sum(c['straight_km'] for c in comps):.2f}x")
