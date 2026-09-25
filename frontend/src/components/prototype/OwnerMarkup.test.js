import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server.node';
import { OwnerMarkup, styleObject, resolveBinding } from './OwnerMarkup';

test('F02/F03 keeps CSS variable shorthands, card borders and original backgrounds', () => {
  expect(styleObject('--blue:#16274a;background:var(--blue);border:1px solid var(--line);padding:20px 22px;border-radius:14px;', {})).toEqual({
    '--blue': '#16274a', background: 'var(--blue)', border: '1px solid var(--line)', padding: '20px 22px', borderRadius: '14px',
  });
});

test('CSS functions and quoted semicolons survive without reinterpreting the template', () => {
  const value = styleObject('background:linear-gradient(90deg,red,blue);font-family:"Some; Font",serif;width:{{ width }};', { width: '45%' });
  expect(value.background).toBe('linear-gradient(90deg,red,blue)');
  expect(value.fontFamily).toBe('"Some; Font",serif');
  expect(value.width).toBe('45%');
});

test('unbound branches stay closed and prototype code cannot execute as expressions', () => {
  expect(resolveBinding('missing', {})).toBeUndefined();
  expect(resolveBinding('!missing', {})).toBe(false);
  expect(resolveBinding('Date.now()', {})).toBeUndefined();
  expect(resolveBinding('constructor.prototype', {})).toBeUndefined();
  expect(resolveBinding('!open', { open: false })).toBe(true);
});

test('F08 model-supplied icon elements have a stable keyed text binding', () => {
  const errors = jest.spyOn(console, 'error').mockImplementation(() => {});
  const template = { nodes: [{ tag: 'div', line: 1, attributes: {}, children: ['{{ icon }}', 'Bound value'] }] };
  renderToStaticMarkup(<OwnerMarkup template={template} surface="os" model={{ icon: <span>Icon</span> }} />);
  expect(errors.mock.calls.filter(args => args.some(a => String(a).includes('unique "key"')))).toHaveLength(0);
  errors.mockRestore();
});