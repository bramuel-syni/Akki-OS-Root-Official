import React from 'react';

const camel = value => value.replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
const forbidden = new Set(['__proto__', 'constructor', 'prototype']);
const booleanAttrs = new Set(['disabled', 'checked', 'selected', 'multiple', 'required', 'autoFocus']);
const voidTags = new Set(['area', 'br', 'col', 'embed', 'hr', 'img', 'input', 'meta', 'source', 'wbr']);

export function resolveBinding(expression, model) {
  const key = expression.trim();
  if (key === 'true') return true;
  if (key === 'false') return false;
  if (key.startsWith('!')) {
    const value = resolveBinding(key.slice(1), model);
    return value === undefined ? false : !value;
  }
  if (!/^[\w$.]+$/.test(key)) return undefined;
  return key.split('.').reduce((value, part) => forbidden.has(part) ? undefined : value?.[part], model);
}

function interpolate(value, model) {
  if (typeof value !== 'string') return value;
  const exact = value.match(/^{{\s*(.*?)\s*}}$/);
  if (exact) return resolveBinding(exact[1], model);
  return value.replace(/{{\s*(.*?)\s*}}/g, (_, key) => {
    const result = resolveBinding(key, model);
    return result == null || typeof result === 'object' ? '' : String(result);
  });
}

export function styleObject(raw, model) {
  // CSSOM expands variable-valued shorthands to empty longhands. Preserve declarations verbatim.
  const declarations = [];
  let current = '', depth = 0, quote = null;
  for (const char of interpolate(raw, model) || '') {
    if (quote) { current += char; if (char === quote) quote = null; continue; }
    if (char === '"' || char === "'") { quote = char; current += char; continue; }
    if (char === '(') depth += 1;
    if (char === ')') depth -= 1;
    if (char === ';' && depth === 0) { declarations.push(current); current = ''; }
    else current += char;
  }
  if (current) declarations.push(current);
  const out = {};
  for (const declaration of declarations) {
    const separator = declaration.indexOf(':');
    if (separator < 1) continue;
    const name = declaration.slice(0, separator).trim();
    const value = declaration.slice(separator + 1).trim();
    if (value) out[name.startsWith('--') ? name : camel(name)] = value;
  }
  // Preserve the owner's dimensions; normalize negative tracking only.
  if (String(out.letterSpacing || '').startsWith('-')) out.letterSpacing = 0;
  return out;
}

/** Declarative original markup only. No eval, iframe, prototype runtime, timers, or mock scripts. */
export function OwnerMarkup({ template, surface, model, replace = {}, slots = {}, enhance = {}, onUnbound, fragment = false }) {
  const render = (nodes, context = model, trace = 'r') => nodes.map((node, index) => {
    const key = `${trace}-${index}`;
    if (typeof node === 'string') return <React.Fragment key={key}>{interpolate(node, context)}</React.Fragment>;
    const { tag, attributes: attrs, line, children } = node;
    if (['script', 'iframe', 'link', 'title', 'meta'].includes(tag)) return null;
    if (tag === 'helmet' || tag === 'x-dc') return <React.Fragment key={key}>{render(children, context, key)}</React.Fragment>;
    if (tag === 'style') return <style key={key}>{children.filter(c => typeof c === 'string').join('')}</style>;
    if (tag === 'sc-if') return interpolate(attrs.value, context) ? <React.Fragment key={key}>{render(children, context, key)}</React.Fragment> : null;
    if (tag === 'sc-for') {
      const list = interpolate(attrs.list, context);
      return Array.isArray(list) ? list.map((item, i) => <React.Fragment key={`${key}-${item.key || item.id || i}`}>{render(children, { ...context, [attrs.as]: item, $index: i }, `${key}-i${i}`)}</React.Fragment>) : null;
    }
    const props = { key, 'data-proto-line': surface.startsWith('nexus-') ? `nexus-${line}` : line };
    let action;
    Object.entries(attrs).forEach(([rawName, rawValue]) => {
      if (rawName.startsWith('hint-') || rawName === 'ref' || rawName === 'style-hover') return;
      if (rawName === 'style') { props.style = styleObject(rawValue, context); return; }
      let name = rawName.startsWith('sc-camel-') ? camel(rawName.slice(9)) : rawName;
      name = ({ class: 'className', for: 'htmlFor', tabindex: 'tabIndex', 'stroke-width': 'strokeWidth', 'stroke-linecap': 'strokeLinecap', 'stroke-linejoin': 'strokeLinejoin', 'stroke-dasharray': 'strokeDasharray', 'fill-rule': 'fillRule', 'clip-rule': 'clipRule' })[name] || name;
      const value = interpolate(rawValue, context);
      if (name.startsWith('on')) {
        if (name === 'onClick') action = rawValue.replace(/[{}]/g, '').trim();
        props[name] = typeof value === 'function' ? value : name === 'onClick' ? () => onUnbound?.(action) : undefined;
      } else if (booleanAttrs.has(name)) props[name] = Boolean(value);
      else if (value != null && typeof value !== 'object') props[name] = value;
    });
    const actionId = action?.replace(/([a-z])([A-Z])/g, '$1-$2').replaceAll('.', '-').toLowerCase();
    if (attrs['style-hover']) {
      const hover = styleObject(attrs['style-hover'], context);
      props.onMouseEnter = event => Object.entries(hover).forEach(([name, value]) => { event.currentTarget.style[name] = value; });
      props.onMouseLeave = event => Object.keys(hover).forEach(name => { event.currentTarget.style[name] = props.style?.[name] || ''; });
    }
    props['data-testid'] = `prototype-${surface}-${actionId || tag}-${line}-${key.replaceAll('r-', '')}`;
    if (action) {
      props['data-action'] = action;
      if (!['button', 'a', 'input', 'select'].includes(tag)) {
        props.role = 'button'; props.tabIndex = 0;
        props.onKeyDown = event => { if (event.target === event.currentTarget && ['Enter', ' '].includes(event.key)) { event.preventDefault(); props.onClick?.(event); } };
      }
      const expanded = context.disclosureStates?.[action];
      if (expanded !== undefined) props['aria-expanded'] = expanded;
    }
    if (props.id === 'dap-nav') props['aria-label'] = 'Data Access Portal navigation';
    if (line === (surface === 'os' ? 29 : 27)) props['data-proto-root'] = surface;
    if (enhance[line]) Object.assign(props, typeof enhance[line] === 'function' ? enhance[line](context, props) : enhance[line]);
    if (line in slots) return React.createElement(tag, props, slots[line]);
    if (line in replace) {
      const value = typeof replace[line] === 'function' ? replace[line](context) : replace[line];
      return React.createElement(tag, props, typeof value === 'string' ? interpolate(value, context) : value);
    }
    return React.createElement(tag, props, voidTags.has(tag) ? undefined : render(children, context, key));
  });
  return fragment ? <>{render(template.nodes)}</> : <div className={`owner-prototype owner-prototype-${surface}`} data-testid={`owner-prototype-${surface}`}>{render(template.nodes)}</div>;
}