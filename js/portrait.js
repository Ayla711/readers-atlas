/* The Reader's Atlas — the reader's portrait (11-19): a dozen small animals, painted soft and a little dry, the way
   gouache sits on rough paper: no outlines, fuzzy edges, two dots for eyes, a neckerchief in one of the atlas's
   accents, inside a thin hand-drawn ring on the page's own paper colour.
   The reader picks one in the account dialog (js/cloud.js); until they do, their account id picks for them.
   Original drawings, plain SVG (the brushwork is an SVG filter), nothing uploaded.
   window.RA_PORTRAIT(key, size) returns an SVG string; RA_PORTRAIT.keys lists the animals; RA_PORTRAIT.label(key, zh);
   RA_PORTRAIT.pick(seed) chooses one from a string. */
(function () {
  "use strict";
  const DOT = "#2e2723", CREAM = "#f6eee2", WHITE = "#fbf8f2", BLUSH = "#e9b9ad";
  const c = (x, y, r, f) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${f}"/>`;
  const e = (x, y, rx, ry, f, rot) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="${f}"${rot ? ` transform="rotate(${rot} ${x} ${y})"` : ""}/>`;
  const p = (d, f) => `<path d="${d}" fill="${f}"/>`;
  const both = (g) => g + `<g transform="translate(64 0) scale(-1 1)">${g}</g>`; // paint the left half, mirror it
  // the face: kept crisp, on top of the brushwork
  const eyes = (x, y, r = 1.05) => both(`<ellipse cx="${x}" cy="${y}" rx="${r}" ry="${r * 1.2}" fill="${DOT}"/><circle cx="${x + 0.3}" cy="${y - 0.4}" r="${r * 0.28}" fill="#fff" opacity=".85"/>`);
  const nose = (x, y, rx = 1.7, ry = 1.25, f = DOT) => `<path d="M${x - rx} ${y - ry * 0.5}Q${x} ${y - ry * 1.3} ${x + rx} ${y - ry * 0.5}Q${x + rx * 0.5} ${y + ry} ${x} ${y + ry}Q${x - rx * 0.5} ${y + ry} ${x - rx} ${y - ry * 0.5}Z" fill="${f}"/>`;
  const smile = (x, y, w = 1.6) => `<path d="M${x} ${y}v1.1M${x} ${y + 1.1}q${-w / 2} ${w * 0.7} ${-w} .2M${x} ${y + 1.1}q${w / 2} ${w * 0.7} ${w} .2" fill="none" stroke="${DOT}" stroke-width=".5" stroke-linecap="round" opacity=".75"/>`;
  const cheeks = (x, y) => both(`<circle cx="${x}" cy="${y}" r="2.3" fill="${BLUSH}" opacity=".5"/>`);
  const whiskers = (y) => both(`<path d="M24.5 ${y}l-6.5-1M24.5 ${y + 1.6}l-6.5 .8" fill="none" stroke="#fff" stroke-width=".4" stroke-linecap="round" opacity=".9"/>`);
  // shoulders and a neckerchief
  // what they wear at the neck (drawn in the shoulders' frame, just under the chin)
  const shade = "#3b2e25";
  const WEAR = {
    // a knitted scarf: wound once round, one end hanging down the chest with a fringe
    scarf: (k) => p("M20.6 40.4Q32 46.8 43.4 40.4L44 45.8Q32 52.8 20 45.8Z", k) + p("M34.8 47.4L41.2 48.2L40.6 58.4L34.2 57.6Z", k) +
      `<path d="M34.6 52.2l6.3.8M34.4 55l6.3.8" fill="none" stroke="#fffdf7" stroke-width=".9" opacity=".55"/><path d="M35 57.6v2.2M37.2 57.9v2.2M39.4 58.2v2.2" fill="none" stroke="${k}" stroke-width="1" stroke-linecap="round"/>` +
      `<path d="M24 43.4Q32 48.6 40 43.4" fill="none" stroke="${shade}" stroke-width=".6" opacity=".25"/>`,
    // a bow tie
    bow: (k) => p("M32 46.6L24.2 42.2Q23 46.6 24.2 51ZM32 46.6L39.8 42.2Q41 46.6 39.8 51Z", k) + `<circle cx="32" cy="46.6" r="2" fill="${k}"/><circle cx="32" cy="46.6" r="2" fill="${shade}" opacity=".22"/>`,
    // a collar and a necktie
    tie: (k) => both(p("M25.4 41.6L32 46.4L27.6 49.8Z", "#fffdf7")) + p("M30.1 45.4h3.8l-.9 3.2h-2Z", k) + p("M31 48.6h2l2 9.4-3 3.2-3-3.2Z", k) + `<path d="M30.1 45.4h3.8l-.9 3.2h-2Z" fill="${shade}" opacity=".2"/>`,
    // a bandana: a triangle of cloth, point down, with a few dots
    bandana: (k) => p("M21 41Q32 47.6 43 41L32 57.6Z", k) + c(29, 47.6, 0.8, "#fffdf7") + c(35, 47.6, 0.8, "#fffdf7") + c(32, 51.6, 0.8, "#fffdf7"),
    // a collar with a bell
    bell: (k) => p("M21.6 41.6Q32 47.6 42.4 41.6L42.6 44.6Q32 50.8 21.4 44.6Z", k) + c(32, 51, 3.2, "#d6ab52") + `<path d="M29.6 51.6h4.8M32 51.6v2.2" fill="none" stroke="${shade}" stroke-width=".6" opacity=".6"/>`,
    none: () => "",
  };
  // shoulders sit right under the chin; `up` tucks them further under it: stocky animals have almost no neck.
  // Only the deer keeps a long neck (tall).
  const tall = (fur, bib, wear, k) => e(32, 60, 17.5, 17, fur) + e(32, 42, 9.5, 8, fur) + (bib ? e(32, 58, 8.5, 13, bib) : "") + `<g transform="translate(0 2)">${WEAR[wear](k)}</g>`;
  const body = (fur, bib, wear, k, up = 2) => `<g transform="translate(0 ${-up})">` + e(32, 57.5, 18.5, 17.5, fur) + e(32, 70, 19, 12, fur) + (bib ? e(32, 56, 8.5, 13, bib) + e(32, 68, 8.5, 10, bib) : "") + WEAR[wear](k) + "</g>";
  // a leaner build for the dog and the wolf: a thick neck running straight down from the jaw into a narrow, upright chest
  const lean = (fur, bib, wear, k, up = 2) => `<g transform="translate(0 ${-up})">` + p("M23.4 40Q32 37 40.6 40C44.6 46.6 46.6 54 47 62V76H17V62C17.4 54 19.4 46.6 23.4 40Z", fur) +
    (bib ? p("M28.4 44Q32 42.6 35.6 44C37 52 37.4 62 37.2 76H26.8C26.6 62 27 52 28.4 44Z", bib) : "") + WEAR[wear](k) + "</g>";
  // on the head
  const beret = (x, y, k) => e(x, y, 11.4, 5.2, k, -10) + `<path d="M${x + 0.6} ${y - 5}l1-2.4" stroke="${k}" stroke-width="1.2" stroke-linecap="round"/>`;
  const flower = (x, y) => [0, 72, 144, 216, 288].map((a) => c((x + 2.9 * Math.cos(a * Math.PI / 180)).toFixed(1), (y + 2.9 * Math.sin(a * Math.PI / 180)).toFixed(1), 2.2, "#e7a79b")).join("") + c(x, y, 1.7, "#d6ab52");

  const RED = "#b86a58", BLUE = "#6b879c", SAGE = "#93a183", GOLD = "#d2ab62";
  // each animal: fur (brushed) and face (crisp)
  const A = {
    fox: { en: "Fox", zh: "狐狸", fur: () => { const f = "#d79a68";
      // the same fox, with the face drawn down to a point at the muzzle
      return body(f, CREAM, "scarf", BLUE, 2.5) + both(p("M19.5 23L17.6 8.6Q23 9.6 29 15.6Z", f) + p("M20.6 18.4L19.8 12Q22.6 13 25.4 15.6Z", "#9a6444")) +
        p("M32 16.9C40.6 16.9 47.4 22 47.4 28.6C47.4 33.4 40.4 39.6 32 44.6C23.6 39.6 16.6 33.4 16.6 28.6C16.6 22 23.4 16.9 32 16.9Z", f) +
        both(p("M16.7 29.6C20.4 28.4 26.2 30.4 29.2 35C30.6 38 31.5 41.4 32 44.6C24.4 40.2 17.4 34.2 16.7 29.6Z", CREAM)); },
      // a half-moon eyeglass on a fine chain, worn low under one eye
      face: () => eyes(26, 28.6) + nose(32, 41.2) +
        `<g fill="none" stroke="#7a5c34" stroke-linecap="round"><path d="M34.5 30.5H41.5A3.5 3.3 0 0 1 34.5 30.5Z" stroke-width=".55" stroke-linejoin="round" fill="#fffdf7" fill-opacity=".3"/><path d="M41.5 30.6Q45.6 34.8 44.4 41.6" stroke-width=".35"/></g>` },
    cat: { en: "Cat", zh: "猫", fur: () => { const f = "#9c9590";
      return `<path d="M43 62C52 60 56.4 50 53.2 42C51.8 38.6 48 38 46.2 40.8" fill="none" stroke="${f}" stroke-width="3.2" stroke-linecap="round"/><path d="M53.6 47.8l-2.8 .6M52.2 42.8l-2.4 1.2" fill="none" stroke="#7e7873" stroke-width="1" stroke-linecap="round"/>` +
        body(f, WHITE, "bow", RED, 2.5) + both(p("M18.6 24L17.4 9.6Q23.4 11 29.4 16.6Z", f) + p("M20 19.4L19.4 13Q22.6 14.2 25.4 16.6Z", BLUSH)) +
        e(32, 29.5, 15.4, 12.8, f) + both(e(26.4, 21, 1, 3, "#7e7873", -12)) + e(32, 19.4, 1, 3.2, "#7e7873") + both(c(29.6, 34.6, 3.3, WHITE)); },
      face: () => eyes(25.8, 28.4, 1.15) + nose(32, 32.9, 1.25, 0.95, "#d49a8f") + smile(32, 33.9, 2.4) + whiskers(34.2) },
    rabbit: { en: "Rabbit", zh: "兔子", fur: () => { const f = "#d9d0c6";
      return body(f, WHITE, "bandana", SAGE, 3) + both(e(25.4, 12.4, 3.8, 11.4, f, -9) + e(25.4, 13, 1.7, 8.4, BLUSH, -9)) +
        e(32, 31, 13.4, 12.2, f) + both(c(29.4, 36, 3.6, WHITE)) + flower(41, 21.4); },
      face: () => eyes(26, 29.6) + nose(32, 34.2, 1.2, 0.9, "#d49a8f") + smile(32, 35.1, 2.4) + cheeks(23.6, 34) + whiskers(35.4) },
    bear: { en: "Bear", zh: "熊", fur: () => { const f = "#a87d5b";
      return body(f, "", "tie", GOLD, 4) + both(c(20.4, 18.4, 5.6, f) + c(20.6, 18.8, 2.7, "#d7b895")) + e(32, 29.5, 15.4, 14, f) + e(32, 35, 6.6, 5.2, "#e0c8aa"); },
      face: () => eyes(25.8, 27.8) + nose(32, 33.2, 2.2, 1.5) + smile(32, 34.7, 2.6) },
    dog: { en: "Dog", zh: "小狗", fur: () => { const f = "#e6cfab", ear = "#c69c6c";
      return body(f, WHITE, "bandana", RED, 3) + e(32, 29, 13.6, 13.2, f) + both(e(18.6, 28.4, 5, 9.4, ear, 14)) + e(32, 17.4, 5.4, 3, f) + e(32, 35, 6.8, 5.8, WHITE); },
      face: () => eyes(26.2, 28) + nose(32, 33.2, 2.1, 1.5) + smile(32, 34.7, 2.6) },
    sheep: { en: "Sheep", zh: "小羊", fur: () => { const w = "#f4efe6", f = "#ecd9c4";
      return body(w, "", "bow", BLUE, 3.5) + both(e(18.8, 30.4, 4.8, 2.5, "#dcc3a8", -22)) +
        [[21.5, 21, 6.4], [27.5, 16, 6.8], [36.5, 16, 6.8], [42.5, 21, 6.4], [18.6, 26.4, 5], [45.4, 26.4, 5]].map(([x, y, r]) => c(x, y, r, w)).join("") +
        e(32, 31.5, 10.4, 11.6, f) + c(28, 21, 4.6, w) + c(36, 21, 4.6, w) + c(32, 19.4, 5, w) + beret(31, 11.6, RED); },
      face: () => eyes(27.2, 30.4) + nose(32, 35.4, 1.3, 0.9, "#c9958a") + smile(32, 36.3, 2.2) + cheeks(24.6, 34.6) },
    deer: { en: "Deer", zh: "小鹿", fur: () => { const f = "#c9a074";
      return tall(f, CREAM, "scarf", SAGE) + both(`<path d="M26 15.4q-2.4-4.6-1.4-8.4M24.9 11.4l-3.2-1.8" fill="none" stroke="#8d6d50" stroke-width="1.5" stroke-linecap="round"/>`) +
        both(e(16.4, 22.6, 7, 3.5, f, 24) + e(16.8, 22.8, 4.4, 1.7, "#eed6c8", 24)) + e(32, 29, 11.6, 14, f) + e(32, 38.2, 5.6, 4.6, CREAM) +
        c(28.6, 19.4, 0.9, CREAM) + c(35.4, 19.4, 0.9, CREAM) + c(32, 17.6, 0.9, CREAM); },
      face: () => eyes(26.4, 28.4, 1.2) + nose(32, 37, 1.8, 1.3) +
        `<g fill="none" stroke="#7a5c34" stroke-width=".55" stroke-linecap="round">` + both(`<circle cx="26.4" cy="28.5" r="3.4" fill="#fffdf7" fill-opacity=".14"/><path d="M23.1 27.9L20.9 27.2"/>`) + `<path d="M29.7 27.9Q32 26.5 34.3 27.9"/></g>` },
    panda: { en: "Panda", zh: "熊猫", fur: () => { const k = "#3f3a37";
      return body(k, "", "bow", RED, 4) + both(c(20.4, 18.2, 5.4, k)) + e(32, 29.5, 15.2, 13.6, "#e7dfd1") + both(e(25.4, 28.6, 3.9, 4.9, k, 22)); },
      face: () => both(`<circle cx="25.6" cy="28.4" r="1.1" fill="#fff"/><circle cx="25.8" cy="28.5" r=".6" fill="${DOT}"/>`) + nose(32, 33.6, 1.7, 1.2) + smile(32, 34.8, 2.2) },
    koala: { en: "Koala", zh: "考拉", fur: () => { const f = "#b4b0ad";
      return body(f, WHITE, "scarf", GOLD, 3.5) + both(c(17.4, 22, 7.6, f) + c(17.8, 22.6, 4.2, "#ecdcd5")) + e(32, 29.5, 14.2, 12.8, f); },
      soft: () => `<g transform="translate(8.4 2.2)">` + `<path d="M29.6 18.8Q33 14.4 37.4 11.4" fill="none" stroke="#7c8f7a" stroke-width=".9" stroke-linecap="round"/>` + c(31.2, 15, 1.8, "#9db8a4") + c(34.8, 16, 1.7, "#8fae98") + c(34.4, 12, 1.8, "#9db8a4") + c(37.8, 10.6, 1.6, "#8fae98") + "</g>",
      face: () => eyes(25.2, 28.2) + `<ellipse cx="32" cy="32.6" rx="2.9" ry="4" fill="#403a37"/>` + cheeks(23.4, 33.4) },
    pig: { en: "Pig", zh: "小猪", fur: () => { const f = "#f2cfca";
      // the same pig, fatter: a wider head with full cheeks, broader shoulders
      return `<g transform="translate(32 0) scale(1.14 1) translate(-32 0)">` + body(f, "", "tie", BLUE, 3.2) + "</g>" + both(p("M19 23L17.2 12.4Q23 13 27.8 18Z", "#eab7b1")) +
        e(32, 29.8, 17, 13.8, f) + both(e(20.6, 34.6, 6.6, 6, f)) + e(32, 35, 5.6, 4, "#e8aca7"); },
      soft: () => `<g transform="rotate(-8 32 16)"><ellipse cx="32" cy="16.4" rx="8.6" ry="1.9" fill="#d6b566"/><path d="M27.5 16.4V11.8Q27.5 10.8 28.7 10.8H35.3Q36.5 10.8 36.5 11.8V16.4Z" fill="#e2c67e"/><path d="M27.5 14.2H36.5V16.2H27.5Z" fill="${RED}"/></g>`,
      face: () => eyes(25.8, 28.6) + c(30.2, 35, 0.75, "#b97a78") + c(33.8, 35, 0.75, "#b97a78") + cheeks(21.6, 34.2) },
    hedgehog: { en: "Hedgehog", zh: "刺猬", fur: () => { const q = "#8f7a69", f = "#f1e3cf";
      // a coat of quills over the head and back, bristling at the edge; a small face narrowing to the nose.
      // It peeks over the bottom of the ring: the head at full size, no body, cut off by the ring, and two paws
      // resting on the ring itself (drawn over the ring line, see `over`).
      let edge = "", marks = "";
      // quill tips along the dome …
      for (let i = 0; i <= 16; i++) { const a = (182 + i * 11) * Math.PI / 180, ca = Math.cos(a), sa = Math.sin(a), x = 32 + 20.5 * ca, y = 30 + 16.4 * sa;
        edge += `<path d="M${(x - 2.2 * sa).toFixed(1)} ${(y + 2.2 * ca).toFixed(1)}L${(x + 4 * ca).toFixed(1)} ${(y + 4 * sa).toFixed(1)}L${(x + 2.2 * sa).toFixed(1)} ${(y - 2.2 * ca).toFixed(1)}Z" fill="${q}"/>`; }
      // … and on down the sides, which leave the dome without a corner and sweep outwards in one curve
      const B = [[53.5, 30], [53.5, 36.5], [59, 43.5], [72, 55]];
      for (let t = 0.12; t < 0.86; t += 0.125) { const u = 1 - t;
        const x = u * u * u * B[0][0] + 3 * u * u * t * B[1][0] + 3 * u * t * t * B[2][0] + t * t * t * B[3][0], y = u * u * u * B[0][1] + 3 * u * u * t * B[1][1] + 3 * u * t * t * B[2][1] + t * t * t * B[3][1];
        const dx = 3 * u * u * (B[1][0] - B[0][0]) + 6 * u * t * (B[2][0] - B[1][0]) + 3 * t * t * (B[3][0] - B[2][0]), dy = 3 * u * u * (B[1][1] - B[0][1]) + 6 * u * t * (B[2][1] - B[1][1]) + 3 * t * t * (B[3][1] - B[2][1]);
        const L = Math.hypot(dx, dy), tx = dx / L, ty = dy / L, nx = ty, ny = -tx; // outward normal on the right side
        edge += both(`<path d="M${(x - 2.2 * tx - 0.6 * nx).toFixed(1)} ${(y - 2.2 * ty - 0.6 * ny).toFixed(1)}L${(x + 4 * nx + 1 * tx).toFixed(1)} ${(y + 4 * ny + 1 * ty).toFixed(1)}L${(x + 2.2 * tx - 0.6 * nx).toFixed(1)} ${(y + 2.2 * ty - 0.6 * ny).toFixed(1)}Z" fill="${q}"/>`); }
      for (let r = 0; r < 3; r++) for (let i = 0; i <= 12 + r * 2; i++) { const a = (172 + i * (196 / (12 + r * 2))) * Math.PI / 180, R = 12.4 + r * 2.6, x = 32 + R * Math.cos(a), y = 31 + R * 0.92 * Math.sin(a);
        marks += `<path d="M${x.toFixed(1)} ${y.toFixed(1)}l${(2.2 * Math.cos(a)).toFixed(1)} ${(2.2 * Math.sin(a)).toFixed(1)}" stroke="${(i + r) % 2 ? "#6b594d" : "#b9a591"}" stroke-width=".8" stroke-linecap="round"/>`; }
      [[16, 35], [19.5, 39], [15.5, 43], [18.5, 47], [22, 51], [16, 52], [26, 47.5], [20.5, 56]].forEach(([x, y], k) => { marks += both(`<path d="M${x} ${y}l-1.3 1.9" stroke="${k % 2 ? "#6b594d" : "#b9a591"}" stroke-width=".8" stroke-linecap="round"/>`); });
      return `<g transform="translate(0 11)">` + edge + p("M10.5 30C10.5 20.4 20.1 12.6 32 12.6C43.9 12.6 53.5 20.4 53.5 30C53.5 36.5 59 43.5 72 55V72H-8V55C5 43.5 10.5 36.5 10.5 30Z", q) + marks + both(c(21.4, 30.4, 2.9, "#dcc3a6")) +
        p("M42.7 30.6L53.8 72H10.2L21.3 30.6Z", "#cbb59d") + // the belly, facing us under the chin: a colour between the face and the quills
        p("M26 25.6H38Q43 25.9 43 32.6C43 37.4 38 42.6 32 43.8C26 42.6 21 37.4 21 32.6Q21 25.9 26 25.6Z", f) + "</g>"; },
      face: () => `<g transform="translate(0 11)">` + eyes(27, 32.6) + nose(32, 41, 2, 1.5) + cheeks(24.6, 36.6) + "</g>",
      // a small round cherry speared on the quills, off to one side. It gets the same brushwork as the fur, only
      // gentler (the `soft` layer), so it keeps the painted look and stays round; two quill tips stand in front of it
      soft: () => `<g transform="translate(0 11)"><path d="M40.4 17.6C36.6 14.6 36.4 9.6 40.6 5.6C45 9 45.2 14.2 40.4 17.6Z" transform="rotate(24 40.4 12)" fill="#c98a3c"/><path d="M40.4 17.2L40.6 7.4M40.5 13.6l2-1.8M40.5 11l-1.8-1.6" transform="rotate(24 40.4 12)" fill="none" stroke="#9a6426" stroke-width=".5" stroke-linecap="round"/>` + p("M36.6 18.6L38 15.6L39.2 18.6ZM39.8 18.8L41.4 16L42.4 19Z", "#8f7a69") + "</g>",
      over: () => both(e(24.6, 57.2, 3.3, 2.4, "#ecd8be", -10)) },
    cow: { en: "Cow", zh: "小牛", fur: () => { const f = "#e7dfd1", k = "#4a423d", pink = "#eec1b8";
      return body(f, "", "bell", RED, 4) + both(p("M22.4 17.4Q19.4 15 20.4 11.2Q23.6 13 25.4 16Z", "#e8dcc6")) + both(e(16.6, 23.6, 5.6, 3, f, 18) + e(17, 23.8, 3.2, 1.5, pink, 18)) +
        e(32, 28.5, 13.6, 13.4, f) + p("M33.6 15.6C40 15.4 45 20 45.4 26.4C42 28.6 37.4 27.6 35.4 24C34 21.4 33.4 18.4 33.6 15.6Z", k) + e(21.4, 31.4, 2.6, 3.4, k, 12) + e(32, 36.6, 8.4, 5.6, pink) +
        `<g transform="translate(0 -4)">` + e(40.5, 54, 4.2, 3.2, k, -20) + e(23, 58, 3.4, 2.6, k, 15) + "</g>"; },
      face: () => eyes(26.6, 28.2) + c(29.4, 36.6, 0.85, "#b97f78") + c(34.6, 36.6, 0.85, "#b97f78") },
    mouse: { en: "Mouse", zh: "小老鼠", fur: () => { const f = "#b9aea3";
      // a mouse: big round ears set wide, a small face narrowing to a pink nose, long whiskers, a thin tail
      return `<path d="M45 61C53.4 59 55.6 50.6 51.4 46.4C49.6 44.6 47 45.4 47.2 47.6" fill="none" stroke="#e3b3aa" stroke-width="1.7" stroke-linecap="round"/>` +
        body(f, WHITE, "bandana", GOLD, 3) + both(c(17.6, 21, 8.8, f) + c(18, 21.6, 5.7, BLUSH)) +
        p("M32 19.6C39.4 19.6 44.6 24.4 44.6 30.4C44.6 36.4 38.4 41.4 32 43C25.6 41.4 19.4 36.4 19.4 30.4C19.4 24.4 24.6 19.6 32 19.6Z", f) + e(32, 38.4, 4.6, 3.6, WHITE); },
      face: () => eyes(26.4, 30.6) + nose(32, 40, 1.5, 1.15, "#d49a8f") +
        both(`<path d="M27 37.6l-8.4-1.6M27 39.2l-8.6 .9M27.4 40.8l-7.4 3" fill="none" stroke="#fff" stroke-width=".4" stroke-linecap="round" opacity=".9"/>`) + cheeks(24.2, 35) },
    giraffe: { en: "Giraffe", zh: "长颈鹿", fur: () => { const f = "#ecca82", sp = "#bb8853";
      return tall(f, "", "scarf", RED) + [[26.4, 55.6, 2.4], [37, 57, 2.8], [31, 60.6, 2.2], [22, 60.6, 2.2], [42, 61.4, 2]].map(([x, y, r]) => c(x, y, r, sp)).join("") +
        both(`<path d="M27.6 15.6l-1-6.4" fill="none" stroke="${f}" stroke-width="2" stroke-linecap="round"/>` + c(26.4, 8.4, 2, sp)) + both(e(17.4, 22.6, 6, 3, f, 22) + e(17.8, 22.8, 3.6, 1.5, BLUSH, 22)) +
        p("M32 14C39 14 43 19 43 26C43 33.4 38.4 43.4 32 43.4C25.6 43.4 21 33.4 21 26C21 19 25 14 32 14Z", f) + e(32, 38, 6.6, 5, "#f6e6c4") +
        c(24.6, 21.4, 1.9, sp) + c(39.6, 22, 1.7, sp) + c(32, 18.4, 1.8, sp) + c(23.6, 33, 1.5, sp) + c(40.4, 33, 1.5, sp); },
      face: () => eyes(26.2, 27.6, 1.15) + both(`<ellipse cx="29.8" cy="37.4" rx=".7" ry="1" fill="#a9825a"/>`) + `<path d="M29.6 40.2Q32 41.6 34.4 40.2" fill="none" stroke="${DOT}" stroke-width=".5" stroke-linecap="round" opacity=".7"/>` + cheeks(23.6, 30.6) },
    blackdog: { en: "Black dog", zh: "大黑狗", fur: () => { const k = "#3a3532", snout = "#565049";
      // a big, all-black dog: tall pricked ears, a broad skull tapering to a long muzzle, a deep red scarf
      return lean(k, "", "scarf", "#9a3f38", 3) +
        both(p("M20.2 24L19.9 8.2Q25.6 10.6 29.4 17.4Z", k) + p("M21.6 19.4L21.5 12.4Q24.2 13.8 26.2 16.8Z", "#5d5450")) +
        p("M32 15.8C40.2 15.8 45.6 20.8 45.6 27.4C45.6 31.8 41.8 35.6 39 39Q38.4 43.4 32 43.6Q25.6 43.4 25 39C22.2 35.6 18.4 31.8 18.4 27.4C18.4 20.8 23.8 15.8 32 15.8Z", k) +
        p("M32 30.6C35.6 30.6 37.6 34 37.6 37.6C37.6 41.2 35.4 42.8 32 42.8C28.6 42.8 26.4 41.2 26.4 37.6C26.4 34 28.4 30.6 32 30.6Z", snout); },
      face: () => both(`<ellipse cx="26.4" cy="27.8" rx="1.45" ry="1.3" fill="#8fa9bd"/><circle cx="26.5" cy="27.9" r=".7" fill="${DOT}"/><circle cx="26.8" cy="27.5" r=".22" fill="#fff"/><path d="M24.2 25.9L28.6 27.3" fill="none" stroke="#2a2522" stroke-width="1.15" stroke-linecap="round"/>`) +
        nose(32, 36.2, 2.5, 1.7) + `<path d="M29.8 40.3Q32 40.9 34.2 40.3" fill="none" stroke="#2a2522" stroke-width=".55" stroke-linecap="round"/>` },
    wolf: { en: "Wolf", zh: "狼", fur: () => { const f = "#8f8b88", pale = "#e9e4dc";
      // grey and lean-faced, in a navy jacket, with a pale mask over the cheeks and muzzle and a darker streak on the brow
      return lean("#44566b", WHITE, "tie", SAGE, 2.5) + `<g transform="translate(32 0) scale(.86 1) translate(-32 0)">` + both(p("M19.8 23L18.6 9.4Q24 10.6 29 16Z", f) + p("M20.9 18.6L20.4 12.6Q23.2 13.6 25.6 16Z", "#5f5b58")) +
        p("M32 16.9C40.6 16.9 46.8 22 46.8 28.6C46.8 33 41.8 38.8 36.2 42.4Q32 44.4 27.8 42.4C22.2 38.8 17.2 33 17.2 28.6C17.2 22 23.4 16.9 32 16.9Z", f) +
        both(p("M17.4 29.8C21 28.6 26.4 30.6 29 34.6C30.6 37.4 31.6 40.4 32 43.4C25.2 40.4 18.2 34.2 17.4 29.8Z", pale)) + e(32, 21.2, 2.6, 4.4, "#75716e") + "</g>"; },
      // an old scar: one thin, tapering slash down through the brow and cheek, painted under the eye
      soft: () => p("M35.6 21.4Q38.8 27.4 39.1 35.2Q36 28.2 35.6 21.4Z", "#c79c93"),
      face: () => eyes(26.8, 28.4) + nose(32, 39.8, 2.1, 1.5) },
    tuxcat: { en: "Tuxedo cat", zh: "奶牛猫", fur: () => { const k = "#3f3a37";
      // a black-and-white cat: black cap and ears, a white blaze running down between the eyes to a white muzzle and chest
      return `<path d="M43 62C52 60 56.4 50 53.2 42C51.8 38.6 48 38 46.2 40.8" fill="none" stroke="${k}" stroke-width="3.2" stroke-linecap="round"/>` +
        body(k, WHITE, "bow", SAGE, 2.5) + both(p("M18.6 24L17.4 9.6Q23.4 11 29.4 16.6Z", k) + p("M20 19.4L19.4 13Q22.6 14.2 25.4 16.6Z", BLUSH)) +
        e(32, 29.5, 15.4, 12.8, k) + p("M32 18.4C33.6 23 39.4 28.6 40.4 34.4C41 39.4 37 42.2 32 42.2C27 42.2 23 39.4 23.6 34.4C24.6 28.6 30.4 23 32 18.4Z", WHITE); },
      face: () => both(`<ellipse cx="25.6" cy="28.2" rx="1.5" ry="1.6" fill="#c7c26a"/><ellipse cx="25.7" cy="28.3" rx=".6" ry="1.15" fill="${DOT}"/><circle cx="26.1" cy="27.6" r=".25" fill="#fff"/>`) +
        nose(32, 32.9, 1.25, 0.95, "#d49a8f") + smile(32, 33.9, 2.4) + both(`<path d="M24.5 34.2l-6.5-1M24.5 35.8l-6.5 .8" fill="none" stroke="#fff" stroke-width=".4" stroke-linecap="round" opacity=".9"/>`) +
        // half-moon glasses: flat along the top, rounded below, sitting over the eyes
        `<g fill="none" stroke="#d6ab52" stroke-width=".6" stroke-linecap="round" stroke-linejoin="round">` + both(`<path d="M21.8 25.9H29.4A3.8 4.9 0 0 1 21.8 25.9Z" fill="#fffdf7" fill-opacity=".1"/><path d="M21.8 25.9L19.4 25.3"/>`) + `<path d="M29.4 26Q32 25.1 34.6 26"/></g>` },
    capybara: { en: "Capybara", zh: "卡皮巴拉", fur: () => { const f = "#c9a777", dark = "#7d5d44", patch = "#9a7654";
      // head and body are one soft, sand-coloured lump, the face round with full cheeks; small round ears at the top corners; a darker band of fur down the middle of the face, from brow to chin
      return p("M32 15.6C38.6 15.6 43.6 18.6 45.6 23.4C46.6 25.8 49.6 27.8 49.6 32C49.6 36 46.4 37.8 46.2 40.4C46.3 45 52.4 54 52.4 64V76H11.6V64C11.6 54 17.7 45 17.8 40.4C17.6 37.8 14.4 36 14.4 32C14.4 27.8 17.4 25.8 18.4 23.4C20.4 18.6 25.4 15.6 32 15.6Z", f) +
        both(c(22, 17.4, 3.1, f) + c(22.3, 17.8, 1.6, dark)) +
        p("M29.6 23.2H34.4Q37 23.4 37 26.2V35.2Q36.8 38.2 32 38.4Q27.2 38.2 27 35.2V26.2Q27 23.4 29.6 23.2Z", patch); },
      // a mandarin orange balanced on its head
      soft: () => e(32.4, 12.2, 4.5, 4, "#e8953a") + c(30.8, 10.8, 0.9, "#f4c58a") + e(34.6, 8.2, 2.3, 1, "#7f9a6a", -28) + c(32.6, 8.6, 0.55, "#6b7d54"),
      // eyes half shut: two short level strokes, set high and wide
      face: () => both(`<path d="M21.4 24.6H24.8" fill="none" stroke="${DOT}" stroke-width=".85" stroke-linecap="round"/>`) + both(c(30.6, 28.4, 0.55, DOT)) +
        `<path d="M32 31V33.2M30.5 34.2Q32 33 33.5 34.2" fill="none" stroke="${DOT}" stroke-width=".55" stroke-linecap="round"/>` + cheeks(21.4, 31) },
  };
  const KEYS = Object.keys(A);
  let uid = 0;
  function portrait(key, size) {
    const a = A[key] || A[KEYS[0]], id = "rap" + (++uid), n = KEYS.indexOf(key) + 3;
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="${size}" height="${size}" aria-hidden="true">
<defs><clipPath id="${id}c"><circle cx="32" cy="32" r="29.2"/></clipPath>
<filter id="${id}b" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency=".55" numOctaves="2" seed="${n}" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="2.6" xChannelSelector="R" yChannelSelector="G" result="d"/>
<feGaussianBlur in="d" stdDeviation=".22" result="s"/>
<feTurbulence type="fractalNoise" baseFrequency=".9 .5" numOctaves="2" seed="${n + 7}" result="g"/>
<feColorMatrix in="g" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 2.6 -1.5" result="lt"/>
<feComposite in="lt" in2="s" operator="in" result="lts"/>
<feColorMatrix in="g" type="matrix" values="0 0 0 0 .32  0 0 0 0 .25  0 0 0 0 .2  0 0 -2.4 0 .95" result="dk"/>
<feComposite in="dk" in2="s" operator="in" result="dks"/>
<feComponentTransfer in="lts" result="l2"><feFuncA type="linear" slope=".38"/></feComponentTransfer>
<feComponentTransfer in="dks" result="d2"><feFuncA type="linear" slope=".16"/></feComponentTransfer>
<feMerge><feMergeNode in="s"/><feMergeNode in="l2"/><feMergeNode in="d2"/></feMerge></filter>
<filter id="${id}s" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="2" seed="${n + 3}" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale=".9" xChannelSelector="R" yChannelSelector="G" result="d"/>
<feGaussianBlur in="d" stdDeviation=".16" result="s"/>
<feTurbulence type="fractalNoise" baseFrequency=".9 .5" numOctaves="2" seed="${n + 7}" result="g"/>
<feColorMatrix in="g" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 2.6 -1.5" result="lt"/>
<feComposite in="lt" in2="s" operator="in" result="lts"/>
<feComponentTransfer in="lts" result="l2"><feFuncA type="linear" slope=".34"/></feComponentTransfer>
<feMerge><feMergeNode in="s"/><feMergeNode in="l2"/></feMerge></filter>
<filter id="${id}r" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".05" numOctaves="1" seed="${n}" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="1.1"/></filter></defs>
<circle cx="32" cy="32" r="30.4" fill="#fffdf7"/>
<g clip-path="url(#${id}c)"><g transform="translate(32 35) scale(1.13) translate(-32 -35)"><g filter="url(#${id}b)">${a.fur()}</g>${a.soft ? `<g filter="url(#${id}s)">${a.soft()}</g>` : ""}${a.face()}</g></g>
<circle cx="32" cy="32" r="30.2" fill="none" stroke="#b08d57" stroke-width=".7" filter="url(#${id}r)"/>${a.over ? `<g transform="translate(32 35) scale(1.13) translate(-32 -35)" filter="url(#${id}b)">${a.over()}</g>` : ""}</svg>`;
  }
  portrait.keys = KEYS;
  portrait.label = (key, zh) => (A[key] ? (zh ? A[key].zh : A[key].en) : "");
  portrait.pick = (seed) => { let h = 2166136261; for (let i = 0; i < seed.length; i++) { h ^= seed.charCodeAt(i); h = Math.imul(h, 16777619); } return KEYS[(h >>> 0) % KEYS.length]; };
  window.RA_PORTRAIT = portrait;
})();
