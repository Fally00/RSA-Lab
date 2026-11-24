/* ==========================================================================
   RSA-Lab — shared behavior
   Theme, masthead, mobile navigation, folio scroll-spy, paper canvas,
   reveal, statue parallax, copy/toast, and BigInt helpers.
   ========================================================================== */
(function () {
  "use strict";

  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ------------------------------------------------------------------------
     Small math helpers (BigInt, exact)
     ------------------------------------------------------------------------ */
  const absBig = (x) => (x < 0n ? -x : x);

  function gcd(a, b) {
    a = absBig(BigInt(a));
    b = absBig(BigInt(b));
    while (b !== 0n) {
      const t = a % b;
      a = b;
      b = t;
    }
    return a;
  }

  function egcd(a, b) {
    a = BigInt(a);
    b = BigInt(b);
    let oldR = a;
    let r = b;
    let oldS = 1n;
    let s = 0n;
    let oldT = 0n;
    let t = 1n;
    const steps = [];
    while (r !== 0n) {
      const q = oldR / r;
      steps.push({ a: oldR, b: r, q, r: oldR - q * r });
      [oldR, r] = [r, oldR - q * r];
      [oldS, s] = [s, oldS - q * s];
      [oldT, t] = [t, oldT - q * t];
    }
    return { g: oldR, x: oldS, y: oldT, steps };
  }

  function modInv(a, m) {
    a = BigInt(a);
    m = BigInt(m);
    const result = egcd(a, m);
    if (result.g !== 1n) {
      throw new Error(`No modular inverse: gcd(${a}, ${m}) = ${result.g}`);
    }
    return ((result.x % m) + m) % m;
  }

  function modPow(base, exponent, modulus) {
    base = BigInt(base);
    exponent = BigInt(exponent);
    modulus = BigInt(modulus);
    if (modulus <= 0n) throw new Error("Modulus must be positive");
    if (exponent < 0n) throw new Error("Exponent must be non-negative");
    base = ((base % modulus) + modulus) % modulus;
    let result = 1n;
    const trace = [];
    let bitIndex = 0;
    while (exponent > 0n) {
      const bit = exponent & 1n;
      if (bit === 1n) result = (result * base) % modulus;
      trace.push({ bitIndex, bit, base, result });
      base = (base * base) % modulus;
      exponent >>= 1n;
      bitIndex += 1;
    }
    return { result, trace };
  }

  function isqrt(n) {
    n = BigInt(n);
    if (n < 0n) throw new Error("Square root of a negative integer");
    if (n < 2n) return n;
    let x = n;
    let y = (x + 1n) >> 1n;
    while (y < x) {
      x = y;
      y = (x + n / x) >> 1n;
    }
    return x;
  }

  function isPrime(n) {
    n = BigInt(n);
    if (n < 2n) return false;
    const small = [2n, 3n, 5n, 7n, 11n, 13n, 17n, 19n, 23n, 29n, 31n, 37n];
    for (const p of small) {
      if (n === p) return true;
      if (n % p === 0n) return false;
    }
    let d = n - 1n;
    let s = 0n;
    while ((d & 1n) === 0n) {
      d >>= 1n;
      s += 1n;
    }
    const bases = n < 18446744073709551616n
      ? [2n, 325n, 9375n, 28178n, 450775n, 9780504n, 1795265022n]
      : [2n, 3n, 5n, 7n, 11n, 13n, 17n, 19n, 23n, 29n, 31n, 37n];
    for (const a of bases) {
      if (a % n === 0n) continue;
      let x = modPow(a, d, n).result;
      if (x === 1n || x === n - 1n) continue;
      let passed = false;
      for (let r = 1n; r < s; r += 1n) {
        x = (x * x) % n;
        if (x === n - 1n) {
          passed = true;
          break;
        }
      }
      if (!passed) return false;
    }
    return true;
  }

  function factorizeSmall(n, limit = 1000000n) {
    n = absBig(BigInt(n));
    const factors = new Map();
    let d = 2n;
    while (d * d <= n && d <= limit) {
      while (n % d === 0n) {
        factors.set(d, (factors.get(d) || 0n) + 1n);
        n /= d;
      }
      d += d === 2n ? 1n : 2n;
    }
    if (n > 1n) factors.set(n, (factors.get(n) || 0n) + 1n);
    return factors;
  }

  function fermatFactor(n, maxSteps = 25000) {
    n = BigInt(n);
    let a = isqrt(n);
    if (a * a < n) a += 1n;
    for (let step = 0; step < maxSteps; step += 1) {
      const b2 = a * a - n;
      const b = isqrt(b2);
      if (b * b === b2) {
        return { found: true, p: a - b, q: a + b, steps: step + 1 };
      }
      a += 1n;
    }
    return { found: false, steps: maxSteps };
  }

  function wienerAttack(n, e, maxConvergents = 64) {
    n = BigInt(n);
    e = BigInt(e);
    let num = e;
    let den = n;
    let hPrev2 = 0n;
    let hPrev1 = 1n;
    let kPrev2 = 1n;
    let kPrev1 = 0n;
    const convergents = [];

    for (let index = 0; index < maxConvergents && den !== 0n; index += 1) {
      const a = num / den;
      const h = a * hPrev1 + hPrev2;
      const k = a * kPrev1 + kPrev2;
      convergents.push({ index, h, k });

      if (h !== 0n && k !== 0n) {
        const numerator = e * k - 1n;
        if (numerator % h === 0n) {
          const phi = numerator / h;
          const s = n - phi + 1n;
          const discriminant = s * s - 4n * n;
          if (discriminant >= 0n) {
            const root = isqrt(discriminant);
            if (root * root === discriminant && (s + root) % 2n === 0n) {
              const p = (s + root) / 2n;
              const q = (s - root) / 2n;
              if (p * q === n && p > 1n && q > 1n) {
                return { found: true, p, q, d: k, index, convergents };
              }
            }
          }
        }
      }

      hPrev2 = hPrev1;
      hPrev1 = h;
      kPrev2 = kPrev1;
      kPrev1 = k;
      const remainder = num % den;
      num = den;
      den = remainder;
    }

    return { found: false, convergents };
  }

  const bitLength = (n) => BigInt(n).toString(2).length;

  function toHex(n) {
    const value = BigInt(n);
    return "0x" + (value < 0n ? "-" : "") + absBig(value).toString(16).toUpperCase();
  }

  function parseBig(value) {
    const cleaned = String(value).trim().replace(/[\s_,:]/g, "");
    if (!cleaned) throw new Error("Enter an integer");
    if (/^-?0x[0-9a-f]+$/i.test(cleaned)) return BigInt(cleaned);
    if (/^-?\d+$/.test(cleaned)) return BigInt(cleaned);
    throw new Error("Use a decimal integer or a 0x-prefixed hex value");
  }

  function truncateMiddle(value, head = 18, tail = 14) {
    const text = String(value);
    if (text.length <= head + tail + 1) return text;
    return `${text.slice(0, head)}…${text.slice(-tail)}`;
  }

  function formatInt(value) {
    try {
      return BigInt(value).toLocaleString("en-US");
    } catch {
      return String(value);
    }
  }

  const math = {
    absBig,
    gcd,
    egcd,
    modInv,
    modPow,
    isqrt,
    isPrime,
    factorizeSmall,
    fermatFactor,
    wienerAttack,
    bitLength,
    toHex,
    parseBig,
    truncateMiddle,
    formatInt,
  };

  /* ------------------------------------------------------------------------
     Toast
     ------------------------------------------------------------------------ */
  let toastTimer = 0;

  function ensureToast() {
    let toast = $("#lab-toast");
    if (toast) return toast;
    toast = document.createElement("div");
    toast.id = "lab-toast";
    toast.className = "toast";
    toast.setAttribute("role", "status");
    toast.setAttribute("aria-live", "polite");
    toast.innerHTML =
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg><span data-toast-message></span>';
    document.body.appendChild(toast);
    return toast;
  }

  function showToast(message, tone = "default") {
    const toast = ensureToast();
    toast.dataset.tone = tone;
    $("[data-toast-message]", toast).textContent = message;
    toast.classList.add("is-visible");
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => toast.classList.remove("is-visible"), 2800);
  }

  /* ------------------------------------------------------------------------
     Copy + download
     ------------------------------------------------------------------------ */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise((resolve, reject) => {
      const area = document.createElement("textarea");
      area.value = text;
      area.setAttribute("readonly", "");
      area.style.position = "fixed";
      area.style.opacity = "0";
      document.body.appendChild(area);
      area.select();
      try {
        document.execCommand("copy");
        resolve();
      } catch (error) {
        reject(error);
      } finally {
        area.remove();
      }
    });
  }

  function initCopyButtons() {
    document.addEventListener("click", (event) => {
      const button = event.target.closest("[data-copy]");
      if (!button) return;
      const value = button.getAttribute("data-copy");
      const label = button.querySelector("[data-copy-label]");
      const original = label ? label.textContent : "";
      copyText(value || "")
        .then(() => {
          showToast("Copied to clipboard", "safe");
          if (label) {
            label.textContent = "Copied";
            window.setTimeout(() => {
              label.textContent = original;
            }, 1200);
          }
        })
        .catch(() => showToast("Clipboard unavailable", "danger"));
    });
  }

  function download(filename, content, mime = "text/plain") {
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  /* ------------------------------------------------------------------------
     Theme
     ------------------------------------------------------------------------ */
  function currentTheme() {
    return document.documentElement.dataset.theme === "dark" ? "dark" : "light";
  }

  function applyTheme(theme, persist = true) {
    document.documentElement.dataset.theme = theme;
    if (persist) {
      try {
        localStorage.setItem("rsa-lab-theme", theme);
      } catch {
        /* storage can be unavailable */
      }
    }
    $$("[data-theme-toggle]").forEach((button) => {
      button.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
      button.setAttribute("aria-label", theme === "dark" ? "Switch to light theme" : "Switch to dark theme");
    });
    document.dispatchEvent(new CustomEvent("themechange", { detail: { theme } }));
  }

  function initTheme() {
    applyTheme(currentTheme(), false);
    $$("[data-theme-toggle]").forEach((button) => {
      button.addEventListener("click", () => {
        applyTheme(currentTheme() === "dark" ? "light" : "dark");
      });
    });
  }

  /* ------------------------------------------------------------------------
     Masthead + mobile menu
     ------------------------------------------------------------------------ */
  function initMasthead() {
    const masthead = $(".masthead");
    const toggle = $("[data-mobile-toggle]");
    const menu = $("[data-mobile-menu]");
    if (!masthead) return;

    const onScroll = () => masthead.classList.toggle("is-scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });

    if (!toggle || !menu) return;

    const setOpen = (open) => {
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      menu.classList.toggle("is-open", open);
      document.body.classList.toggle("menu-open", open);
    };

    toggle.addEventListener("click", () => {
      setOpen(!menu.classList.contains("is-open"));
    });

    $$("a", menu).forEach((link) => link.addEventListener("click", () => setOpen(false)));

    document.addEventListener("click", (event) => {
      if (!menu.classList.contains("is-open")) return;
      if (menu.contains(event.target) || toggle.contains(event.target)) return;
      setOpen(false);
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && menu.classList.contains("is-open")) {
        setOpen(false);
        toggle.focus();
      }
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 900 && menu.classList.contains("is-open")) setOpen(false);
    });
  }

  /* ------------------------------------------------------------------------
     Paper canvas
     ------------------------------------------------------------------------ */
  function hexToRgb(hex) {
    const value = hex.trim().replace("#", "");
    const full = value.length === 3 ? value.split("").map((c) => c + c).join("") : value;
    const num = Number.parseInt(full, 16);
    if (Number.isNaN(num)) return { r: 18, g: 18, b: 18 };
    return { r: (num >> 16) & 255, g: (num >> 8) & 255, b: num & 255 };
  }

  function cssVar(name, fallback) {
    const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return value || fallback;
  }

  function initCanvas() {
    const canvas = $("#math-canvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    const full = document.body.dataset.bg !== "quiet";

    const draw = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const width = window.innerWidth;
      const height = window.innerHeight;
      canvas.width = Math.floor(width * dpr);
      canvas.height = Math.floor(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, width, height);

      const ink = hexToRgb(cssVar("--ink", "#121212"));
      const crimson = hexToRgb(cssVar("--crimson", "#8b1e24"));
      const dark = currentTheme() === "dark";
      const gridAlpha = dark ? 0.055 : 0.045;

      ctx.strokeStyle = `rgba(${ink.r}, ${ink.g}, ${ink.b}, ${gridAlpha})`;
      ctx.lineWidth = 1;
      const step = 48;
      for (let x = 0; x < width; x += step) {
        ctx.beginPath();
        ctx.moveTo(x + 0.5, 0);
        ctx.lineTo(x + 0.5, height);
        ctx.stroke();
      }
      for (let y = 0; y < height; y += step) {
        ctx.beginPath();
        ctx.moveTo(0, y + 0.5);
        ctx.lineTo(width, y + 0.5);
        ctx.stroke();
      }

      if (!full) return;

      // Prime-density plot in the lower right margin.
      const originX = width * 0.62;
      const originY = height * 0.8;
      if (width > 760) {
        ctx.save();
        ctx.strokeStyle = `rgba(${crimson.r}, ${crimson.g}, ${crimson.b}, ${dark ? 0.22 : 0.16})`;
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        for (let i = 10; i < 380; i += 4) {
          const px = originX + i;
          const py = originY - (i / Math.log(i + 12)) * 2.4;
          if (i === 10) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        }
        ctx.stroke();
        ctx.strokeStyle = `rgba(${ink.r}, ${ink.g}, ${ink.b}, ${dark ? 0.1 : 0.08})`;
        ctx.beginPath();
        ctx.moveTo(originX, originY - 220);
        ctx.lineTo(originX, originY);
        ctx.lineTo(originX + 400, originY);
        ctx.stroke();
        ctx.restore();
      }

      const equations = [
        ["φ(N) = (p − 1)(q − 1)", 0.08, 0.24],
        ["a^φ(n) ≡ 1 (mod n)", 0.72, 0.2],
        ["gcd(a, b) = ax + by = 1", 0.12, 0.7],
        ["x² − N = y²  →  (x − y)(x + y) = N", 0.64, 0.86],
        ["π(x) ~ x / ln(x)", 0.82, 0.58],
        ["c ≡ m^e (mod N)", 0.16, 0.9],
      ];

      ctx.save();
      ctx.font = 'italic 15px "Cormorant Garamond", Georgia, serif';
      ctx.fillStyle = `rgba(${ink.r}, ${ink.g}, ${ink.b}, ${dark ? 0.16 : 0.13})`;
      equations.forEach(([text, x, y]) => {
        if (width < 760 && x > 0.5) return;
        ctx.fillText(text, width * x, height * y);
      });
      ctx.restore();
    };

    draw();
    let frame = 0;
    window.addEventListener("resize", () => {
      window.cancelAnimationFrame(frame);
      frame = window.requestAnimationFrame(draw);
    });
    document.addEventListener("themechange", draw);
  }

  /* ------------------------------------------------------------------------
     Statue parallax
     ------------------------------------------------------------------------ */
  function initStatue() {
    const stage = $("#statue-stage");
    const card = $("#statue-card");
    if (!stage || !card) return;
    if (reduceMotion || !window.matchMedia("(pointer: fine)").matches) return;

    let frame = 0;
    let targetX = 0;
    let targetY = 0;
    let currentX = 0;
    let currentY = 0;

    const render = () => {
      currentX += (targetX - currentX) * 0.12;
      currentY += (targetY - currentY) * 0.12;
      card.style.transform = `rotateY(${currentX.toFixed(2)}deg) rotateX(${currentY.toFixed(2)}deg)`;
      if (Math.abs(targetX - currentX) > 0.02 || Math.abs(targetY - currentY) > 0.02) {
        frame = window.requestAnimationFrame(render);
      } else {
        frame = 0;
      }
    };

    window.addEventListener("mousemove", (event) => {
      const rect = stage.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      const deltaX = (event.clientX - centerX) / Math.max(window.innerWidth / 2, 1);
      const deltaY = (event.clientY - centerY) / Math.max(window.innerHeight / 2, 1);
      targetX = Math.max(-9, Math.min(9, deltaX * 7));
      targetY = Math.max(-7, Math.min(7, -deltaY * 5));
      if (!frame) frame = window.requestAnimationFrame(render);
    });

    document.addEventListener("mouseleave", () => {
      targetX = 0;
      targetY = 0;
      if (!frame) frame = window.requestAnimationFrame(render);
    });
  }

  /* ------------------------------------------------------------------------
     Reveal
     ------------------------------------------------------------------------ */
  function initReveal() {
    const items = $$("[data-reveal]");
    if (!items.length) return;
    if (reduceMotion || !("IntersectionObserver" in window)) {
      items.forEach((item) => item.classList.add("is-visible"));
      return;
    }
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.1, rootMargin: "0px 0px -6% 0px" },
    );
    items.forEach((item) => observer.observe(item));
  }

  /* ------------------------------------------------------------------------
     Scroll spy
     ------------------------------------------------------------------------ */
  function initScrollSpy() {
    const sections = $$("[data-spy]");
    if (!sections.length) return;
    const links = $$(".folio-rail a, .subindex a, .mobile-menu__sections a");
    if (!links.length) return;
    let frame = 0;

    const update = () => {
      frame = 0;
      const masthead = $(".masthead");
      const offset = (masthead ? masthead.offsetHeight : 64) + 80;
      const y = window.scrollY + offset;
      let current = sections[0].id;
      sections.forEach((section) => {
        const top = section.getBoundingClientRect().top + window.scrollY;
        if (top <= y) current = section.id;
      });
      links.forEach((link) => {
        const active = link.getAttribute("href") === `#${current}`;
        link.classList.toggle("is-active", active);
        if (active) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      });
    };

    const request = () => {
      if (frame) return;
      frame = window.requestAnimationFrame(update);
    };

    update();
    window.addEventListener("scroll", request, { passive: true });
    window.addEventListener("resize", request);
  }

  /* ------------------------------------------------------------------------
     Tabs + accordions
     ------------------------------------------------------------------------ */
  function initTabs() {
    $$("[data-tabs]").forEach((group) => {
      const tabs = $$('[role="tab"]', group);
      const panels = tabs
        .map((tab) => document.getElementById(tab.getAttribute("aria-controls")))
        .filter(Boolean);

      const activate = (tab) => {
        tabs.forEach((item) => {
          const selected = item === tab;
          item.setAttribute("aria-selected", selected ? "true" : "false");
          item.tabIndex = selected ? 0 : -1;
        });
        panels.forEach((panel) => {
          panel.hidden = panel.id !== tab.getAttribute("aria-controls");
        });
        const onChange = group.getAttribute("data-tab-change");
        if (onChange && typeof window[onChange] === "function") window[onChange](tab.dataset.tab);
      };

      tabs.forEach((tab, index) => {
        tab.addEventListener("click", () => activate(tab));
        tab.addEventListener("keydown", (event) => {
          if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
          event.preventDefault();
          const direction = event.key === "ArrowRight" ? 1 : -1;
          const next = tabs[(index + direction + tabs.length) % tabs.length];
          next.focus();
          activate(next);
        });
      });
    });
  }

  function initAccordions() {
    $$("[data-accordion-toggle]").forEach((button) => {
      const target = document.getElementById(button.getAttribute("aria-controls"));
      if (!target) return;
      button.addEventListener("click", () => {
        const open = button.getAttribute("aria-expanded") === "true";
        button.setAttribute("aria-expanded", open ? "false" : "true");
        target.hidden = open;
      });
    });
  }

  /* ------------------------------------------------------------------------
     Misc
     ------------------------------------------------------------------------ */
  function initMisc() {
    $$("[data-year]").forEach((node) => {
      node.textContent = String(new Date().getFullYear());
    });
  }

  /* ------------------------------------------------------------------------
     Boot
     ------------------------------------------------------------------------ */
  function boot() {
    initTheme();
    initMasthead();
    initCanvas();
    initStatue();
    initReveal();
    initScrollSpy();
    initTabs();
    initAccordions();
    initCopyButtons();
    initMisc();
  }

  window.RSALab = {
    $,
    $$,
    math,
    showToast,
    copyText,
    download,
    applyTheme,
    currentTheme,
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
