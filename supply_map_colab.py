# ============================================================
# PLEASANTVIEW TOWNHOME SUPPLY MAP - Colab
# ============================================================
# 1. Edit PROJECTS below as needed
# 2. Run the cell
# 3. Download: Files panel > right-click file > Download
# ============================================================

import re
import base64
from IPython.display import IFrame, display

PROJECTS = [
    # Add one dict per townhome project. Template row (copy, uncomment, fill in):
    # status must be one of: "Stabilized" | "Active" | "Under Construction" | "Proposed"
    # {"id": 0, "name": "Project Name", "address": "0000 00 Ave NW", "units": 0, "status": "Proposed", "year_built": None, "est_completion": None, "lat": 53.4825, "lng": -113.5075},
]


def _val(val):
    if val is None:
        return "null"
    elif isinstance(val, str):
        return '"' + val + '"'
    else:
        return str(val)


def build_js_array(projects):
    out = "[\n"
    for p in projects:
        out += "  {\n"
        out += "    id: " + str(p["id"]) + ",\n"
        out += '    name: "' + p["name"] + '",\n'
        out += '    address: "' + p["address"] + '",\n'
        out += "    units: " + str(p["units"]) + ",\n"
        out += '    status: "' + p["status"] + '",\n'
        out += "    year_built: " + _val(p["year_built"]) + ",\n"
        out += "    est_completion: " + _val(p["est_completion"]) + ",\n"
        out += "    lat: " + str(p["lat"]) + ",\n"
        out += "    lng: " + str(p["lng"]) + "\n"
        out += "  },\n"
    out += "]"
    return out


_BASE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Pleasantview Townhome Supply</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#f7f6f3;--surface:#fff;--border:#e8e5df;--border-light:#f0ede8;
  --text-primary:#1a1917;--text-secondary:#6b6760;--text-muted:#a09d99;
  --accent:#c8572a;--accent-subtle:rgba(200,87,42,0.08);
  --amber:#d4830f;--amber-subtle:rgba(212,131,15,0.08);
  --blue:#2a6496;--green:#2e7d4f;
  --shadow-md:0 4px 12px rgba(0,0,0,0.08);--shadow-lg:0 12px 32px rgba(0,0,0,0.1);--radius:8px;
}
html,body{height:100%;font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text-primary);overscroll-behavior:none}
body{display:flex;flex-direction:column}
@supports (height:100dvh){body{height:100dvh}}
#header{flex-shrink:0;z-index:1000;height:52px;background:var(--surface);border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;padding:0 20px;box-shadow:0 1px 3px rgba(0,0,0,0.07)}
#header-left{display:flex;align-items:center}
#header-title{font-size:13px;font-weight:500;color:var(--text-secondary)}
#header-title strong{color:var(--text-primary);font-weight:600}
#header-right{display:flex;align-items:center;gap:16px}
.stat-chip{text-align:right}
.stat-num{font-size:18px;font-weight:600;color:var(--text-primary);line-height:1;font-variant-numeric:tabular-nums}
.stat-label{font-size:9px;font-weight:500;letter-spacing:.08em;text-transform:uppercase;color:var(--text-muted);margin-top:1px;white-space:nowrap}
.stat-div{width:1px;height:28px;background:var(--border)}
#filter-bar{display:flex;align-items:center;gap:6px}
.ftab{padding:5px 13px;border-radius:20px;border:1.5px solid var(--border);font-size:11.5px;font-weight:500;cursor:pointer;background:var(--surface);color:var(--text-secondary);display:flex;align-items:center;gap:5px;transition:all .15s}
.ftab:hover{border-color:var(--text-primary);color:var(--text-primary)}
.ftab.active{background:var(--text-primary);border-color:var(--text-primary);color:#fff}
.ftab.active.tst{background:var(--green);border-color:var(--green)}
.ftab.active.tac{background:var(--amber);border-color:var(--amber)}
.ftab.active.tuc{background:var(--accent);border-color:var(--accent)}
.ftab.active.tpr{background:var(--blue);border-color:var(--blue)}
.fdot{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.tst .fdot{background:var(--green)}.tst.active .fdot{background:#fff}
.tac .fdot{background:var(--amber)}.tac.active .fdot{background:#fff}
.tuc .fdot{background:var(--accent)}.tuc.active .fdot{background:#fff}
.tpr .fdot{background:var(--blue)}.tpr.active .fdot{background:#fff}
#layout{flex:1;min-height:0;display:flex}
#map{flex:1;min-height:0}
#sidebar{width:340px;flex-shrink:0;background:var(--surface);border-left:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden;box-shadow:-2px 0 8px rgba(0,0,0,0.04)}
#sb-head{padding:16px 18px 12px;border-bottom:1px solid var(--border-light)}
#sb-head h2{font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--text-muted)}
#proj-list{flex:1;min-height:0;overflow-y:auto;padding:8px 0}
#proj-list::-webkit-scrollbar{width:4px}
#proj-list::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}
.pcard{padding:14px 18px;cursor:pointer;border-bottom:1px solid var(--border-light);transition:background .15s}
.pcard:hover{background:var(--bg)}
.pcard.active{background:var(--accent-subtle);border-left:3px solid var(--accent);padding-left:15px}
.pcard-top{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:5px}
.pname{font-size:13.5px;font-weight:600;line-height:1.3;flex:1}
.pbadge{background:var(--text-primary);color:#fff;font-size:11px;font-weight:600;padding:2px 7px;border-radius:12px;white-space:nowrap;flex-shrink:0}
.pcard.active .pbadge{background:var(--accent)}
.pstatus{display:inline-flex;align-items:center;gap:4px;font-size:11px;color:var(--text-muted)}
.sdot{width:5px;height:5px;border-radius:50%;flex-shrink:0}
.sdot.st{background:var(--green)}
.sdot.ac{background:var(--amber)}
.sdot.uc{background:var(--accent)}
.sdot.pr{background:var(--blue)}
#detail{border-top:1px solid var(--border);background:var(--surface);flex-shrink:0;max-height:0;overflow:hidden;transition:max-height .3s}
#detail.open{max-height:480px}
#det-inner{padding:18px}
#det-name{font-size:15px;font-weight:600;margin-bottom:14px;line-height:1.3}
.dgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.dfield{background:var(--bg);border:1px solid var(--border-light);border-radius:var(--radius);padding:10px 12px}
.dfield.full{grid-column:1/-1}
.dflabel{font-size:9.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);margin-bottom:3px}
.dfval{font-size:13px;font-weight:500;line-height:1.3}
.leaflet-popup-content-wrapper{border-radius:var(--radius)!important;box-shadow:var(--shadow-lg)!important;border:1px solid var(--border)!important;padding:0!important;overflow:hidden;font-family:'DM Sans',sans-serif!important}
.leaflet-popup-content{margin:0!important;width:240px!important;max-width:calc(100vw - 56px)!important}
.leaflet-popup-tip-container{display:none}
.popup-inner{padding:14px 16px}
.popup-name{font-size:13px;font-weight:600;margin-bottom:3px;line-height:1.3}
.popup-sub{font-size:11.5px;color:var(--text-secondary);margin-bottom:8px}
.popup-row{display:flex;justify-content:space-between;align-items:center;padding:5px 0;border-top:1px solid var(--border-light);font-size:11.5px}
.popup-row-label{color:var(--text-muted)}
.popup-row-value{font-weight:500;font-family:'DM Mono',monospace}
.cmarker{width:32px;height:32px;border:2.5px solid #fff;border-radius:50% 50% 50% 0;transform:rotate(-45deg);box-shadow:var(--shadow-md);cursor:pointer}

@media (max-width:768px){
  #header{flex-wrap:wrap;height:auto;padding:10px 12px 8px;gap:8px;align-items:flex-start;box-shadow:0 1px 3px rgba(0,0,0,0.07)}
  #header-left{width:100%}
  #header-title{font-size:12px}
  #filter-bar{width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding-bottom:2px}
  #filter-bar::-webkit-scrollbar{display:none}
  .ftab{flex-shrink:0;white-space:nowrap;padding:7px 13px}
  #header-right{width:100%;justify-content:flex-start;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;gap:18px}
  #header-right::-webkit-scrollbar{display:none}
  .stat-chip{flex-shrink:0;text-align:left}
  #layout{flex-direction:column}
  #map{flex:1;min-height:200px}
  #sidebar{width:100%;flex:0 0 auto;height:24vh;min-height:180px;max-height:230px;overflow-y:auto;-webkit-overflow-scrolling:touch;border-left:none;border-top:1px solid var(--border);box-shadow:0 -2px 8px rgba(0,0,0,0.04)}
  #proj-list{flex:none;overflow-y:visible}
  #detail.open{max-height:2000px}
  .ftab,.pcard,.stat-chip{touch-action:manipulation}
}
</style>
</head>
<body>
<div id="header">
  <div id="header-left">
    <div id="header-title"><strong>Pleasantview Townhome Supply</strong></div>
  </div>
  <div id="filter-bar">
    <div class="ftab active" data-filter="all">ALL</div>
    <div class="ftab tst" data-filter="Stabilized"><span class="fdot"></span>Stabilized</div>
    <div class="ftab tac" data-filter="Active"><span class="fdot"></span>Active</div>
    <div class="ftab tuc" data-filter="Under Construction"><span class="fdot"></span>Under Construction</div>
    <div class="ftab tpr" data-filter="Proposed"><span class="fdot"></span>Proposed</div>
  </div>
  <div id="header-right">
    <div class="stat-chip">
      <div class="stat-num" id="stat-st">0</div>
      <div class="stat-label">Stabilized Units</div>
    </div>
    <div class="stat-div"></div>
    <div class="stat-chip">
      <div class="stat-num" id="stat-ac">0</div>
      <div class="stat-label">Active Projects</div>
    </div>
    <div class="stat-div"></div>
    <div class="stat-chip">
      <div class="stat-num" id="stat-uc">0</div>
      <div class="stat-label">UC Units</div>
    </div>
    <div class="stat-div"></div>
    <div class="stat-chip">
      <div class="stat-num" id="stat-pr">0</div>
      <div class="stat-label">Proposed Units</div>
    </div>
  </div>
</div>
<div id="layout">
  <div id="map"></div>
  <div id="sidebar">
    <div id="sb-head"><h2>Townhome Supply</h2></div>
    <div id="proj-list"></div>
    <div id="detail">
      <div id="det-inner">
        <div id="det-name"></div>
        <div class="dgrid" id="det-grid"></div>
      </div>
    </div>
  </div>
</div>
<script>
const PROJECTS = [
  {
    id: 0,
    name: "The Switch",
    address: "10465 101 St NW",
    units: 285,
    status: "Stabilized",
    year_built: 2024,
    est_completion: null,
    lat: 53.54773198,
    lng: -113.492485
  },
];

let activeId = null, markers = {}, popups = {}, activeFilter = 'all';

const map = L.map('map', {zoomControl: false, attributionControl: false});
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {maxZoom: 19}).addTo(map);
L.control.zoom({position: 'topleft'}).addTo(map);
L.control.attribution({position: 'bottomleft', prefix: false}).addAttribution('&copy; Esri &middot; OpenStreetMap contributors').addTo(map);
map.setView([53.4825, -113.5075], 15);

function markerColor(status) {
  if (status === 'Stabilized') return '#2e7d4f';
  if (status === 'Active') return '#d4830f';
  if (status === 'Under Construction') return '#c8572a';
  return '#2a6496';
}

function markerIcon(active, status) {
  var color = active ? '#1a1917' : markerColor(status);
  var scale = active ? 'transform:rotate(-45deg) scale(1.2);' : '';
  return L.divIcon({
    className: '',
    html: '<div class="cmarker" style="background:' + color + ';' + scale + '"></div>',
    iconSize: [32,32], iconAnchor: [16,32], popupAnchor: [0,-36]
  });
}

function yearInfo(p) {
  if (p.status === 'Proposed') return null;
  if (p.year_built != null) return {label: 'Year Built', val: p.year_built};
  if (p.est_completion != null) return {label: 'Est. Completion', val: p.est_completion};
  return null;
}

function popupHTML(p) {
  var yr = yearInfo(p);
  return '<div class="popup-inner">'
    + '<div class="popup-name">' + p.name + '</div>'
    + '<div class="popup-sub">' + p.units + ' units · ' + p.status + '</div>'
    + (yr ? '<div class="popup-row"><span class="popup-row-label">' + yr.label + '</span><span class="popup-row-value">' + yr.val + '</span></div>' : '')
    + '</div>';
}

PROJECTS.forEach(function(p) {
  var marker = L.marker([p.lat, p.lng], {icon: markerIcon(false, p.status), title: p.name}).addTo(map);
  var popup = L.popup({closeButton: false, offset: [0,0]}).setContent(popupHTML(p));
  marker.bindPopup(popup);
  marker.on('click', function() { selectProject(p.id); });
  markers[p.id] = marker;
  popups[p.id] = popup;
});

function statusDotClass(status) {
  if (status === 'Stabilized') return 'st';
  if (status === 'Active') return 'ac';
  if (status === 'Under Construction') return 'uc';
  return 'pr';
}

function buildSidebar() {
  var list = document.getElementById('proj-list');
  list.innerHTML = '';
  var visible = PROJECTS.filter(function(p) { return activeFilter === 'all' || p.status === activeFilter; });
  visible.forEach(function(p) {
    var yr = yearInfo(p);
    var yrText = yr ? (' &middot; ' + (yr.label === 'Year Built' ? yr.val : 'Est. ' + yr.val)) : '';
    var card = document.createElement('div');
    card.className = 'pcard' + (activeId === p.id ? ' active' : '');
    card.innerHTML = '<div class="pcard-top"><div class="pname">' + p.name + '</div><div class="pbadge">' + p.units + ' units</div></div>'
      + '<div class="pstatus"><span class="sdot ' + statusDotClass(p.status) + '"></span>' + p.status + yrText + '</div>';
    card.addEventListener('click', function() { selectProject(p.id); });
    list.appendChild(card);
  });
}

function buildDetail(p) {
  var yr = yearInfo(p);
  document.getElementById('det-name').textContent = p.name;
  document.getElementById('det-grid').innerHTML =
    '<div class="dfield"><div class="dflabel">Total Units</div><div class="dfval">' + p.units + '</div></div>'
    + '<div class="dfield"><div class="dflabel">Status</div><div class="dfval">' + p.status + '</div></div>'
    + (yr ? '<div class="dfield"><div class="dflabel">' + yr.label + '</div><div class="dfval">' + yr.val + '</div></div>' : '')
    + '<div class="dfield full"><div class="dflabel">Address</div><div class="dfval">' + p.address + '</div></div>';
}

function selectProject(id) {
  if (activeId !== null && activeId !== id) {
    markers[activeId].setIcon(markerIcon(false, PROJECTS[activeId].status));
    markers[activeId].closePopup();
  }
  if (activeId === id) {
    markers[id].setIcon(markerIcon(false, PROJECTS[id].status));
    markers[id].closePopup();
    activeId = null;
    document.getElementById('detail').classList.remove('open');
    buildSidebar();
    return;
  }
  activeId = id;
  var p = PROJECTS[id];
  map.flyTo([p.lat, p.lng], 16, {duration: 0.8});
  markers[id].setIcon(markerIcon(true, p.status));
  markers[id].openPopup();
  buildDetail(p);
  document.getElementById('detail').classList.add('open');
  buildSidebar();
}

document.querySelectorAll('.ftab').forEach(function(tab) {
  tab.addEventListener('click', function() {
    activeFilter = tab.dataset.filter;
    document.querySelectorAll('.ftab').forEach(function(t) { t.classList.remove('active'); });
    tab.classList.add('active');
    if (activeId !== null) {
      var p = PROJECTS[activeId];
      if (activeFilter !== 'all' && p.status !== activeFilter) {
        markers[activeId].setIcon(markerIcon(false, p.status));
        markers[activeId].closePopup();
        activeId = null;
        document.getElementById('detail').classList.remove('open');
      }
    }
    PROJECTS.forEach(function(p) {
      var show = activeFilter === 'all' || p.status === activeFilter;
      if (show) { if (!map.hasLayer(markers[p.id])) markers[p.id].addTo(map); }
      else { if (map.hasLayer(markers[p.id])) markers[p.id].remove(); }
    });
    buildSidebar();
  });
});

buildSidebar();
</script>
</body>
</html>"""

_new_js = "const PROJECTS = " + build_js_array(PROJECTS)
_html = re.sub(r"const PROJECTS = \[.*?\];", _new_js + ";", _BASE, count=1, flags=re.DOTALL)

# Header stats are computed from PROJECTS above, so they never go stale.
_st = sum(p["units"] for p in PROJECTS if p["status"] == "Stabilized")
_ac = sum(1 for p in PROJECTS if p["status"] == "Active")
_uc = sum(p["units"] for p in PROJECTS if p["status"] == "Under Construction")
_pr = sum(p["units"] for p in PROJECTS if p["status"] == "Proposed")

_html = re.sub(r'id="stat-st">\d+', f'id="stat-st">{_st}', _html)
_html = re.sub(r'id="stat-ac">\d+', f'id="stat-ac">{_ac}', _html)
_html = re.sub(r'id="stat-uc">\d+', f'id="stat-uc">{_uc}', _html)
_html = re.sub(r'id="stat-pr">\d+', f'id="stat-pr">{_pr}', _html)

_encoded = base64.b64encode(_html.encode("utf-8")).decode("ascii")
_html = (
    '<!DOCTYPE html><html><head><meta charset="UTF-8"/></head>'
    "<body><script>document.write(decodeURIComponent(escape(atob('"
    + _encoded
    + "'))));</script></body></html>"
)

_path = "/content/pleasantview_townhome_supply_map.html"
with open(_path, "w", encoding="utf-8") as f:
    f.write(_html)

print("Saved:", _path)
print(f"Stabilized: {_st} units | Active: {_ac} projects | UC: {_uc} units | Proposed: {_pr} units")
display(IFrame(src=_path, width="100%", height="700"))
