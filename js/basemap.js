/* The Reader's Atlas — vintage street basemap (visual only, never clickable)
   A MapLibre GL map drawn underneath the SVG atlas and kept in step with it.
   Tiles: OpenFreeMap (OpenStreetMap data, OpenMapTiles schema), free, no key.
   Colours follow the design system's map tokens (MapTiler "Vintage" look).
   Offline, or if WebGL is unavailable, it simply stays empty and the SVG map works as before. */
(function () {
  "use strict";
  const W = 1000; // world width of the SVG projection (js/app.js)
  const C = {
    land: "#feedc3", residential: "#f8e4b8", wood: "#c2cda2", water: "#9ab1a4",
    building: "#f2bda5", buildingEdge: "#e2a68b",
    minor: "#fffaf0", minorCase: "#d4bc94",
    mid: "#f6e3be", midCase: "#b39a71",
    major: "#e9c995", majorCase: "#8f6a3c",
    motorway: "#e0ac70", motorwayCase: "#7a5126",
    rail: "#a99f8c", label: "#64453f", labelSoft: "#7a5f55", road: "#6e5a48",
    water_label: "#2c3a33", park_label: "#56633f", halo: "#f9f1dc",
  };
  const name = (zh) => zh
    ? ["coalesce", ["get", "name:zh"], ["get", "name:en"], ["get", "name"]]
    : ["coalesce", ["get", "name:en"], ["get", "name"]];
  const lerp = (stops) => ["interpolate", ["exponential", 1.4], ["zoom"], ...stops];
  const cls = (...c) => ["match", ["get", "class"], c, true, false];
  const tunnelFade = ["match", ["get", "brunnel"], "tunnel", 0.35, 1];
  const SANS = ["Noto Sans Regular"], BOLD = ["Noto Sans Bold"], ITAL = ["Noto Sans Italic"];

  function road(id, classes, minzoom, casing, fill, caseW, fillW) {
    return [
      { id: id + "-case", type: "line", source: "omt", "source-layer": "transportation", minzoom,
        filter: cls(...classes), layout: { "line-cap": "round", "line-join": "round" },
        paint: { "line-color": casing, "line-width": lerp(caseW), "line-opacity": tunnelFade } },
      { id: id, type: "line", source: "omt", "source-layer": "transportation", minzoom,
        filter: cls(...classes), layout: { "line-cap": "round", "line-join": "round" },
        paint: { "line-color": fill, "line-width": lerp(fillW), "line-opacity": tunnelFade } },
    ];
  }

  function style(zh) {
    return {
      version: 8,
      glyphs: "https://tiles.openfreemap.org/fonts/{fontstack}/{range}.pbf",
      sources: { omt: { type: "vector", url: "https://tiles.openfreemap.org/planet",
        attribution: "OpenFreeMap © OpenMapTiles · data © OpenStreetMap contributors" } },
      layers: [
        { id: "background", type: "background", paint: { "background-color": C.land } },
        { id: "residential", type: "fill", source: "omt", "source-layer": "landuse", minzoom: 9,
          filter: cls("residential", "suburb", "neighbourhood"),
          paint: { "fill-color": C.residential, "fill-opacity": ["interpolate", ["linear"], ["zoom"], 9, 0, 11, 0.8] } },
        { id: "wood", type: "fill", source: "omt", "source-layer": "landcover", minzoom: 6,
          filter: cls("wood", "forest"), paint: { "fill-color": C.wood, "fill-opacity": 0.6 } },
        { id: "grass", type: "fill", source: "omt", "source-layer": "landcover", minzoom: 9,
          filter: cls("grass", "farmland", "wetland"), paint: { "fill-color": C.wood, "fill-opacity": 0.25 } },
        { id: "park", type: "fill", source: "omt", "source-layer": "park", minzoom: 8,
          paint: { "fill-color": C.wood, "fill-opacity": 0.65 } },
        { id: "water", type: "fill", source: "omt", "source-layer": "water",
          filter: ["!=", ["get", "intermittent"], 1], paint: { "fill-color": C.water } },
        { id: "river", type: "line", source: "omt", "source-layer": "waterway", minzoom: 6,
          filter: cls("river"), layout: { "line-cap": "round", "line-join": "round" },
          paint: { "line-color": C.water, "line-width": lerp([6, 0.6, 10, 1.6, 14, 4, 17, 12]) } },
        { id: "stream", type: "line", source: "omt", "source-layer": "waterway", minzoom: 11,
          filter: cls("canal", "stream", "drain", "ditch"),
          paint: { "line-color": C.water, "line-width": lerp([11, 0.5, 14, 1.2, 17, 4]) } },
        { id: "building", type: "fill", source: "omt", "source-layer": "building", minzoom: 13.5,
          paint: { "fill-color": C.building, "fill-outline-color": C.buildingEdge,
            "fill-opacity": ["interpolate", ["linear"], ["zoom"], 13.5, 0, 15, 0.8] } },
        { id: "path", type: "line", source: "omt", "source-layer": "transportation", minzoom: 14,
          filter: cls("path", "track"),
          paint: { "line-color": C.midCase, "line-width": 0.8, "line-dasharray": [2, 2] } },
        { id: "rail", type: "line", source: "omt", "source-layer": "transportation", minzoom: 9,
          filter: ["all", cls("rail"), ["!=", ["get", "brunnel"], "tunnel"]],
          paint: { "line-color": C.rail, "line-width": lerp([9, 0.5, 14, 1, 18, 2]) } },
        { id: "rail-hatch", type: "line", source: "omt", "source-layer": "transportation", minzoom: 14,
          filter: ["all", cls("rail"), ["!=", ["get", "brunnel"], "tunnel"]],
          paint: { "line-color": C.rail, "line-width": lerp([14, 3, 18, 7]), "line-dasharray": [0.2, 8] } },
        { id: "country-border", type: "line", source: "omt", "source-layer": "boundary",
          filter: ["all", ["==", ["get", "admin_level"], 2], ["!=", ["get", "maritime"], 1]],
          paint: { "line-color": "#eea891", "line-width": lerp([5, 1, 10, 1.6, 14, 3]) } },
        ...road("minor", ["minor", "service"], 12.5, C.minorCase, C.minor, [12.5, 0.8, 14, 2.6, 16, 9, 18, 26], [12.5, 0.3, 14, 1.6, 16, 7, 18, 23]),
        ...road("mid", ["secondary", "tertiary"], 9, C.midCase, C.mid, [9, 0.6, 12, 2.4, 14, 5, 16, 13, 18, 32], [9, 0.3, 12, 1.5, 14, 3.6, 16, 11, 18, 29]),
        ...road("major", ["primary", "trunk"], 7, C.majorCase, C.major, [7, 0.6, 10, 2, 13, 4, 16, 16, 18, 36], [7, 0.3, 10, 1.2, 13, 2.8, 16, 14, 18, 33]),
        ...road("motorway", ["motorway"], 5.5, C.motorwayCase, C.motorway, [6, 0.7, 10, 2.4, 14, 5.5, 16, 18], [6, 0.35, 10, 1.5, 14, 4, 16, 15.5]),
        // labels
        { id: "river-name", type: "symbol", source: "omt", "source-layer": "waterway", minzoom: 9,
          filter: cls("river", "canal"),
          layout: { "symbol-placement": "line", "text-field": name(zh), "text-font": ITAL,
            "text-size": ["interpolate", ["linear"], ["zoom"], 9, 11, 15, 15], "text-letter-spacing": 0.15,
            "symbol-spacing": 400 },
          paint: { "text-color": C.water_label, "text-halo-color": C.halo, "text-halo-width": 1.2 } },
        { id: "water-name", type: "symbol", source: "omt", "source-layer": "water_name", minzoom: 8,
          layout: { "text-field": name(zh), "text-font": ITAL, "text-size": 12, "text-letter-spacing": 0.12 },
          paint: { "text-color": C.water_label, "text-halo-color": "rgba(154,177,164,0.7)", "text-halo-width": 1 } },
        { id: "park-name", type: "symbol", source: "omt", "source-layer": "poi", minzoom: 14.5,
          filter: cls("park"),
          layout: { "text-field": name(zh), "text-font": ITAL, "text-size": 11, "text-max-width": 7 },
          paint: { "text-color": C.park_label, "text-halo-color": C.halo, "text-halo-width": 1.2 } },
        { id: "street-name", type: "symbol", source: "omt", "source-layer": "transportation_name", minzoom: 13,
          filter: ["any", ["all", cls("minor", "service"), [">=", ["zoom"], 14.5]], cls("primary", "secondary", "tertiary", "trunk")],
          layout: { "symbol-placement": "line", "text-field": name(zh), "text-font": SANS,
            "text-size": ["interpolate", ["linear"], ["zoom"], 13, 10, 17, 13] },
          paint: { "text-color": C.road, "text-halo-color": C.minor, "text-halo-width": 1.4 } },
        { id: "neighbourhood", type: "symbol", source: "omt", "source-layer": "place", minzoom: 13.5,
          filter: cls("neighbourhood", "hamlet", "isolated_dwelling"),
          layout: { "text-field": name(zh), "text-font": SANS, "text-size": 10.5, "text-letter-spacing": 0.08, "text-max-width": 8 },
          paint: { "text-color": C.labelSoft, "text-halo-color": C.halo, "text-halo-width": 1.4 } },
        { id: "suburb", type: "symbol", source: "omt", "source-layer": "place", minzoom: 11.5, maxzoom: 16,
          filter: cls("suburb", "quarter"),
          layout: { "text-field": name(zh), "text-font": SANS, "text-transform": "uppercase",
            "text-size": ["interpolate", ["linear"], ["zoom"], 11.5, 10, 15, 13], "text-letter-spacing": 0.2, "text-max-width": 8 },
          paint: { "text-color": C.label, "text-halo-color": C.halo, "text-halo-width": 1.5 } },
        { id: "village", type: "symbol", source: "omt", "source-layer": "place", minzoom: 10.5, maxzoom: 15,
          filter: cls("village"),
          layout: { "text-field": name(zh), "text-font": SANS, "text-size": 11 },
          paint: { "text-color": C.labelSoft, "text-halo-color": C.halo, "text-halo-width": 1.4 } },
        { id: "town", type: "symbol", source: "omt", "source-layer": "place", minzoom: 7.5, maxzoom: 14,
          filter: cls("city", "town"),
          layout: { "text-field": name(zh), "text-font": BOLD,
            "text-size": ["interpolate", ["linear"], ["zoom"], 7.5, 10.5, 12, 14] },
          paint: { "text-color": C.label, "text-halo-color": C.halo, "text-halo-width": 1.5 } },
      ],
    };
  }

  let map = null, host = null, zh = false, warned = false, tiles = false;
  let regionData = null, hl = { hover: null, active: null };
  let styleReady = false; const pending = [];
  const listeners = [];
  function init(container, chinese) {
    host = container;
    zh = !!chinese;
    if (!window.maplibregl) return;
    try { // WebGL is required; without it the SVG atlas carries on alone
      const c = document.createElement("canvas");
      if (!(c.getContext("webgl2") || c.getContext("webgl"))) return;
    } catch (e) { return; }
    try {
      map = new maplibregl.Map({
        container, style: style(zh), interactive: false, attributionControl: false,
        center: [-2, 54], zoom: 5, maxZoom: 20, renderWorldCopies: false, fadeDuration: 0,
      });
      // show the layer only once real tiles arrive, so offline the SVG sea and land stay visible
      map.on("data", (e) => {
        if (tiles || e.dataType !== "source" || !e.tile || e.sourceId !== "omt") return;
        tiles = true;
        host.classList.add("has-tiles");
        listeners.forEach((f) => f());
      });
      // our own flag: map.isStyleLoaded() is also false while tiles stream in
      map.once("style.load", () => { styleReady = true; pending.splice(0).forEach((f) => f()); });
      map.on("error", (e) => { if (!warned) { warned = true; console.warn("[basemap]", e && e.error ? e.error.message : e); } });
    } catch (e) {
      map = null;
      console.warn("[basemap] not available:", e);
    }
  }
  // SVG view {k, x, y} -> MapLibre camera: same Web Mercator, so only scale and centre differ
  function sync(view, w, h) {
    if (!map) return;
    const z = Math.log2((view.k * W) / 512);
    const X = (w / 2 - view.x) / view.k, Y = (h / 2 - view.y) / view.k;
    const lon = (X / W) * 360 - 180;
    const lat = (Math.atan(Math.sinh(Math.PI - (2 * Math.PI * Y) / W)) * 180) / Math.PI;
    host.classList.toggle("is-on", z >= 4.5);
    if (z < 4.5) return; // whole-world views: the SVG draws everything
    map.jumpTo({ center: [lon, Math.max(-85, Math.min(85, lat))], zoom: z });
  }
  // The twelve regions as washes *under* the basemap's water, so the detailed OSM coastline
  // trims them: coarse Natural Earth coasts never show once the streets are visible.
  function whenReady(f) { if (!map) return; styleReady ? f() : pending.push(f); }
  function setRegions(fc) {
    regionData = fc;
    whenReady(() => {
      if (map.getSource("regions")) { map.getSource("regions").setData(fc); return; }
      map.addSource("regions", { type: "geojson", data: fc });
      const fade = (o) => ["interpolate", ["linear"], ["zoom"], 5.8, 0, 7.2, o];
      map.addLayer({ id: "region-wash", type: "fill", source: "regions",
        paint: { "fill-color": ["get", "wash"], "fill-opacity": fade(0.55) } }, "water");
      map.addLayer({ id: "region-hover", type: "fill", source: "regions", filter: ["==", ["get", "r"], ""],
        paint: { "fill-color": "#ecd0ca", "fill-opacity": fade(0.55) } }, "water");
      map.addLayer({ id: "region-active", type: "fill", source: "regions", filter: ["==", ["get", "r"], ""],
        paint: { "fill-color": "#ecd0ca", "fill-opacity": fade(0.5) } }, "water");
      applyHighlight();
    });
  }
  function applyHighlight() {
    if (!map || !map.getLayer("region-hover")) return;
    map.setFilter("region-hover", ["==", ["get", "r"], hl.hover && hl.hover !== hl.active ? hl.hover : ""]);
    map.setFilter("region-active", ["==", ["get", "r"], hl.active || ""]);
  }
  function setHighlight(hover, active) {
    if (hover === hl.hover && active === hl.active) return;
    hl = { hover, active };
    applyHighlight();
  }
  // Invisible copies of the atlas's own labels and markers, placed above every basemap label:
  // they take up collision space, so a basemap name that would overlap one is simply not drawn.
  function setBlockers(fc) {
    whenReady(() => {
      if (map.getSource("blockers")) { map.getSource("blockers").setData(fc); return; }
      map.addSource("blockers", { type: "geojson", data: fc });
      const hidden = { "text-opacity": 0 };
      const always = { "text-allow-overlap": true, "text-ignore-placement": false };
      map.addLayer({ id: "block-dot", type: "symbol", source: "blockers",
        layout: { ...always, "text-field": "●", "text-font": SANS, "text-size": 18, "text-padding": 2 }, paint: hidden });
      map.addLayer({ id: "block-marker", type: "symbol", source: "blockers", filter: ["==", ["get", "kind"], "marker"],
        // the SVG name sits right of its marker, or left / above / below when that side is taken (map-layers.md 3)
        layout: { ...always, "text-field": ["get", "t"], "text-font": SANS, "text-size": 13,
          "text-anchor": ["match", ["get", "side"], "left", "right", "above", "bottom", "below", "top", "left"],
          "text-offset": ["match", ["get", "side"], "left", ["literal", [-0.75, 0]], "above", ["literal", [0, -0.7]], "below", ["literal", [0, 0.7]], ["literal", [0.75, 0]]],
          "text-padding": 3, "text-max-width": 40 }, paint: hidden });
      map.addLayer({ id: "block-unit", type: "symbol", source: "blockers", filter: ["==", ["get", "kind"], "unit"],
        layout: { ...always, "text-field": ["get", "t"], "text-font": ITAL, "text-size": 11.5, "text-letter-spacing": 0.06,
          "text-padding": 3, "text-max-width": 40 }, paint: hidden });
    });
  }
  function setLanguage(chinese) {
    if (!map || !!chinese === zh) { zh = !!chinese; return; }
    zh = !!chinese;
    const apply = () => {
      for (const id of ["river-name", "water-name", "park-name", "street-name", "neighbourhood", "suburb", "village", "town"]) {
        if (map.getLayer(id)) map.setLayoutProperty(id, "text-field", name(zh));
      }
    };
    whenReady(apply);
  }
  function resize() { if (map) map.resize(); }
  window.RA_BASEMAP = { init, sync, setLanguage, resize, hasTiles: () => tiles, onTiles: (f) => listeners.push(f), setRegions, setHighlight, setBlockers, zoomFor: (k) => Math.log2((k * W) / 512), _map: () => map, _style: style };
})();
