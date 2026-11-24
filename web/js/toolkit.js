/* ==========================================================================
   RSA-Lab — Mathematical Toolkit
   Eleven exact BigInt operations with constructive derivations.
   ========================================================================== */
(function () {
  "use strict";

  const Lab = window.RSALab;
  if (!Lab) return;
  const { $, $$, math, showToast } = Lab;
  const { absBig, gcd, egcd, modInv, modPow, isqrt, isPrime, factorizeSmall, fermatFactor, parseBig, bitLength } = math;

  const OPS = {
    gcd: {
      num: "01",
      rubric: "Operation 01 / Arithmetic",
      title: "Greatest Common Divisor",
      desc: "Compute <code>gcd(a, b)</code> by repeated Euclidean division until the remainder vanishes.",
      mode: "pair",
      defaults: { a: "240", b: "46" },
    },
    lcm: {
      num: "02",
      rubric: "Operation 02 / Arithmetic",
      title: "Least Common Multiple",
      desc: "Derive <code>lcm(a, b) = |a·b| / gcd(a, b)</code> from the same Euclidean chain.",
      mode: "pair",
      defaults: { a: "240", b: "46" },
    },
    egcd: {
      num: "03",
      rubric: "Operation 03 / Bézout Identity",
      title: "Extended Euclidean Algorithm",
      desc: "Find integers <code>x, y</code> satisfying <code>a·x + b·y = gcd(a, b)</code>.",
      mode: "pair",
      defaults: { a: "240", b: "46" },
    },
    modinv: {
      num: "04",
      rubric: "Operation 04 / Ring Inverses",
      title: "Modular Multiplicative Inverse",
      desc: "Solve <code>a·x ≡ 1 (mod m)</code> when <code>gcd(a, m) = 1</code>.",
      mode: "modinv",
      defaults: { a: "17", m: "3120" },
    },
    modexp: {
      num: "05",
      rubric: "Operation 05 / Binary Exponentiation",
      title: "Modular Exponentiation",
      desc: "Evaluate <code>a<sup>e</sup> mod m</code> by right-to-left square-and-multiply.",
      mode: "modexp",
      defaults: { base: "7", exponent: "2753", modulus: "3233" },
    },
    crt: {
      num: "06",
      rubric: "Operation 06 / Simultaneous Congruences",
      title: "Chinese Remainder Theorem",
      desc: "Reconstruct <code>x (mod m₁m₂)</code> from <code>x ≡ a₁ (mod m₁)</code> and <code>x ≡ a₂ (mod m₂)</code>.",
      mode: "crt",
      defaults: { a1: "2", m1: "3", a2: "3", m2: "5" },
    },
    totient: {
      num: "07",
      rubric: "Operation 07 / Group Order",
      title: "Euler's Totient Function",
      desc: "Compute <code>φ(n) = n ∏ (1 − 1/p)</code> over the distinct prime factors of <code>n</code>.",
      mode: "single",
      label: "Integer n",
      defaultN: "3233",
    },
    "rsa-rel": {
      num: "08",
      rubric: "Operation 08 / Keypair Synthesis",
      title: "RSA Parameter Relationships",
      desc: "Derive <code>N = p·q</code>, <code>φ(N) = (p−1)(q−1)</code>, and <code>d ≡ e⁻¹ (mod φ(N))</code>.",
      mode: "rsa",
      defaults: { p: "61", q: "53", e: "17" },
    },
    primality: {
      num: "09",
      rubric: "Operation 09 / Primality Certification",
      title: "Miller–Rabin Primality Test",
      desc: "Decompose <code>n − 1 = 2<sup>s</sup>·d</code> and test strong probable-prime witnesses.",
      mode: "single",
      label: "Candidate integer n",
      defaultN: "104729",
    },
    factor: {
      num: "10",
      rubric: "Operation 10 / Integer Factorization",
      title: "Fermat & Trial Factorization",
      desc: "Factor composite <code>N</code> by searching for <code>a² − N = b²</code> above <code>⌈√N⌉</code>.",
      mode: "single",
      label: "Composite modulus N",
      defaultN: "3233",
    },
    cf: {
      num: "11",
      rubric: "Operation 11 / Diophantine Approximation",
      title: "Continued Fractions & Convergents",
      desc: "Expand <code>a/b = [a₀; a₁, a₂, …]</code> and compute its convergents <code>hₖ/kₖ</code>.",
      mode: "pair",
      defaults: { a: "17993", b: "90581" },
    },
  };

  const state = { op: "gcd" };

  /* ------------------------------------------------------------------------
     Small rendering helpers
     ------------------------------------------------------------------------ */
  const escapeHTML = (value) =>
    String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));

  const formula = (text) => `<span class="formula-line">${text}</span>`;

  const step = (title, body) => ({ title, body });

  function field(id, label, value) {
    return `<div class="field"><label for="${id}">${label}</label><input class="input" id="${id}" type="text" value="${value}" spellcheck="false" autocomplete="off"></div>`;
  }

  function renderInputs(meta) {
    const wrap = $("#op-inputs");
    if (!wrap) return;

    if (meta.mode === "pair") {
      wrap.innerHTML = `<div class="op-input-grid">${field("in-a", "Integer a", meta.defaults.a)}${field("in-b", "Integer b", meta.defaults.b)}</div>`;
      return;
    }

    if (meta.mode === "modinv") {
      wrap.innerHTML = `<div class="op-input-grid">${field("in-a", "Integer a", meta.defaults.a)}${field("in-m", "Modulus m", meta.defaults.m)}</div>`;
      return;
    }

    if (meta.mode === "modexp") {
      wrap.innerHTML = `<div class="op-input-grid">${field("in-base", "Base a", meta.defaults.base)}${field("in-exponent", "Exponent e", meta.defaults.exponent)}</div>${field("in-modulus", "Modulus m", meta.defaults.modulus)}`;
      return;
    }

    if (meta.mode === "crt") {
      wrap.innerHTML = `<div class="op-input-grid">${field("in-a1", "Residue a₁", meta.defaults.a1)}${field("in-m1", "Modulus m₁", meta.defaults.m1)}${field("in-a2", "Residue a₂", meta.defaults.a2)}${field("in-m2", "Modulus m₂", meta.defaults.m2)}</div>`;
      return;
    }

    if (meta.mode === "rsa") {
      wrap.innerHTML = `<div class="op-input-grid">${field("in-p", "Prime p", meta.defaults.p)}${field("in-q", "Prime q", meta.defaults.q)}</div>${field("in-e", "Public exponent e", meta.defaults.e)}`;
      return;
    }

    wrap.innerHTML = field("in-n", meta.label || "Integer n", meta.defaultN || "3233");
  }

  function readInputs(meta) {
    if (meta.mode === "pair") {
      return { a: parseBig($("#in-a").value), b: parseBig($("#in-b").value) };
    }
    if (meta.mode === "modinv") {
      return { a: parseBig($("#in-a").value), m: parseBig($("#in-m").value) };
    }
    if (meta.mode === "modexp") {
      return {
        base: parseBig($("#in-base").value),
        exponent: parseBig($("#in-exponent").value),
        modulus: parseBig($("#in-modulus").value),
      };
    }
    if (meta.mode === "crt") {
      return {
        a1: parseBig($("#in-a1").value),
        m1: parseBig($("#in-m1").value),
        a2: parseBig($("#in-a2").value),
        m2: parseBig($("#in-m2").value),
      };
    }
    if (meta.mode === "rsa") {
      return { p: parseBig($("#in-p").value), q: parseBig($("#in-q").value), e: parseBig($("#in-e").value) };
    }
    return { n: parseBig($("#in-n").value) };
  }

  function setDerivStatus(text) {
    const node = $("#deriv-status");
    if (node) node.textContent = text;
  }

  function emptyDerivation() {
    const content = $("#deriv-content");
    if (content) {
      content.innerHTML =
        '<div class="derivation-empty">Choose an operation, enter integers, and execute to inspect the exact derivation.</div>';
    }
    setDerivStatus("Awaiting input");
  }

  function renderSteps(steps) {
    const content = $("#deriv-content");
    if (!content) return;
    content.innerHTML = steps
      .map(
        (item, index) => `<div class="derivation-step">
          <div class="derivation-step__label">Step ${String(index + 1).padStart(2, "0")} · ${item.title}</div>
          <div class="derivation-step__body">${item.body}</div>
        </div>`,
      )
      .join("");
  }

  function hideResult() {
    const box = $("#result-box");
    if (box) box.hidden = true;
    const copy = $("#copy-result");
    if (copy) {
      copy.disabled = true;
      copy.setAttribute("data-copy", "");
    }
  }

  function showResult(value, meta) {
    const box = $("#result-box");
    const valueNode = $("#result-value");
    const metaNode = $("#result-meta");
    const copy = $("#copy-result");
    if (box) box.hidden = false;
    if (valueNode) valueNode.textContent = value;
    if (metaNode) metaNode.textContent = meta || "Exact BigInt";
    if (copy) {
      copy.disabled = false;
      copy.setAttribute("data-copy", value);
    }
  }

  function clearResult() {
    hideResult();
    emptyDerivation();
  }

  /* ------------------------------------------------------------------------
     Operations
     ------------------------------------------------------------------------ */
  function runGcd({ a, b }) {
    const A = absBig(a);
    const B = absBig(b);
    const res = egcd(A, B);
    const steps = [
      step(
        "Euclidean division",
        formula("rₖ₋₁ = rₖ · qₖ + rₖ₊₁") +
          "<p>Apply repeated division until the remainder vanishes. The last non-zero remainder is the GCD.</p>",
      ),
      ...res.steps.slice(0, 8).map((item) => step("Division step", formula(`${item.a} = ${item.b} · ${item.q} + ${item.r}`))),
      step("Greatest common divisor", formula(`gcd(${A}, ${B}) = ${res.g}`)),
    ];
    if (res.steps.length > 8) {
      steps.splice(9, 0, step("Remaining steps", `<p>${res.steps.length - 8} further divisions are omitted for readability; the recurrence is identical.</p>`));
    }
    return { value: res.g.toString(), meta: `gcd(${A}, ${B})`, steps };
  }

  function runLcm({ a, b }) {
    const A = absBig(a);
    const B = absBig(b);
    const res = egcd(A, B);
    const lcm = res.g === 0n ? 0n : (A * B) / res.g;
    return {
      value: lcm.toString(),
      meta: `lcm(${A}, ${B})`,
      steps: [
        step(
          "Euclidean chain",
          formula(`gcd(${A}, ${B}) = ${res.g}`) + "<p>The same Euclidean chain that computes the GCD also supplies the denominator of the LCM identity.</p>",
        ),
        step("LCM identity", formula(`lcm(a, b) = |a · b| / gcd(a, b)`) + formula(`lcm(${A}, ${B}) = (${A} · ${B}) / ${res.g} = ${lcm}`)),
        step("Verification", formula(`${res.g} · ${lcm} = ${A} · ${B}`)),
      ],
    };
  }

  function runEgcd({ a, b }) {
    const res = egcd(a, b);
    const steps = [
      step("Bézout identity", formula(`Find x, y such that ${a}·x + ${b}·y = gcd(${a}, ${b}).`)),
      ...res.steps.slice(0, 8).map((item) => step("Quotient reduction", formula(`${item.a} = ${item.b} · ${item.q} + ${item.r}`))),
      step("Linear combination", formula(`${a}(${res.x}) + ${b}(${res.y}) = ${res.g}`)),
    ];
    if (res.steps.length > 8) {
      steps.splice(9, 0, step("Remaining steps", `<p>${res.steps.length - 8} further reductions are omitted for readability.</p>`));
    }
    return { value: `gcd = ${res.g} · x = ${res.x} · y = ${res.y}`, meta: `Bézout coefficients for (${a}, ${b})`, steps };
  }

  function runModinv({ a, m }) {
    if (m <= 1n) throw new Error("Modulus must exceed 1.");
    const g = gcd(a, m);
    if (g !== 1n) {
      return {
        value: `No inverse · gcd(${a}, ${m}) = ${g}`,
        meta: "Non-invertible residue",
        steps: [
          step("Invertibility criterion", formula(`a is a unit modulo m ⇔ gcd(a, m) = 1.`)),
          step("Obstruction", formula(`gcd(${a}, ${m}) = ${g} > 1`) + "<p>No integer x can satisfy the congruence; the residue is a zero divisor.</p>"),
        ],
      };
    }
    const res = egcd(a, m);
    const inv = ((res.x % m) + m) % m;
    return {
      value: inv.toString(),
      meta: `${a}⁻¹ mod ${m}`,
      steps: [
        step("Coprimality verified", formula(`gcd(${a}, ${m}) = 1`)),
        step("Bézout coefficient", formula(`${a}(${res.x}) + ${m}(${res.y}) = 1`)),
        step("Canonical residue", formula(`${a}⁻¹ ≡ ${inv} (mod ${m})`)),
        step("Verification", formula(`${a} · ${inv} ≡ 1 (mod ${m})`)),
      ],
    };
  }

  function runModexp({ base, exponent, modulus }) {
    if (exponent < 0n) throw new Error("Exponent must be non-negative.");
    if (modulus <= 1n) throw new Error("Modulus must exceed 1.");
    const res = modPow(base, exponent, modulus);
    const steps = [
      step(
        "Binary decomposition",
        formula(`e = ${exponent} = (${exponent.toString(2)})₂`) +
          "<p>Scan the exponent from least significant bit to most significant bit, squaring the base at each step.</p>",
      ),
      ...res.trace.slice(0, 8).map((item) =>
        step(
          `Bit ${item.bitIndex} · b = ${item.bit}`,
          formula(`base ≡ ${item.base} (mod ${modulus}) · accumulator ≡ ${item.result} (mod ${modulus})`),
        ),
      ),
      step("Final congruence", formula(`${base}^${exponent} ≡ ${res.result} (mod ${modulus})`)),
    ];
    if (res.trace.length > 8) {
      steps.splice(9, 0, step("Remaining bits", `<p>${res.trace.length - 8} further bit operations are omitted; the square-and-multiply recurrence is identical.</p>`));
    }
    return { value: res.result.toString(), meta: `${base}^${exponent} mod ${modulus}`, steps };
  }

  function runCrt({ a1, m1, a2, m2 }) {
    if (m1 <= 0n || m2 <= 0n) throw new Error("Moduli must be positive.");
    const g = gcd(m1, m2);
    if ((a2 - a1) % g !== 0n) {
      return {
        value: "No solution",
        meta: "Inconsistent congruence system",
        steps: [
          step("Compatibility criterion", formula(`x ≡ a₁ (mod m₁) and x ≡ a₂ (mod m₂) is solvable ⇔ a₁ ≡ a₂ (mod gcd(m₁, m₂)).`)),
          step("Obstruction", formula(`a₁ − a₂ = ${a1 - a2} is not divisible by gcd(${m1}, ${m2}) = ${g}.`)),
        ],
      };
    }
    const modulus = absBig((m1 / g) * m2);
    const res = egcd(m1, m2);
    const reduced = m2 / g;
    const t = (((a2 - a1) / g) * res.x) % reduced;
    const x = ((a1 + m1 * t) % modulus + modulus) % modulus;
    return {
      value: `${x} (mod ${modulus})`,
      meta: `CRT solution modulo ${modulus}`,
      steps: [
        step("Congruence system", formula(`x ≡ ${a1} (mod ${m1})`) + formula(`x ≡ ${a2} (mod ${m2})`)),
        step("Compatibility", formula(`gcd(${m1}, ${m2}) = ${g} divides ${a2 - a1}.`)),
        step("Bézout coefficients", formula(`${m1}(${res.x}) + ${m2}(${res.y}) = ${g}`)),
        step("Parameter t", formula(`t ≡ (a₂ − a₁)/g · x ≡ ${t} (mod ${reduced})`)),
        step("Reconstruction", formula(`x = a₁ + m₁·t = ${x} (mod ${modulus})`)),
        step("Verification", formula(`${x} mod ${m1} = ${a1} · ${x} mod ${m2} = ${a2}`)),
      ],
    };
  }

  function runTotient({ n }) {
    if (n <= 0n) throw new Error("n must be a positive integer.");
    const factors = factorizeSmall(n);
    let phi = n;
    const factorParts = [];
    const productParts = [];
    for (const [prime, power] of factors) {
      phi = (phi / prime) * (prime - 1n);
      factorParts.push(`${prime}^${power}`);
      productParts.push(`(1 − 1/${prime})`);
    }
    return {
      value: phi.toString(),
      meta: `φ(${n})`,
      steps: [
        step("Prime-power decomposition", formula(`${n} = ${factorParts.length ? factorParts.join(" · ") : "1"}`)),
        step("Product formula", formula(`φ(n) = n · ∏ (1 − 1/p)`) + (productParts.length ? formula(`φ(${n}) = ${n} · ${productParts.join(" · ")}`) : "")),
        step("Result", formula(`φ(${n}) = ${phi}`)),
      ],
    };
  }

  function runRsa({ p, q, e }) {
    if (p <= 1n || q <= 1n) throw new Error("Primes p and q must exceed 1.");
    if (e <= 1n) throw new Error("Public exponent e must exceed 1.");
    const n = p * q;
    const phi = (p - 1n) * (q - 1n);
    const g = gcd(e, phi);
    if (g !== 1n) {
      return {
        value: `No private exponent · gcd(e, φ(N)) = ${g}`,
        meta: "Invalid RSA parameter set",
        steps: [
          step("Modulus", formula(`N = p · q = ${p} · ${q} = ${n}`)),
          step("Totient", formula(`φ(N) = (p − 1)(q − 1) = ${phi}`)),
          step("Invertibility obstruction", formula(`gcd(${e}, ${phi}) = ${g} > 1`) + "<p>e is not invertible modulo φ(N).</p>"),
        ],
      };
    }
    const d = modInv(e, phi);
    return {
      value: `N = ${n} · φ(N) = ${phi} · d = ${d}`,
      meta: `${bitLength(n)}-bit RSA parameter set`,
      steps: [
        step("Modulus", formula(`N = p · q = ${p} · ${q} = ${n}`)),
        step("Totient", formula(`φ(N) = (p − 1)(q − 1) = ${phi}`)),
        step("Private exponent", formula(`d ≡ e⁻¹ (mod φ(N)) ≡ ${d}`)),
        step("Verification", formula(`${e} · ${d} mod ${phi} = 1`)),
      ],
    };
  }

  function runPrimality({ n }) {
    if (n < 2n) {
      return { value: "Not prime", meta: `${n} is below 2`, steps: [step("Definition", "<p>A prime must be an integer greater than 1 with no positive divisors other than 1 and itself.</p>")] };
    }
    const prime = isPrime(n);
    let d = n - 1n;
    let s = 0n;
    while (d % 2n === 0n) {
      d /= 2n;
      s += 1n;
    }
    const steps = [
      step("Trial division", "<p>Reject candidates divisible by the small primes 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, and 37.</p>"),
      step("Binary decomposition", formula(`n − 1 = 2^${s} · ${d}`)),
      step(
        "Miller–Rabin witnesses",
        "<p>Strong probable-prime witnesses are tested against the decomposition. For values below 2⁶⁴ the witness set is deterministic; larger values are probabilistic.</p>",
      ),
      step("Verdict", formula(`${n} is ${prime ? "a probable prime" : "composite"}`)),
    ];
    if (!prime) {
      const factors = factorizeSmall(n);
      const parts = [];
      for (const [factor, power] of factors) parts.push(`${factor}^${power}`);
      if (parts.length > 1 || (parts.length === 1 && parts[0] !== `${n}^1`)) {
        steps.push(step("Witness factor", formula(`${n} = ${parts.join(" · ")}`)));
      }
    }
    return { value: prime ? "Probable prime" : "Composite", meta: `${n}`, steps };
  }

  function runFactor({ n }) {
    if (n <= 1n) throw new Error("N must exceed 1.");
    const res = fermatFactor(n, 20000);
    if (res.found && res.p > 1n && res.q > 1n) {
      return {
        value: `${res.p} × ${res.q}`,
        meta: `${n} = p · q`,
        steps: [
          step("Difference of squares", formula(`N = a² − b² = (a − b)(a + b)`)),
          step("Fermat search", formula(`⌈√N⌉ = ${isqrt(n) + (isqrt(n) * isqrt(n) === n ? 0n : 1n)}`) + formula(`b² = a² − N became a perfect square after ${res.steps} step${res.steps === 1 ? "" : "s"}.`)),
          step("Factor recovery", formula(`p = a − b = ${res.p}`) + formula(`q = a + b = ${res.q}`)),
          step("Verification", formula(`${res.p} · ${res.q} = ${n}`)),
        ],
      };
    }
    const factors = factorizeSmall(n);
    const parts = [];
    for (const [factor, power] of factors) parts.push(`${factor}^${power}`);
    return {
      value: parts.join(" · ") || n.toString(),
      meta: `Trial factorization of ${n}`,
      steps: [
        step("Fermat search", `<p>No perfect square <code>b² = a² − N</code> appeared within 20,000 increments.</p>`),
        step("Small-factor fallback", formula(`${n} = ${parts.join(" · ") || n}`)),
        step("Conclusion", "<p>The remaining cofactor may be prime or may require a stronger factorization method.</p>"),
      ],
    };
  }

  function runContinuedFraction({ a, b }) {
    if (a <= 0n || b <= 0n) throw new Error("Both integers must be positive.");
    let num = a;
    let den = b;
    const terms = [];
    while (den !== 0n && terms.length < 24) {
      const q = num / den;
      terms.push(q);
      const remainder = num - q * den;
      num = den;
      den = remainder;
    }

    let hPrev2 = 0n;
    let hPrev1 = 1n;
    let kPrev2 = 1n;
    let kPrev1 = 0n;
    const convergents = [];
    for (const term of terms) {
      const h = term * hPrev1 + hPrev2;
      const k = term * kPrev1 + kPrev2;
      convergents.push({ h, k });
      hPrev2 = hPrev1;
      hPrev1 = h;
      kPrev2 = kPrev1;
      kPrev1 = k;
    }

    const rows = convergents
      .slice(0, 10)
      .map((item, index) => `<tr><td>${index}</td><td>${item.h}</td><td>${item.k}</td></tr>`)
      .join("");

    return {
      value: `[${terms.join("; ")}]`,
      meta: `${a} / ${b}`,
      steps: [
        step("Continued-fraction expansion", formula(`${a} / ${b} = [${terms.join("; ")}]`)),
        step(
          "Convergents",
          `<table class="convergent-table"><thead><tr><th>#</th><th>hₖ</th><th>kₖ</th></tr></thead><tbody>${rows}</tbody></table>` +
            (convergents.length > 10 ? `<p>${convergents.length - 10} further convergents are omitted.</p>` : ""),
        ),
        step("Limit", formula(`hₖ / kₖ → ${a} / ${b}`) + "<p>Convergents are the best rational approximations with bounded denominator — the structure Wiener's attack exploits.</p>"),
      ],
    };
  }

  function execute(op, inputs) {
    switch (op) {
      case "gcd":
        return runGcd(inputs);
      case "lcm":
        return runLcm(inputs);
      case "egcd":
        return runEgcd(inputs);
      case "modinv":
        return runModinv(inputs);
      case "modexp":
        return runModexp(inputs);
      case "crt":
        return runCrt(inputs);
      case "totient":
        return runTotient(inputs);
      case "rsa-rel":
        return runRsa(inputs);
      case "primality":
        return runPrimality(inputs);
      case "factor":
        return runFactor(inputs);
      case "cf":
        return runContinuedFraction(inputs);
      default:
        throw new Error("Unknown operation.");
    }
  }

  /* ------------------------------------------------------------------------
     Wiring
     ------------------------------------------------------------------------ */
  function renderOperation(op, { autorun = false } = {}) {
    const meta = OPS[op];
    if (!meta) return;
    state.op = op;

    $$("[data-op]").forEach((button) => {
      button.classList.toggle("is-active", button.dataset.op === op);
    });
    const select = $("#op-select");
    if (select) select.value = op;

    const rubric = $("#op-rubric");
    const title = $("#op-title");
    const desc = $("#op-desc");
    const index = $("#op-index-label");
    if (rubric) rubric.textContent = meta.rubric;
    if (title) title.textContent = meta.title;
    if (desc) desc.innerHTML = meta.desc;
    if (index) index.textContent = `${meta.num} / 11`;

    renderInputs(meta);
    clearResult();
    if (autorun) runOperation({ silent: true });
  }

  function runOperation({ silent = false } = {}) {
    const meta = OPS[state.op];
    if (!meta) return;
    try {
      const inputs = readInputs(meta);
      const result = execute(state.op, inputs);
      showResult(result.value, result.meta);
      renderSteps(result.steps);
      setDerivStatus(`Complete · ${result.steps.length} step${result.steps.length === 1 ? "" : "s"}`);
      if (!silent) showToast(`${meta.title} computed`, "safe");
    } catch (error) {
      hideResult();
      const content = $("#deriv-content");
      if (content) {
        content.innerHTML = `<div class="derivation-empty">${escapeHTML(error.message || "Operation failed.")}</div>`;
      }
      setDerivStatus("Invalid input");
      if (!silent) showToast(error.message || "Operation failed", "danger");
    }
  }

  function bind() {
    $$("[data-op]").forEach((button) => {
      button.addEventListener("click", () => renderOperation(button.dataset.op));
    });

    const select = $("#op-select");
    if (select) {
      select.addEventListener("change", () => renderOperation(select.value));
    }

    const run = $("#btn-run");
    if (run) run.addEventListener("click", () => runOperation());

    const clear = $("#btn-clear");
    if (clear) clear.addEventListener("click", clearResult);

    const inputs = $("#op-inputs");
    if (inputs) {
      inputs.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          event.preventDefault();
          runOperation();
        }
      });
    }
  }

  bind();
  renderOperation("gcd", { autorun: true });
})();
