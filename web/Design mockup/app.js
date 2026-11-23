(() => {
  const root = document.documentElement;
  const saved = localStorage.getItem('nt-theme');
  const preferred = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  root.dataset.theme = saved || 'dark';
  const syncThemeButtons = () => {
    document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
      btn.setAttribute('aria-label', root.dataset.theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
      btn.querySelector('.theme-glyph').textContent = root.dataset.theme === 'dark' ? '☼' : '◐';
    });
  };
  document.querySelectorAll('[data-theme-toggle]').forEach(btn => btn.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('nt-theme', root.dataset.theme);
    syncThemeButtons();
  }));
  syncThemeButtons();

  const menu = document.querySelector('[data-menu-toggle]');
  const nav = document.querySelector('[data-nav]');
  if (menu && nav) menu.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menu.setAttribute('aria-expanded', String(open));
  });

  document.querySelectorAll('[data-tool-tab]').forEach(tab => tab.addEventListener('click', () => {
    const group = tab.closest('[data-tool-group]');
    group.querySelectorAll('[data-tool-tab]').forEach(t => t.setAttribute('aria-selected', String(t === tab)));
    group.querySelectorAll('[data-tool-panel]').forEach(panel => panel.classList.toggle('active', panel.dataset.toolPanel === tab.dataset.toolTab));
  }));

  const byId = id => document.getElementById(id);
  const setStatus = (id, message, type='') => {
    const el = byId(id);
    if (!el) return;
    el.textContent = message;
    el.className = 'inline-status' + (type ? ' ' + type : '');
  };
  const integer = (id) => {
    const value = Number(byId(id)?.value);
    if (!Number.isSafeInteger(value)) throw new Error('Enter a safe integer.');
    return value;
  };
  const gcd = (a,b) => { a=Math.abs(a); b=Math.abs(b); while(b){[a,b]=[b,a%b];} return a; };
  const modPow = (base, exp, mod) => {
    if (mod <= 0 || exp < 0) throw new Error('Use a positive modulus and non-negative exponent.');
    let result=1n, b=((BigInt(base)%BigInt(mod))+BigInt(mod))%BigInt(mod), e=BigInt(exp), m=BigInt(mod);
    while(e>0n){if(e&1n) result=result*b%m; b=b*b%m; e>>=1n;}
    return result.toString();
  };
  const isPrime = n => {
    if(n<2) return false;
    if(n%2===0) return n===2;
    for(let d=3;d*d<=n;d+=2) if(n%d===0) return false;
    return true;
  };
  const factorize = n => {
    if(n<2) throw new Error('Enter an integer greater than 1.');
    const factors=[];
    for(let p=2;p*p<=n;p+=(p===2?1:2)) {
      if(n%p===0){let e=0;while(n%p===0){n/=p;e++;}factors.push(e===1?String(p):`${p}^${e}`);}
    }
    if(n>1) factors.push(String(n));
    return factors.join(' × ') || '1';
  };

  const auditForm = byId('audit-form');
  if(auditForm) auditForm.addEventListener('submit', e => {
    e.preventDefault();
    try {
      const n=integer('audit-n'), m=integer('audit-m');
      if(n<1 || m<1) throw new Error('Enter positive integers.');
      byId('audit-prime').textContent = isPrime(n) ? 'Prime' : 'Composite';
      byId('audit-factor').textContent = factorize(n);
      byId('audit-gcd').textContent = gcd(n,m).toString();
      byId('audit-result').hidden = false;
      setStatus('audit-status','Preview calculation completed in the browser. Connect this form to the application audit endpoint for production results.','success');
    } catch(err) { setStatus('audit-status',err.message,'error'); }
  });

  const keyForm=byId('keygen-form');
  if(keyForm) keyForm.addEventListener('submit', e => {
    e.preventDefault();
    setStatus('keygen-status','Interface preview only. Connect this form to the existing /keygen backend before generating or displaying real key material.','success');
  });

  const modForm=byId('mod-form');
  if(modForm) modForm.addEventListener('submit', e => {
    e.preventDefault();
    try {
      const a=integer('mod-a'), b=integer('mod-b'), m=integer('mod-m');
      byId('mod-result').textContent=modPow(a,b,m);
      setStatus('mod-status','Computed locally using integer arithmetic.','success');
    } catch(err) { setStatus('mod-status',err.message,'error'); }
  });
  const gcdForm=byId('gcd-form');
  if(gcdForm) gcdForm.addEventListener('submit', e => {
    e.preventDefault();
    try {
      const a=integer('gcd-a'), b=integer('gcd-b');
      byId('gcd-result').textContent=gcd(a,b).toString();
      setStatus('gcd-status','Computed locally.','success');
    } catch(err) { setStatus('gcd-status',err.message,'error'); }
  });
  document.querySelectorAll('[data-copy-target]').forEach(btn => btn.addEventListener('click', async () => {
    const el=byId(btn.dataset.copyTarget);
    if(!el) return;
    try { await navigator.clipboard.writeText(el.textContent); btn.textContent='Copied'; setTimeout(()=>btn.textContent='Copy',1200); }
    catch { btn.textContent='Select to copy'; }
  }));
})();
