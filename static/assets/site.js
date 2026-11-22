(function(){
  var d=document, ar=d.documentElement.lang==='ar';
  // sticky header shadow
  var h=d.querySelector('header.site');
  function sc(){ if(h) h.classList.toggle('scrolled', window.scrollY>8); }
  window.addEventListener('scroll', sc, {passive:true}); sc();

  // mega menu
  d.querySelectorAll('.dd').forEach(function(dd){
    var b=dd.querySelector('button');
    b.addEventListener('click', function(e){ e.stopPropagation(); var o=dd.classList.toggle('open'); b.setAttribute('aria-expanded', o); });
  });
  d.addEventListener('click', function(e){ d.querySelectorAll('.dd.open').forEach(function(dd){ if(!dd.contains(e.target)){dd.classList.remove('open'); dd.querySelector('button').setAttribute('aria-expanded','false');} }); });
  d.addEventListener('keydown', function(e){ if(e.key==='Escape'){ d.querySelectorAll('.dd.open').forEach(function(dd){dd.classList.remove('open');}); closeDrawer(); } });

  // drawer
  var dr=d.querySelector('.drawer');
  function closeDrawer(){ if(dr){ dr.classList.remove('open'); d.body.style.overflow=''; } }
  d.querySelectorAll('[data-open-drawer]').forEach(function(b){ b.addEventListener('click', function(){ dr.classList.add('open'); d.body.style.overflow='hidden'; dr.querySelector('button').focus(); }); });
  if(dr){ dr.addEventListener('click', function(e){ if(e.target===dr || e.target.closest('[data-close-drawer]')) closeDrawer(); }); }

  // category tabs
  var tabs=d.querySelectorAll('.tab');
  tabs.forEach(function(t, i){
    t.addEventListener('click', function(){
      tabs.forEach(function(x){ x.setAttribute('aria-selected','false'); d.getElementById(x.getAttribute('aria-controls')).hidden=true; });
      t.setAttribute('aria-selected','true'); d.getElementById(t.getAttribute('aria-controls')).hidden=false;
    });
    t.addEventListener('keydown', function(e){
      var k=e.key, n=null;
      if(k==='ArrowDown'||k==='ArrowRight') n=tabs[(i+1)%tabs.length];
      if(k==='ArrowUp'||k==='ArrowLeft') n=tabs[(i-1+tabs.length)%tabs.length];
      if(n){ e.preventDefault(); n.focus(); n.click(); }
    });
  });

  // solar savings estimator (indicative)
  var c=d.querySelector('.calc');
  if(c){
    var bill=c.querySelector('#bill'), out=c.querySelector('#billOut'), type='villa';
    var cfg={villa:{cov:.5,max:25,lo:4200,hi:5400}, business:{cov:.5,max:400,lo:3400,hi:4600}, factory:{cov:.45,max:2000,lo:2800,hi:3800}};
    var TARIFF=.45, SAVE_RATE=.42, YIELD=1600;
    function fmt(n){ return Math.round(n).toLocaleString(ar?'ar-AE':'en-AE'); }
    function run(){
      var b=+bill.value, k=cfg[type];
      out.textContent=(ar?'':'AED ')+fmt(b)+(ar?' درهم':'');
      var kwhYear=b/TARIFF*12, kw=Math.min(k.max, Math.max(3, kwhYear*k.cov/YIELD)), save=Math.min(kw*YIELD*SAVE_RATE, b*12*.9);
      var cost=(kw*(k.lo+k.hi)/2), pay=cost/save;
      c.querySelector('#rSize').textContent=kw.toFixed(1)+(ar?' كيلوواط':' kWp');
      c.querySelector('#rCost').textContent=(ar?'':'AED ')+fmt(kw*k.lo/1000)+'k–'+fmt(kw*k.hi/1000)+'k'+(ar?' درهم':'');
      c.querySelector('#rSave').textContent=(ar?'':'AED ')+fmt(save)+(ar?' درهم سنوياً':' / year');
      c.querySelector('#rPay').textContent=pay.toFixed(1)+(ar?' سنوات':' years');
      var q=c.querySelector('.btn'); if(q){ q.dataset.msg=(ar?'تقدير الطاقة الشمسية: فاتورة شهرية ':'Solar estimate: monthly bill AED ')+fmt(b)+', '+kw.toFixed(1)+' kWp, '+type; }
    }
    bill.addEventListener('input', run);
    c.querySelectorAll('.seg button').forEach(function(b){ b.addEventListener('click', function(){ c.querySelectorAll('.seg button').forEach(function(x){x.setAttribute('aria-pressed','false');}); b.setAttribute('aria-pressed','true'); type=b.dataset.t; run(); }); });
    run();
    var cb=c.querySelector('.btn');
    if(cb) cb.addEventListener('click', function(e){ e.preventDefault(); window.open('https://wa.me/971507867872?text='+encodeURIComponent((ar?'مرحباً فيفكو، أود معاينة مجانية للطاقة الشمسية. ':'Hello FEFCO, I would like a free solar site survey. ')+(cb.dataset.msg||'')),'_blank','noopener'); });
  }

  // lead form -> WhatsApp (works without a backend)
  d.querySelectorAll('form.lead-form').forEach(function(f){
    f.addEventListener('submit', function(e){
      e.preventDefault();
      var g=function(n){ var el=f.elements[n]; return el?el.value.trim():''; };
      var err=f.querySelector('.form-err');
      if(!g('name')||g('phone').replace(/\D/g,'').length<7){ err.classList.add('show'); f.elements[g('name')?'phone':'name'].focus(); return; }
      err.classList.remove('show');
      var L=ar?['طلب جديد من موقع fefco.ae','الاسم','الجوال','البريد','الخدمة','الإمارة','التفاصيل','الصفحة']:['New enquiry from fefco.ae','Name','Mobile','Email','Service','Emirate','Details','Page'];
      var msg=L[0]+'\n'+L[1]+': '+g('name')+'\n'+L[2]+': '+g('phone')+(g('email')?'\n'+L[3]+': '+g('email'):'')+'\n'+L[4]+': '+g('service')+'\n'+L[5]+': '+g('emirate')+(g('message')?'\n'+L[6]+': '+g('message'):'')+'\n'+L[7]+': '+location.pathname;
      if(window.dataLayer) window.dataLayer.push({event:'generate_lead', service:g('service')});
      window.open('https://wa.me/971507867872?text='+encodeURIComponent(msg),'_blank','noopener');
    });
  });

  // track WhatsApp / phone clicks for ads conversion
  d.addEventListener('click', function(e){
    var a=e.target.closest('a[href^="https://wa.me"],a[href^="tel:"]');
    if(a && window.dataLayer) window.dataLayer.push({event: a.href.indexOf('tel:')===0?'click_call':'click_whatsapp'});
  });
})();
