/* <county-map> — Kenya county choropleth built on real Natural Earth geometry.
   Country outline comes from world-atlas TopoJSON; counties are plotted at their
   true coordinates. Attributes: places (JSON), selected, legend (JSON), height. */
(function(){
  const ATLAS = 'https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/countries-110m.json';
  let atlasPromise = null;

  function libsReady(){
    return new Promise(res => {
      const tick = () => (window.d3 && window.topojson) ? res() : setTimeout(tick, 60);
      tick();
    });
  }
  function loadKenya(){
    if(!atlasPromise){
      atlasPromise = libsReady()
        .then(() => fetch(ATLAS))
        .then(r => r.json())
        .then(topo => {
          const fc = window.topojson.feature(topo, topo.objects.countries);
          return fc.features.find(f => f.properties && f.properties.name === 'Kenya');
        });
    }
    return atlasPromise;
  }

  class CountyMap extends HTMLElement {
    static get observedAttributes(){ return ['places','selected','legend','height']; }
    connectedCallback(){ this.render(); }
    attributeChangedCallback(){ if(this.isConnected) this.render(); }
    parse(name, fallback){ try { return JSON.parse(this.getAttribute(name) || ''); } catch(e){ return fallback; } }

    async render(){
      const places = this.parse('places', []);
      const legend = this.parse('legend', []);
      const selected = this.getAttribute('selected') || '';
      const h = Number(this.getAttribute('height') || 320);
      this.style.display = 'block';

      if(!this._shell){
        this._shell = document.createElement('div');
        this.appendChild(this._shell);
      }
      const shell = this._shell;
      shell.innerHTML = '<div style="font-size:11px;color:#5b6270;padding:6px 0;">Loading county geometry…</div>';

      let kenya;
      try { kenya = await loadKenya(); } catch(e){ kenya = null; }
      if(!kenya){
        shell.innerHTML = '<div style="font-size:11.5px;color:#b8395b;padding:8px 0;line-height:1.5;">County geometry could not be loaded. The simple view still works.</div>';
        return;
      }

      const d3 = window.d3;
      const w = this.clientWidth || 360;
      const proj = d3.geoMercator().fitSize([w, h], kenya);
      const path = d3.geoPath(proj);

      const svg = d3.create('svg')
        .attr('viewBox', '0 0 ' + w + ' ' + h)
        .attr('width', '100%')
        .attr('height', h)
        .style('display', 'block');

      svg.append('path')
        .attr('d', path(kenya))
        .attr('fill', '#f2eee4')
        .attr('stroke', '#c9c2ae')
        .attr('stroke-width', 1);

      // Voronoi-style county fills clipped to Kenya: each county's catchment tinted.
      const pts = places.map(p => proj([p.lon, p.lat]));
      if(pts.length > 2){
        const clip = svg.append('defs').append('clipPath').attr('id', 'ke-clip-' + Math.random().toString(36).slice(2));
        clip.append('path').attr('d', path(kenya));
        const del = d3.Delaunay.from(pts);
        const vor = del.voronoi([0, 0, w, h]);
        const g = svg.append('g').attr('clip-path', 'url(#' + clip.attr('id') + ')');
        places.forEach((p, i) => {
          g.append('path')
            .attr('d', vor.renderCell(i))
            .attr('fill', p.fill || '#f7f4ec')
            .attr('fill-opacity', 0.55)
            .attr('stroke', '#ffffff')
            .attr('stroke-width', 0.8)
            .style('cursor', 'pointer')
            .on('click', () => this.dispatchEvent(new CustomEvent('pick', {detail:p.name, bubbles:true})));
        });
        svg.append('path')
          .attr('d', path(kenya))
          .attr('fill', 'none')
          .attr('stroke', '#8b8371')
          .attr('stroke-width', 1.1);
      }

      const placed = [];
      const order = places.map((p,i)=>({p,i,xy:pts[i]})).filter(o=>o.xy).sort((a,b)=>a.xy[1]-b.xy[1]);
      order.forEach(o => {
        const p = o.p, i = o.i;
        let xy = o.xy.slice();
        while(placed.some(q => Math.abs(q[1]-xy[1]) < 12 && Math.abs(q[0]-xy[0]) < 78)) xy[1] += 12;
        placed.push(xy);
        o.labelXY = xy;
        const sel = p.name === selected;
        const g = svg.append('g')
          .style('cursor', 'pointer')
          .on('click', () => this.dispatchEvent(new CustomEvent('pick', {detail:p.name, bubbles:true})));
        g.append('circle')
          .attr('cx', o.xy[0]).attr('cy', o.xy[1])
          .attr('r', sel ? 6 : 4)
          .attr('fill', p.dot || '#1b1f27')
          .attr('stroke', '#ffffff')
          .attr('stroke-width', sel ? 2 : 1.2);
        g.append('text')
          .attr('x', xy[0] + (sel ? 10 : 8))
          .attr('y', xy[1] + 3.5)
          .attr('font-size', sel ? 11.5 : 10.5)
          .attr('font-weight', sel ? 700 : 500)
          .attr('font-family', 'Söhne, Helvetica Neue, Arial, sans-serif')
          .attr('fill', '#1b1f27')
          .text(p.name)
          .clone(true).lower()
          .attr('stroke', '#f7f4ec').attr('stroke-width', 3.5).attr('stroke-linejoin', 'round');
      });

      shell.innerHTML = '';
      shell.appendChild(svg.node());

      if(legend.length){
        const wrap = document.createElement('div');
        wrap.style.cssText = 'display:flex;gap:14px;flex-wrap:wrap;margin-top:12px;';
        legend.forEach(l => {
          const item = document.createElement('div');
          item.style.cssText = 'display:flex;align-items:center;gap:6px;';
          const sw = document.createElement('span');
          sw.style.cssText = 'width:11px;height:11px;border-radius:3px;flex-shrink:0;background:' + l.swatch + ';';
          const tx = document.createElement('span');
          tx.style.cssText = 'font-size:11px;color:#5b6270;';
          tx.textContent = l.label;
          item.appendChild(sw); item.appendChild(tx); wrap.appendChild(item);
        });
        shell.appendChild(wrap);
      }
      const src = document.createElement('div');
      src.style.cssText = 'font-size:10px;color:#8b8371;margin-top:9px;';
      src.textContent = 'Outline: Natural Earth (public domain). Tinted areas are county catchments, not surveyed county boundaries.';
      shell.appendChild(src);
    }
  }
  if(!customElements.get('county-map')) customElements.define('county-map', CountyMap);
})();
