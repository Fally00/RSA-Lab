//Made by Remas
/* RSA-Lab — Toolkit: 11 operations, BigInt only (no floating point at any stage). */
(function () {
  'use strict';

  /* ---------- helpers ---------- */
  class InputError extends Error { }
  const abs = (x) => (x < 0n ? -x : x);
  const modp = (a, m) => { const r = a % m; return r < 0n ? r + m : r; };
  const pad2 = (n) => String(n).padStart(2, '0');
  const SUB = '₀₁₂₃₄₅₆₇₈₉';
  const sub = (i) => String(i).split('').map((c) => SUB[+c]).join('');
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const par = (x) => (x < 0n ? `(${x})` : `${x}`);

  function I(raw, name) {
    let s = String(raw == null ? '' : raw).trim().replace(/_/g, '');
    if (!s) throw new InputError(`${name} is required.`);
    let neg = false;
    if (s[0] === '-' || s[0] === '+') { neg = s[0] === '-'; s = s.slice(1); }
    if (!/^(0x[0-9a-f]+|[0-9]+)$/i.test(s)) {
      throw new InputError(`${name} must be a decimal or 0x-prefixed hexadecimal integer.`);
    }
    const v = BigInt(s);
    return neg ? -v : v;
  }

  function gcdB(a, b) { a = abs(a); b = abs(b); while (b) { [a, b] = [b, a % b]; } return a; }

  function modpow(b, e, m) {
    let r = 1n % m; b = modp(b, m);
    while (e > 0n) { if (e & 1n) r = (r * b) % m; b = (b * b) % m; e >>= 1n; }
    return r;
  }

  function isqrt(n) {
    if (n < 2n) return n;
    let x = 1n << BigInt((n.toString(2).length + 1) >> 1);
    for (; ;) { const y = (x + n / x) >> 1n; if (y >= x) return x; x = y; }
  }

  /* extended Euclid on non-negative a, b; rows record every division with its Bézout coefficients */
  function egcdRows(a, b) {
    let or = a, r = b, os = 1n, s = 0n, ot = 0n, t = 1n;
    const rows = [];
    while (r !== 0n) {
      const q = or / r;
      const nr = or - q * r, ns = os - q * s, nt = ot - q * t;
      rows.push({ dividend: or, divisor: r, q, rem: nr, s: ns, t: nt });
      or = r; r = nr; os = s; s = ns; ot = t; t = nt;
    }
    return { g: or, x: os, y: ot, rows };
  }

  function trialFactor(n, limit = 1000000) {
    const out = []; let d = 2n, count = 0;
    for (; d * d <= n; d += d === 2n ? 1n : 2n) {
      if (++count > limit) throw new InputError(`n is too large for trial division here (limit ${limit.toLocaleString('en-US')} divisors).`);
      if (n % d === 0n) { let e = 0; while (n % d === 0n) { n /= d; e++; } out.push([d, e]); }
    }
    if (n > 1n) out.push([n, 1]);
    return out;
  }

  function decompose(n) { let d = n - 1n, s = 0; while (!(d & 1n)) { d >>= 1n; s++; } return { d, s }; }

  function mrRound(n, a, d, s) {
    const xs = []; let x = modpow(a, d, n); xs.push(x);
    if (x === 1n || x === n - 1n) return { pass: true, xs };
    for (let i = 1; i < s; i++) {
      x = (x * x) % n; xs.push(x);
      if (x === n - 1n) return { pass: true, xs };
      if (x === 1n) return { pass: false, xs };
    }
    return { pass: false, xs };
  }

  const SMALL_PRIMES = [2n, 3n, 5n, 7n, 11n, 13n, 17n, 19n, 23n, 29n, 31n, 37n];
  function isProbablePrime(n) {
    if (n < 2n) return false;
    for (const p of SMALL_PRIMES) { if (n === p) return true; if (n % p === 0n) return false; }
    const { d, s } = decompose(n);
    return SMALL_PRIMES.every((a) => mrRound(n, a, d, s).pass);
  }


  /* ---------- plain text -> LaTeX (rendered by MathJax when available) ---------- */
  const SUBS = { '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9', '₋': '-', '₊': '+', 'ₖ': 'k', 'ᵢ': 'i', 'ₙ': 'n' };
  const SUPS = { '²': '2', '³': '3', '¹': '1', '⁻': '-', 'ⁱ': 'i', 'ᵉ': 'e', 'ˢ': 's', 'ʳ': 'r' };
  const subRe = new RegExp('[' + Object.keys(SUBS).join('') + ']+', 'g');
  const supRe = new RegExp('[' + Object.keys(SUPS).join('') + ']+', 'g');
  const SYM = { '·': '\\cdot ', '≡': '\\equiv ', '−': '-', '≠': '\\neq ', '→': '\\to ', '←': '\\leftarrow ', 'φ': '\\varphi ', 'Σ': '\\sum ', 'Π': '\\prod ', '✓': '\\checkmark ', '✗': '\\times ', '…': '\\ldots ', '′': "'", '×': '\\times ' };
  function toTex(line) {
    let t = line;
    t = t.replace(/ᵇⁱᵗ/g, '^{\\mathrm{bit}}');
    t = t.replace(subRe, (m) => '_{' + [...m].map((c) => SUBS[c]).join('') + '}');
    t = t.replace(supRe, (m) => '^{' + [...m].map((c) => SUPS[c]).join('') + '}');
    t = t.replace(/\^(-?\w+)/g, '^{$1}');
    t = t.replace(/\(mod ([^)]+)\)/g, '\\pmod{$1}');
    t = t.replace(/\bmod\b/g, '\\bmod ');
    t = t.replace(/\bgcd\b/g, '\\gcd').replace(/\blcm\b/g, '\\operatorname{lcm}');
    return t.replace(/[·≡−≠→←φΣΠ✓✗…′×]/g, (c) => SYM[c]);
  }
  const isTextLine = (l) => /[A-Za-z]{3,}/.test(l.replace(/\b(gcd|lcm|mod)\b/g, '')) || /^[…\s.]*$/.test(l);

  const S = (label, code, note) => ({ label, code, note });

  /* ---------- operations ---------- */
  const OPS = [
    {
      id: 'gcd', cat: 'Arithmetic', name: 'GCD (Euclidean)', title: 'Greatest Common Divisor',
      desc: 'Compute <code>gcd(a, b)</code> by repeated Euclidean division until the remainder vanishes.',
      fields: [{ id: 'a', label: 'Integer A', value: '240' }, { id: 'b', label: 'Integer B', value: '46' }],
      run(v) {
        const a = I(v.a, 'Integer A'), b = I(v.b, 'Integer B');
        const steps = [S('EUCLIDEAN DIVISION', 'rₖ₋₁ = rₖ · qₖ + rₖ₊₁', 'Apply repeated division until the remainder vanishes. The last non-zero remainder is the GCD.')];
        if (a < 0n || b < 0n) steps.push(S('ABSOLUTE VALUES', `gcd(${a}, ${b}) = gcd(${abs(a)}, ${abs(b)})`));
        let x = abs(a), y = abs(b);
        while (y !== 0n) {
          const q = x / y, r = x % y;
          steps.push(S('DIVISION STEP', `${x} = ${y} · ${q} + ${r}`));
          x = y; y = r;
        }
        steps.push(S('GREATEST COMMON DIVISOR', `gcd(${a}, ${b}) = ${x}`));
        return { value: x.toString(), caption: `GCD(${a}, ${b})`, steps };
      }
    },
    {
      id: 'lcm', cat: 'Arithmetic', name: 'LCM', title: 'Least Common Multiple',
      desc: 'Compute <code>lcm(a, b)</code> from the GCD, using <code>|a · b| / gcd(a, b)</code>.',
      fields: [{ id: 'a', label: 'Integer A', value: '240' }, { id: 'b', label: 'Integer B', value: '46' }],
      run(v) {
        const a = I(v.a, 'Integer A'), b = I(v.b, 'Integer B');
        const steps = [];
        if (a === 0n || b === 0n) {
          steps.push(S('DEFINITION', 'lcm(a, b) = 0 when a = 0 or b = 0'));
          steps.push(S('LEAST COMMON MULTIPLE', `lcm(${a}, ${b}) = 0`));
          return { value: '0', caption: `LCM(${a}, ${b})`, steps };
        }
        steps.push(S('IDENTITY', 'lcm(a, b) = |a · b| / gcd(a, b)', 'Compute the GCD first, then divide it out of the product.'));
        let x = abs(a), y = abs(b);
        while (y !== 0n) {
          const q = x / y, r = x % y;
          steps.push(S('DIVISION STEP', `${x} = ${y} · ${q} + ${r}`));
          x = y; y = r;
        }
        steps.push(S('GREATEST COMMON DIVISOR', `gcd(${a}, ${b}) = ${x}`));
        const l = abs(a * b) / x;
        steps.push(S('LEAST COMMON MULTIPLE', `lcm(${a}, ${b}) = |${par(a)} · ${par(b)}| / ${x} = ${l}`));
        return { value: l.toString(), caption: `LCM(${a}, ${b})`, steps };
      }
    },
    {
      id: 'egcd', cat: 'Arithmetic', name: 'Extended Euclidean', title: 'Extended Euclidean Algorithm',
      desc: 'Find integers <code>x, y</code> with <code>a·x + b·y = gcd(a, b)</code> (Bézout coefficients).',
      fields: [{ id: 'a', label: 'Integer A', value: '240' }, { id: 'b', label: 'Integer B', value: '46' }],
      run(v) {
        const a = I(v.a, 'Integer A'), b = I(v.b, 'Integer B');
        if (a === 0n && b === 0n) throw new InputError('A and B cannot both be zero.');
        const A = abs(a), B = abs(b);
        const sa = a < 0n ? -1n : 1n, sb = b < 0n ? -1n : 1n;
        const { g, x, y, rows } = egcdRows(A, B);
        const X = x * sa, Y = y * sb;
        const steps = [S('BÉZOUT IDENTITY', 'a · x + b · y = gcd(a, b)', 'Run the Euclidean algorithm and track coefficients (s, t) so that every remainder is written as a combination of a and b.')];
        if (a < 0n || b < 0n) steps.push(S('ABSOLUTE VALUES', `Work with |a| = ${A} and |b| = ${B}, then restore the signs.`));
        rows.forEach((r) => steps.push(S('DIVISION STEP', `${r.dividend} = ${r.divisor} · ${r.q} + ${r.rem}\n${r.rem} = ${A}·${par(r.s)} + ${B}·${par(r.t)}`)));
        steps.push(S('GREATEST COMMON DIVISOR', `gcd(${a}, ${b}) = ${g}`));
        steps.push(S('BÉZOUT COEFFICIENTS', `x = ${X},  y = ${Y}`));
        steps.push(S('VERIFY', `${par(a)}·${par(X)} + ${par(b)}·${par(Y)} = ${a * X + b * Y}`));
        return { value: `gcd = ${g}`, caption: `x = ${X} · y = ${Y}`, steps };
      }
    },
    {
      id: 'modinv', cat: 'Modular', name: 'Modular Inverse', title: 'Modular Inverse',
      desc: 'Find <code>a⁻¹ mod m</code> — the number <code>x</code> with <code>a·x ≡ 1 (mod m)</code>.',
      fields: [{ id: 'a', label: 'Integer A', value: '17' }, { id: 'm', label: 'Modulus M', value: '3120' }],
      run(v) {
        const a = I(v.a, 'Integer A'); const m = abs(I(v.m, 'Modulus M'));
        if (m < 2n) throw new InputError('Modulus M must be at least 2.');
        const A = modp(a, m);
        const { g, x, rows } = egcdRows(A, m);
        const steps = [S('MODULAR INVERSE', 'a · x ≡ 1 (mod m)', 'An inverse exists only when gcd(a, m) = 1. Bézout then gives a·x + m·y = 1, and x is the inverse.')];
        if (A !== a) steps.push(S('REDUCE', `${a} mod ${m} = ${A}`));
        rows.forEach((r) => steps.push(S('DIVISION STEP', `${r.dividend} = ${r.divisor} · ${r.q} + ${r.rem}\n${r.rem} = ${A}·${par(r.s)} + ${m}·${par(r.t)}`)));
        steps.push(S('GREATEST COMMON DIVISOR', `gcd(${A}, ${m}) = ${g}`));
        if (g !== 1n) {
          steps.push(S('NO INVERSE', `gcd = ${g} ≠ 1, so ${a} has no inverse modulo ${m}.`));
          return { value: 'No inverse exists', caption: `GCD(${a}, ${m}) = ${g} ≠ 1`, steps };
        }
        const inv = modp(x, m);
        steps.push(S('INVERSE', `x = ${x}  →  ${x} mod ${m} = ${inv}`));
        steps.push(S('VERIFY', `${A} · ${inv} = ${A * inv} ≡ ${(A * inv) % m} (mod ${m})`));
        return { value: inv.toString(), caption: `${a}^-1 MOD ${m}`, steps };
      }
    },
    {
      id: 'modexp', cat: 'Modular', name: 'Modular Exponentiation', title: 'Modular Exponentiation',
      desc: 'Compute <code>a^e mod m</code> efficiently by square-and-multiply.',
      fields: [{ id: 'b', label: 'Base A', value: '4' }, { id: 'e', label: 'Exponent E', value: '13' }, { id: 'm', label: 'Modulus M', value: '497' }],
      run(v) {
        const b = I(v.b, 'Base A'), e = I(v.e, 'Exponent E'), m = I(v.m, 'Modulus M');
        if (e < 0n) throw new InputError('Exponent E must be zero or positive.');
        if (m < 1n) throw new InputError('Modulus M must be positive.');
        const bits = e.toString(2);
        const shown = bits.length > 64 ? `${bits.slice(0, 32)}…${bits.slice(-16)}` : bits;
        const steps = [
          S('SQUARE AND MULTIPLY', 'r ← r² · aᵇⁱᵗ  (mod m)', 'Scan the exponent from its most significant bit. Square at every bit, and multiply by the base when the bit is 1.'),
          S('BINARY EXPONENT', `${e} = (${shown})₂\n${bits.length} bits`)
        ];
        const bb = modp(b, m);
        if (bb !== b) steps.push(S('REDUCE BASE', `${b} mod ${m} = ${bb}`));
        let r = 1n % m;
        bits.split('').forEach((bit, i) => {
          const before = r; const sq = (before * before) % m;
          if (bit === '1') { r = (sq * bb) % m; steps.push(S(`BIT ${i + 1} = 1`, `r = (${before}² · ${bb}) mod ${m} = ${r}`)); }
          else { r = sq; steps.push(S(`BIT ${i + 1} = 0`, `r = ${before}² mod ${m} = ${r}`)); }
        });
        steps.push(S('RESULT', `${b}^${e} mod ${m} = ${r}`));
        return { value: r.toString(), caption: `${b}^${e} MOD ${m}`, steps };
      }
    },
    {
      id: 'crt', cat: 'Modular', name: 'Chinese Remainder', title: 'Chinese Remainder Theorem',
      desc: 'Solve <code>x ≡ rᵢ (mod mᵢ)</code> for pairwise coprime moduli. The third congruence is optional.',
      fields: [
        { id: 'r1', label: 'Remainder r₁', value: '2' }, { id: 'm1', label: 'Modulus m₁', value: '3' },
        { id: 'r2', label: 'Remainder r₂', value: '3' }, { id: 'm2', label: 'Modulus m₂', value: '5' },
        { id: 'r3', label: 'Remainder r₃ (optional)', value: '2' }, { id: 'm3', label: 'Modulus m₃ (optional)', value: '7' }
      ],
      run(v) {
        const pairs = [];
        for (const i of [1, 2, 3]) {
          const rs = (v['r' + i] || '').trim(), ms = (v['m' + i] || '').trim();
          if (i === 3 && !rs && !ms) continue;
          const m = I(ms, `Modulus m${i}`);
          if (m < 2n) throw new InputError(`Modulus m${i} must be at least 2.`);
          pairs.push({ r: modp(I(rs, `Remainder r${i}`), m), m });
        }
        for (let i = 0; i < pairs.length; i++) for (let j = i + 1; j < pairs.length; j++) {
          const g = gcdB(pairs[i].m, pairs[j].m);
          if (g !== 1n) throw new InputError(`Moduli m${i + 1} and m${j + 1} are not coprime (gcd = ${g}).`);
        }
        const M = pairs.reduce((p, c) => p * c.m, 1n);
        const steps = [
          S('SIMULTANEOUS CONGRUENCES', pairs.map((p) => `x ≡ ${p.r} (mod ${p.m})`).join('\n'), 'When the moduli are pairwise coprime, there is exactly one solution modulo their product M.'),
          S('MODULUS PRODUCT', `M = ${pairs.map((p) => p.m).join(' · ')} = ${M}`)
        ];
        let sum = 0n; const terms = [];
        pairs.forEach((p, i) => {
          const Mi = M / p.m;
          const yi = modp(egcdRows(Mi % p.m, p.m).x, p.m);
          const term = p.r * Mi * yi; sum += term; terms.push(term);
          steps.push(S(`PARTIAL PRODUCT ${i + 1}`, `M${sub(i + 1)} = M / ${p.m} = ${Mi}\ny${sub(i + 1)} = M${sub(i + 1)}^-1 mod ${p.m} = ${yi}`));
        });
        const x = modp(sum, M);
        steps.push(S('COMBINE', `x = Σ rᵢ · Mᵢ · yᵢ = ${terms.join(' + ')} = ${sum}`));
        steps.push(S('REDUCE', `x = ${sum} mod ${M} = ${x}`));
        steps.push(S('VERIFY', pairs.map((p) => `${x} mod ${p.m} = ${x % p.m}`).join('\n')));
        return { value: x.toString(), caption: `x ≡ ${x} (mod ${M})`, steps };
      }
    },
    {
      id: 'totient', cat: 'Structure', name: 'Euler’s Totient', title: 'Euler’s Totient',
      desc: 'Compute <code>φ(n)</code>, the count of integers in <code>1…n</code> that are coprime to <code>n</code>.',
      fields: [{ id: 'n', label: 'Integer N', value: '3233' }],
      run(v) {
        const n = I(v.n, 'Integer N');
        if (n < 1n) throw new InputError('Integer N must be at least 1.');
        const steps = [S('EULER TOTIENT', 'φ(n) = n · Π (1 − 1/p)', 'φ is multiplicative, and for a prime power φ(pᵉ) = pᵉ − pᵉ⁻¹.')];
        if (n === 1n) { steps.push(S('BASE CASE', 'φ(1) = 1')); return { value: '1', caption: 'φ(1)', steps }; }
        const f = trialFactor(n);
        steps.push(S('FACTORIZATION', `${n} = ${f.map(([p, e]) => (e > 1 ? `${p}^${e}` : `${p}`)).join(' · ')}`, f.length === 1 && f[0][1] === 1 ? 'n is prime, so φ(n) = n − 1.' : undefined));
        const vals = f.map(([p, e]) => {
          const val = e > 1 ? p ** BigInt(e) - p ** BigInt(e - 1) : p - 1n;
          steps.push(S('PRIME POWER', e > 1 ? `φ(${p}^${e}) = ${p}^${e} − ${p}^${e - 1} = ${val}` : `φ(${p}) = ${p} − 1 = ${val}`));
          return val;
        });
        const phi = vals.reduce((a, c) => a * c, 1n);
        steps.push(S('PRODUCT', `φ(${n}) = ${vals.join(' · ')} = ${phi}`));
        return { value: phi.toString(), caption: `φ(${n})`, steps };
      }
    },
    {
      id: 'rsa', cat: 'Structure', name: 'RSA Relationships', title: 'RSA Relationships',
      desc: 'Link <code>n = pq</code>, <code>φ(n)</code> and <code>d ≡ e⁻¹ (mod φ(n))</code>, then round-trip a message.',
      fields: [
        { id: 'p', label: 'Prime P', value: '61' }, { id: 'q', label: 'Prime Q', value: '53' },
        { id: 'e', label: 'Public exponent E', value: '17' }, { id: 'msg', label: 'Message M', value: '65' }
      ],
      run(v) {
        const p = I(v.p, 'Prime P'), q = I(v.q, 'Prime Q'), e = I(v.e, 'Public exponent E'), msg = I(v.msg, 'Message M');
        if (p < 2n || q < 2n) throw new InputError('P and Q must be at least 2.');
        if (p === q) throw new InputError('P and Q must be different primes.');
        if (!isProbablePrime(p)) throw new InputError(`P = ${p} is not prime.`);
        if (!isProbablePrime(q)) throw new InputError(`Q = ${q} is not prime.`);
        const n = p * q, phi = (p - 1n) * (q - 1n);
        const steps = [
          S('MODULUS', `n = p · q = ${p} · ${q} = ${n}`, 'The public modulus is the product of two primes. Only someone who knows p and q can compute φ(n).'),
          S('TOTIENT', `φ(n) = (p − 1)(q − 1) = ${p - 1n} · ${q - 1n} = ${phi}`)
        ];
        const g = gcdB(e, phi);
        steps.push(S('EXPONENT CHECK', `gcd(e, φ(n)) = gcd(${e}, ${phi}) = ${g}`));
        if (e < 2n || g !== 1n) {
          steps.push(S('INVALID EXPONENT', 'e must satisfy 1 < e < φ(n) with gcd(e, φ(n)) = 1.'));
          return { value: 'e is not a valid exponent', caption: `n = ${n} · φ(n) = ${phi}`, steps };
        }
        const d = modp(egcdRows(modp(e, phi), phi).x, phi);
        steps.push(S('PRIVATE EXPONENT', `d = e^-1 mod φ(n) = ${d}\ne · d = ${e * d} ≡ ${(e * d) % phi} (mod ${phi})`));
        if (msg < 0n || msg >= n) {
          steps.push(S('MESSAGE RANGE', `M must satisfy 0 ≤ M < n = ${n}; round trip skipped.`));
        } else {
          const c = modpow(msg, e, n), back = modpow(c, d, n);
          steps.push(S('ENCRYPT', `c = M^e mod n = ${msg}^${e} mod ${n} = ${c}`));
          steps.push(S('DECRYPT', `M′ = c^d mod n = ${c}^${d} mod ${n} = ${back}\n${back === msg ? 'M′ = M  ✓' : 'M′ ≠ M  ✗'}`));
        }
        return { value: `d = ${d}`, caption: `n = ${n} · φ(n) = ${phi}`, steps };
      }
    },
    {
      id: 'mr', cat: 'Structure', name: 'Miller-Rabin', title: 'Miller–Rabin Primality Test',
      desc: 'Test whether <code>n</code> is prime by looking for witnesses among the chosen bases.',
      fields: [{ id: 'n', label: 'Integer N', value: '561' }, { id: 'bases', label: 'Bases (comma separated)', value: '2, 3, 5, 7' }],
      run(v) {
        const n = I(v.n, 'Integer N');
        if (n < 2n) throw new InputError('Integer N must be at least 2.');
        const steps = [S('MILLER–RABIN', 'n − 1 = 2ˢ · d', 'Write n − 1 as 2ˢ · d. A base a proves n composite unless a^d ≡ 1 or a^(2ʳ·d) ≡ −1 (mod n) for some 0 ≤ r < s.')];
        if (n < 4n) { steps.push(S('SMALL CASE', `${n} is prime.`)); return { value: 'Prime', caption: `MILLER-RABIN(${n})`, steps }; }
        if (n % 2n === 0n) { steps.push(S('EVEN NUMBER', `${n} is even and greater than 2, so it is composite.`)); return { value: 'Composite', caption: `MILLER-RABIN(${n})`, steps }; }
        const { d, s } = decompose(n);
        steps.push(S('DECOMPOSE', `${n} − 1 = ${n - 1n} = 2^${s} · ${d}`));
        const bases = String(v.bases || '').split(/[,\s]+/).filter(Boolean).slice(0, 20).map((x, i) => I(x, `Base ${i + 1}`));
        if (!bases.length) throw new InputError('Provide at least one base.');
        let tested = 0, witness = null;
        for (const a of bases) {
          if (a < 2n || a > n - 2n) { steps.push(S('SKIP BASE', `a = ${a} is outside [2, n − 2].`)); continue; }
          const { pass, xs } = mrRound(n, a, d, s); tested++;
          let lines = xs.map((x, i) => (i === 0 ? `x${sub(0)} = ${a}^${d} mod ${n} = ${x}` : `x${sub(i)} = x${sub(i - 1)}² mod ${n} = ${x}`));
          if (lines.length > 10) lines = [...lines.slice(0, 6), '…', ...lines.slice(-2)];
          lines.push(pass ? '→ passes this base' : '→ WITNESS: n is composite');
          steps.push(S(`BASE a = ${a}`, lines.join('\n')));
          if (!pass) { witness = a; break; }
        }
        if (!tested) throw new InputError('No valid base in [2, n − 2].');
        if (witness !== null) {
          steps.push(S('VERDICT', `${n} is composite (witness a = ${witness}).`));
          return { value: 'Composite', caption: `MILLER-RABIN(${n}) · WITNESS ${witness}`, steps };
        }
        steps.push(S('VERDICT', `${n} passes ${tested} base${tested > 1 ? 's' : ''}: probably prime.`, 'A prime always passes. A composite passes a given base with probability at most 1/4.'));
        return { value: 'Probably prime', caption: `MILLER-RABIN(${n}) · ${tested} BASES`, steps };
      }
    },
    {
      id: 'fermat', cat: 'Factorization', name: 'Fermat Factorization', title: 'Fermat Factorization',
      desc: 'Write <code>n = a² − b²</code> to split an odd number into <code>(a − b)(a + b)</code>.',
      fields: [{ id: 'n', label: 'Odd integer N', value: '5959' }],
      run(v) {
        const n = I(v.n, 'Odd integer N');
        if (n < 3n) throw new InputError('Integer N must be at least 3.');
        const steps = [S('DIFFERENCE OF SQUARES', 'n = a² − b² = (a − b)(a + b)', 'Start at a = ⌈√n⌉ and increase a until a² − n is a perfect square b².')];
        if (n % 2n === 0n) {
          steps.push(S('EVEN NUMBER', `${n} = 2 · ${n / 2n}. Fermat’s method needs an odd n.`));
          return { value: `2 · ${n / 2n}`, caption: `${n} IS EVEN`, steps };
        }
        let a = isqrt(n); if (a * a < n) a += 1n;
        const a0 = a, LIMIT = 200000;
        for (let i = 0; i < LIMIT; i++, a += 1n) {
          const b2 = a * a - n, b = isqrt(b2);
          const hit = b * b === b2;
          if (i < 12 || hit) steps.push(S(`TRY a = ${a}`, `a² − n = ${a * a} − ${n} = ${b2}${hit ? ` = ${b}²\nperfect square ✓` : '\nnot a perfect square'}`));
          if (hit) {
            if (i >= 12) steps.splice(13, 0, S('ITERATIONS', `${i + 1} candidates tested (a = ${a0} … ${a}).`));
            const f1 = a - b, f2 = a + b;
            steps.push(S('FACTORS', `(${a} − ${b}) · (${a} + ${b}) = ${f1} · ${f2} = ${n}`, f1 === 1n ? 'The factorization is trivial, so n is prime.' : undefined));
            return { value: f1 === 1n ? `${n} is prime` : `${f1} · ${f2}`, caption: `FERMAT(${n})`, steps };
          }
        }
        steps.push(S('LIMIT REACHED', `No square found after ${LIMIT.toLocaleString('en-US')} candidates.`));
        return { value: 'No factor found', caption: `FERMAT(${n}) · LIMIT ${LIMIT.toLocaleString('en-US')}`, steps };
      }
    },
    {
      id: 'cf', cat: 'Factorization', name: 'Continued Fractions', title: 'Continued Fractions',
      desc: 'Expand <code>p / q</code> as <code>[a₀; a₁, a₂, …]</code> and list its convergents (used in Wiener’s attack).',
      fields: [{ id: 'p', label: 'Numerator P', value: '415' }, { id: 'q', label: 'Denominator Q', value: '93' }],
      run(v) {
        let p = I(v.p, 'Numerator P'), q = I(v.q, 'Denominator Q');
        if (q === 0n) throw new InputError('Denominator Q cannot be zero.');
        if (q < 0n) { p = -p; q = -q; }
        const steps = [S('CONTINUED FRACTION', 'p / q = a₀ + 1 / (a₁ + 1 / (a₂ + …))', 'Take the integer part, invert the remainder, and repeat. Each quotient is a partial quotient aᵢ.')];
        const terms = [], conv = [];
        let n = p, d = q, h1 = 1n, h2 = 0n, k1 = 0n, k2 = 1n;
        while (d !== 0n) {
          let a = n / d; if (n % d !== 0n && n < 0n) a -= 1n;
          const r = n - a * d;
          terms.push(a);
          const h = a * h1 + h2, k = a * k1 + k2;
          conv.push([h, k]);
          steps.push(S('DIVISION STEP', `${n} = ${d} · ${par(a)} + ${r}\nc${sub(terms.length - 1)} = ${h}/${k}`));
          h2 = h1; h1 = h; k2 = k1; k1 = k; n = d; d = r;
        }
        const expo = `[${terms[0]}${terms.length > 1 ? '; ' + terms.slice(1).join(', ') : ''}]`;
        steps.push(S('EXPANSION', `${p}/${q} = ${expo}`));
        steps.push(S('CONVERGENTS', conv.slice(0, 15).map(([h, k], i) => `c${sub(i)} = ${h}/${k}`).join('\n') + (conv.length > 15 ? '\n…' : '')));
        return { value: expo, caption: `CF(${p}/${q})`, steps };
      }
    }
  ];

  /* ---------- UI ---------- */
  const $ = (s) => document.querySelector(s);
  const el = {
    metaL: $('#tk-meta-l'), metaR: $('#tk-meta-r'), title: $('#tk-title'), desc: $('#tk-desc'),
    fields: $('#tk-fields'), run: $('#tk-run'), clear: $('#tk-clear'),
    result: $('#tk-result'), rLabel: $('#tk-result-label'), rValue: $('#tk-result-value'), rCap: $('#tk-result-cap'),
    copy: $('#tk-copy'), status: $('#tk-status'), list: $('#tk-steps')
  };
  const values = {}; let cur = 0; let lastValue = '';

  function readValues() { const o = {}; el.fields.querySelectorAll('input').forEach((i) => { o[i.dataset.f] = i.value; values[OPS[cur].id + ':' + i.dataset.f] = i.value; }); return o; }

  function stepHtml(st, i) {
    const math = String(st.code).split('\n').map((l) => (isTextLine(l)
      ? `<div class="tk-line txt">${esc(l)}</div>`
      : `<div class="tk-line">\\(${toTex(l)}\\)</div>`)).join('');
    return `<div class="tk-step"><span class="tk-mono acc tk-step-label">STEP ${pad2(i + 1)} · ${esc(st.label)}</span>` +
      `<div class="tk-code" data-math="${esc(math)}">${esc(st.code)}</div>${st.note ? `<p class="tk-step-note">${esc(st.note)}</p>` : ''}</div>`;
  }

  function showSteps(steps) {
    const total = steps.length; let html = '';
    if (total > 42) {
      steps.slice(0, 30).forEach((s, i) => { html += stepHtml(s, i); });
      html += `<div class="tk-omit tk-mono">… ${total - 40} steps omitted …</div>`;
      steps.slice(-10).forEach((s, i) => { html += stepHtml(s, total - 10 + i); });
    } else steps.forEach((s, i) => { html += stepHtml(s, i); });
    el.list.innerHTML = html;
    mathify(0);
  }

  /* swap the plain-text fallback for typeset math as soon as MathJax is ready */
  function mathify(tries) {
    const MJ = window.MathJax;
    if (!(MJ && MJ.typesetPromise)) { if (tries < 40) setTimeout(() => mathify(tries + 1), 250); return; }
    const boxes = [...el.list.querySelectorAll('.tk-code[data-math]:not(.math)')];
    if (!boxes.length) return;
    boxes.forEach((b) => { b.innerHTML = b.dataset.math; b.classList.add('math'); });
    MJ.typesetPromise(boxes).catch(() => { });
  }

  function setStatus(text, accent) { el.status.textContent = text; el.status.classList.toggle('acc', !!accent); }

  function renderEmpty() {
    el.result.hidden = true; lastValue = '';
    el.list.innerHTML = '<div class="tk-empty tk-mono">Run an operation to see<br>the step-by-step derivation.</div>';
    setStatus('IDLE', false);
  }

  function run() {
    const op = OPS[cur];
    try {
      const res = op.run(readValues());
      el.result.classList.remove('error');
      el.rLabel.textContent = 'RESULT';
      el.rValue.textContent = res.value; el.rCap.textContent = res.caption; el.rCap.hidden = false;
      el.result.hidden = false; el.copy.hidden = false; lastValue = res.value;
      showSteps(res.steps);
      setStatus(`COMPLETE · ${res.steps.length} STEPS`, true);
    } catch (err) {
      if (!(err instanceof InputError)) { console.error(err); }
      el.result.classList.add('error');
      el.rLabel.textContent = 'INPUT ERROR';
      el.rValue.textContent = err instanceof InputError ? err.message : 'Something went wrong. Check the inputs and try again.';
      el.rCap.hidden = true; el.copy.hidden = true; el.result.hidden = false; lastValue = '';
      el.list.innerHTML = '<div class="tk-empty tk-mono">Fix the input and run again.</div>';
      setStatus('ERROR', true);
    }
  }

  function select(i, runNow) {
    cur = i; const op = OPS[i];
    document.querySelectorAll('.tk-index button').forEach((b) => {
      const on = b.dataset.op === op.id; b.classList.toggle('active', on);
      if (on) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current');
    });
    el.metaL.textContent = `OPERATION ${pad2(i + 1)} / ${op.cat.toUpperCase()}`;
    el.metaR.textContent = `${pad2(i + 1)} / ${pad2(OPS.length)}`;
    el.title.textContent = op.title; el.desc.innerHTML = op.desc;
    el.fields.innerHTML = op.fields.map((f) => {
      const val = values[op.id + ':' + f.id] != null ? values[op.id + ':' + f.id] : f.value;
      return `<div class="tk-field"><label class="tk-mono" for="tk-f-${f.id}">${esc(f.label)}</label>` +
        `<input id="tk-f-${f.id}" data-f="${f.id}" type="text" value="${esc(val)}" autocomplete="off" spellcheck="false" inputmode="text"></div>`;
    }).join('');
    el.fields.querySelectorAll('input').forEach((inp) => inp.addEventListener('keydown', (e) => { if (e.key === 'Enter') run(); }));
    if (runNow) run(); else renderEmpty();
    try { history.replaceState(null, '', '#' + op.id); } catch (e) { /* ignore */ }
  }

  document.querySelectorAll('.tk-index button').forEach((b) => b.addEventListener('click', () => select(OPS.findIndex((o) => o.id === b.dataset.op), true)));
  el.run.addEventListener('click', run);
  el.clear.addEventListener('click', renderEmpty);
  el.copy.addEventListener('click', async () => {
    if (!lastValue) return;
    const label = el.copy.querySelector('span');
    try { await navigator.clipboard.writeText(lastValue); }
    catch (e) { const t = document.createElement('textarea'); t.value = lastValue; document.body.appendChild(t); t.select(); try { document.execCommand('copy'); } catch (_) { /* ignore */ } t.remove(); }
    label.textContent = 'COPIED'; setTimeout(() => { label.textContent = 'COPY'; }, 1500);
  });

  const start = Math.max(0, OPS.findIndex((o) => o.id === location.hash.slice(1)));
  select(start, true);
})();
