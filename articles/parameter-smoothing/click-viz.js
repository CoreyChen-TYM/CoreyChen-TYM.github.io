/* Waveform view linked to an <audio> player.
 * When playback reaches the gain change, the change point lights up:
 * red "click!" for the hard step, green "no cliff" for the smoothed version.
 * Data comes from click-data.js (window.CLICK_DATA). */
(function () {
var FLASH_MS = 1100;
var WAVE = '#4a6cd4';
var STYLES = {
  step:   { rgb: '229,72,61', label: 'click!' },
  smooth: { rgb: '46,160,90', label: 'no cliff' }
};

function setup(root) {
  var DATA = window.CLICK_DATA && window.CLICK_DATA[root.getAttribute('data-set')];
  if (!DATA) return;
  var style = STYLES[root.getAttribute('data-set')] || STYLES.step;
  var hot = 'rgb(' + style.rgb + ')';
  var audio = root.querySelector('audio');
  var overview = root.querySelector('.click-overview');
  var zoom = root.querySelector('.click-zoom');
  var jumpT = DATA.jump / DATA.rate;
  var duration = DATA.frames / DATA.rate;
  var flashStart = -Infinity;
  var prevT = 0;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function prep(canvas) {
    var dpr = window.devicePixelRatio || 1;
    var w = canvas.clientWidth, h = canvas.clientHeight;
    if (canvas.width !== Math.round(w * dpr) || canvas.height !== Math.round(h * dpr)) {
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
    }
    var ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    return { ctx: ctx, w: w, h: h };
  }

  function axis(ctx, w, mid) {
    ctx.strokeStyle = 'rgba(0,0,0,0.25)';
    ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(0, mid + 0.5); ctx.lineTo(w, mid + 0.5); ctx.stroke();
  }

  function drawOverview(glow) {
    var c = prep(overview), ctx = c.ctx, w = c.w, h = c.h, mid = h / 2, amp = h / 2 - 4;
    axis(ctx, w, mid);
    ctx.fillStyle = WAVE;
    var n = DATA.env.length;
    for (var i = 0; i < n; i++) {
      var x = i * w / n, bw = Math.max(1, w / n + 0.5);
      var lo = DATA.env[i][0], hi = DATA.env[i][1];
      ctx.fillRect(x, mid - hi * amp, bw, (hi - lo) * amp);
    }
    var jx = jumpT / duration * w;
    if (glow > 0) {
      ctx.fillStyle = 'rgba(' + style.rgb + ',' + (0.35 * glow) + ')';
      ctx.fillRect(jx - 10, 0, 20, h);
    }
    ctx.strokeStyle = hot; ctx.lineWidth = 1; ctx.globalAlpha = 0.4 + 0.6 * glow; ctx.setLineDash([3, 3]);
    ctx.beginPath(); ctx.moveTo(jx + 0.5, 0); ctx.lineTo(jx + 0.5, h); ctx.stroke();
    ctx.setLineDash([]); ctx.globalAlpha = 1;
    var px = Math.min(audio.currentTime / duration, 1) * w;
    ctx.strokeStyle = '#111'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(px, 0); ctx.lineTo(px, h); ctx.stroke();
  }

  function drawZoom(glow) {
    var c = prep(zoom), ctx = c.ctx, w = c.w, h = c.h, mid = h / 2, amp = h / 2 - 14;
    axis(ctx, w, mid);
    var z = DATA.zoom, n = z.length, k = DATA.jump - DATA.zoomStart;
    function X(i) { return i / (n - 1) * w; }
    function Y(v) { return mid - v * amp; }
    ctx.strokeStyle = WAVE; ctx.lineWidth = 2; ctx.lineJoin = 'round';
    ctx.beginPath();
    for (var i = 0; i < n; i++) { if (i) ctx.lineTo(X(i), Y(z[i])); else ctx.moveTo(X(i), Y(z[i])); }
    ctx.stroke();
    var x0 = X(k - 1), y0 = Y(z[k - 1]), x1 = X(k), y1 = Y(z[k]);
    var cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    if (glow > 0) {
      var r = 18 + (reduce ? 0 : 22 * (1 - glow));
      var g = ctx.createRadialGradient(cx, cy, 0, cx, cy, r);
      g.addColorStop(0, 'rgba(' + style.rgb + ',' + (0.55 * glow) + ')');
      g.addColorStop(1, 'rgba(' + style.rgb + ',0)');
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fill();
      ctx.strokeStyle = hot; ctx.globalAlpha = glow; ctx.lineWidth = 4;
      ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke();
      ctx.font = '600 14px system-ui, sans-serif'; ctx.fillStyle = hot; ctx.textAlign = 'left';
      ctx.fillText(style.label, cx + 12, Math.max(14, Math.min(y0, y1) - 6));
      ctx.globalAlpha = 1;
    }
    ctx.font = '12px system-ui, sans-serif'; ctx.fillStyle = 'rgba(0,0,0,0.55)';
    ctx.textAlign = 'left';  ctx.fillText((DATA.zoomStart / DATA.rate).toFixed(4) + ' s', 4, h - 4);
    ctx.textAlign = 'right'; ctx.fillText(((DATA.zoomStart + n - 1) / DATA.rate).toFixed(4) + ' s', w - 4, h - 4);
  }

  function glowNow() {
    var e = performance.now() - flashStart;
    return e >= 0 && e < FLASH_MS ? 1 - e / FLASH_MS : 0;
  }

  var running = false;
  function kick() { if (!running) { running = true; requestAnimationFrame(frame); } }

  function frame() {
    running = false;
    var t = audio.currentTime;
    if (prevT < jumpT && t >= jumpT && t - jumpT < 0.25) flashStart = performance.now();
    prevT = t;
    var g = glowNow();
    drawOverview(g); drawZoom(g);
    if (!audio.paused || g > 0) kick();
  }

  audio.addEventListener('play', function () { prevT = audio.currentTime; kick(); });
  audio.addEventListener('seeked', function () { prevT = audio.currentTime; kick(); });
  window.addEventListener('resize', kick);
  kick();
}

function init() {
  var roots = document.querySelectorAll('.click-viz');
  for (var i = 0; i < roots.length; i++) setup(roots[i]);
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
else init();
})();
