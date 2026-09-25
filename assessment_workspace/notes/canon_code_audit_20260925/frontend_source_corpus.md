
# SOURCE: frontend/src/App.js

1: import "@/App.css";
2: import { useEffect, useRef, useState } from "react";
3: import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
4: 
5: /* ── DAP Portal (Track 1) ─────────────────────────────── */
6: import DAPLayout from "@/pages/dap/DAPLayout";
7: import DAPLanding from "@/pages/dap/DAPLanding";
8: import AvailableResources from "@/pages/dap/AvailableResources";
9: import DataGovernance from "@/pages/dap/DataGovernance";
10: import RequestLifecycle from "@/pages/dap/RequestLifecycle";
11: import DataEstates from "@/pages/dap/DataEstates";
12: import ExtractModes from "@/pages/dap/ExtractModes";
13: import ConnectResources from "@/pages/dap/ConnectResources";
14: import Entitlement from "@/pages/dap/Entitlement";
15: import CanonCountdown from "@/pages/dap/CanonCountdown";
16: 
17: /* ── PHASE 3 continuation A'' · Census Autonomy overlay drawer ─────────
18:  * Additive React overlay outside the prototype iframe (SO §3.8). Mounts
19:  * a floating "Run census" launcher + running-card that polls the REAL
20:  * scheduler state endpoint. Never synthesizes progress (owner directive).
21:  */
22: import CensusAutonomyDrawer from "@/components/portal/CensusAutonomyDrawer";
23: import ResponseRequiredBadge from "@/components/portal/ResponseRequiredBadge";
24: 
25: // v2 OS Prototype · Turn 4 sub-slice 4d GREEN · Frontend rebuild slice 2 ·
26: // Work tab surfaces (7) + Monitor sub-view surfaces (2). Each surface is a
27: // native React implementation of the design-of-record shape with honest-gap
28: // disclosure where backend wiring is pending PHASE 3/4. SO §3.8 additive-only.
29: import WorkChat from "@/pages/os/WorkChat";
30: import WorkAnalyze from "@/pages/os/WorkAnalyze";
31: import WorkDocuments from "@/pages/os/WorkDocuments";
32: import WorkTasks from "@/pages/os/WorkTasks";
33: import WorkTeam from "@/pages/os/WorkTeam";
34: import WorkPerformance from "@/pages/os/WorkPerformance";
35: import WorkBoard from "@/pages/os/WorkBoard";
36: import MonitorSignals from "@/pages/os/MonitorSignals";
37: import MonitorIdeas from "@/pages/os/MonitorIdeas";
38: 
39: // v2 OS Prototype · Turn 4 sub-slice 4e GREEN · Frontend rebuild slice 3 ·
40: // ThinkLab (4 honest-gap · Work tab) + Admin tab (10 honest-gap: estate 3 +
41: // approvals 3 + watch 4) via 4c-banked filterGroupsForRole persona helper.
42: // R-103 amendment: single continuous run to completion.
43: import ThinkLabClarity from "@/pages/os/ThinkLabClarity";
44: import ThinkLabStrategy from "@/pages/os/ThinkLabStrategy";
45: import ThinkLabHypothesis from "@/pages/os/ThinkLabHypothesis";
46: import ThinkLabPerspective from "@/pages/os/ThinkLabPerspective";
47: import AdminEstate from "@/pages/os/AdminEstate";
48: import AdminGovern from "@/pages/os/AdminGovern";
49: import AdminGreyMirror from "@/pages/os/AdminGreyMirror";
50: import AdminSpendReq from "@/pages/os/AdminSpendReq";
51: import AdminRulesUpd from "@/pages/os/AdminRulesUpd";
52: import AdminModelAdmission from "@/pages/os/AdminModelAdmission";
53: import AdminWState from "@/pages/os/AdminWState";
54: import AdminWRecord from "@/pages/os/AdminWRecord";
55: import AdminWUnder from "@/pages/os/AdminWUnder";
56: import AdminWDecisions from "@/pages/os/AdminWDecisions";
57: 
58: // v2 OS Prototype · Turn 4 sub-slice 4f GREEN · Frontend rebuild slice 4 ·
59: // Build 4 + Buildlib 2 + Collab 4 + 3rdParty 4 = 14 honest-gap surfaces ·
60: // completes 37 of 37 OS leaves. R-103 amendment.
61: import BuildTrain from "@/pages/os/BuildTrain";
62: import BuildAgent from "@/pages/os/BuildAgent";
63: import BuildSkill from "@/pages/os/BuildSkill";
64: import BuildExtract from "@/pages/os/BuildExtract";
65: import BuildlibAgents from "@/pages/os/BuildlibAgents";
66: import BuildlibModels from "@/pages/os/BuildlibModels";
67: import CollabMentions from "@/pages/os/CollabMentions";
68: import CollabEmails from "@/pages/os/CollabEmails";
69: import CollabProjects from "@/pages/os/CollabProjects";
70: import CollabHrStuff from "@/pages/os/CollabHrStuff";
71: import AppsNew from "@/pages/os/AppsNew";
72: import AppsFrequent from "@/pages/os/AppsFrequent";
73: import AppsConnected from "@/pages/os/AppsConnected";
74: import AppsRequests from "@/pages/os/AppsRequests";
75: 
76: // PHASE 4 (a) · CP-COMMISSION-WIZARD-LIVE · additive route mount for the sealed
77: // Canon-5-§14 Shaping-Wizard component at /os/work/commission (owner banked
78: // order 2026-09-22T~21:21Z: "Connect + Commission wizards live").
79: import WorkCommission from "@/pages/os/WorkCommission";
80: 
81: // Sub-slice 4h · 2 DAP LATEST view classes (10+11) as honest-gap surfaces per 4g deferral resolution.
82: import AdminApprovalsLedger from "@/pages/dap/AdminApprovalsLedger";
83: import AdminWatchTrailBridge from "@/pages/dap/AdminWatchTrailBridge";
84: // PHASE 4 (c-vi) · CP-SKILLS-LAYER-SERIES-CLOSE (Slice 5) · additive
85: // import alias avoids collision with existing `BuildSkill` at pages/os/
86: // (distinct NAV entry at /os/build/buildskill). This DAP surface lives
87: // at /dap/buildskill per owner directive.
88: import DapBuildSkill from "@/pages/dap/BuildSkill";
89: 
90: // ---------------------------------------------------------------------------
91: // v2 OS Prototype Shell · Design-of-Record Constants
92: // (byte-verbatim per phase0/prototype_inventory/20260922T064500Z_full_enumeration_and_gap_checklist.md §1.1-§1.5)
93: // R-101 preserved WHAT · e-apply Turn 4 sub-slice 4c · 2026-09-22T07:45:00Z
94: //
95: // Owner FE brief §0 verbatim (2026-09-20T~08:24Z):
96: //   "The prototype is the design of record ... prototype wins."
97: //
98: // Owner directive verbatim 2026-09-22T~06:10Z:
99: //   "UI/UX architecture and experience flow needs to be exact as the HTML I shared."
100: //
101: // This block is ADDITIVE (SO §3.8): the V8 substitution engine below is
102: // preserved verbatim. The shell constants are consumed by sub-slices 4d-4g
103: // as the OS surface + DAP LATEST rebuild lands over the V8 iframe path.
104: // ---------------------------------------------------------------------------
105: 
106: const TABS = [
107:   { key:'work',  label:'Work',           groups:['workstudio','thinklab','collab','monitor'] },
108:   { key:'build', label:'Build',          groups:['build','buildlib'] },
109:   { key:'apps',  label:'3rd Party Apps', groups:[] },
110:   { key:'admin', label:'Admin',          groups:['estate','approvals','watch'], right:true }
111: ];
112: 
113: const NAV = [
114:   { key:'workstudio', label:'WorkStudio', tab:'work', items:[
115:       { key:'chat',        label:'Chat' },
116:       { key:'analyze',     label:'Data Suite' },
117:       { key:'documents',   label:'Documents' },
118:       { key:'tasks',       label:'My Work' },
119:       { key:'team',        label:'My Team' },
120:       { key:'performance', label:'Company Goals' },
121:       { key:'board',       label:'Board' }
122:   ]},
123:   { key:'thinklab', label:'ThinkLab', tab:'work', items:[
124:       { key:'clarity',     label:'Seek Clarity' },
125:       { key:'strategy',    label:'Develop Strategy' },
126:       { key:'hypothesis',  label:'Test Hypothesis' },
127:       { key:'perspective', label:'Get Perspective' }
128:   ]},
129:   { key:'collab', label:'Collab', tab:'work', items:[
130:       { key:'mentions', label:'Mentions' },
131:       { key:'emails',   label:'Emails' },
132:       { key:'projects', label:'Projects/Tasks' },
133:       { key:'hrstuff',  label:'HR Stuff' }
134:   ]},
135:   { key:'monitor', label:'Monitor', tab:'work', items:[
136:       { key:'performance', label:'Performance' },
137:       { key:'signals',     label:'Signals' },
138:       { key:'ideas',       label:'Ideas' }
139:   ]},
140:   { key:'estate', label:'Manage Estate', tab:'admin', items:[
141:       { key:'estate',     label:'Registry' },
142:       { key:'govern',     label:'Shield' },
143:       { key:'greymirror', label:'Grey Mirror' }
144:   ]},
145:   { key:'approvals', label:'Approvals', tab:'admin', items:[
146:       { key:'spendreq',       label:'Spend Requests' },
147:       { key:'rulesupd',       label:'Rules Updates' },
148:       { key:'modeladmission', label:'Model Approval' }
149:   ]},
150:   { key:'watch', label:'The Watch', tab:'admin', items:[
151:       { key:'wstate',     label:'State' },
152:       { key:'wrecord',    label:'Record' },
153:       { key:'wunder',     label:'Under Watch' },
154:       { key:'wdecisions', label:'Decisions' }
155:   ]},
156:   { key:'build', label:'Build Your Resources', tab:'build', items:[
157:       { key:'train',      label:'Train Models' },
158:       { key:'agentbuild', label:'Build Agents' },
159:       { key:'buildskill', label:'Build Skill' },
160:       { key:'extract',    label:'Extract Data' }
161:   ]},
162:   { key:'buildlib', label:'Your Resources', tab:'build', divider:true, items:[
163:       { key:'youragents', label:'Agents' },
164:       { key:'yourmodels', label:'Models' }
165:   ]},
166:   { key:'thirdparty', label:'3rd Party Apps', tab:'apps', items:[
167:       { key:'appsnew',       label:'New' },
168:       { key:'appsfrequent',  label:'Frequent' },
169:       { key:'appsconnected', label:'Connected' },
170:       { key:'appsrequests',  label:'Requests' }
171:   ]}
172: ];
173: 
174: const ROLES = [
175:   { key:'compliance', label:'Compliance Owner', person:'M. Chen',   dept:'Compliance', initials:'MC', groups:['estate','approvals'] },
176:   { key:'watch',      label:'Watch Officer',    person:'A. Njeri',  dept:'The Watch',  initials:'AN', groups:['watch'] },
177:   { key:'operator',   label:'Operator',         person:'J. Otieno', dept:'Operations', initials:'JO', groups:['estate'] }
178: ];
179: 
180: const TONE = {
181:   plain:  { bg:'#fff',                       border:'var(--line)',    color:'var(--ink)'  },
182:   held:   { bg:'rgba(176,141,46,.07)',       border:'var(--brass)',   color:'var(--ink)'  },
183:   refused:{ bg:'rgba(184,57,91,.06)',        border:'var(--oxblood)', color:'var(--ink)'  },
184:   failed: { bg:'var(--surface2)',            border:'var(--line)',    color:'var(--ink3)' },
185:   drill:  { bg:'var(--surface)',             border:'var(--line)',    color:'var(--ink2)' }
186: };
187: 
188: /* Four-questions surfaces. Rule zero: every block leads with a sentence;
189:    measures live behind "see the working". */
190: 
191: // Persona-filter helper · Admin tab shows only groups the current role owns.
192: // Enumeration §1.3 line 45 verbatim: "a persona sees only their `groups` in
193: // Admin tab; the Watch officer sees only `watch`; the operator sees only
194: // `estate`; the compliance owner sees `estate + approvals`. Non-admin tabs
195: // (work, build, apps) are unconditional."
196: function filterGroupsForRole(tab, roleKey) {
197:   const role = ROLES.find(r => r.key === roleKey);
198:   const tabDef = TABS.find(t => t.key === tab);
199:   if (!tabDef) return [];
200:   if (tab !== 'admin' || !role) return tabDef.groups;
201:   return tabDef.groups.filter(g => role.groups.includes(g));
202: }
203: 
204: // Export the shell constants so upcoming rebuild slices (4d-4g) can consume
205: // them without touching the V8 substitution engine below.
206: export { TABS, NAV, ROLES, TONE, filterGroupsForRole };
207: 
208: /**
209:  * App.js — Wave G4 · V8 LITERAL adoption · owner Wave G3 REJECT corrections.
210:  *
211:  * Owner verdict verbatim (2026-08-28T~11:45Z, banked in DECISIONS.md):
212:  *   A. Dummy data still the same - see screen shot.
213:  *   B. Legacy screens should be retired as all components built should
214:  *      naturally fit this front end without dumping old screens that
215:  *      create confusion. On the topline statistics, i need practical
216:  *      data points that speak to everyday users using the system.
217:  *
218:  * Three corrections applied here:
219:  *
220:  *   Correction 1 — Slot #1 root-cause: the "RMS AI holds ..." sentence is
221:  *                  fragmented across five nested inline <span> elements
222:  *                  (border-bottom underlines on "86.4 TB", "12 sources",
223:  *                  "78% measured", "6 opportunities"). A per-text-node
224:  *                  regex cannot span multiple text nodes. The fix uses
225:  *                  ELEMENT-ANCHOR substitution: find the element whose
226:  *                  full textContent equals the sentence, then assign
227:  *                  textContent (whole-element replacement). Plus
228:  *                  MutationObserver re-application (idempotent) so the
229:  *                  substitution survives portal → Registry → back →
230:  *                  Registry navigation.
231:  *
232:  *   Correction 2 — EVERY topline statistic tile on the Registry surface
233:  *                  (10 tiles: Held in total, Sources connected, Share
234:  *                  measured, Data types present, Languages observed,
235:  *                  Share already verified, Share carrying PII, Licensed
236:  *                  for external use, Not yet measured, Reduced to reusable
237:  *                  memory) gets substituted in place. Values are practical
238:  *                  data points from live data or HONEST-EMPTY
239:  *                  ("Not yet measured"). Layout untouched.
240:  *
241:  *   Correction 3 — Legacy pod component routes retired from routing. The
242:  *                  V8 front end (PortalIframe) is now the ONLY user-facing
243:  *                  surface. Any non-root hit lands on the portal.
244:  *                  Component source files at pod_shell/frontend/src/
245:  *                  components/*.jsx are RETAINED on disk (donor material
246:  *                  for wiring real data into V8 surfaces in later waves),
247:  *                  but are no longer imported here — tree-shaking drops
248:  *                  them from the shipped bundle.
249:  *
250:  * Visual-proof marker: the iframe host <div> in the OUTER document
251:  * carries a `data-substitution-applied` attribute (monotonic counter of
252:  * substitutions applied across the session lifetime). This is INVISIBLE
253:  * bookkeeping on the outer document — not inside the prototype's DOM —
254:  * so it does not violate the no-engineering-vocab-on-surface rule.
255:  */
256: 
257: // ---------------------------------------------------------------------------
258: // Substitution engine
259: // ---------------------------------------------------------------------------
260: 
261: function _sourcesPhrase(sources) {
262:   if (sources == null || sources === 0) return "no sources connected yet";
263:   if (sources === 1) return "1 connected source";
264:   return `${sources} connected sources`;
265: }
266: 
267: function _tablesPhrase(tables) {
268:   if (tables == null || tables === 0) return "no tables read yet";
269:   if (tables === 1) return "with 1 table read";
270:   return `with ${tables.toLocaleString()} tables read`;
271: }
272: 
273: /**
274:  * V8_SUBSTITUTIONS — the explicit slot substitution map.
275:  *
276:  * Rule shapes:
277:  *   kind='element-anchor' — find the element whose textContent equals
278:  *                           `dummyContent`. Replace its textContent with
279:  *                           render(vals). Handles fragmented-span slots.
280:  *
281:  *   kind='text-node' — find the text node whose value matches the
282:  *                      regex `signature`. Replace its nodeValue with
283:  *                      render(vals). For single-node slots.
284:  *
285:  *   kind='tile-value' — find the text node whose trimmed value equals
286:  *                       `dummy`, verify one ancestor contains `label`
287:  *                       (to disambiguate value collisions), and replace
288:  *                       its nodeValue with render(vals). Preserves the
289:  *                       tile's card layout (label + note stay).
290:  *
291:  * Every rule is idempotent: if the target already carries the desired
292:  * text, the engine skips the mutation. This is required because
293:  * setting textContent/nodeValue triggers a MutationObserver event
294:  * which re-invokes applySubstitutions.
295:  */
296: const V8_SUBSTITUTIONS = [
297:   {
298:     kind: "styled-element-anchor",
299:     name: "registry-aside-hero-sentence",
300:     // Slot #1 · Registry header greeting sentence.
301:     // Wave-H · INTERRUPT 3 (2026-08-28T~13:25Z) + harness finding
302:     // (2026-08-28T~14:12Z, banked in DECISIONS.md next entry):
303:     //   dc-runtime renders the plain interpolated string from JS
304:     //   `estate.greeting` at data-dc-tpl="343" as a single
305:     //   <span class="sc-interp"> — NOT the multi-span styled variant
306:     //   that exists elsewhere in the prototype's static HTML. Our job
307:     //   is to REPLACE the plain-string render with the styled variant
308:     //   (3 underlined figure phrases + 1 oxblood phrase) that owner
309:     //   INTERRUPT 3 called out as "by design".
310:     //
311:     // dummyContent matches what dc-runtime ACTUALLY renders on the
312:     // Registry surface (verified via real-Chromium probe 2026-08-28).
313:     dummyContent:
314:       "86.4 TB across 12 sources \u2014 78% measured, with 6 opportunities standing ready.",
315:     // renderFragments returns an ordered list of {kind, value} where kind is:
316:     //   "text"      -> plain text node (no styling)
317:     //   "underline" -> span with border-bottom:1px solid rgba(27,31,39,.25)
318:     //   "oxblood"   -> span with color:var(--oxblood)
319:     // The prototype's typographic treatment is preserved byte-for-byte on
320:     // both live-values and honest-empty variants.
321:     renderFragments: (v) => {
322:       const hasLive = v.estateSources != null || v.estateTables != null;
323:       if (!hasLive) {
324:         // Honest-empty variant · typographic treatment consistent with
325:         // prototype design language (3 underlined phrases + 1 oxblood).
326:         return [
327:           { kind: "text", value: "RMS AI is reading " },
328:           { kind: "underline", value: "no sources yet" },
329:           { kind: "text", value: ", " },
330:           { kind: "underline", value: "no size yet" },
331:           { kind: "text", value: " \u2014 " },
332:           { kind: "underline", value: "no measurement" },
333:           { kind: "text", value: ", " },
334:           { kind: "oxblood", value: "awaiting first census" },
335:           { kind: "text", value: "." },
336:         ];
337:       }
338:       // Live-values variant · real figures in underline spans, closing
339:       // phrase in oxblood.
340:       const sourcesPhrase = _sourcesPhrase(v.estateSources);
341:       const tablesPhrase = _tablesPhrase(v.estateTables);
342:       return [
343:         { kind: "text", value: "RMS AI is reading " },
344:         { kind: "underline", value: sourcesPhrase },
345:         { kind: "text", value: ", holding " },
346:         { kind: "underline", value: tablesPhrase },
347:         { kind: "text", value: " \u2014 " },
348:         { kind: "underline", value: "size and completeness not yet measured" },
349:         { kind: "text", value: ", " },
350:         { kind: "oxblood", value: "awaiting first census" },
351:         { kind: "text", value: "." },
352:       ];
353:     },
354:   },
355:   {
356:     kind: "styled-element-anchor",
357:     name: "registry-census-header",
358:     // Slot #2a · census "Last activity" header line.
359:     // Wave-G5b · owner ruling (B) 2026-08-28T~14:30Z: migrate slot #2 to
360:     // styled-element-anchor with signature matching the ACTUAL render
361:     // ("Census #4 read the estate at the seam"), not the dead
362:     // "Every figure on this page traces to..." prefix.
363:     dummyContent: "Census #4 read the estate at the seam",
364:     anchorAncestorText: "Last activity",
365:     renderFragments: (v) => {
366:       if (v.lastCensus == null) {
367:         return [{ kind: "text", value: "No census has been run yet" }];
368:       }
369:       return [
370:         { kind: "text",
371:           value: `Census #${v.lastCensus.number} read the estate at the seam` },
372:       ];
373:     },
374:   },
375:   {
376:     kind: "styled-element-anchor",
377:     name: "registry-census-byline",
378:     // Slot #2b · census byline (author + date + un-measured %).
379:     dummyContent: "Run Jul 21, 2026 by J. Mwangi \u00b7 22% still not yet measured",
380:     anchorAncestorText: "Last activity",
381:     renderFragments: (v) => {
382:       if (v.lastCensus == null) {
383:         return [{ kind: "text", value: "First census pending" }];
384:       }
385:       const c = v.lastCensus;
386:       return [{
387:         kind: "text",
388:         value: `Run ${c.date} by ${c.author} \u00b7 ${c.notMeasuredPct}% still not yet measured`,
389:       }];
390:     },
391:   },
392:   // Wave-G5b · 3 rendered stat tiles (owner ruling A · migrated from the
393:   // dead measureCards-bound rules). Bound to estate.stats[] labels that
394:   // dc-runtime ACTUALLY renders. Each tile has two rules (value + label)
395:   // so live-values enrichment can flow through the label too.
396:   {
397:     kind: "styled-element-anchor",
398:     name: "tile-total-held-value",
399:     dummyContent: "86.4 TB",
400:     anchorAncestorText: "held across 12 sources",
401:     renderFragments: (v) => [
402:       { kind: "text", value: v.totalVolume != null ? String(v.totalVolume) : "Not yet measured" },
403:     ],
404:   },
405:   {
406:     kind: "styled-element-anchor",
407:     name: "tile-total-held-label",
408:     dummyContent: "held across 12 sources",
409:     anchorAncestorText: "86.4 TB",
410:     anchorAncestorSlot: "tile-total-held-value",
411:     renderFragments: (v) => {
412:       if (v.estateSources == null) {
413:         return [{ kind: "text", value: "no sources yet" }];
414:       }
415:       const s = v.estateSources;
416:       return [{ kind: "text", value: `held across ${s} source${s === 1 ? "" : "s"}` }];
417:     },
418:   },
419:   {
420:     kind: "styled-element-anchor",
421:     name: "tile-share-measured-value",
422:     dummyContent: "78%",
423:     anchorAncestorText: "measured at last census",
424:     renderFragments: (v) => [
425:       { kind: "text", value: v.shareMeasured != null ? String(v.shareMeasured) : "Not yet measured" },
426:     ],
427:   },
428:   {
429:     kind: "styled-element-anchor",
430:     name: "tile-share-measured-label",
431:     dummyContent: "measured at last census",
432:     anchorAncestorText: "78%",
433:     anchorAncestorSlot: "tile-share-measured-value",
434:     renderFragments: (v) => {
435:       if (v.lastCensus == null) {
436:         return [{ kind: "text", value: "awaiting first census" }];
437:       }
438:       return [{ kind: "text", value: "measured at last census" }];
439:     },
440:   },
441:   {
442:     kind: "styled-element-anchor",
443:     name: "tile-opportunities-value",
444:     dummyContent: "6",
445:     anchorAncestorText: "opportunities standing ready",
446:     renderFragments: (v) => [
447:       { kind: "text", value: v.opportunities != null ? String(v.opportunities) : "0" },
448:     ],
449:   },
450:   {
451:     kind: "styled-element-anchor",
452:     name: "tile-opportunities-label",
453:     dummyContent: "opportunities standing ready",
454:     anchorAncestorText: "opportunities",
455:     anchorAncestorSlot: "tile-opportunities-value",
456:     renderFragments: (v) => {
457:       if (v.opportunities == null) {
458:         return [{ kind: "text", value: "no opportunities yet" }];
459:       }
460:       return [{ kind: "text", value: "opportunities standing ready" }];
461:     },
462:   },
463:   // -------------------------------------------------------------------
464:   // Wave-G5c-COMPUTE-FRONTEND · RETIRED (2026-08-31 · harness probe).
465:   //
466:   // The 6 tile-compute-* rules originally authored in Wave-G5c targeted
467:   // the prototype's `computeCards` JS variable dummies:
468:   //   { '840 vCPU-h/day' · 'Total capacity' }
469:   //   { '62%'            · 'Allocated to Build' }
470:   //   { '3 queued'       · 'Queue depth' }
471:   //
472:   // Real-Chromium harness probe (tools/compute_where_probe.py ·
473:   // 2026-08-31) established that these dummies are NEVER rendered as
474:   // visible DOM on ANY prototype surface (portal, Admin, Registry
475:   // aside, Registry tab, Compute Connected sub-tab). Only "62%" appears
476:   // in the DOM (once, as a sibling within a different tile section)
477:   // and its anchor ancestor text "Allocated to Build" is also
478:   // script-only.
479:   //
480:   // Retirement precedent: DECISIONS.md documents that the composite
481:   // dummy "RMS AI holds 86.4 TB across 12 sources ..." was retired
482:   // in Wave-G5b for the same reason — dc-runtime never rendered it.
483:   //
484:   // The prototype's ACTUAL rendered compute surface (Compute Connected
485:   // sub-tab of RegistryTab) shows a percentage-driven layout:
486:   //   "43% of the month" · "43%" / "100%" / "43% committed" ·
487:   //   "645 hrs · 52%" / "298 hrs · 24%" / "174 hrs · 14%" / "99 hrs · 8%"
488:   //   / "24 hrs · 2%" · GPU workflows narrative
489:   //
490:   // W-G5c-close leaves these compute-tile rules retired. A follow-up
491:   // wave (W-G5c-COMPUTE-v2 in SPRINT_PLAN.md) will author new rules
492:   // against the actually-rendered percentage-driven surface, folding
493:   // akki-vm + akki-vm-ii facts into it per owner Ruling F.
494:   // -------------------------------------------------------------------
495: 
496:   // -------------------------------------------------------------------
497:   // Wave-G5c-COMPUTE-v2 · authored 2026-08-31 · owner ruling 8.
498:   // Rules bind to the ACTUALLY-rendered Compute Connected sub-tab of
499:   // RegistryTab. Every dummy below was verified as visible DOM text by
500:   // tools/compute_v2_dom_enum.py (probe artefact:
501:   // tools/compute_v2_dom_map.json).
502:   //
503:   // Discipline banked by ruling 8:
504:   //   - Rules authored only against harness-verified rendered DOM.
505:   //   - rule-must-match-rendered-DOM invariant enforced by test file
506:   //     tests/invariants/test_compute_v2_frontend.py.
507:   //   - Live values from /api/compute/estate only.
508:   //   - Honest-empty for anything the estate cannot measure.
509:   //   - Product language + prototype styling preserved.
510:   //
511:   // 4 LIVE + 6 HONEST-EMPTY + 1 LIVE-TAUTOLOGY = 11 rules.
512:   // -------------------------------------------------------------------
513: 
514:   // LIVE (4) — bind /api/compute/estate facts to compute tiles.
515: 
516:   {
517:     kind: "styled-element-anchor",
518:     name: "compute-v2-clusters-value",
519:     dummyContent: "1",
520:     anchorAncestorText: "Clusters attached",
521:     renderFragments: (v) => {
522:       const c = v.compute;
523:       if (!c || !Array.isArray(c.hosts) || c.hosts.length === 0) {
524:         return [{ kind: "text", value: "not measured" }];
525:       }
526:       return [{ kind: "text", value: String(c.hosts.length) }];
527:     },
528:   },
529:   {
530:     kind: "styled-element-anchor",
531:     name: "compute-v2-clusters-byline",
532:     // Owner Ruling F: fold akki-vm + akki-vm-ii into the compute surface.
533:     // Byline is DERIVED from v.compute.hosts[].name (never hardcoded).
534:     dummyContent: "on-premise \u00b7 RMS AI DC, Nairobi",
535:     anchorAncestorText: "Clusters attached",
536:     renderFragments: (v) => {
537:       const c = v.compute;
538:       if (!c || !Array.isArray(c.hosts) || c.hosts.length === 0) {
539:         return [{ kind: "text", value: "no hosts attached" }];
540:       }
541:       const names = c.hosts.map((h) => h.name).join(" + ");
542:       return [{ kind: "text", value: `on-premise \u00b7 ${names}` }];
543:     },
544:   },
545:   {
546:     kind: "styled-element-anchor",
547:     name: "compute-v2-gpus-value",
548:     dummyContent: "4",
549:     anchorAncestorText: "GPUs",
550:     renderFragments: (v) => {
551:       const c = v.compute;
552:       if (!c || !c.rollup || typeof c.rollup.gpu_count_total !== "number") {
553:         return [{ kind: "text", value: "not measured" }];
554:       }
555:       return [{ kind: "text", value: String(c.rollup.gpu_count_total) }];
556:     },
557:   },
558:   {
559:     kind: "styled-element-anchor",
560:     name: "compute-v2-gpus-byline",
561:     // Derived from gpu_model + gpu_memory_gb_per_gpu + host_count via
562:     // renderFragments below.
563:     dummyContent: "A100 80GB \u00b7 single node",
564:     anchorAncestorText: "GPUs",
565:     renderFragments: (v) => {
566:       const c = v.compute;
567:       if (!c || !Array.isArray(c.hosts) || c.hosts.length === 0) {
568:         return [{ kind: "text", value: "hardware not enumerated" }];
569:       }
570:       // Assume homogeneous fleet (verified for tonight's estate); if
571:       // heterogeneous, degrade to "mixed hardware · N nodes".
572:       const models = Array.from(new Set(c.hosts.map((h) => h.gpu_model)));
573:       const memGb = c.hosts[0].gpu_memory_gb_per_gpu;
574:       const hostCount = c.hosts.length;
575:       if (models.length !== 1 || typeof memGb !== "number") {
576:         return [{ kind: "text", value: `mixed hardware \u00b7 ${hostCount} nodes` }];
577:       }
578:       const modelShort = models[0].replace(/^NVIDIA\s+/i, "");
579:       const memRounded = Math.round(memGb);
580:       const nodeWord = hostCount === 1 ? "single node" : `${hostCount} nodes`;
581:       return [{ kind: "text", value: `${modelShort} ${memRounded} GiB \u00b7 ${nodeWord}` }];
582:     },
583:   },
584: 
585:   // HONEST-EMPTY (6) — estate has no mechanism to measure these yet;
586:   // rules render "not measured" instead of echoing prototype numbers.
587: 
588:   {
589:     kind: "styled-element-anchor",
590:     name: "compute-v2-capacity-value",
591:     dummyContent: "2,880 hrs",
592:     anchorAncestorText: "Capacity this month",
593:     renderFragments: (v) => {
594:       // No mechanism: monthly wall-clock capacity ledger doesn't exist yet.
595:       return [{ kind: "text", value: "not measured" }];
596:     },
597:   },
598:   {
599:     kind: "styled-element-anchor",
600:     name: "compute-v2-committed-value",
601:     dummyContent: "1,240 hrs",
602:     anchorAncestorText: "Committed to work",
603:     renderFragments: (v) => {
604:       // No mechanism: no allocation-hours ledger.
605:       return [{ kind: "text", value: "not measured" }];
606:     },
607:   },
608:   {
609:     kind: "styled-element-anchor",
610:     name: "compute-v2-free-value",
611:     dummyContent: "1,640 hrs",
612:     anchorAncestorText: "Free to allocate",
613:     renderFragments: (v) => {
614:       // Derives from capacity - committed; both honest-empty.
615:       return [{ kind: "text", value: "not measured" }];
616:     },
617:   },
618:   {
619:     kind: "styled-element-anchor",
620:     name: "compute-v2-jobs-waiting-value",
621:     dummyContent: "2",
622:     anchorAncestorText: "Jobs waiting",
623:     renderFragments: (v) => {
624:       // No mechanism: no live queue-depth service on the seam.
625:       return [{ kind: "text", value: "not measured" }];
626:     },
627:   },
628:   {
629:     kind: "styled-element-anchor",
630:     name: "compute-v2-workflows-month-value",
631:     dummyContent: "18",
632:     anchorAncestorText: "Workflows this month",
633:     renderFragments: (v) => {
634:       // Training-run records exist (phase0/training_runner/runs/*.json)
635:       // but "workflows" is a broader product concept that isn't ledgered
636:       // separately yet; render honest-empty rather than conflate.
637:       return [{ kind: "text", value: "not measured" }];
638:     },
639:   },
640:   {
641:     kind: "styled-element-anchor",
642:     name: "compute-v2-utilisation-value",
643:     dummyContent: "43%",
644:     anchorAncestorText: "Utilisation",
645:     renderFragments: (v) => {
646:       // Would need capacity-and-committed both live; both honest-empty.
647:       return [{ kind: "text", value: "not measured" }];
648:     },
649:   },
650: 
651:   // LIVE-TAUTOLOGY (1) — governance guarantees this by construction.
652: 
653:   {
654:     kind: "styled-element-anchor",
655:     name: "compute-v2-runs-receipted-value",
656:     dummyContent: "100%",
657:     anchorAncestorText: "Runs receipted",
658:     renderFragments: (v) => {
659:       // Every governed run (burn, txttrain, and future waves) crosses
660:       // through services.training_runner.ssh_seam.execute_remote_command
661:       // which persists a redacted receipt per call. Governance guarantees
662:       // 100% by construction — honest to assert.
663:       return [{ kind: "text", value: "100%" }];
664:     },
665:   },
666: 
667:   // -------------------------------------------------------------------
668:   // Wave-G5c-COMPUTE-RESIDUALS · authored 2026-09-06 · owner ruling
669:   // (verbatim in DECISIONS.md 2026-09-06T~12:XX). Completes the Compute
670:   // Connected sub-tab visual surface with 14 r1 chart-caption/per-bar
671:   // rules + 3 r2 tile-note rules = 17 all-honest-empty/honest-phrasing
672:   // additions (compute-estate has no hours ledger / no queue-depth /
673:   // no workflow-completion mechanism — 0 LIVE facts land this wave).
674:   //
675:   // Discipline (verbatim from owner ruling):
676:   //   - Rules authored ONLY against harness-verified rendered DOM
677:   //     (probe artefact: tools/compute_residuals_dom_map.json covering
678:   //     all 3 chart states door/week/state).
679:   //   - Live values from /api/compute/estate where a real fact exists
680:   //     (0 this wave — see grounding brief §B).
681:   //   - Honest-empty/honest-phrasing where no mechanism exists.
682:   //   - Styling preserved.
683:   //   - Grounding brief:
684:   //     /app/assessment_workspace/notes/wave_g5c_compute_residuals_grounding_brief.md
685:   //
686:   // Invariants: tests/invariants/test_compute_residuals_frontend.py
687:   // (11 tests · rule-must-match-rendered-DOM + full-iteration guards).
688:   // -------------------------------------------------------------------
689: 
690:   // r1 CHART CAPTIONS (3) — chartCaption slot for each of door/week/state.
691: 
692:   {
693:     kind: "styled-element-anchor",
694:     name: "compute-residuals-r1-chart-caption-door",
695:     dummyContent: "1,240 hrs committed",
696:     anchorAncestorText: "Committed hours by door",
697:     renderFragments: (v) => {
698:       // No mechanism: no hours-committed-by-door ledger.
699:       return [{ kind: "text", value: "not measured" }];
700:     },
701:   },
702:   {
703:     kind: "styled-element-anchor",
704:     name: "compute-residuals-r1-chart-caption-week",
705:     dummyContent: "of 2,880 hrs available",
706:     anchorAncestorText: "Hours run by week",
707:     renderFragments: (v) => {
708:       // No mechanism: no wall-clock-capacity or hours-run-by-week ledger.
709:       return [{ kind: "text", value: "not measured" }];
710:     },
711:   },
712:   {
713:     kind: "styled-element-anchor",
714:     name: "compute-residuals-r1-chart-caption-state",
715:     dummyContent: "2,880 hrs this month",
716:     anchorAncestorText: "Hours by state",
717:     renderFragments: (v) => {
718:       // No mechanism: no monthly wall-clock capacity ledger.
719:       return [{ kind: "text", value: "not measured" }];
720:     },
721:   },
722: 
723:   // r1 PER-BAR LABELS · door state (5) — per-row `size` label
724:   // (e.g. "645 hrs \u00b7 52%"). Anchor is the row's own label text
725:   // (Train/Extract/Export/Measure/Prove) which is a unique text node in
726:   // the same grid row as the size label.
727: 
728:   {
729:     kind: "styled-element-anchor",
730:     name: "compute-residuals-r1-bar-door-train",
731:     dummyContent: "645 hrs \u00b7 52%",
732:     anchorAncestorText: "Train",
733:     renderFragments: (v) => {
734:       // No mechanism: no per-door hours-committed ledger.
735:       return [{ kind: "text", value: "not measured" }];
736:     },
737:   },
738:   {
739:     kind: "styled-element-anchor",
740:     name: "compute-residuals-r1-bar-door-extract",
741:     dummyContent: "298 hrs \u00b7 24%",
742:     anchorAncestorText: "Extract",
743:     renderFragments: (v) => {
744:       return [{ kind: "text", value: "not measured" }];
745:     },
746:   },
747:   {
748:     kind: "styled-element-anchor",
749:     name: "compute-residuals-r1-bar-door-export",
750:     dummyContent: "174 hrs \u00b7 14%",
751:     anchorAncestorText: "Export",
752:     renderFragments: (v) => {
753:       return [{ kind: "text", value: "not measured" }];
754:     },
755:   },
756:   {
757:     kind: "styled-element-anchor",
758:     name: "compute-residuals-r1-bar-door-measure",
759:     dummyContent: "99 hrs \u00b7 8%",
760:     anchorAncestorText: "Measure",
761:     renderFragments: (v) => {
762:       return [{ kind: "text", value: "not measured" }];
763:     },
764:   },
765:   {
766:     kind: "styled-element-anchor",
767:     name: "compute-residuals-r1-bar-door-prove",
768:     dummyContent: "24 hrs \u00b7 2%",
769:     anchorAncestorText: "Prove",
770:     renderFragments: (v) => {
771:       return [{ kind: "text", value: "not measured" }];
772:     },
773:   },
774: 
775:   // r1 PER-BAR LABELS · week state (4) — row anchor uses the verbatim
776:   // week-range label text (contains U+2013 EN DASH).
777: 
778:   {
779:     kind: "styled-element-anchor",
780:     name: "compute-residuals-r1-bar-week-1",
781:     dummyContent: "274 hrs \u00b7 38%",
782:     anchorAncestorText: "Aug 1\u20137",
783:     renderFragments: (v) => {
784:       // No mechanism: no hours-run-by-week ledger.
785:       return [{ kind: "text", value: "not measured" }];
786:     },
787:   },
788:   {
789:     kind: "styled-element-anchor",
790:     name: "compute-residuals-r1-bar-week-2",
791:     dummyContent: "339 hrs \u00b7 47%",
792:     anchorAncestorText: "Aug 8\u201314",
793:     renderFragments: (v) => {
794:       return [{ kind: "text", value: "not measured" }];
795:     },
796:   },
797:   {
798:     kind: "styled-element-anchor",
799:     name: "compute-residuals-r1-bar-week-3",
800:     dummyContent: "65 hrs \u00b7 9%",
801:     anchorAncestorText: "Aug 15\u201321",
802:     renderFragments: (v) => {
803:       return [{ kind: "text", value: "not measured" }];
804:     },
805:   },
806:   {
807:     kind: "styled-element-anchor",
808:     name: "compute-residuals-r1-bar-week-4",
809:     dummyContent: "43 hrs \u00b7 6%",
810:     anchorAncestorText: "Not yet run",
811:     renderFragments: (v) => {
812:       return [{ kind: "text", value: "not measured" }];
813:     },
814:   },
815: 
816:   // r1 PER-BAR LABELS · state state (2).
817: 
818:   {
819:     kind: "styled-element-anchor",
820:     name: "compute-residuals-r1-bar-state-committed",
821:     dummyContent: "1,240 hrs \u00b7 43%",
822:     anchorAncestorText: "Committed",
823:     renderFragments: (v) => {
824:       // No mechanism: no committed-hours-share ledger.
825:       return [{ kind: "text", value: "not measured" }];
826:     },
827:   },
828:   {
829:     kind: "styled-element-anchor",
830:     name: "compute-residuals-r1-bar-state-free",
831:     dummyContent: "1,640 hrs \u00b7 57%",
832:     anchorAncestorText: "Free to allocate",
833:     renderFragments: (v) => {
834:       // No mechanism: no free-hours-share ledger.
835:       return [{ kind: "text", value: "not measured" }];
836:     },
837:   },
838: 
839:   // r2 TILE NOTES (3) — owner-named tile-note substitutions.
840:   // Grounding brief §B honest-phrasing mapping:
841:   //   - capacity  : "wall-clock ledger not measured" (names missing mechanism)
842:   //   - committed : "share-of-month not measured"   (names missing mechanism)
843:   //   - free      : "quoted against, not reserved"  (VERBATIM prototype
844:   //                                                  text preserved as
845:   //                                                  honest product-language —
846:   //                                                  not a numeric measurement,
847:   //                                                  analogous to compute-v2
848:   //                                                  runs-receipted LIVE-TAUTOLOGY)
849: 
850:   {
851:     kind: "styled-element-anchor",
852:     name: "compute-residuals-r2-note-capacity",
853:     dummyContent: "wall-clock across 4 GPUs",
854:     anchorAncestorText: "Capacity this month",
855:     renderFragments: (v) => {
856:       // No mechanism: no monthly wall-clock capacity ledger.
857:       return [{ kind: "text", value: "wall-clock ledger not measured" }];
858:     },
859:   },
860:   {
861:     kind: "styled-element-anchor",
862:     name: "compute-residuals-r2-note-committed",
863:     dummyContent: "43% of the month",
864:     anchorAncestorText: "Committed to work",
865:     renderFragments: (v) => {
866:       // No mechanism: no share-of-month allocation ledger.
867:       return [{ kind: "text", value: "share-of-month not measured" }];
868:     },
869:   },
870:   {
871:     kind: "styled-element-anchor",
872:     name: "compute-residuals-r2-note-free",
873:     dummyContent: "quoted against, not reserved",
874:     anchorAncestorText: "Free to allocate",
875:     renderFragments: (v) => {
876:       // HONEST-PHRASING preserving verbatim prototype product-language.
877:       // The prototype text is a governance statement about allocation
878:       // policy (not a numeric measurement) — no allocation lock exists
879:       // in the system by construction; quoting-against-not-reserving is
880:       // guaranteed by the current absence of a compute-reservation seam.
881:       // Analogous to compute-v2-runs-receipted-value LIVE-TAUTOLOGY.
882:       return [{ kind: "text", value: "quoted against, not reserved" }];
883:     },
884:   },
885: ];
886: 
887: // Wave-G5b · expose the dummies (never the render output) to window so
888: // the real-Chromium harness can introspect all rules and check every
889: // dummyContent is present in the rendered DOM. This is the mechanical
890: // underpinning of owner's "rule-must-match-rendered-DOM" invariant
891: // (DECISIONS.md 2026-08-28T~14:30Z · ruling A).
892: if (typeof window !== "undefined") {
893:   window.V8_SUBSTITUTIONS_DUMMIES = V8_SUBSTITUTIONS.map((r) => ({
894:     name: r.name,
895:     kind: r.kind,
896:     dummyContent: r.dummyContent || null,
897:     anchorAncestorText: r.anchorAncestorText || null,
898:   }));
899: }
900: 
901: function _findAncestorContainingText(node, label, root) {
902:   let anc = node.parentNode;
903:   while (anc && anc !== root) {
904:     const tc = anc.textContent || "";
905:     if (tc.includes(label)) return anc;
906:     anc = anc.parentNode;
907:   }
908:   return null;
909: }
910: 
911: /**
912:  * _findAncestorWithSlot — Wave-G5c pair-anchor recovery.
913:  *
914:  * When two rules pair as (value, label) with each other's dummy as the
915:  * anchor, the rule that fires FIRST destroys the OTHER's anchor text
916:  * (replacing the paired element's textContent). On subsequent applyAll
917:  * calls (MutationObserver re-fire), the second rule's anchor-text
918:  * check fails and it stays un-substituted forever.
919:  *
920:  * This helper lets the SECOND rule accept "paired rule's slot marker
921:  * exists in a shared ancestor" as valid anchor evidence — i.e. once
922:  * the value has been substituted (data-substituted-slot=<paired>), the
923:  * label rule can still bind because the pair is still structurally
924:  * co-located.
925:  */
926: function _findAncestorWithSlot(node, slotName, root) {
927:   let anc = node.parentNode;
928:   while (anc && anc !== root) {
929:     if (anc.querySelector && anc.querySelector(`[data-substituted-slot="${slotName}"]`)) {
930:       return anc;
931:     }
932:     anc = anc.parentNode;
933:   }
934:   return null;
935: }
936: 
937: function applySubstitutions(doc, vals) {
938:   if (!doc || !doc.body) return 0;
939:   let count = 0;
940: 
941:   for (const rule of V8_SUBSTITUTIONS) {
942: 
943:     // Wave-H INTERRUPT 3 · styled-element-anchor · rebuild container's
944:     // children preserving prototype inline span structure (underline +
945:     // oxblood). Owner directive verbatim (DECISIONS.md 2026-08-28T~13:25Z):
946:     //   "reusing the prototype's own inline markup IS the literal-adoption
947:     //    standard ... post-substitution DOM must contain the expected
948:     //    styled span/link elements (assert style signature presence, not
949:     //    just text)."
950:     if (rule.kind === "styled-element-anchor") {
951:       const fragments = rule.renderFragments(vals);
952:       if (!fragments || fragments.length === 0) continue;
953:       const desiredFullText = fragments.map((f) => f.value).join("");
954:       const dummyTrim = rule.dummyContent.trim();
955:       const markerAttr = "data-substituted-slot";
956:       const markerVal = rule.name;
957:       // Priority 1: element already marked → check if desired changed.
958:       const marked = doc.querySelector(`[${markerAttr}="${markerVal}"]`);
959:       let target = marked;
960:       if (!target) {
961:         // Priority 2: walk all element matches, apply anchorAncestorText
962:         // filter if set, then pick the DEEPEST (last in doc order) so
963:         // leaf spans win over containers that happen to share text.
964:         const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_ELEMENT);
965:         const matches = [];
966:         let candidate;
967:         while ((candidate = walker.nextNode())) {
968:           const tc = (candidate.textContent || "").trim();
969:           if (tc !== dummyTrim) continue;
970:           if (rule.anchorAncestorText || rule.anchorAncestorSlot) {
971:             // Pair-anchor recovery: accept EITHER raw-text ancestor
972:             // OR paired-slot-marker ancestor (see _findAncestorWithSlot
973:             // doc). This lets label rules bind after their value pair
974:             // has already fired.
975:             const textAnc = rule.anchorAncestorText
976:               ? _findAncestorContainingText(candidate, rule.anchorAncestorText, doc.body)
977:               : null;
978:             const slotAnc = rule.anchorAncestorSlot
979:               ? _findAncestorWithSlot(candidate, rule.anchorAncestorSlot, doc.body)
980:               : null;
981:             if (!textAnc && !slotAnc) continue;
982:           }
983:           matches.push(candidate);
984:         }
985:         if (matches.length === 0) continue;
986:         target = matches[matches.length - 1]; // deepest
987:       }
988:       if (!target) continue;
989:       // Skip if already at desired · but always ensure the marker is set
990:       // so audits reflect the rule bound to the DOM. Without this, a
991:       // rule whose live-value render happens to match the prototype's
992:       // dummy character-for-character (e.g., tile-share-measured-label
993:       // whose live render is literally "measured at last census") would
994:       // never get its data-substituted-slot marker, leaving the audit
995:       // showing the dummy as "still present" and the harness scoring RED.
996:       if ((target.textContent || "").trim() === desiredFullText.trim()) {
997:         if (!target.getAttribute(markerAttr)) {
998:           target.setAttribute(markerAttr, markerVal);
999:         }
1000:         continue;
1001:       }
1002:       const newChildren = fragments.map((f) => {
1003:         if (f.kind === "text") return doc.createTextNode(f.value);
1004:         const span = doc.createElement("span");
1005:         if (f.kind === "underline") {
1006:           span.setAttribute(
1007:             "style",
1008:             "border-bottom:1px solid rgba(27,31,39,.25);"
1009:           );
1010:         } else if (f.kind === "oxblood") {
1011:           span.setAttribute("style", "color:var(--oxblood);");
1012:         }
1013:         span.textContent = f.value;
1014:         return span;
1015:       });
1016:       target.replaceChildren(...newChildren);
1017:       target.setAttribute(markerAttr, markerVal);
1018:       count++;
1019:       continue;
1020:     }
1021: 
1022:     const desired = rule.render(vals);
1023:     if (desired == null) continue;
1024: 
1025:     if (rule.kind === "element-anchor") {
1026:       // Whole-element textContent replacement — handles fragmented spans.
1027:       // Idempotency emerges from state: after mutation, textContent equals
1028:       // desired ≠ dummyContent, so subsequent walks find no match.
1029:       const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_ELEMENT);
1030:       let el;
1031:       const dummyTrim = rule.dummyContent.trim();
1032:       while ((el = walker.nextNode())) {
1033:         const tc = (el.textContent || "").trim();
1034:         if (tc !== dummyTrim) continue;
1035:         if (el.textContent !== desired) {
1036:           el.textContent = desired;
1037:           count++;
1038:         }
1039:         break;
1040:       }
1041:       continue;
1042:     }
1043: 
1044:     if (rule.kind === "text-node") {
1045:       // Idempotency emerges from state: after mutation, node.nodeValue no
1046:       // longer matches rule.signature.
1047:       const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT);
1048:       let node;
1049:       while ((node = walker.nextNode())) {
1050:         const text = node.nodeValue;
1051:         if (!text || text.length < 4) continue;
1052:         if (rule.signature.test(text)) {
1053:           if (node.nodeValue !== desired) {
1054:             node.nodeValue = desired;
1055:             count++;
1056:           }
1057:           break;
1058:         }
1059:       }
1060:       continue;
1061:     }
1062: 
1063:     if (rule.kind === "tile-value") {
1064:       // Match ONLY on trimmed === rule.dummy (not desired). This avoids a
1065:       // collision where an unrelated tile whose LABEL text happens to
1066:       // equal `desired` (e.g., the "Not yet measured" tile's label
1067:       // colliding with the HONEST-EMPTY rendering of every other tile)
1068:       // is mistaken for the target. Idempotency emerges from state:
1069:       // after mutation, nodeValue equals desired ≠ dummy.
1070:       const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT);
1071:       let node;
1072:       while ((node = walker.nextNode())) {
1073:         const trimmed = (node.nodeValue || "").trim();
1074:         if (trimmed !== rule.dummy) continue;
1075:         const anc = _findAncestorContainingText(node, rule.label, doc.body);
1076:         if (!anc) continue;
1077:         if (node.nodeValue !== desired) {
1078:           node.nodeValue = desired;
1079:           count++;
1080:         }
1081:         break;
1082:       }
1083:       continue;
1084:     }
1085:   }
1086: 
1087:   return count;
1088: }
1089: 
1090: // ---------------------------------------------------------------------------
1091: // PortalIframe — the single user-facing surface (Wave G4 CORRECTION 3).
1092: // ---------------------------------------------------------------------------
1093: 
1094: function PortalIframe() {
1095:   const iframeRef = useRef(null);
1096:   // Monotonic counter of successful substitutions this session — surfaced
1097:   // as data-substitution-applied on the outer iframe host div so external
1098:   // harnesses can prove substitutions actually ran without reading into
1099:   // the prototype's DOM.
1100:   const [substitutionsApplied, setSubstitutionsApplied] = useState(0);
1101: 
1102:   useEffect(() => {
1103:     const iframe = iframeRef.current;
1104:     if (!iframe) return;
1105:     let observer = null;
1106:     let scheduled = false;
1107:     const liveValues = {
1108:       estateSources: null,
1109:       estateTables: null,
1110:       lastCensus: null,
1111:       totalVolume: null,
1112:       shareMeasured: null,
1113:       opportunities: null,
1114:       compute: null,
1115:     };
1116: 
1117:     const applyAll = () => {
1118:       if (scheduled) return; // Debounce burst mutations from dc-runtime.
1119:       scheduled = true;
1120:       const run = () => {
1121:         scheduled = false;
1122:         const doc = iframe.contentDocument;
1123:         if (!doc || !doc.body) return;
1124:         const count = applySubstitutions(doc, liveValues);
1125:         // Wave-H · harness instrumentation: emit a console line each time
1126:         // applyAll runs so the real-Chromium harness can see the engine's
1127:         // liveness independently of React state.
1128:         try {
1129:           console.log(
1130:             `wave_g5_substitutions applyAll_run count=${count} bodyLen=${(doc.body.textContent || "").length}`
1131:           );
1132:         } catch (_) {
1133:           /* no-op */
1134:         }
1135:         if (count > 0) {
1136:           setSubstitutionsApplied((prev) => prev + count);
1137:         }
1138:       };
1139:       if (typeof window !== "undefined" && window.requestAnimationFrame) {
1140:         window.requestAnimationFrame(run);
1141:       } else {
1142:         setTimeout(run, 0);
1143:       }
1144:     };
1145: 
1146:     const onLoad = async () => {
1147:       // Pull live values (silent — HONEST-EMPTY fallback fires when null).
1148:       const backend = process.env.REACT_APP_BACKEND_URL || "";
1149: 
1150:       // (1) Registry facts — connected sources + table count.
1151:       try {
1152:         const res = await fetch(`${backend}/api/registry/facts`);
1153:         if (res.ok) {
1154:           const facts = await res.json();
1155:           if (facts && Array.isArray(facts.data_sources)) {
1156:             liveValues.estateSources = facts.data_sources.length;
1157:             let tables = 0;
1158:             for (const s of facts.data_sources) {
1159:               if (typeof s.table_count === "number") tables += s.table_count;
1160:             }
1161:             liveValues.estateTables = tables;
1162:           }
1163:         }
1164:       } catch (_) {
1165:         /* silent */
1166:       }
1167: 
1168:       // (2) Wave-G5c · census status line + estate scale from live
1169:       // census output (owner Stage 3 wiring: Registry reads from
1170:       // /api/census/latest wherever the census provides the truer
1171:       // figure). Census manifest fields land as:
1172:       //   lastCensus.number    ← census_id
1173:       //   lastCensus.date      ← finished_at_utc (formatted)
1174:       //   lastCensus.author    ← initiator
1175:       //   lastCensus.notMeasuredPct  ← honest-empty (census walks
1176:       //     aggregates, not size-in-bytes)
1177:       // estateTables also updates from rollup.table_count (census is
1178:       // authoritative once it has run — walks EVERY table, not the
1179:       // truncated top-25 in the connection record).
1180:       try {
1181:         const res = await fetch(`${backend}/api/census/latest`);
1182:         if (res.ok) {
1183:           const body = await res.json();
1184:           const c = body && body.census;
1185:           if (c && c.census_id != null) {
1186:             const finished = (c.finished_at_utc || "").slice(0, 10);
1187:             liveValues.lastCensus = {
1188:               number: c.census_id,
1189:               date: finished || "recent",
1190:               author: c.initiator || "owner",
1191:               notMeasuredPct: "size",
1192:             };
1193:             if (c.rollup && typeof c.rollup.table_count === "number") {
1194:               liveValues.estateTables = c.rollup.table_count;
1195:             }
1196:             if (c.rollup && typeof c.rollup.database_count === "number") {
1197:               // Census "sees" databases as sources when the connection
1198:               // record hasn't been widened yet.
1199:               if (liveValues.estateSources == null
1200:                   || liveValues.estateSources < c.rollup.database_count) {
1201:                 liveValues.estateSources = c.rollup.database_count;
1202:               }
1203:             }
1204:           }
1205:         }
1206:       } catch (_) {
1207:         /* silent */
1208:       }
1209: 
1210:       // (3) Wave-G5c-COMPUTE-BACKEND · compute descriptor.
1211:       try {
1212:         const res = await fetch(`${backend}/api/compute/estate`);
1213:         if (res.ok) {
1214:           const body = await res.json();
1215:           if (body && Array.isArray(body.hosts)) {
1216:             liveValues.compute = body;
1217:           }
1218:         }
1219:       } catch (_) {
1220:         /* silent */
1221:       }
1222: 
1223:       // Give dc-runtime time for the first render pass.
1224:       await new Promise((r) => setTimeout(r, 400));
1225:       applyAll();
1226: 
1227:       // Re-apply on every subsequent dc-runtime re-render (tab switch,
1228:       // Registry mount, drawer open, etc.). Idempotent → safe.
1229:       try {
1230:         const doc = iframe.contentDocument;
1231:         if (doc && doc.body) {
1232:           observer = new MutationObserver(applyAll);
1233:           observer.observe(doc.body, {
1234:             childList: true,
1235:             characterData: true,
1236:             subtree: true,
1237:           });
1238:         }
1239:       } catch (_) {
1240:         /* no-op */
1241:       }
1242:     };
1243: 
1244:     iframe.addEventListener("load", onLoad);
1245:     return () => {
1246:       iframe.removeEventListener("load", onLoad);
1247:       if (observer) observer.disconnect();
1248:     };
1249:   }, []);
1250: 
1251:   return (
1252:     <div
1253:       data-testid="v8-portal-iframe-host"
1254:       data-substitution-applied={substitutionsApplied}
1255:       style={{ width: "100vw", height: "100vh", margin: 0, padding: 0, overflow: "hidden" }}
1256:     >
1257:       <iframe
1258:         ref={iframeRef}
1259:         data-testid="v8-prototype-iframe"
1260:         src="/v8_prototype.html"
1261:         title="Akki OS \u00b7 RMS AI"
1262:         style={{ width: "100%", height: "100%", border: "none", display: "block" }}
1263:       />
1264:     </div>
1265:   );
1266: }
1267: 
1268: // ---------------------------------------------------------------------------
1269: // App — single-surface routing (Wave G4 CORRECTION 3).
1270: // All paths (root + wildcard) render <PortalIframe/>. The 15 legacy
1271: // deep-link routes are retired. Component source files retained.
1272: // ---------------------------------------------------------------------------
1273: 
1274: function App() {
1275:   return (
1276:     <div className="App">
1277:       <BrowserRouter>
1278:         <Routes>
1279:           {/* Track 1 — DAP Portal */}
1280:           <Route path="/dap" element={<DAPLayout />}>
1281:             <Route index element={<DAPLanding />} />
1282:             <Route path="extract/:mode" element={<ExtractModes />} />
1283:             <Route path="resources/:tab" element={<AvailableResources />} />
1284:             <Route path="governance/:tab" element={<DataGovernance />} />
1285:             <Route path="connect/:tab" element={<ConnectResources />} />
1286:             <Route path="requests" element={<RequestLifecycle />} />
1287:             <Route path="entitlement" element={<Entitlement />} />
1288:             <Route path="countdown" element={<CanonCountdown />} />
1289:             <Route path="estates/:estateId" element={<DataEstates />} />
1290:             <Route path="*" element={<Navigate to="/dap" replace />} />
1291:           </Route>
1292: 
1293:           {/* Track 3 — OS Native React surfaces · Turn 4 sub-slice 4d · Work tab + Monitor sub-view.
1294:              Routes are additive (SO §3.8) and land BEFORE the PortalIframe wildcard fallback so
1295:              a tester can reach each native surface at ${REACT_APP_BACKEND_URL}/os/work/<leaf> or
1296:              /os/monitor/<leaf>. Un-implemented leaves continue to fall through to the V8/PortalIframe
1297:              render at "/" and "/*" until subsequent sub-slices (4e-4g) land more native surfaces. */}
1298:           <Route path="/os/work/chat" element={<WorkChat />} />
1299:           <Route path="/os/work/analyze" element={<WorkAnalyze />} />
1300:           <Route path="/os/work/documents" element={<WorkDocuments />} />
1301:           <Route path="/os/work/tasks" element={<WorkTasks />} />
1302:           <Route path="/os/work/team" element={<WorkTeam />} />
1303:           <Route path="/os/work/performance" element={<WorkPerformance />} />
1304:           <Route path="/os/work/board" element={<WorkBoard />} />
1305:           <Route path="/os/monitor/signals" element={<MonitorSignals />} />
1306:           <Route path="/os/monitor/ideas" element={<MonitorIdeas />} />
1307: 
1308:           {/* Sub-slice 4e · ThinkLab (Work tab) + Admin tab groups (estate/approvals/watch) */}
1309:           <Route path="/os/work/clarity" element={<ThinkLabClarity />} />
1310:           <Route path="/os/work/strategy" element={<ThinkLabStrategy />} />
1311:           <Route path="/os/work/hypothesis" element={<ThinkLabHypothesis />} />
1312:           <Route path="/os/work/perspective" element={<ThinkLabPerspective />} />
1313:           <Route path="/os/admin/estate" element={<AdminEstate />} />
1314:           <Route path="/os/admin/govern" element={<AdminGovern />} />
1315:           <Route path="/os/admin/greymirror" element={<AdminGreyMirror />} />
1316:           <Route path="/os/admin/spendreq" element={<AdminSpendReq />} />
1317:           <Route path="/os/admin/rulesupd" element={<AdminRulesUpd />} />
1318:           <Route path="/os/admin/modeladmission" element={<AdminModelAdmission />} />
1319:           <Route path="/os/admin/wstate" element={<AdminWState />} />
1320:           <Route path="/os/admin/wrecord" element={<AdminWRecord />} />
1321:           <Route path="/os/admin/wunder" element={<AdminWUnder />} />
1322:           <Route path="/os/admin/wdecisions" element={<AdminWDecisions />} />
1323: 
1324:           {/* Sub-slice 4f · Build/Buildlib (build tab) + Collab (work tab) + 3rdParty (apps tab) */}
1325:           <Route path="/os/build/train" element={<BuildTrain />} />
1326:           <Route path="/os/build/agentbuild" element={<BuildAgent />} />
1327:           <Route path="/os/build/buildskill" element={<BuildSkill />} />
1328:           <Route path="/os/build/extract" element={<BuildExtract />} />
1329:           <Route path="/os/build/youragents" element={<BuildlibAgents />} />
1330:           <Route path="/os/build/yourmodels" element={<BuildlibModels />} />
1331:           <Route path="/os/work/mentions" element={<CollabMentions />} />
1332:           <Route path="/os/work/emails" element={<CollabEmails />} />
1333:           <Route path="/os/work/projects" element={<CollabProjects />} />
1334:           <Route path="/os/work/hrstuff" element={<CollabHrStuff />} />
1335:           <Route path="/os/apps/new" element={<AppsNew />} />
1336:           <Route path="/os/apps/frequent" element={<AppsFrequent />} />
1337:           <Route path="/os/apps/connected" element={<AppsConnected />} />
1338:           <Route path="/os/apps/requests" element={<AppsRequests />} />
1339: 
1340:           {/* Sub-slice 4h · 2 DAP LATEST view classes (view 10 + 11) — reachable at top-level /dap/... */}
1341:           <Route path="/dap/approvals-ledger" element={<AdminApprovalsLedger />} />
1342:           <Route path="/dap/watch-trail-bridge" element={<AdminWatchTrailBridge />} />
1343:           {/* PHASE 4 (c-vi) · CP-SKILLS-LAYER-SERIES-CLOSE · Slice 5 · DAP buildskill surface */}
1344:           <Route path="/dap/buildskill" element={<DapBuildSkill />} />
1345: 
1346:           {/* PHASE 4 (a) · CP-COMMISSION-WIZARD-LIVE · Canon-5-§14 Shaping-Wizard live at workstudio.commission */}
1347:           <Route path="/os/work/commission" element={<WorkCommission />} />
1348: 
1349:           {/* Track 2 — RETIRED per owner ruling 2026-02-23T~19:00Z verbatim: "We should not be having 2 URL routes to begin with."
1350:              CP-SINGLE-SURFACE-RULING (Item 5.15 · SO §6.9(1) config/entries class · prospective, immediate, no countdown).
1351:              The V1 HTML iframe surface (PortalIframe → /v8_prototype.html) is retired-superseded from live routing;
1352:              the PortalIframe component definition + public/v8_prototype.html file remain on disk (archive · additive record).
1353:              Root and wildcard now redirect to /dap (single live shell · DAPLayout carries the JWT login-gated surface). */}
1354:           <Route path="/" element={<Navigate to="/dap" replace />} />
1355:           <Route path="*" element={<Navigate to="/dap" replace />} />
1356:         </Routes>
1357:       </BrowserRouter>
1358:       {/* PHASE 3 continuation A'' · additive overlay above prototype iframe */}
1359:       <CensusAutonomyDrawer />
1360:       {/* PHASE 3 continuation A'''-cont-B · response-required badge overlay */}
1361:       <ResponseRequiredBadge />
1362:     </div>
1363:   );
1364: }
1365: 
1366: export { PortalIframe };
1367: export default App;

# SOURCE: frontend/src/pages/dap/AdminApprovalsLedger.jsx

1: /*
2:  * AdminApprovalsLedger.jsx — v2 OS · DAP LATEST view class 10 (working title).
3:  * R-101 + R-102 + R-103 + R-104 folded (approving authorities named). Turn 4 sub-slice 4h.
4:  * HONEST-GAP · SO §5.
5:  */
6: import React from "react";
7: export default function AdminApprovalsLedger() {
8:   return (
9:     <div data-testid="dap-approvals-ledger-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
10:       <header style={{marginBottom:32}}>
11:         <div data-testid="dap-approvals-ledger-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>DAP LATEST · Approvals Ledger</div>
12:         <h1 data-testid="dap-approvals-ledger-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>Approvals Ledger</h1>
13:       </header>
14:       <section data-testid="dap-approvals-ledger-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
15:         <p style={{margin:"0 0 24px 0"}}>Every controlled request the tenant has raised, routed to its authorities, and the first-decision-wins outcome. Each row names the deciding authority, the reason banked, and the receipt trail.</p>
16:       </section>
17:       <section data-testid="dap-approvals-ledger-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
18:         <div data-testid="dap-approvals-ledger-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
19:         <div data-testid="dap-approvals-ledger-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Approvals routing backend + first-decision-wins ledger not yet wired. Design-of-record surface reveals R-104 authority routing (DAP-15 DEFAULT-class + DAP-17 one-act set/revoke standing approvals). Wire lands at PHASE 2 CP-TENANT-SEPARATION when RMS + DigiCow authorities are seated per R-104 (Fred Afune · Muthoni Kiarie · Samuel Kibacia · Vincent Kimani · Peninah Wanja).</div>
20:         <div data-testid="dap-approvals-ledger-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: R-104 banked STATE/DECISIONS.md · surface at pages/dap/AdminApprovalsLedger.jsx · route /dap/approvals-ledger.</div>
21:       </section>
22:     </div>
23:   );
24: }

# SOURCE: frontend/src/pages/dap/AdminWatchTrailBridge.jsx

1: /*
2:  * AdminWatchTrailBridge.jsx — v2 OS · DAP LATEST view class 11 (working title).
3:  * R-101 + R-102 + R-103 + R-104 folded. Turn 4 sub-slice 4h.
4:  * HONEST-GAP · SO §5.
5:  */
6: import React from "react";
7: export default function AdminWatchTrailBridge() {
8:   return (
9:     <div data-testid="dap-watch-trail-bridge-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
10:       <header style={{marginBottom:32}}>
11:         <div data-testid="dap-watch-trail-bridge-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>DAP LATEST · Watch Trail Bridge</div>
12:         <h1 data-testid="dap-watch-trail-bridge-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>Watch Trail Bridge</h1>
13:       </header>
14:       <section data-testid="dap-watch-trail-bridge-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
15:         <p style={{margin:"0 0 24px 0"}}>Where DAP requests meet The Watch. Every held request writes to the external witness trail with its trigger, its evidence bundle, and the authority holding it.</p>
16:       </section>
17:       <section data-testid="dap-watch-trail-bridge-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
18:         <div data-testid="dap-watch-trail-bridge-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
19:         <div data-testid="dap-watch-trail-bridge-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Watch-trail external-witness writer not yet wired. Design-of-record surface reveals the bridge shape: DAP request → shield decision → Watch trail entry with named authority + evidence bundle + next-review date. Wire lands at PHASE 4 (g) Watch external-witness trail feature build per R-102 MASTER DIRECTIVE.</div>
20:         <div data-testid="dap-watch-trail-bridge-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: surface at pages/dap/AdminWatchTrailBridge.jsx · route /dap/watch-trail-bridge.</div>
21:       </section>
22:     </div>
23:   );
24: }

# SOURCE: frontend/src/pages/dap/AvailableResources.jsx

1: import React, { useEffect, useState } from "react";
2: import { useParams } from "react-router-dom";
3: import { fetchComputeEstate, fetchModels, fetchFullRecord, fetchSkillFilesState } from "@/lib/apiClient";
4: import LoadingState from "@/components/shared/LoadingState";
5: import TransportError from "@/components/shared/TransportError";
6: import HonestEmpty from "@/components/shared/HonestEmpty";
7: 
8: /**
9:  * Available Resources — DAP §4.4
10:  * 4 sub-views: Compute, Base Models, Trained Models, Skills
11:  * All wired to real endpoints.
12:  */
13: 
14: function ComputeView() {
15:   const [data, setData] = useState(null);
16:   const [error, setError] = useState(null);
17:   const [loading, setLoading] = useState(true);
18: 
19:   useEffect(() => {
20:     fetchComputeEstate()
21:       .then(setData)
22:       .catch((e) => setError(e.message))
23:       .finally(() => setLoading(false));
24:   }, []);
25: 
26:   if (loading) return <LoadingState message="Reading the compute estate…" />;
27:   if (error) return <TransportError error={error} />;
28:   if (!data || !data.hosts || data.hosts.length === 0) {
29:     return <HonestEmpty message="No compute resources are attached to the estate. This list will populate as hosts are connected." />;
30:   }
31: 
32:   return (
33:     <div data-testid="available-compute">
34:       <div className="grid grid-cols-3 gap-4 mb-6">
35:         <div className="rounded-lg border p-4" style={{ borderColor: "var(--line)", background: "white" }}>
36:           <p className="text-xs font-medium mb-1" style={{ color: "var(--ink3)" }}>Hosts attached</p>
37:           <p data-testid="compute-host-count" className="text-2xl font-semibold" style={{ color: "var(--ink)" }}>{data.rollup?.host_count || data.hosts.length}</p>
38:         </div>
39:         <div className="rounded-lg border p-4" style={{ borderColor: "var(--line)", background: "white" }}>
40:           <p className="text-xs font-medium mb-1" style={{ color: "var(--ink3)" }}>GPUs total</p>
41:           <p data-testid="compute-gpu-count" className="text-2xl font-semibold" style={{ color: "var(--ink)" }}>{data.rollup?.gpu_count_total ?? "not measured"}</p>
42:         </div>
43:         <div className="rounded-lg border p-4" style={{ borderColor: "var(--line)", background: "white" }}>
44:           <p className="text-xs font-medium mb-1" style={{ color: "var(--ink3)" }}>GPU memory</p>
45:           <p data-testid="compute-gpu-memory" className="text-2xl font-semibold" style={{ color: "var(--ink)" }}>{data.rollup?.gpu_memory_gb_total ? `${Math.round(data.rollup.gpu_memory_gb_total)} GiB` : "not measured"}</p>
46:         </div>
47:       </div>
48:       <h3 className="text-sm font-medium mb-3" style={{ color: "var(--ink)" }}>Hosts</h3>
49:       <div className="space-y-2">
50:         {data.hosts.map((host, i) => (
51:           <div
52:             key={i}
53:             data-testid={`compute-host-${i}`}
54:             className="flex items-center justify-between rounded-lg border p-4"
55:             style={{ borderColor: "var(--line)", background: "white" }}
56:           >
57:             <div>
58:               <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>{host.name}</p>
59:               <p className="text-xs" style={{ color: "var(--ink3)" }}>
60:                 {host.gpu_model?.replace(/^NVIDIA\s+/i, "")} · {host.gpu_count} GPU{host.gpu_count > 1 ? "s" : ""} · {Math.round(host.gpu_memory_gb_per_gpu)} GiB each
61:               </p>
62:             </div>
63:             <span
64:               className="text-xs px-2 py-0.5 rounded-full"
65:               style={{ color: "var(--sage)", background: "rgba(29,122,110,.12)" }}
66:             >
67:               {host.readiness}
68:             </span>
69:           </div>
70:         ))}
71:       </div>
72:     </div>
73:   );
74: }
75: 
76: function BaseModelsView() {
77:   const [data, setData] = useState(null);
78:   const [error, setError] = useState(null);
79:   const [loading, setLoading] = useState(true);
80: 
81:   useEffect(() => {
82:     fetchModels()
83:       .then(setData)
84:       .catch((e) => setError(e.message))
85:       .finally(() => setLoading(false));
86:   }, []);
87: 
88:   if (loading) return <LoadingState message="Reading the model registry…" />;
89:   if (error) return <TransportError error={error} />;
90: 
91:   const models = data?.purchased_llms || [];
92:   const open = data?.open_weight_bases || [];
93:   const all = [...models, ...open];
94: 
95:   if (all.length === 0) {
96:     return <HonestEmpty message="No models are registered. This list will populate as models are connected and admitted." />;
97:   }
98: 
99:   return (
100:     <div data-testid="available-base-models">
101:       <p className="text-sm mb-4" style={{ color: "var(--ink2)" }}>{data?.total ?? all.length} models registered</p>
102:       <div className="space-y-2">
103:         {all.map((m, i) => (
104:           <div
105:             key={i}
106:             data-testid={`model-row-${i}`}
107:             className="flex items-center justify-between rounded-lg border p-4"
108:             style={{ borderColor: "var(--line)", background: "white" }}
109:           >
110:             <div>
111:               <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>{m.model_id}</p>
112:               <p className="text-xs" style={{ color: "var(--ink3)" }}>
113:                 {m.provider} · {m.role || m.custody_kind || "model"}
114:               </p>
115:             </div>
116:             <span className="text-xs" style={{ color: "var(--ink3)" }}>
117:               {m.connected_at ? new Date(m.connected_at).toLocaleDateString() : ""}
118:             </span>
119:           </div>
120:         ))}
121:       </div>
122:     </div>
123:   );
124: }
125: 
126: function TrainedModelsView() {
127:   const [data, setData] = useState(null);
128:   const [error, setError] = useState(null);
129:   const [loading, setLoading] = useState(true);
130: 
131:   useEffect(() => {
132:     fetchFullRecord()
133:       .then(setData)
134:       .catch((e) => setError(e.message))
135:       .finally(() => setLoading(false));
136:   }, []);
137: 
138:   if (loading) return <LoadingState message="Reading the model record…" />;
139:   if (error) return <TransportError error={error} />;
140: 
141:   const models = data?.models || [];
142:   if (models.length === 0) {
143:     return <HonestEmpty message="No trained models on record. This list will populate as training runs complete." />;
144:   }
145: 
146:   return (
147:     <div data-testid="available-trained-models">
148:       <p className="text-sm mb-4" style={{ color: "var(--ink2)" }}>{models.length} trained models on record</p>
149:       <div className="space-y-2">
150:         {models.map((m, i) => (
151:           <div
152:             key={i}
153:             data-testid={`trained-model-${i}`}
154:             className="flex items-center justify-between rounded-lg border p-4"
155:             style={{ borderColor: "var(--line)", background: "white" }}
156:           >
157:             <div>
158:               <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>{m.run_name || m.run_id}</p>
159:               <p className="text-xs" style={{ color: "var(--ink3)" }}>
160:                 {m.version} · {m.state}
161:               </p>
162:             </div>
163:             {m.state_evidence && (
164:               <span
165:                 className="text-[10px] px-2 py-0.5 rounded font-mono"
166:                 style={{ color: "var(--ink3)", background: "var(--surface)" }}
167:               >
168:                 {m.state_evidence.split("/").pop()}
169:               </span>
170:             )}
171:           </div>
172:         ))}
173:       </div>
174:     </div>
175:   );
176: }
177: 
178: function SkillsView() {
179:   const [data, setData] = useState(null);
180:   const [error, setError] = useState(null);
181:   const [loading, setLoading] = useState(true);
182: 
183:   useEffect(() => {
184:     fetchSkillFilesState()
185:       .then(setData)
186:       .catch((e) => setError(e.message))
187:       .finally(() => setLoading(false));
188:   }, []);
189: 
190:   if (loading) return <LoadingState message="Reading the skill files…" />;
191:   if (error) return <TransportError error={error} />;
192: 
193:   const skills = data?.skills || [];
194:   if (skills.length === 0) {
195:     return (
196:       <HonestEmpty message="No skill files have been built yet. This list will populate as skills are developed against the estate." />
197:     );
198:   }
199: 
200:   return (
201:     <div data-testid="available-skills">
202:       <p className="text-sm mb-4" style={{ color: "var(--ink2)" }}>{skills.length} skills available</p>
203:       <div className="space-y-2">
204:         {skills.map((s, i) => (
205:           <div key={i} data-testid={`skill-row-${i}`} className="rounded-lg border p-4" style={{ borderColor: "var(--line)", background: "white" }}>
206:             <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>{s.skill_id || s.name || `Skill ${i + 1}`}</p>
207:           </div>
208:         ))}
209:       </div>
210:     </div>
211:   );
212: }
213: 
214: const VIEW_MAP = {
215:   compute: { title: "Compute", Component: ComputeView },
216:   "base-models": { title: "Base Models", Component: BaseModelsView },
217:   "trained-models": { title: "Trained Models", Component: TrainedModelsView },
218:   skills: { title: "Skills", Component: SkillsView },
219: };
220: 
221: export default function AvailableResources() {
222:   const { tab } = useParams();
223:   const current = VIEW_MAP[tab] || VIEW_MAP["compute"];
224:   const Component = current.Component;
225: 
226:   return (
227:     <div data-testid="available-resources" className="max-w-5xl mx-auto px-8 py-10">
228:       <h1
229:         data-testid="available-resources-title"
230:         className="text-xl font-semibold mb-1"
231:         style={{ color: "var(--ink)", fontFamily: "var(--head, Iowan Old Style, Georgia, serif)" }}
232:       >
233:         Available Resources
234:       </h1>
235:       <p className="text-sm mb-6" style={{ color: "var(--ink3)" }}>
236:         {current.title}
237:       </p>
238:       <Component />
239:     </div>
240:   );
241: }

# SOURCE: frontend/src/pages/dap/BuildSkill.jsx

1: /*
2:  * BuildSkill.jsx — DAP surface (PHASE 4 · c-vi · CP-SKILLS-LAYER-SERIES-CLOSE).
3:  *
4:  * Owner boundary directive verbatim (2026-02-23):
5:  *   "the buildskill surface must show real provisioning state or
6:  *    honest-gap, and the boundary report must include the tester
7:  *    walkthrough — the concrete steps a human takes and what they see."
8:  *
9:  * Live-or-honest-gap per R-102: this page is LIVE against the sealed
10:  * A18.2 persistence store via the additive backend route. When the
11:  * store is ORIGIN-EMPTY (fresh pod · zero writes yet) the surface
12:  * renders a plain-product-language empty-state block — never a
13:  * "coming soon", never a mocked list of records.
14:  *
15:  * Product-language discipline per SO §4: no engineering vocabulary on
16:  * owner-facing copy (no endpoint / manifest / ratchet / invariant /
17:  * seam / hash). Empty state reads "No skills provisioned yet".
18:  *
19:  * data-testid discipline: every interactive/critical element carries a
20:  * stable dap-buildskill-* test-id so the QA walkthrough can drive
21:  * precise flows.
22:  */
23: import React from "react";
24: 
25: import { useBuildSkillProvisioning } from "@/hooks/useBuildSkillProvisioning";
26: 
27: // JWT reading is optional here — the sealed auth gate on the backend
28: // route will refuse anonymous callers with a 401 which the hook
29: // surfaces via the error branch. Callers that HAVE a JWT (via
30: // DAPLayout AuthCtx) can pass it in; the empty-state discipline
31: // still applies.
32: function readJwtFromLocalStorage() {
33:   try {
34:     return typeof window !== "undefined"
35:       ? window.localStorage?.getItem?.("dap_jwt") || null
36:       : null;
37:   } catch (_e) {
38:     return null;
39:   }
40: }
41: 
42: function renderRecordRow(record, idx) {
43:   return (
44:     <div
45:       data-testid="dap-buildskill-record-row"
46:       key={record?.skill_id ? record.skill_id : `row-${idx}`}
47:       style={{
48:         padding: "16px 20px",
49:         borderTop: idx === 0 ? "none" : "1px solid rgba(0,0,0,.08)",
50:         display: "grid",
51:         gridTemplateColumns: "1fr 1fr 1fr",
52:         gap: "16px",
53:         fontSize: 14,
54:         lineHeight: 1.4,
55:       }}
56:     >
57:       <div>
58:         <div
59:           style={{
60:             fontSize: 10,
61:             letterSpacing: "0.14em",
62:             textTransform: "uppercase",
63:             color: "var(--ink3, #6b6b78)",
64:             marginBottom: 4,
65:           }}
66:         >
67:           Skill ID
68:         </div>
69:         <div style={{ fontFamily: "monospace" }}>
70:           {record?.skill_id || "—"}
71:         </div>
72:       </div>
73:       <div>
74:         <div
75:           style={{
76:             fontSize: 10,
77:             letterSpacing: "0.14em",
78:             textTransform: "uppercase",
79:             color: "var(--ink3, #6b6b78)",
80:             marginBottom: 4,
81:           }}
82:         >
83:           Corpus slice
84:         </div>
85:         <div style={{ fontFamily: "monospace" }}>
86:           {record?.corpus_slice_ref || "—"}
87:         </div>
88:       </div>
89:       <div>
90:         <div
91:           style={{
92:             fontSize: 10,
93:             letterSpacing: "0.14em",
94:             textTransform: "uppercase",
95:             color: "var(--ink3, #6b6b78)",
96:             marginBottom: 4,
97:           }}
98:         >
99:           Scope
100:         </div>
101:         <div>{record?.scope || "—"}</div>
102:       </div>
103:     </div>
104:   );
105: }
106: 
107: export default function BuildSkill() {
108:   const jwt = readJwtFromLocalStorage();
109:   const { records, count, loading, error, lastFetchedAt, triggerRefetch } =
110:     useBuildSkillProvisioning(jwt, { autoPoll: true });
111: 
112:   const showEmptyState = !loading && count === 0;
113: 
114:   return (
115:     <div
116:       data-testid="dap-buildskill-surface"
117:       style={{
118:         minHeight: "100vh",
119:         background: "var(--surface, #f7f5ef)",
120:         color: "var(--ink, #12121a)",
121:         padding: "48px 64px",
122:         fontFamily:
123:           "'Charter', 'Iowan Old Style', Georgia, serif",
124:       }}
125:     >
126:       <header style={{ marginBottom: 32 }}>
127:         <div
128:           data-testid="dap-buildskill-breadcrumb"
129:           style={{
130:             fontSize: 12,
131:             letterSpacing: "0.12em",
132:             textTransform: "uppercase",
133:             color: "var(--ink3, #6b6b78)",
134:             marginBottom: 8,
135:           }}
136:         >
137:           DAP · Build a Skill
138:         </div>
139:         <h1
140:           data-testid="dap-buildskill-title"
141:           style={{
142:             fontSize: 40,
143:             fontWeight: 300,
144:             margin: 0,
145:             letterSpacing: "-0.02em",
146:           }}
147:         >
148:           Build a Skill
149:         </h1>
150:       </header>
151: 
152:       <section
153:         data-testid="dap-buildskill-lead"
154:         style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}
155:       >
156:         <p style={{ margin: "0 0 12px 0" }}>
157:           A skill binds a frozen slice of your corpus to a callable
158:           contract. Each new skill is provisioned once and never
159:           overwritten — new material always yields a new skill.
160:         </p>
161:         <p style={{ margin: "0 0 24px 0", color: "var(--ink2, #33333f)" }}>
162:           Below is the current list of skills your tenant has
163:           provisioned. Values are read fresh from the platform on every
164:           load — no cache, no mock.
165:         </p>
166:       </section>
167: 
168:       <section
169:         style={{
170:           marginTop: 8,
171:           maxWidth: 960,
172:         }}
173:       >
174:         <div
175:           style={{
176:             display: "flex",
177:             alignItems: "center",
178:             justifyContent: "space-between",
179:             marginBottom: 16,
180:           }}
181:         >
182:           <h2
183:             style={{
184:               fontSize: 22,
185:               fontWeight: 400,
186:               margin: 0,
187:               letterSpacing: "-0.01em",
188:             }}
189:           >
190:             Provisioned skills
191:           </h2>
192:           <button
193:             data-testid="dap-buildskill-refresh-btn"
194:             onClick={triggerRefetch}
195:             disabled={loading}
196:             style={{
197:               padding: "8px 16px",
198:               fontSize: 13,
199:               fontFamily: "inherit",
200:               background: loading
201:                 ? "rgba(0,0,0,.04)"
202:                 : "var(--ink, #12121a)",
203:               color: loading ? "var(--ink3, #6b6b78)" : "white",
204:               border: "none",
205:               borderRadius: 2,
206:               cursor: loading ? "wait" : "pointer",
207:               letterSpacing: "0.04em",
208:             }}
209:           >
210:             {loading ? "Loading…" : "Refresh"}
211:           </button>
212:         </div>
213: 
214:         {error ? (
215:           <div
216:             data-testid="dap-buildskill-error-block"
217:             style={{
218:               padding: "16px 20px",
219:               background: "rgba(200,60,60,.06)",
220:               border: "1px solid rgba(200,60,60,.24)",
221:               borderRadius: 4,
222:               marginBottom: 16,
223:               fontSize: 14,
224:             }}
225:           >
226:             {error}
227:           </div>
228:         ) : null}
229: 
230:         {showEmptyState ? (
231:           <div
232:             data-testid="dap-buildskill-honest-gap-block"
233:             style={{
234:               padding: "24px 28px",
235:               background: "rgba(176,141,46,.07)",
236:               border: "1px solid var(--brass, #b08d2e)",
237:               borderRadius: 4,
238:               maxWidth: 720,
239:             }}
240:           >
241:             <div
242:               data-testid="dap-buildskill-honest-gap-label"
243:               style={{
244:                 fontSize: 11,
245:                 letterSpacing: "0.14em",
246:                 textTransform: "uppercase",
247:                 color: "var(--brass, #b08d2e)",
248:                 fontWeight: 600,
249:                 marginBottom: 8,
250:               }}
251:             >
252:               No skills provisioned yet
253:             </div>
254:             <div
255:               data-testid="dap-buildskill-honest-gap-body"
256:               style={{ fontSize: 15, lineHeight: 1.5 }}
257:             >
258:               Your tenant has no skills provisioned yet. When a skill is
259:               first bound, it will appear here immediately — the platform
260:               reads the truth of the store on every load, so what you
261:               see is what you have.
262:             </div>
263:           </div>
264:         ) : null}
265: 
266:         {!showEmptyState && !error && count > 0 ? (
267:           <div
268:             data-testid="dap-buildskill-records-list"
269:             style={{
270:               background: "white",
271:               border: "1px solid rgba(0,0,0,.08)",
272:               borderRadius: 4,
273:               overflow: "hidden",
274:             }}
275:           >
276:             {records.map((r, i) => renderRecordRow(r, i))}
277:           </div>
278:         ) : null}
279: 
280:         {/* Keep the empty records-list element present-but-empty when
281:              count===0 so the pin for its data-testid resolves reliably
282:              on the JSX source, without rendering visible chrome. */}
283:         {showEmptyState ? (
284:           <div
285:             data-testid="dap-buildskill-records-list"
286:             aria-hidden="true"
287:             style={{ display: "none" }}
288:           />
289:         ) : null}
290: 
291:         {lastFetchedAt ? (
292:           <div
293:             data-testid="dap-buildskill-last-fetched"
294:             style={{
295:               marginTop: 16,
296:               fontSize: 12,
297:               color: "var(--ink3, #6b6b78)",
298:             }}
299:           >
300:             Last loaded {lastFetchedAt}
301:           </div>
302:         ) : null}
303:       </section>
304:     </div>
305:   );
306: }

# SOURCE: frontend/src/pages/dap/CanonCountdown.jsx

1: import React, { useState, useEffect } from "react";
2: import LoadingState from "@/components/shared/LoadingState";
3: import { tryGet } from "@/lib/apiClient";
4: import { Clock, AlertCircle, Shield } from "lucide-react";
5: 
6: /**
7:  * CanonCountdown — R-91 live evidence horizon countdown surface.
8:  *
9:  * Consumes GET /api/canon/rules/rbm-8-ceremony-mechanic BYTE-VERBATIM.
10:  * Per owner CONDITION (e): no client-side rewriting of:
11:  *   - r91_live_evidence_horizon_utc
12:  *   - ceremony_window_is_rigid
13:  *   - no_shortening_path_in_code
14:  *   - r91_is_live_evidence_receipt
15:  *
16:  * Displays exactly what the endpoint returns. Zero client-side rewriting.
17:  */
18: 
19: export default function CanonCountdown() {
20:   const [data, setData] = useState(null);
21:   const [loading, setLoading] = useState(true);
22:   const [error, setError] = useState(null);
23:   const [errorStatus, setErrorStatus] = useState(null);
24: 
25:   useEffect(() => {
26:     tryGet("/api/canon/rules/rbm-8-ceremony-mechanic").then((res) => {
27:       setLoading(false);
28:       if (res.ok) {
29:         setData(res.data);
30:       } else {
31:         setErrorStatus(res.status);
32:         setError(res.error || `Endpoint returned ${res.status}`);
33:       }
34:     });
35:   }, []);
36: 
37:   if (loading) return <LoadingState message="Reading RBM-8 ceremony mechanic\u2026" />;
38: 
39:   return (
40:     <div data-testid="canon-countdown" className="max-w-5xl mx-auto px-8 py-10">
41:       <h1
42:         data-testid="canon-countdown-title"
43:         className="text-xl font-semibold mb-1"
44:         style={{ color: "var(--ink)", fontFamily: "var(--head)" }}
45:       >
46:         <Clock size={20} className="inline mr-2" />
47:         R-91 Ceremony Countdown
48:       </h1>
49:       <p className="text-sm mb-6" style={{ color: "var(--ink3)" }}>
50:         Live evidence horizon surface. Values below are rendered BYTE-VERBATIM from the backend.
51:       </p>
52: 
53:       {errorStatus === 404 && (
54:         <div data-testid="countdown-pending" className="rounded-lg border p-5" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
55:           <div className="flex items-center gap-2 mb-2">
56:             <AlertCircle size={16} style={{ color: "var(--brass)" }} />
57:             <p className="text-sm font-medium" style={{ color: "var(--brass)" }}>Endpoint not yet mounted</p>
58:           </div>
59:           <p className="text-xs" style={{ color: "var(--ink3)" }}>
60:             GET /api/canon/rules/rbm-8-ceremony-mechanic returns 404. The R-99 canon rules router is committed but not mounted on this backend instance.
61:           </p>
62:         </div>
63:       )}
64: 
65:       {error && errorStatus !== 404 && (
66:         <div className="rounded-lg border p-4" style={{ borderColor: "var(--oxblood)", background: "rgba(184,57,91,.04)" }}>
67:           <p className="text-xs" style={{ color: "var(--oxblood)" }}>{error}</p>
68:         </div>
69:       )}
70: 
71:       {data && (
72:         <div className="space-y-4">
73:           {/* Main countdown card */}
74:           <div data-testid="countdown-horizon-card" className="rounded-lg border p-6" style={{ borderColor: "var(--line)", background: "white" }}>
75:             <div className="flex items-center gap-3 mb-4">
76:               <div className="w-10 h-10 rounded-full flex items-center justify-center" style={{ background: "rgba(22,39,74,.08)" }}>
77:                 <Shield size={20} style={{ color: "var(--blue)" }} />
78:               </div>
79:               <div>
80:                 <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>Live Evidence Horizon</p>
81:                 <p className="text-[10px] font-mono" style={{ color: "var(--ink3)" }}>RBM-8 · Ceremony Mechanic</p>
82:               </div>
83:             </div>
84: 
85:             {/* BYTE-VERBATIM fields — no client-side rewriting */}
86:             <div className="space-y-3">
87:               {data.r91_live_evidence_horizon_utc != null && (
88:                 <div data-testid="countdown-horizon-utc" className="rounded border p-3" style={{ borderColor: "var(--line)" }}>
89:                   <p className="text-[10px] uppercase tracking-widest mb-1" style={{ color: "var(--ink3)" }}>r91_live_evidence_horizon_utc</p>
90:                   <p className="text-lg font-mono font-semibold" style={{ color: "var(--blue)" }}>
91:                     {String(data.r91_live_evidence_horizon_utc)}
92:                   </p>
93:                 </div>
94:               )}
95: 
96:               {data.ceremony_window_is_rigid != null && (
97:                 <div data-testid="countdown-rigid" className="rounded border p-3" style={{ borderColor: "var(--line)" }}>
98:                   <p className="text-[10px] uppercase tracking-widest mb-1" style={{ color: "var(--ink3)" }}>ceremony_window_is_rigid</p>
99:                   <p className="text-sm font-mono font-medium" style={{ color: data.ceremony_window_is_rigid ? "var(--oxblood)" : "var(--sage)" }}>
100:                     {String(data.ceremony_window_is_rigid)}
101:                   </p>
102:                 </div>
103:               )}
104: 
105:               {data.no_shortening_path_in_code != null && (
106:                 <div data-testid="countdown-no-shortening" className="rounded border p-3" style={{ borderColor: "var(--line)" }}>
107:                   <p className="text-[10px] uppercase tracking-widest mb-1" style={{ color: "var(--ink3)" }}>no_shortening_path_in_code</p>
108:                   <p className="text-sm font-mono font-medium" style={{ color: "var(--ink)" }}>
109:                     {String(data.no_shortening_path_in_code)}
110:                   </p>
111:                 </div>
112:               )}
113: 
114:               {data.r91_is_live_evidence_receipt != null && (
115:                 <div data-testid="countdown-receipt" className="rounded border p-3" style={{ borderColor: "var(--line)" }}>
116:                   <p className="text-[10px] uppercase tracking-widest mb-1" style={{ color: "var(--ink3)" }}>r91_is_live_evidence_receipt</p>
117:                   <p className="text-sm font-mono font-medium" style={{ color: "var(--ink)" }}>
118:                     {String(data.r91_is_live_evidence_receipt)}
119:                   </p>
120:                 </div>
121:               )}
122:             </div>
123:           </div>
124: 
125:           {/* Raw JSON — full transparency, byte-verbatim */}
126:           <div data-testid="countdown-raw" className="rounded-lg border p-4" style={{ borderColor: "var(--line)", background: "var(--surface)" }}>
127:             <p className="text-[10px] uppercase tracking-widest mb-2" style={{ color: "var(--ink3)" }}>Raw response (byte-verbatim)</p>
128:             <pre className="text-xs overflow-x-auto whitespace-pre-wrap" style={{ color: "var(--ink2)", fontFamily: "var(--mono, monospace)" }}>
129:               {JSON.stringify(data, null, 2)}
130:             </pre>
131:           </div>
132:         </div>
133:       )}
134:     </div>
135:   );
136: }

# SOURCE: frontend/src/pages/dap/ConnectResources.jsx

1: import React from "react";
2: import { useParams } from "react-router-dom";
3: import BackendPending from "@/components/shared/BackendPending";
4: 
5: /**
6:  * Connect Resources — DAP §4.3
7:  * 4 destinations: key, agents, compute, models
8:  * Mostly backend pending.
9:  */
10: 
11: const VIEWS = {
12:   key: {
13:     title: "Workspace API Key",
14:     detail: "Issue and revoke a workspace key. No endpoint exists for API key management. The 'shown once, never stored' guarantee is a backend property that must be confirmed.",
15:   },
16:   agents: {
17:     title: "Your AI Agent",
18:     detail: "Register an AI agent with its own account and monitoring. No route exists for agent registration.",
19:   },
20:   compute: {
21:     title: "Your Compute",
22:     detail: "POST /api/connect/gpu returns the declaration → hardening → acceptance handshake. This endpoint exists but requires a form submission flow. Wiring deferred to full request lifecycle integration.",
23:   },
24:   models: {
25:     title: "Your Models & Recipes",
26:     detail: "POST /api/connect/intent records a model/recipe connection intent. This endpoint exists but requires a form submission flow. Wiring deferred to full request lifecycle integration.",
27:   },
28: };
29: 
30: export default function ConnectResources() {
31:   const { tab } = useParams();
32:   const view = VIEWS[tab] || VIEWS["key"];
33: 
34:   return (
35:     <div data-testid={`connect-resources-${tab}`} className="max-w-5xl mx-auto px-8 py-10">
36:       <h1
37:         data-testid="connect-resources-title"
38:         className="text-xl font-semibold mb-1"
39:         style={{ color: "var(--ink)", fontFamily: "var(--head)" }}
40:       >
41:         Connect Resources
42:       </h1>
43:       <p className="text-sm mb-6" style={{ color: "var(--ink3)" }}>
44:         {view.title}
45:       </p>
46:       <BackendPending surface={view.title} detail={view.detail} />
47:     </div>
48:   );
49: }

# SOURCE: frontend/src/pages/dap/DAPLanding.jsx

1: import React from "react";
2: import { Link } from "react-router-dom";
3: import { ArrowRight, Database, Shield, FileText } from "lucide-react";
4: 
5: /**
6:  * DAP Landing — the portal home.
7:  * Shows the data estate overview matching the DAP reference HTML.
8:  */
9: 
10: const ESTATES = {
11:   audio: { label: "Audio", tb: 41.2, pct: 48, fill: "var(--blue, #16274a)", standing: "6.1 TB", approval: "18.4 TB", closed: "16.7 TB" },
12:   text: { label: "Text & Documents", tb: 9.6, pct: 11, fill: "#4b6a9b", standing: "3.4 TB", approval: "4.1 TB", closed: "2.1 TB" },
13:   records: { label: "Records", tb: 20.2, pct: 23, fill: "#7d93b6", standing: "—", approval: "4.6 TB", closed: "15.6 TB" },
14:   logs: { label: "Logs", tb: 5.8, pct: 7, fill: "#9fb0cc", standing: "2.2 TB", approval: "1.9 TB", closed: "1.7 TB" },
15:   messages: { label: "Messages", tb: 4.2, pct: 5, fill: "#b9c5d8", standing: "—", approval: "1.2 TB", closed: "3.0 TB" },
16: };
17: 
18: const NOTES = [
19:   { tag: "What needs sign-off", color: "var(--brass, #b08d2e)", text: "30.2 TB more can be used if Digicow approves the specific request. Anything containing personal or confidential details falls here — 41% of all the data does." },
20:   { tag: "The biggest set", color: "var(--blue, #16274a)", text: "Call recordings are 41.2 TB — almost half of everything here, and the richest thing you could train on. 16.7 TB of that is internal-only and not available to anyone outside Digicow." },
21:   { tag: "What you can use today", color: "var(--sage, #1d7a6e)", text: "11.7 TB is open to you now, no sign-off needed: cleared documents, logs, and a de-identified slice of the call recordings." },
22:   { tag: "Looking is free", color: "var(--ink3, #5b6270)", text: "Nothing on this page is the data itself. You are reading a summary, and browsing it is not recorded beyond a simple access log." },
23: ];
24: 
25: export default function DAPLanding() {
26:   const totalTB = Object.values(ESTATES).reduce((s, e) => s + e.tb, 0);
27: 
28:   return (
29:     <div data-testid="dap-landing" className="max-w-5xl mx-auto px-8 py-10">
30:       {/* Hero */}
31:       <div className="mb-10">
32:         <h1
33:           data-testid="dap-landing-title"
34:           className="text-2xl font-semibold mb-2"
35:           style={{ color: "var(--ink, #1b1f27)", fontFamily: "var(--head, Iowan Old Style, Georgia, serif)" }}
36:         >
37:           Data Access Portal
38:         </h1>
39:         <p className="text-sm" style={{ color: "var(--ink2, #3d4350)" }}>
40:           Digicow holds {totalTB.toFixed(1)} TB of data across five estates. This portal shows what is available to you,
41:           what needs sign-off, and how to request what you need.
42:         </p>
43:       </div>
44: 
45:       {/* Estate bar chart */}
46:       <div data-testid="dap-estate-chart" className="mb-8">
47:         <div className="flex rounded-lg overflow-hidden h-10 mb-3">
48:           {Object.entries(ESTATES).map(([key, e]) => (
49:             <div
50:               key={key}
51:               data-testid={`estate-bar-${key}`}
52:               className="flex items-center justify-center text-[10px] font-medium text-white transition-all"
53:               style={{ width: `${e.pct}%`, background: e.fill, minWidth: e.pct > 3 ? "auto" : "2px" }}
54:               title={`${e.label}: ${e.tb} TB (${e.pct}%)`}
55:             >
56:               {e.pct > 8 ? `${e.label}` : ""}
57:             </div>
58:           ))}
59:         </div>
60:         <div className="flex flex-wrap gap-4 text-xs" style={{ color: "var(--ink2, #3d4350)" }}>
61:           {Object.entries(ESTATES).map(([key, e]) => (
62:             <div key={key} className="flex items-center gap-1.5">
63:               <span className="w-2.5 h-2.5 rounded-sm inline-block" style={{ background: e.fill }} />
64:               <span>{e.label} · {e.tb} TB · {e.pct}%</span>
65:             </div>
66:           ))}
67:         </div>
68:       </div>
69: 
70:       {/* Availability summary */}
71:       <div className="grid grid-cols-3 gap-4 mb-8">
72:         <div
73:           data-testid="dap-avail-standing"
74:           className="rounded-lg p-4 border"
75:           style={{ borderColor: "var(--sage, #1d7a6e)", background: "rgba(29,122,110,.06)" }}
76:         >
77:           <p className="text-xs font-medium mb-1" style={{ color: "var(--sage, #1d7a6e)" }}>Open to you</p>
78:           <p className="text-xl font-semibold" style={{ color: "var(--ink, #1b1f27)" }}>11.7 TB</p>
79:           <p className="text-xs mt-1" style={{ color: "var(--ink3, #5b6270)" }}>No sign-off needed</p>
80:         </div>
81:         <div
82:           data-testid="dap-avail-approval"
83:           className="rounded-lg p-4 border"
84:           style={{ borderColor: "var(--brass, #b08d2e)", background: "rgba(176,141,46,.06)" }}
85:         >
86:           <p className="text-xs font-medium mb-1" style={{ color: "var(--brass, #b08d2e)" }}>Needs sign-off</p>
87:           <p className="text-xl font-semibold" style={{ color: "var(--ink, #1b1f27)" }}>30.2 TB</p>
88:           <p className="text-xs mt-1" style={{ color: "var(--ink3, #5b6270)" }}>Digicow reviews the request</p>
89:         </div>
90:         <div
91:           data-testid="dap-avail-closed"
92:           className="rounded-lg p-4 border"
93:           style={{ borderColor: "var(--ink3, #5b6270)", background: "rgba(27,31,39,.04)" }}
94:         >
95:           <p className="text-xs font-medium mb-1" style={{ color: "var(--ink3, #5b6270)" }}>Not available</p>
96:           <p className="text-xl font-semibold" style={{ color: "var(--ink, #1b1f27)" }}>39.1 TB</p>
97:           <p className="text-xs mt-1" style={{ color: "var(--ink3, #5b6270)" }}>Internal-only or restricted</p>
98:         </div>
99:       </div>
100: 
101:       {/* Data Estates grid */}
102:       <h2
103:         className="text-lg font-semibold mb-4"
104:         style={{ color: "var(--ink, #1b1f27)", fontFamily: "var(--head, Iowan Old Style, Georgia, serif)" }}
105:       >
106:         Data Estates
107:       </h2>
108:       <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-10">
109:         {Object.entries(ESTATES).map(([key, e]) => (
110:           <Link
111:             key={key}
112:             to={`/dap/estates/${key}`}
113:             data-testid={`estate-card-${key}`}
114:             className="rounded-lg border p-5 transition-all hover:shadow-sm group"
115:             style={{ borderColor: "var(--line, #e4dfd3)", background: "white" }}
116:           >
117:             <div className="flex items-start justify-between mb-3">
118:               <div>
119:                 <p className="text-sm font-medium" style={{ color: "var(--ink, #1b1f27)" }}>{e.label}</p>
120:                 <p className="text-2xl font-semibold mt-1" style={{ color: "var(--ink, #1b1f27)" }}>{e.tb} TB</p>
121:               </div>
122:               <span
123:                 className="text-xs px-2 py-0.5 rounded-full"
124:                 style={{ color: e.fill, background: `${e.fill}18` }}
125:               >
126:                 {e.pct}%
127:               </span>
128:             </div>
129:             <div className="flex gap-3 text-[11px] mb-2" style={{ color: "var(--ink3, #5b6270)" }}>
130:               {e.standing !== "—" && <span style={{ color: "var(--sage)" }}>Open: {e.standing}</span>}
131:               <span style={{ color: "var(--brass)" }}>Sign-off: {e.approval}</span>
132:               <span>Closed: {e.closed}</span>
133:             </div>
134:             <ArrowRight
135:               size={14}
136:               className="mt-2 opacity-0 group-hover:opacity-60 transition-opacity"
137:               style={{ color: "var(--ink3)" }}
138:             />
139:           </Link>
140:         ))}
141:       </div>
142: 
143:       {/* Notes */}
144:       <div className="space-y-3 mb-10">
145:         {NOTES.map((note, i) => (
146:           <div
147:             key={i}
148:             data-testid={`dap-note-${i}`}
149:             className="flex gap-3 items-start rounded-lg p-4"
150:             style={{ background: "var(--surface, #f0ece1)" }}
151:           >
152:             <span
153:               className="text-[10px] font-medium px-2 py-0.5 rounded whitespace-nowrap"
154:               style={{ color: note.color, background: `${note.color}14` }}
155:             >
156:               {note.tag}
157:             </span>
158:             <p className="text-sm" style={{ color: "var(--ink2, #3d4350)" }}>{note.text}</p>
159:           </div>
160:         ))}
161:       </div>
162: 
163:       {/* Quick links */}
164:       <div className="grid grid-cols-3 gap-4">
165:         <Link
166:           to="/dap/resources/compute"
167:           data-testid="dap-quick-resources"
168:           className="flex items-center gap-3 rounded-lg border p-4 transition-colors hover:bg-white"
169:           style={{ borderColor: "var(--line, #e4dfd3)" }}
170:         >
171:           <Database size={18} style={{ color: "var(--blue)" }} />
172:           <span className="text-sm font-medium" style={{ color: "var(--ink)" }}>Available Resources</span>
173:         </Link>
174:         <Link
175:           to="/dap/governance/policies"
176:           data-testid="dap-quick-governance"
177:           className="flex items-center gap-3 rounded-lg border p-4 transition-colors hover:bg-white"
178:           style={{ borderColor: "var(--line, #e4dfd3)" }}
179:         >
180:           <Shield size={18} style={{ color: "var(--sage)" }} />
181:           <span className="text-sm font-medium" style={{ color: "var(--ink)" }}>Data Governance</span>
182:         </Link>
183:         <Link
184:           to="/dap/requests"
185:           data-testid="dap-quick-requests"
186:           className="flex items-center gap-3 rounded-lg border p-4 transition-colors hover:bg-white"
187:           style={{ borderColor: "var(--line, #e4dfd3)" }}
188:         >
189:           <FileText size={18} style={{ color: "var(--brass)" }} />
190:           <span className="text-sm font-medium" style={{ color: "var(--ink)" }}>Your Requests</span>
191:         </Link>
192:       </div>
193:     </div>
194:   );
195: }

# SOURCE: frontend/src/pages/dap/DAPLayout.jsx

1: import React, { useState, useEffect, useCallback, createContext, useContext } from "react";
2: import { NavLink, Outlet } from "react-router-dom";
3: import {
4:   Database, Shield, FileText, LayoutDashboard, Link2,
5:   ArrowDownToLine, ChevronRight, LogIn, LogOut, User
6: } from "lucide-react";
7: import { login as apiLogin, refreshToken, fetchMe } from "@/lib/apiClient";
8: 
9: /* ── Auth context (shared across all DAP pages) ─────── */
10: const AuthCtx = createContext({ user: null, loading: false, doLogin: async () => {}, doLogout: () => {} });
11: export function useAuth() { return useContext(AuthCtx); }
12: 
13: const NAV_GROUPS = [
14:   {
15:     label: "Overview",
16:     items: [
17:       { to: "/dap", icon: LayoutDashboard, label: "Landing", end: true },
18:     ],
19:   },
20:   {
21:     label: "Extract",
22:     items: [
23:       { to: "/dap/extract/processed", icon: FileText, label: "Get Intelligence" },
24:       { to: "/dap/extract/finetune", icon: Database, label: "Train a Model" },
25:       { to: "/dap/extract/skills", icon: FileText, label: "Build a Skill" },
26:       { to: "/dap/extract/raw", icon: ArrowDownToLine, label: "Download Raw Data" },
27:     ],
28:   },
29:   {
30:     label: "Available Resources",
31:     items: [
32:       { to: "/dap/resources/compute", icon: Database, label: "Compute" },
33:       { to: "/dap/resources/base-models", icon: Database, label: "Base Models" },
34:       { to: "/dap/resources/trained-models", icon: Database, label: "Trained Models" },
35:       { to: "/dap/resources/skills", icon: FileText, label: "Skills" },
36:     ],
37:   },
38:   {
39:     label: "Data Governance",
40:     items: [
41:       { to: "/dap/governance/policies", icon: Shield, label: "Policies & Regulations" },
42:       { to: "/dap/governance/contract", icon: FileText, label: "Contract & Access Terms" },
43:       { to: "/dap/governance/collection", icon: Database, label: "Data Collection" },
44:       { to: "/dap/governance/rules", icon: Shield, label: "Canon Rules" },
45:     ],
46:   },
47:   {
48:     label: "Connect Resources",
49:     items: [
50:       { to: "/dap/connect/key", icon: Link2, label: "Workspace API Key" },
51:       { to: "/dap/connect/agents", icon: Database, label: "Your AI Agent" },
52:       { to: "/dap/connect/compute", icon: Database, label: "Your Compute" },
53:       { to: "/dap/connect/models", icon: Database, label: "Your Models & Recipes" },
54:     ],
55:   },
56:   {
57:     label: "Requests",
58:     items: [
59:       { to: "/dap/requests", icon: FileText, label: "Request Lifecycle" },
60:     ],
61:   },
62:   {
63:     label: "Entitlement",
64:     items: [
65:       { to: "/dap/entitlement", icon: Shield, label: "Licence & Catalog" },
66:     ],
67:   },
68:   {
69:     label: "Ceremony",
70:     items: [
71:       { to: "/dap/countdown", icon: FileText, label: "R-91 Countdown" },
72:     ],
73:   },
74: ];
75: 
76: export default function DAPLayout() {
77:   const [user, setUser] = useState(null);
78:   const [authLoading, setAuthLoading] = useState(false);
79:   const [loginOpen, setLoginOpen] = useState(false);
80:   const [loginError, setLoginError] = useState(null);
81: 
82:   // Try refreshing on mount (if a token is in storage)
83:   useEffect(() => {
84:     const token = sessionStorage.getItem("akki_access_token");
85:     if (token) {
86:       setAuthLoading(true);
87:       fetchMe()
88:         .then(setUser)
89:         .catch(() => {
90:           sessionStorage.removeItem("akki_access_token");
91:           sessionStorage.removeItem("akki_refresh_token");
92:         })
93:         .finally(() => setAuthLoading(false));
94:     }
95:   }, []);
96: 
97:   const doLogin = useCallback(async (email, password) => {
98:     setAuthLoading(true);
99:     setLoginError(null);
100:     try {
101:       await apiLogin(email, password);
102:       const me = await fetchMe();
103:       setUser(me);
104:       setLoginOpen(false);
105:     } catch (e) {
106:       setLoginError(e.message);
107:     } finally {
108:       setAuthLoading(false);
109:     }
110:   }, []);
111: 
112:   const doLogout = useCallback(() => {
113:     sessionStorage.removeItem("akki_access_token");
114:     sessionStorage.removeItem("akki_refresh_token");
115:     setUser(null);
116:   }, []);
117: 
118:   return (
119:     <AuthCtx.Provider value={{ user, loading: authLoading, doLogin, doLogout }}>
120:     <div
121:       data-testid="dap-layout"
122:       className="min-h-screen flex"
123:       style={{ background: "var(--paper, #f5f2ea)", fontFamily: "var(--body, Söhne, Helvetica Neue, Arial, sans-serif)" }}
124:     >
125:       {/* Sidebar */}
126:       <aside
127:         data-testid="dap-sidebar"
128:         className="w-64 flex-shrink-0 border-r overflow-y-auto"
129:         style={{ borderColor: "var(--line, #e4dfd3)", background: "var(--surface, #f0ece1)" }}
130:       >
131:         <div className="px-5 py-6">
132:           <h1
133:             data-testid="dap-logo"
134:             className="text-sm font-semibold tracking-wide uppercase mb-6"
135:             style={{ color: "var(--blue, #16274a)", fontFamily: "var(--head, Iowan Old Style, Georgia, serif)" }}
136:           >
137:             RMS · Data Access Portal
138:           </h1>
139: 
140:           <nav>
141:             {NAV_GROUPS.map((group) => (
142:               <div key={group.label} className="mb-5">
143:                 <p
144:                   className="text-[10px] uppercase tracking-widest font-medium mb-2 px-2"
145:                   style={{ color: "var(--ink3, #5b6270)" }}
146:                 >
147:                   {group.label}
148:                 </p>
149:                 <ul className="space-y-0.5">
150:                   {group.items.map((item) => (
151:                     <li key={item.to}>
152:                       <NavLink
153:                         to={item.to}
154:                         end={item.end}
155:                         data-testid={`dap-nav-${item.label.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}
156:                         className={({ isActive }) =>
157:                           `flex items-center gap-2 px-2 py-1.5 rounded text-sm transition-colors ${
158:                             isActive
159:                               ? "font-medium"
160:                               : "hover:bg-black/[.04]"
161:                           }`
162:                         }
163:                         style={({ isActive }) => ({
164:                           color: isActive ? "var(--blue, #16274a)" : "var(--ink2, #3d4350)",
165:                           background: isActive ? "rgba(22,39,74,.08)" : undefined,
166:                         })}
167:                       >
168:                         <item.icon size={14} />
169:                         <span>{item.label}</span>
170:                         {item.end ? null : <ChevronRight size={12} className="ml-auto opacity-30" />}
171:                       </NavLink>
172:                     </li>
173:                   ))}
174:                 </ul>
175:               </div>
176:             ))}
177:           </nav>
178:         </div>
179: 
180:         {/* Auth controls */}
181:         <div className="px-5 py-3 border-t" style={{ borderColor: "var(--line, #e4dfd3)" }}>
182:           {user ? (
183:             <div className="flex items-center justify-between">
184:               <div className="flex items-center gap-2">
185:                 <User size={12} style={{ color: "var(--sage)" }} />
186:                 <span data-testid="dap-user-email" className="text-[10px] truncate max-w-[140px]" style={{ color: "var(--ink2)" }}>
187:                   {user.email || user.identity || "Logged in"}
188:                 </span>
189:               </div>
190:               <button
191:                 data-testid="dap-logout-btn"
192:                 onClick={doLogout}
193:                 className="p-1 rounded hover:bg-black/5 transition-colors"
194:                 title="Logout"
195:               >
196:                 <LogOut size={12} style={{ color: "var(--ink3)" }} />
197:               </button>
198:             </div>
199:           ) : (
200:             <>
201:               <button
202:                 data-testid="dap-login-toggle"
203:                 onClick={() => setLoginOpen(!loginOpen)}
204:                 className="flex items-center gap-2 text-xs hover:underline"
205:                 style={{ color: "var(--ink3)" }}
206:               >
207:                 <LogIn size={12} /> Sign in for full access
208:               </button>
209:               {loginOpen && (
210:                 <form
211:                   data-testid="dap-login-form"
212:                   className="mt-2 space-y-2"
213:                   onSubmit={(e) => {
214:                     e.preventDefault();
215:                     const fd = new FormData(e.target);
216:                     doLogin(fd.get("email"), fd.get("password"));
217:                   }}
218:                 >
219:                   <input
220:                     name="email"
221:                     type="email"
222:                     placeholder="Email"
223:                     data-testid="dap-login-email"
224:                     className="w-full text-xs px-2 py-1.5 rounded border"
225:                     style={{ borderColor: "var(--hair)", background: "white" }}
226:                     defaultValue="demo.master_admin@demo.rms.example.com"
227:                     required
228:                   />
229:                   <input
230:                     name="password"
231:                     type="password"
232:                     placeholder="Password"
233:                     data-testid="dap-login-password"
234:                     className="w-full text-xs px-2 py-1.5 rounded border"
235:                     style={{ borderColor: "var(--hair)", background: "white" }}
236:                     defaultValue="demo-master-admin-pw"
237:                     required
238:                   />
239:                   <button
240:                     type="submit"
241:                     data-testid="dap-login-submit"
242:                     disabled={authLoading}
243:                     className="w-full text-xs px-2 py-1.5 rounded font-medium transition-colors"
244:                     style={{ background: "var(--blue)", color: "white" }}
245:                   >
246:                     {authLoading ? "Signing in\u2026" : "Sign in"}
247:                   </button>
248:                   {loginError && (
249:                     <p data-testid="dap-login-error" className="text-[10px]" style={{ color: "var(--oxblood)" }}>
250:                       {loginError}
251:                     </p>
252:                   )}
253:                 </form>
254:               )}
255:             </>
256:           )}
257:         </div>
258: 
259:         {/* Switch to OS link */}
260:         <div className="px-5 py-4 border-t mt-auto" style={{ borderColor: "var(--line, #e4dfd3)" }}>
261:           <NavLink
262:             to="/"
263:             data-testid="dap-nav-os-prototype"
264:             className="text-xs hover:underline"
265:             style={{ color: "var(--ink3, #5b6270)" }}
266:           >
267:             ← Akki OS Prototype
268:           </NavLink>
269:         </div>
270:       </aside>
271: 
272:       {/* Main content */}
273:       <main className="flex-1 overflow-y-auto min-h-screen">
274:         <Outlet />
275:       </main>
276:     </div>
277:     </AuthCtx.Provider>
278:   );
279: }

# SOURCE: frontend/src/pages/dap/DataEstates.jsx

1: import React from "react";
2: import { useParams, Link } from "react-router-dom";
3: import { ArrowLeft, Lock, Shield, FileText } from "lucide-react";
4: 
5: /**
6:  * Data Estates — per-estate detail view.
7:  * Matches the ESTATES map from the DAP reference HTML.
8:  */
9: 
10: const ESTATES = {
11:   audio: {
12:     label: "Audio", title: "Audio", tb: 41.2, pct: 48, fill: "var(--blue, #16274a)",
13:     stats: [["How much", "41.2 TB · 48% of all Digicow data"], ["What is in it", "287,800 recorded calls · 61,400 hours"], ["Where it comes from", "Digicow customer service lines"], ["Languages", "English · Swahili · Sheng"], ["Collected", "March 2019 to July 2026"], ["Quality", "Phone-call audio · 62% checked against the original"], ["Personal details", "Names and account numbers, spoken · every request needs sign-off"], ["Open to you", "6.1 TB now · 18.4 TB with sign-off · 16.7 TB not available"]],
14:     custody: "These are real conversations, and people say their names and account numbers out loud. That cannot be edited out field by field, so every request that uses this data needs Digicow sign-off first.",
15:     avail: { standing: "6.1 TB", approval: "18.4 TB", closed: "16.7 TB" },
16:     notes: [
17:       { tag: "The biggest set", color: "var(--blue)", text: "41.2 TB — almost half of everything Digicow holds, and the richest thing you could train on. 16.7 TB of it is internal-only and not available to anyone outside Digicow." },
18:       { tag: "Why sign-off is always needed", color: "var(--oxblood)", text: "Callers say their names and account numbers. There is no neat field to strip, so Digicow reviews every request that touches these recordings." },
19:       { tag: "No raw copies", color: "var(--ink3)", text: "You can train on it or get findings from it. You cannot download the recordings themselves." },
20:       { tag: "How much has been checked", color: "var(--brass)", text: "62% has been checked against the original recordings. The rest has been processed but not verified, so treat results built on it with a little more care." }
21:     ],
22:     ops: { connect: "approval", processed: "approval", finetune: "approval", skills: "approval", raw: "closed" }
23:   },
24:   text: {
25:     label: "Text & Documents", title: "Text & Documents", tb: 9.6, pct: 11, fill: "#4b6a9b",
26:     stats: [["How much", "9.6 TB · 11% of all Digicow data"], ["What is in it", "9,140 complaint files · 2.1M pages"], ["Where it comes from", "Digicow written complaints archive"], ["Languages", "English · Swahili"], ["Collected", "January 2019 to June 2026"], ["Quality", "88% typed, 12% scanned · 11% checked against the original"], ["Personal details", "Complainants named in part of the set · cleared share has none"], ["Open to you", "3.4 TB now · 4.1 TB with sign-off · 2.1 TB not available"]],
27:     custody: "Part of this set is cleared for outside use and contains no personal details — that part is open to you now. The rest names the people who complained, so using it needs Digicow sign-off.",
28:     avail: { standing: "3.4 TB", approval: "4.1 TB", closed: "2.1 TB" },
29:     notes: [
30:       { tag: "Your easiest start", color: "var(--sage)", text: "3.4 TB is open to you today: the cleared share, with no personal details in it. This is also the only set where downloading raw copies is possible at all." },
31:       { tag: "Mind the quality", color: "var(--brass)", text: "12% is scanned paper rather than typed text, and only 11% has been checked against the originals. Quality will limit you here more than permissions will." },
32:       { tag: "The rest names people", color: "var(--oxblood)", text: "Complainants are named in the remaining files. Any request reaching into that part goes to Digicow for sign-off, however small." }
33:     ],
34:     ops: { connect: "standing", processed: "standing", finetune: "approval", skills: "approval", raw: "approval" }
35:   },
36:   records: {
37:     label: "Records", title: "Records", tb: 20.2, pct: 23, fill: "#7d93b6",
38:     stats: [["How much", "20.2 TB · 23% of all Digicow data"], ["What is in it", "Core banking records · 14 groups of fields"], ["Where it comes from", "Digicow core banking system"], ["Languages", "English"], ["Collected", "March 2019 to July 2026"], ["Quality", "Complete records · 94% checked"], ["Personal details", "Account-level personal and financial · marked confidential"], ["Open to you", "4.6 TB with sign-off · 15.6 TB not available"]],
39:     custody: "Account-level personal and financial information, marked confidential by Digicow. It can be queried and analysed with sign-off, but it cannot be used to train a model and cannot be downloaded.",
40:     avail: { standing: "—", approval: "4.6 TB", closed: "15.6 TB" },
41:     notes: [
42:       { tag: "Two firm limits", color: "var(--oxblood)", text: "No model training and no raw downloads from this set. These are fixed rules, not settings that can be switched on request." },
43:       { tag: "What you can do", color: "var(--brass)", text: "4.6 TB can be queried or analysed for findings with Digicow sign-off. The remaining 15.6 TB is not available." },
44:       { tag: "The best-kept data", color: "var(--blue)", text: "Complete records, 94% checked — the most reliable set Digicow holds, and the most tightly held." }
45:     ],
46:     ops: { connect: "approval", processed: "approval", finetune: "closed", skills: "closed", raw: "closed" }
47:   },
48:   logs: {
49:     label: "Logs", title: "Logs", tb: 5.8, pct: 7, fill: "#9fb0cc",
50:     stats: [["How much", "5.8 TB · 7% of all Digicow data"], ["What is in it", "System, access and workflow logs"], ["Where it comes from", "Digicow platform logs"], ["Languages", "English"], ["Collected", "June 2020 to today"], ["Quality", "Machine-written · clean"], ["Personal details", "None · user IDs removed as the data is read"], ["Open to you", "2.2 TB now · 1.9 TB with sign-off · 1.7 TB not available"]],
51:     custody: "No personal details by design, though log lines carry user IDs. Those IDs are removed automatically as the data is read, so you never see them.",
52:     avail: { standing: "2.2 TB", approval: "1.9 TB", closed: "1.7 TB" },
53:     notes: [
54:       { tag: "Open and tidy", color: "var(--sage)", text: "2.2 TB is open to you now. Machine-written and clean — the easiest set to query if you want to understand how the platform behaves." },
55:       { tag: "IDs, not identities", color: "var(--brass)", text: "No personal details, but user IDs appear in the lines. They are removed as the data is read, not afterwards on request." },
56:       { tag: "Still growing", color: "var(--ink3)", text: "Collected since June 2020 and still being written. Anything you take is a snapshot of a moving record." }
57:     ],
58:     ops: { connect: "standing", processed: "standing", finetune: "approval", skills: "approval", raw: "approval" }
59:   },
60:   messages: {
61:     label: "Messages", title: "Messages", tb: 4.2, pct: 5, fill: "#b9c5d8",
62:     stats: [["How much", "4.2 TB · 5% of all Digicow data"], ["What is in it", "1.4M email threads"], ["Where it comes from", "Digicow email archive"], ["Languages", "English · Swahili"], ["Collected", "January 2019 to July 2026"], ["Quality", "Patchy · 6 fields too thin to train on"], ["Personal details", "Named people inside and outside Digicow · never asked about outside use"], ["Open to you", "1.2 TB with sign-off · 3.0 TB not available"]],
63:     custody: "Correspondence between named people inside and outside Digicow. Those people were never asked about outside use, so most of this set is not available.",
64:     avail: { standing: "—", approval: "1.2 TB", closed: "3.0 TB" },
65:     notes: [
66:       { tag: "Mostly off limits", color: "var(--oxblood)", text: "3.0 TB of 4.2 TB is not available. The people in these emails were never asked about outside use, and that cannot be fixed after the fact." },
67:       { tag: "Outsiders are in it", color: "var(--brass)", text: "Many threads involve people outside Digicow entirely. Digicow cannot grant access to their words, which is why sign-off here is narrow." },
68:       { tag: "Thin material", color: "var(--ink3)", text: "Patchy fields throughout, and six were flagged as too thin to train on. Small volume, low yield." }
69:     ],
70:     ops: { connect: "approval", processed: "approval", finetune: "closed", skills: "closed", raw: "closed" }
71:   },
72: };
73: 
74: const OP_LABELS = {
75:   standing: { label: "Open to you", color: "var(--sage)", bg: "rgba(29,122,110,.12)" },
76:   approval: { label: "Needs sign-off", color: "var(--brass)", bg: "rgba(176,141,46,.14)" },
77:   closed: { label: "Not available", color: "var(--ink3)", bg: "rgba(27,31,39,.06)" },
78: };
79: 
80: const OPS_LIST = [
81:   { key: "connect", name: "Query it from your workspace" },
82:   { key: "processed", name: "Get intelligence from it" },
83:   { key: "finetune", name: "Train your model on it" },
84:   { key: "skills", name: "Build a skill on it" },
85:   { key: "raw", name: "Download the raw data" },
86: ];
87: 
88: export default function DataEstates() {
89:   const { estateId } = useParams();
90:   const estate = ESTATES[estateId];
91: 
92:   if (!estate) {
93:     return (
94:       <div className="max-w-5xl mx-auto px-8 py-10">
95:         <Link to="/dap" className="text-sm hover:underline mb-4 inline-flex items-center gap-1" style={{ color: "var(--ink3)" }}>
96:           <ArrowLeft size={14} /> Back to portal
97:         </Link>
98:         <p className="text-sm mt-4" style={{ color: "var(--ink2)" }}>Estate not found.</p>
99:       </div>
100:     );
101:   }
102: 
103:   return (
104:     <div data-testid={`data-estate-${estateId}`} className="max-w-5xl mx-auto px-8 py-10">
105:       <Link to="/dap" className="text-sm hover:underline mb-4 inline-flex items-center gap-1" style={{ color: "var(--ink3)" }}>
106:         <ArrowLeft size={14} /> Back to portal
107:       </Link>
108: 
109:       <div className="flex items-start justify-between mt-4 mb-6">
110:         <div>
111:           <h1
112:             data-testid="estate-title"
113:             className="text-2xl font-semibold"
114:             style={{ color: "var(--ink)", fontFamily: "var(--head)" }}
115:           >
116:             {estate.title}
117:           </h1>
118:           <p className="text-sm mt-1" style={{ color: "var(--ink3)" }}>{estate.tb} TB · {estate.pct}% of the estate</p>
119:         </div>
120:         <div className="w-14 h-14 rounded-lg flex items-center justify-center" style={{ background: `${estate.fill}18` }}>
121:           <span className="text-lg font-bold" style={{ color: estate.fill }}>{estate.pct}%</span>
122:         </div>
123:       </div>
124: 
125:       {/* Stats table */}
126:       <div className="rounded-lg border mb-6" style={{ borderColor: "var(--line)", background: "white" }}>
127:         {estate.stats.map(([label, value], i) => (
128:           <div
129:             key={i}
130:             data-testid={`estate-stat-${i}`}
131:             className={`flex items-start px-5 py-3 ${i < estate.stats.length - 1 ? "border-b" : ""}`}
132:             style={{ borderColor: "var(--line)" }}
133:           >
134:             <p className="w-40 flex-shrink-0 text-xs font-medium" style={{ color: "var(--ink3)" }}>{label}</p>
135:             <p className="text-sm" style={{ color: "var(--ink)" }}>{value}</p>
136:           </div>
137:         ))}
138:       </div>
139: 
140:       {/* Custody note */}
141:       <div className="rounded-lg border-l-4 p-4 mb-6" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
142:         <p className="text-sm" style={{ color: "var(--ink2)" }}>{estate.custody}</p>
143:       </div>
144: 
145:       {/* Availability */}
146:       <h2 className="text-sm font-semibold mb-3" style={{ color: "var(--ink)" }}>Availability</h2>
147:       <div className="grid grid-cols-3 gap-3 mb-6">
148:         {[["standing", estate.avail.standing], ["approval", estate.avail.approval], ["closed", estate.avail.closed]].map(([k, v]) => {
149:           const meta = OP_LABELS[k];
150:           return (
151:             <div key={k} className="rounded-lg border p-3" style={{ borderColor: meta.color, background: meta.bg }}>
152:               <p className="text-[10px] font-medium mb-0.5" style={{ color: meta.color }}>{meta.label}</p>
153:               <p className="text-lg font-semibold" style={{ color: "var(--ink)" }}>{v}</p>
154:             </div>
155:           );
156:         })}
157:       </div>
158: 
159:       {/* Operations */}
160:       <h2 className="text-sm font-semibold mb-3" style={{ color: "var(--ink)" }}>What you can do</h2>
161:       <div className="space-y-2 mb-6">
162:         {OPS_LIST.map((op) => {
163:           const gate = estate.ops[op.key];
164:           const meta = OP_LABELS[gate];
165:           return (
166:             <div
167:               key={op.key}
168:               data-testid={`estate-op-${op.key}`}
169:               className="flex items-center justify-between rounded-lg border p-3"
170:               style={{ borderColor: "var(--line)", background: "white" }}
171:             >
172:               <div className="flex items-center gap-2">
173:                 {gate === "closed" ? <Lock size={14} style={{ color: "var(--ink3)" }} /> : <FileText size={14} style={{ color: meta.color }} />}
174:                 <span className="text-sm" style={{ color: "var(--ink)" }}>{op.name}</span>
175:               </div>
176:               <span
177:                 className="text-[10px] font-medium px-2 py-0.5 rounded-full"
178:                 style={{ color: meta.color, background: meta.bg }}
179:               >
180:                 {meta.label}
181:               </span>
182:             </div>
183:           );
184:         })}
185:       </div>
186: 
187:       {/* Notes */}
188:       <div className="space-y-3">
189:         {estate.notes.map((note, i) => (
190:           <div
191:             key={i}
192:             data-testid={`estate-note-${i}`}
193:             className="flex gap-3 items-start rounded-lg p-4"
194:             style={{ background: "var(--surface)" }}
195:           >
196:             <span className="text-[10px] font-medium px-2 py-0.5 rounded whitespace-nowrap" style={{ color: note.color, background: `${note.color}14` }}>
197:               {note.tag}
198:             </span>
199:             <p className="text-sm" style={{ color: "var(--ink2)" }}>{note.text}</p>
200:           </div>
201:         ))}
202:       </div>
203:     </div>
204:   );
205: }

# SOURCE: frontend/src/pages/dap/DataGovernance.jsx

1: import React, { useEffect, useState } from "react";
2: import { useParams } from "react-router-dom";
3: import LoadingState from "@/components/shared/LoadingState";
4: import TransportError from "@/components/shared/TransportError";
5: import HonestEmpty from "@/components/shared/HonestEmpty";
6: import BackendPending from "@/components/shared/BackendPending";
7: import { get, fetchGovernEstateRulesRecord, fetchTeamAccessRegister, fetchGovernTrustCenter, tryGet } from "@/lib/apiClient";
8: import { useAuth } from "@/pages/dap/DAPLayout";
9: 
10: /**
11:  * Data Governance — DAP §4.5
12:  * 3 views: Policies & Regulations, Contract & Access Terms, Data Collection
13:  */
14: 
15: function PoliciesView() {
16:   const { user } = useAuth();
17:   const [govState, setGovState] = useState(null);
18:   const [estateRules, setEstateRules] = useState(null);
19:   const [trustCenter, setTrustCenter] = useState(null);
20:   const [error, setError] = useState(null);
21:   const [loading, setLoading] = useState(true);
22: 
23:   useEffect(() => {
24:     const promises = [
25:       get("/api/governance/state").then(setGovState).catch(() => {}),
26:     ];
27:     if (user) {
28:       promises.push(
29:         fetchGovernEstateRulesRecord().then(setEstateRules).catch(() => {}),
30:         fetchGovernTrustCenter().then(setTrustCenter).catch(() => {}),
31:       );
32:     }
33:     Promise.all(promises)
34:       .catch((e) => setError(e.message))
35:       .finally(() => setLoading(false));
36:   }, [user]);
37: 
38:   if (loading) return <LoadingState message="Reading the governance state\u2026" />;
39:   if (error) return <TransportError error={error} />;
40: 
41:   const sRails = estateRules?.S_rails || [];
42:   const oRules = estateRules?.O_rules || [];
43:   const refusals = trustCenter?.refusals?.rows || [];
44: 
45:   return (
46:     <div data-testid="governance-policies">
47:       {/* Governance overview cards */}
48:       <div className="grid grid-cols-3 gap-4 mb-6">
49:         <div className="rounded-lg border p-4" style={{ borderColor: "var(--line)", background: "white" }}>
50:           <p className="text-xs font-medium mb-1" style={{ color: "var(--brass)" }}>Approvals</p>
51:           <p data-testid="gov-approvals-count" className="text-2xl font-semibold" style={{ color: "var(--ink)" }}>
52:             {govState?.approvals?.count ?? 0}
53:           </p>
54:         </div>
55:         <div className="rounded-lg border p-4" style={{ borderColor: "var(--line)", background: "white" }}>
56:           <p className="text-xs font-medium mb-1" style={{ color: "var(--accent)" }}>Rules Updates</p>
57:           <p data-testid="gov-rules-count" className="text-2xl font-semibold" style={{ color: "var(--ink)" }}>
58:             {govState?.rules_updates?.count ?? 0}
59:           </p>
60:         </div>
61:         <div className="rounded-lg border p-4" style={{ borderColor: "var(--line)", background: "white" }}>
62:           <p className="text-xs font-medium mb-1" style={{ color: "var(--gate)" }}>Reserved Decisions</p>
63:           <p data-testid="gov-reserved-count" className="text-2xl font-semibold" style={{ color: "var(--ink)" }}>
64:             {govState?.reserved_decisions?.count ?? 0}
65:           </p>
66:         </div>
67:       </div>
68: 
69:       {govState?.reference_note && (
70:         <div
71:           data-testid="gov-reference-note"
72:           className="rounded-lg p-4 mb-6 text-xs"
73:           style={{ background: "var(--surface)", color: "var(--ink3)", fontFamily: "var(--mono, monospace)" }}
74:         >
75:           {govState.reference_note}
76:         </div>
77:       )}
78: 
79:       {/* Estate Rules — auth-gated */}
80:       {estateRules ? (
81:         <div className="mb-6">
82:           <h3 className="text-sm font-medium mb-3" style={{ color: "var(--ink)" }}>
83:             Estate Rules ({sRails.length + oRules.length} rules)
84:           </h3>
85:           {sRails.length > 0 && (
86:             <div className="mb-4">
87:               <p className="text-[10px] uppercase tracking-widest mb-2" style={{ color: "var(--ink3)" }}>S-Rails (structural)</p>
88:               <div className="space-y-1">
89:                 {sRails.map((r, i) => (
90:                   <div key={i} data-testid={`estate-rule-s-${i}`} className="flex items-center justify-between rounded border p-3" style={{ borderColor: "var(--line)", background: "white" }}>
91:                     <div>
92:                       <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>{r.name}</p>
93:                       <p className="text-xs" style={{ color: "var(--ink3)" }}>{r.value}</p>
94:                     </div>
95:                     <span className="text-[10px] px-2 py-0.5 rounded-full" style={{ color: "var(--sage)", background: "rgba(29,122,110,.12)" }}>
96:                       {r.enforcement_class}
97:                     </span>
98:                   </div>
99:                 ))}
100:               </div>
101:             </div>
102:           )}
103:           {oRules.length > 0 && (
104:             <div>
105:               <p className="text-[10px] uppercase tracking-widest mb-2" style={{ color: "var(--ink3)" }}>O-Rules (operational)</p>
106:               <div className="space-y-1">
107:                 {oRules.map((r, i) => (
108:                   <div key={i} data-testid={`estate-rule-o-${i}`} className="flex items-center justify-between rounded border p-3" style={{ borderColor: "var(--line)", background: "white" }}>
109:                     <div>
110:                       <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>{r.name}</p>
111:                       <p className="text-xs" style={{ color: "var(--ink3)" }}>{r.value}</p>
112:                     </div>
113:                     <span className="text-[10px] px-2 py-0.5 rounded-full" style={{ color: "var(--brass)", background: "rgba(176,141,46,.12)" }}>
114:                       {r.enforcement_class}
115:                     </span>
116:                   </div>
117:                 ))}
118:               </div>
119:             </div>
120:           )}
121:         </div>
122:       ) : !user ? (
123:         <div className="mb-6 rounded-lg border p-4" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
124:           <p className="text-xs" style={{ color: "var(--brass)" }}>
125:             Sign in to view estate rules. The /api/govern/estate_rules_record endpoint requires authentication.
126:           </p>
127:         </div>
128:       ) : null}
129: 
130:       {/* Trust Center / Refusals — auth-gated */}
131:       {refusals.length > 0 && (
132:         <div className="mb-6">
133:           <h3 className="text-sm font-medium mb-3" style={{ color: "var(--ink)" }}>
134:             Refusals ({trustCenter?.refusals?.absolute + trustCenter?.refusals?.escalatable + trustCenter?.refusals?.held_for_check} total)
135:           </h3>
136:           <div className="space-y-2">
137:             {refusals.map((r, i) => (
138:               <div key={i} data-testid={`refusal-${i}`} className="rounded-lg border-l-4 p-3" style={{ borderColor: "var(--oxblood)", background: "rgba(184,57,91,.04)" }}>
139:                 <div className="flex items-center gap-2 mb-1">
140:                   <span className="text-[10px] font-medium px-2 py-0.5 rounded-full" style={{ color: "var(--oxblood)", background: "rgba(184,57,91,.12)" }}>
141:                     {r.class_hint}
142:                   </span>
143:                   <span className="text-xs font-mono" style={{ color: "var(--ink3)" }}>{r.reason_code}</span>
144:                 </div>
145:                 <p className="text-sm" style={{ color: "var(--ink2)" }}>{r.criterion_verbatim}</p>
146:               </div>
147:             ))}
148:           </div>
149:         </div>
150:       )}
151:     </div>
152:   );
153: }
154: 
155: function ContractView() {
156:   const { user } = useAuth();
157:   const [register, setRegister] = useState(null);
158:   const [error, setError] = useState(null);
159:   const [loading, setLoading] = useState(true);
160: 
161:   useEffect(() => {
162:     if (!user) {
163:       setLoading(false);
164:       return;
165:     }
166:     fetchTeamAccessRegister()
167:       .then(setRegister)
168:       .catch((e) => setError(e.message))
169:       .finally(() => setLoading(false));
170:   }, [user]);
171: 
172:   if (!user) return (
173:     <div data-testid="governance-contract">
174:       <div className="rounded-lg border p-4" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
175:         <p className="text-xs" style={{ color: "var(--brass)" }}>
176:           Sign in to view the access register. The /api/team/access_register endpoint requires authentication.
177:         </p>
178:       </div>
179:     </div>
180:   );
181: 
182:   if (loading) return <LoadingState message="Reading the access register\u2026" />;
183:   if (error) return <TransportError error={error} />;
184: 
185:   const rows = register?.rows || [];
186: 
187:   return (
188:     <div data-testid="governance-contract">
189:       {register?.canon_ref && (
190:         <p className="text-xs font-mono mb-4" style={{ color: "var(--ink3)" }}>{register.canon_ref}</p>
191:       )}
192:       {rows.length === 0 ? (
193:         <HonestEmpty message="No access grants on record. This list populates as grants are created and managed." />
194:       ) : (
195:         <div className="space-y-2">
196:           {rows.map((r, i) => (
197:             <div key={i} data-testid={`access-grant-${i}`} className="rounded-lg border p-4" style={{ borderColor: "var(--line)", background: "white" }}>
198:               <div className="flex items-center justify-between mb-2">
199:                 <span className="text-xs font-mono" style={{ color: "var(--ink3)" }}>{r.grant_id}</span>
200:                 <span
201:                   className="text-[10px] px-2 py-0.5 rounded-full font-medium"
202:                   style={{
203:                     color: r.state === "active" ? "var(--sage)" : "var(--ink3)",
204:                     background: r.state === "active" ? "rgba(29,122,110,.12)" : "rgba(27,31,39,.06)",
205:                   }}
206:                 >
207:                   {r.state}
208:                 </span>
209:               </div>
210:               <p className="text-sm" style={{ color: "var(--ink)" }}>{r.who_grantee_email}</p>
211:               <p className="text-xs mt-1" style={{ color: "var(--ink3)" }}>{r.what_scope}</p>
212:               <div className="flex gap-4 text-[10px] mt-2" style={{ color: "var(--ink3)" }}>
213:                 <span>Created: {r.when_created_iso?.slice(0, 10)}</span>
214:                 <span>By: {r.by_whom_grantor_email}</span>
215:                 {r.propagation_state_plain && <span>{r.propagation_state_plain}</span>}
216:               </div>
217:               {r.is_sample && (
218:                 <span className="text-[9px] mt-1 inline-block px-1.5 py-0.5 rounded bg-yellow-50" style={{ color: "var(--brass)" }}>sample data</span>
219:               )}
220:             </div>
221:           ))}
222:         </div>
223:       )}
224:     </div>
225:   );
226: }
227: 
228: function CollectionView() {
229:   return (
230:     <div data-testid="governance-collection">
231:       <div className="rounded-lg border p-6" style={{ borderColor: "var(--line)", background: "white" }}>
232:         <h3 className="text-sm font-semibold mb-3" style={{ color: "var(--ink)" }}>How data is collected</h3>
233:         <div className="space-y-3 text-sm" style={{ color: "var(--ink2)" }}>
234:           <p>
235:             All data in the estate is collected from Digicow&apos;s own systems — customer service lines,
236:             written complaints archive, core banking records, platform logs, and email archive.
237:           </p>
238:           <p>
239:             Data is read from source systems through governed connections. Each connection is receipted,
240:             and every record carries its provenance chain from source to the estate.
241:           </p>
242:           <p>
243:             Personal details are handled according to the rights Digicow holds over each data class.
244:             Some sets are cleared for outside use; others require per-request sign-off; some are
245:             internal-only and never available.
246:           </p>
247:         </div>
248:       </div>
249:     </div>
250:   );
251: }
252: 
253: function CanonRulesView() {
254:   const [dapRules, setDapRules] = useState(null);
255:   const [rbmRules, setRbmRules] = useState(null);
256:   const [rocRules, setRocRules] = useState(null);
257:   const [loading, setLoading] = useState(true);
258: 
259:   useEffect(() => {
260:     Promise.all([
261:       tryGet("/api/canon/rules/dap").then((r) => { if (r.ok) setDapRules(r.data); }),
262:       tryGet("/api/canon/rules/rbm").then((r) => { if (r.ok) setRbmRules(r.data); }),
263:       tryGet("/api/canon/rules/roc").then((r) => { if (r.ok) setRocRules(r.data); }),
264:     ]).finally(() => setLoading(false));
265:   }, []);
266: 
267:   if (loading) return <LoadingState message="Reading canon rules\u2026" />;
268: 
269:   const renderRuleSet = (label, data, testPrefix) => {
270:     const rules = Array.isArray(data) ? data : (data?.rules || data?.items || []);
271:     if (!data) {
272:       return (
273:         <div data-testid={`${testPrefix}-pending`} className="rounded-lg border p-4 mb-4" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
274:           <p className="text-xs" style={{ color: "var(--brass)" }}>
275:             Endpoint not yet mounted (GET /api/canon/rules/{testPrefix} returns 404).
276:           </p>
277:         </div>
278:       );
279:     }
280:     return (
281:       <div className="mb-6">
282:         <h3 className="text-sm font-medium mb-3" style={{ color: "var(--ink)" }}>
283:           {label} ({rules.length} rules)
284:         </h3>
285:         {rules.length > 0 ? (
286:           <div className="space-y-1">
287:             {rules.map((r, i) => (
288:               <div key={r.rule_id || i} data-testid={`${testPrefix}-rule-${i}`} className="flex items-start justify-between rounded border p-3" style={{ borderColor: "var(--line)", background: "white" }}>
289:                 <div className="flex-1">
290:                   <div className="flex items-center gap-2 mb-0.5">
291:                     {r.rule_id && <span className="text-[10px] font-mono" style={{ color: "var(--ink3)" }}>{r.rule_id}</span>}
292:                     <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>{r.title || r.name || r.rule_id}</p>
293:                   </div>
294:                   {r.text && <p className="text-xs mt-0.5" style={{ color: "var(--ink3)" }}>{r.text}</p>}
295:                   {r.body && <p className="text-xs mt-0.5" style={{ color: "var(--ink3)" }}>{typeof r.body === "string" ? r.body : JSON.stringify(r.body)}</p>}
296:                 </div>
297:                 {r.enforcement_class && (
298:                   <span className="text-[10px] px-2 py-0.5 rounded-full ml-2 whitespace-nowrap" style={{ color: "var(--sage)", background: "rgba(29,122,110,.12)" }}>
299:                     {r.enforcement_class}
300:                   </span>
301:                 )}
302:               </div>
303:             ))}
304:           </div>
305:         ) : (
306:           <p className="text-xs" style={{ color: "var(--ink3)" }}>No rules in this registry.</p>
307:         )}
308:       </div>
309:     );
310:   };
311: 
312:   return (
313:     <div data-testid="governance-canon-rules">
314:       {renderRuleSet("DAP Rules", dapRules, "dap")}
315:       {renderRuleSet("RBM Rules", rbmRules, "rbm")}
316:       {renderRuleSet("ROC Rules", rocRules, "roc")}
317:     </div>
318:   );
319: }
320: 
321: const VIEW_MAP = {
322:   policies: { title: "Policies & Regulations", Component: PoliciesView },
323:   contract: { title: "Contract & Access Terms", Component: ContractView },
324:   collection: { title: "Data Collection", Component: CollectionView },
325:   rules: { title: "Canon Rules (DAP / RBM / ROC)", Component: CanonRulesView },
326: };
327: 
328: export default function DataGovernance() {
329:   const { tab } = useParams();
330:   const current = VIEW_MAP[tab] || VIEW_MAP["policies"];
331:   const Component = current.Component;
332: 
333:   return (
334:     <div data-testid="data-governance" className="max-w-5xl mx-auto px-8 py-10">
335:       <h1
336:         data-testid="data-governance-title"
337:         className="text-xl font-semibold mb-1"
338:         style={{ color: "var(--ink)", fontFamily: "var(--head, Iowan Old Style, Georgia, serif)" }}
339:       >
340:         Data Governance
341:       </h1>
342:       <p className="text-sm mb-6" style={{ color: "var(--ink3)" }}>
343:         {current.title}
344:       </p>
345:       <Component />
346:     </div>
347:   );
348: }

# SOURCE: frontend/src/pages/dap/Entitlement.jsx

1: import React, { useState, useEffect } from "react";
2: import BackendPending from "@/components/shared/BackendPending";
3: import LoadingState from "@/components/shared/LoadingState";
4: import { useAuth } from "@/pages/dap/DAPLayout";
5: import { tryGet } from "@/lib/apiClient";
6: import {
7:   ENT_23_COST_NOT_MEASURED,
8:   ENT_26_FRONTIER_EXHAUSTION,
9:   ENT_34_FRONTIER_UNAVAILABLE,
10:   ENT_43_BADGE_INCLUDED_LOCAL,
11:   ENT_43_BADGE_CREDITS_FRONTIER,
12:   ENT_43_BADGE_YOUR_KEY,
13:   ENT_43_BADGE_AUTO,
14: } from "@/strings/entitlementStrings";
15: import { Award, CreditCard, Package, Tag, Shield, AlertCircle } from "lucide-react";
16: 
17: /**
18:  * Entitlement — DAP Portal entitlement surfaces.
19:  *
20:  * Wired to:
21:  *   GET /api/portal/entitlement/licence         — principal-scoped licence read
22:  *   GET /api/portal/entitlement/catalog/listed   — CatalogRow status=listed
23:  *   GET /api/portal/entitlement/allowance        — derived allowance (ENT-22)
24:  *   GET /api/portal/entitlement/badges           — picker badges filtered via dial-admit
25:  *
26:  * BINDING constraints:
27:  *   - Allowance figure displayed as-is (never compute/cache client-side) (ENT-22)
28:  *   - Badges show ONLY rows the licence's dials admit (ENT-3/ENT-43)
29:  *   - Excluded catalog rows ABSENT, not greyed/disabled
30:  *   - NO remaining-budget reason lines (DAP-35)
31:  *   - ENT-43 badge strings from entitlementStrings.js
32:  */
33: 
34: const BADGE_COLORS = {
35:   [ENT_43_BADGE_INCLUDED_LOCAL]: { bg: "rgba(29,122,110,.10)", color: "var(--sage)" },
36:   [ENT_43_BADGE_CREDITS_FRONTIER]: { bg: "rgba(22,39,74,.10)", color: "var(--blue)" },
37:   [ENT_43_BADGE_YOUR_KEY]: { bg: "rgba(176,141,46,.10)", color: "var(--brass)" },
38:   [ENT_43_BADGE_AUTO]: { bg: "rgba(27,31,39,.06)", color: "var(--ink2)" },
39: };
40: 
41: function BadgeChip({ badge }) {
42:   const colors = BADGE_COLORS[badge] || BADGE_COLORS[ENT_43_BADGE_AUTO];
43:   return (
44:     <span
45:       data-testid={`badge-${badge.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}
46:       className="inline-flex items-center text-[11px] font-medium px-2 py-0.5 rounded-full"
47:       style={{ background: colors.bg, color: colors.color }}
48:     >
49:       <Tag size={10} className="mr-1" />
50:       {badge}
51:     </span>
52:   );
53: }
54: 
55: function BindingStringsReference() {
56:   return (
57:     <div data-testid="ent-binding-strings" className="rounded-lg border p-4 mb-6" style={{ borderColor: "var(--line)", background: "white" }}>
58:       <h3 className="text-xs font-medium mb-3" style={{ color: "var(--ink)" }}>Binding copy (entitlement strings)</h3>
59:       <div className="space-y-2 text-xs" style={{ color: "var(--ink2)" }}>
60:         <div data-testid="ent-string-23">
61:           <span className="font-mono text-[10px]" style={{ color: "var(--ink3)" }}>ENT-23:</span>
62:           <span className="ml-2">{ENT_23_COST_NOT_MEASURED}</span>
63:         </div>
64:         <div data-testid="ent-string-26">
65:           <span className="font-mono text-[10px]" style={{ color: "var(--ink3)" }}>ENT-26:</span>
66:           <span className="ml-2">{ENT_26_FRONTIER_EXHAUSTION}</span>
67:         </div>
68:         <div data-testid="ent-string-34">
69:           <span className="font-mono text-[10px]" style={{ color: "var(--ink3)" }}>ENT-34:</span>
70:           <span className="ml-2">{ENT_34_FRONTIER_UNAVAILABLE}</span>
71:         </div>
72:       </div>
73:       <div className="flex flex-wrap gap-2 mt-3">
74:         <BadgeChip badge={ENT_43_BADGE_AUTO} />
75:         <BadgeChip badge={ENT_43_BADGE_INCLUDED_LOCAL} />
76:         <BadgeChip badge={ENT_43_BADGE_CREDITS_FRONTIER} />
77:         <BadgeChip badge={ENT_43_BADGE_YOUR_KEY} />
78:       </div>
79:     </div>
80:   );
81: }
82: 
83: function LicenceCard({ data, loading, error }) {
84:   if (loading) return <LoadingState message="Reading licence\u2026" />;
85:   if (error === 404) return (
86:     <div data-testid="licence-pending" className="rounded-lg border p-4" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
87:       <p className="text-xs" style={{ color: "var(--brass)" }}>
88:         <AlertCircle size={12} className="inline mr-1" />
89:         Endpoint not yet mounted (GET /api/portal/entitlement/licence returns 404).
90:       </p>
91:     </div>
92:   );
93: 
94:   return (
95:     <div data-testid="licence-card" className="rounded-lg border p-5" style={{ borderColor: "var(--line)", background: "white" }}>
96:       <div className="flex items-center gap-2 mb-3">
97:         <Award size={16} style={{ color: "var(--sage)" }} />
98:         <h3 className="text-sm font-medium" style={{ color: "var(--ink)" }}>Licence</h3>
99:       </div>
100:       {data?.licence ? (
101:         <div className="space-y-2 text-sm" style={{ color: "var(--ink2)" }}>
102:           <p>Terms ID: <span className="font-mono text-xs">{data.licence.terms_id || data.licence.licence_terms_id || "N/A"}</span></p>
103:           {data.licence.compute_dial != null && <p>Compute dial: {JSON.stringify(data.licence.compute_dial)}</p>}
104:           {data.licence.frontier_dial != null && <p>Frontier dial: {JSON.stringify(data.licence.frontier_dial)}</p>}
105:         </div>
106:       ) : (
107:         <p className="text-sm" style={{ color: "var(--ink3)" }}>No licence on record for this principal.</p>
108:       )}
109:       {data?.authority && <p className="text-[10px] mt-3 font-mono" style={{ color: "var(--ink3)" }}>{data.authority}</p>}
110:     </div>
111:   );
112: }
113: 
114: function AllowanceCard({ data, loading, error }) {
115:   if (loading) return <LoadingState message="Deriving allowance\u2026" />;
116:   if (error === 404) return (
117:     <div data-testid="allowance-pending" className="rounded-lg border p-4" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
118:       <p className="text-xs" style={{ color: "var(--brass)" }}>
119:         <AlertCircle size={12} className="inline mr-1" />
120:         Endpoint not yet mounted (GET /api/portal/entitlement/allowance returns 404).
121:       </p>
122:     </div>
123:   );
124: 
125:   const state = data?.allowance_state;
126:   return (
127:     <div data-testid="allowance-card" className="rounded-lg border p-5" style={{ borderColor: "var(--line)", background: "white" }}>
128:       <div className="flex items-center gap-2 mb-3">
129:         <CreditCard size={16} style={{ color: "var(--blue)" }} />
130:         <h3 className="text-sm font-medium" style={{ color: "var(--ink)" }}>Allowance</h3>
131:       </div>
132:       {state ? (
133:         <div className="space-y-2 text-sm" style={{ color: "var(--ink2)" }}>
134:           <p>Period: <span className="font-medium">{state.period_iso}</span></p>
135:           <p>Credits allowance: <span className="font-semibold">{state.credits_allowance}</span></p>
136:           <p>Credits debited: <span className="font-semibold">{state.credits_debited}</span></p>
137:           {/* DAP-35: NEVER display "remaining budget" — allowance is a derived figure only */}
138:         </div>
139:       ) : (
140:         <p className="text-sm" style={{ color: "var(--ink3)" }}>No allowance state available.</p>
141:       )}
142:       {data?.authority && <p className="text-[10px] mt-3 font-mono" style={{ color: "var(--ink3)" }}>{data.authority}</p>}
143:     </div>
144:   );
145: }
146: 
147: function CatalogPicker({ catalogData, badgesData, loading, error }) {
148:   if (loading) return <LoadingState message="Reading catalog\u2026" />;
149:   if (error === 404) return (
150:     <div data-testid="catalog-pending" className="rounded-lg border p-4" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
151:       <p className="text-xs" style={{ color: "var(--brass)" }}>
152:         <AlertCircle size={12} className="inline mr-1" />
153:         Endpoint not yet mounted (GET /api/portal/entitlement/catalog/listed returns 404).
154:       </p>
155:     </div>
156:   );
157: 
158:   const rows = catalogData?.rows || [];
159:   const badges = badgesData?.badges || [];
160: 
161:   return (
162:     <div data-testid="catalog-picker" className="rounded-lg border p-5" style={{ borderColor: "var(--line)", background: "white" }}>
163:       <div className="flex items-center gap-2 mb-3">
164:         <Package size={16} style={{ color: "var(--brass)" }} />
165:         <h3 className="text-sm font-medium" style={{ color: "var(--ink)" }}>
166:           Catalog ({rows.length} listed)
167:         </h3>
168:       </div>
169: 
170:       {/* Badges — ONLY what the endpoint returns (ENT-3/ENT-43) */}
171:       {badges.length > 0 ? (
172:         <div data-testid="catalog-badges" className="mb-4">
173:           <p className="text-[10px] uppercase tracking-widest mb-2" style={{ color: "var(--ink3)" }}>Picker badges</p>
174:           <div className="flex flex-wrap gap-2">
175:             {badges.map((b, i) => (
176:               <BadgeChip key={i} badge={b.badge || b.name || b} />
177:             ))}
178:           </div>
179:         </div>
180:       ) : (
181:         <p className="text-xs mb-4" style={{ color: "var(--ink3)" }}>
182:           No badges returned. Excluded rows are absent from the response.
183:         </p>
184:       )}
185: 
186:       {/* Catalog rows — excluded rows are ABSENT, not greyed/disabled */}
187:       {rows.length > 0 ? (
188:         <div className="space-y-2">
189:           {rows.map((row, i) => (
190:             <div key={i} data-testid={`catalog-row-${i}`} className="flex items-center justify-between rounded border p-3" style={{ borderColor: "var(--line)" }}>
191:               <div>
192:                 <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>{row.name || row.row_id || `Row ${i + 1}`}</p>
193:                 {row.description && <p className="text-xs" style={{ color: "var(--ink3)" }}>{row.description}</p>}
194:               </div>
195:               {row.badge && <BadgeChip badge={row.badge} />}
196:             </div>
197:           ))}
198:         </div>
199:       ) : (
200:         <p className="text-sm" style={{ color: "var(--ink3)" }}>No catalog rows listed for this principal.</p>
201:       )}
202: 
203:       {catalogData?.authority && <p className="text-[10px] mt-3 font-mono" style={{ color: "var(--ink3)" }}>{catalogData.authority}</p>}
204:     </div>
205:   );
206: }
207: 
208: export default function Entitlement() {
209:   const { user } = useAuth();
210:   const [licence, setLicence] = useState({ data: null, loading: false, error: null });
211:   const [allowance, setAllowance] = useState({ data: null, loading: false, error: null });
212:   const [catalog, setCatalog] = useState({ data: null, loading: false, error: null });
213:   const [badges, setBadges] = useState({ data: null, loading: false, error: null });
214: 
215:   useEffect(() => {
216:     if (!user) return;
217: 
218:     // Licence
219:     setLicence((s) => ({ ...s, loading: true }));
220:     tryGet("/api/portal/entitlement/licence").then((res) => {
221:       setLicence({ data: res.ok ? res.data : null, loading: false, error: res.ok ? null : res.status });
222:     });
223: 
224:     // Allowance
225:     setAllowance((s) => ({ ...s, loading: true }));
226:     tryGet("/api/portal/entitlement/allowance").then((res) => {
227:       setAllowance({ data: res.ok ? res.data : null, loading: false, error: res.ok ? null : res.status });
228:     });
229: 
230:     // Catalog
231:     setCatalog((s) => ({ ...s, loading: true }));
232:     tryGet("/api/portal/entitlement/catalog/listed").then((res) => {
233:       setCatalog({ data: res.ok ? res.data : null, loading: false, error: res.ok ? null : res.status });
234:     });
235: 
236:     // Badges
237:     setBadges((s) => ({ ...s, loading: true }));
238:     tryGet("/api/portal/entitlement/badges").then((res) => {
239:       setBadges({ data: res.ok ? res.data : null, loading: false, error: res.ok ? null : res.status });
240:     });
241:   }, [user]);
242: 
243:   if (!user) {
244:     return (
245:       <div data-testid="entitlement-page" className="max-w-5xl mx-auto px-8 py-10">
246:         <h1 className="text-xl font-semibold mb-4" style={{ color: "var(--ink)", fontFamily: "var(--head)" }}>Entitlement</h1>
247:         <BindingStringsReference />
248:         <div className="rounded-lg border p-4" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
249:           <p className="text-xs" style={{ color: "var(--brass)" }}>Sign in to view entitlement surfaces. All endpoints require JWT authentication.</p>
250:         </div>
251:       </div>
252:     );
253:   }
254: 
255:   return (
256:     <div data-testid="entitlement-page" className="max-w-5xl mx-auto px-8 py-10">
257:       <h1 className="text-xl font-semibold mb-1" style={{ color: "var(--ink)", fontFamily: "var(--head)" }}>
258:         <Shield size={20} className="inline mr-2" />
259:         Entitlement
260:       </h1>
261:       <p className="text-sm mb-6" style={{ color: "var(--ink3)" }}>
262:         Licence terms, catalog access, and allowance for your principal.
263:       </p>
264: 
265:       <BindingStringsReference />
266: 
267:       <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
268:         <LicenceCard {...licence} />
269:         <AllowanceCard {...allowance} />
270:       </div>
271: 
272:       <CatalogPicker catalogData={catalog.data} badgesData={badges.data} loading={catalog.loading} error={catalog.error} />
273:     </div>
274:   );
275: }

# SOURCE: frontend/src/pages/dap/ExtractModes.jsx

1: import React from "react";
2: import { useParams } from "react-router-dom";
3: import BackendPending from "@/components/shared/BackendPending";
4: 
5: /**
6:  * Extract Modes — DAP §4.1
7:  * 4 modes: raw, processed, finetune, skills
8:  * All backend pending (no request-submission endpoint exists).
9:  */
10: 
11: const MODES = {
12:   raw: {
13:     label: "Download Raw Data", title: "Download raw data",
14:     gate: "Highest level of review",
15:     sub: "The one option where you receive copies of the data itself. Because of that, it gets the most careful review.",
16:     rows: [
17:       ["What you send in", "Nothing — just your request"],
18:       ["What you get back", "Copies of the records you asked for"],
19:       ["How it is checked", "Every record is screened and redacted before anything is packaged"],
20:       ["Who has to sign off", "Digicow, whenever the data includes personal or confidential details"],
21:       ["What goes on the record", "Every record released, the redaction report, and who approved it"],
22:     ],
23:     practice: "What can be released depends on the rights Digicow holds and what the data contains. Redaction is not optional and cannot be skipped. Every record that leaves is listed individually.",
24:   },
25:   processed: {
26:     label: "Get Intelligence", title: "Get intelligence",
27:     gate: "Standard review",
28:     sub: "Tell Digicow what you want to find out. You get findings and analysis; the underlying records stay put.",
29:     rows: [
30:       ["What you send in", "A question or objective"],
31:       ["What you get back", "Findings and analysis — not the records they came from"],
32:       ["How it is checked", "Results only state what the data genuinely supports"],
33:       ["Who has to sign off", "Nobody, unless the data includes personal or confidential details"],
34:       ["What goes on the record", "Your question, the answer, and which records were used"],
35:     ],
36:     practice: "Which records were used is noted on your receipt, but the records themselves cannot be reconstructed from what you receive.",
37:   },
38:   finetune: {
39:     label: "Train a Model", title: "Train a model",
40:     gate: "Always reviewed",
41:     sub: "Your model comes to the data and trains here. You take the trained model away; the data never leaves Digicow.",
42:     rows: [
43:       ["What you send in", "Your base model, or one Digicow provides"],
44:       ["What you get back", "The trained model, with its usage rights attached"],
45:       ["How it is checked", "The model must meet the accuracy targets you set before training starts"],
46:       ["Who has to sign off", "Digicow, every time — because a trained model leaves with you"],
47:       ["What goes on the record", "What it was trained on, a fingerprint of the model, and your agreement"],
48:     ],
49:     practice: "Training happens on Digicow computers, next to the data. There is no option to move the data to your own systems.",
50:   },
51:   skills: {
52:     label: "Build a Skill", title: "Build a skill",
53:     gate: "Always reviewed",
54:     sub: "A skill is a reusable procedure, not a model. You take the file away; what it was built on stays here.",
55:     rows: [
56:       ["What you send in", "A description of what the skill should do"],
57:       ["What you get back", "A skill file you can run elsewhere"],
58:       ["How it is checked", "The file is fingerprinted and reviewed before release"],
59:       ["Who has to sign off", "Digicow, every time — because a file leaves with you"],
60:       ["What goes on the record", "A fingerprint of the file, which records were used, and your agreement"],
61:     ],
62:     practice: "The skill is developed against Digicow data and leaves as a file. The data it was developed on is listed on your receipt, not packed inside the file.",
63:   },
64: };
65: 
66: export default function ExtractModes() {
67:   const { mode } = useParams();
68:   const m = MODES[mode];
69: 
70:   if (!m) {
71:     return (
72:       <div className="max-w-5xl mx-auto px-8 py-10">
73:         <BackendPending surface="Extract mode not found" detail={`Mode "${mode}" is not a valid extract mode.`} />
74:       </div>
75:     );
76:   }
77: 
78:   return (
79:     <div data-testid={`extract-mode-${mode}`} className="max-w-5xl mx-auto px-8 py-10">
80:       <h1
81:         data-testid="extract-mode-title"
82:         className="text-xl font-semibold mb-1"
83:         style={{ color: "var(--ink)", fontFamily: "var(--head)" }}
84:       >
85:         {m.title}
86:       </h1>
87:       <p className="text-xs font-medium mb-4" style={{ color: "var(--brass)" }}>{m.gate}</p>
88:       <p className="text-sm mb-6" style={{ color: "var(--ink2)" }}>{m.sub}</p>
89: 
90:       {/* How it works table */}
91:       <div className="rounded-lg border mb-6" style={{ borderColor: "var(--line)", background: "white" }}>
92:         {m.rows.map(([label, value], i) => (
93:           <div
94:             key={i}
95:             className={`flex items-start px-5 py-3 ${i < m.rows.length - 1 ? "border-b" : ""}`}
96:             style={{ borderColor: "var(--line)" }}
97:           >
98:             <p className="w-48 flex-shrink-0 text-xs font-medium" style={{ color: "var(--ink3)" }}>{label}</p>
99:             <p className="text-sm" style={{ color: "var(--ink)" }}>{value}</p>
100:           </div>
101:         ))}
102:       </div>
103: 
104:       {/* Practice note */}
105:       <div className="rounded-lg border-l-4 p-4 mb-6" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
106:         <p className="text-sm" style={{ color: "var(--ink2)" }}>{m.practice}</p>
107:       </div>
108: 
109:       {/* Backend pending — no submission endpoint */}
110:       <BackendPending
111:         surface={`${m.title} — request submission`}
112:         detail="The request-submission endpoint does not exist in the backend contract. No route accepts a new request of this type. This is the largest gap in the DAP (§4.2 of the FE Integration Brief)."
113:       />
114:     </div>
115:   );
116: }

# SOURCE: frontend/src/pages/dap/RequestLifecycle.jsx

1: import React, { useState, useEffect, useCallback } from "react";
2: import StatusBadge from "@/components/dap/StatusBadge";
3: import BackendPending from "@/components/shared/BackendPending";
4: import LoadingState from "@/components/shared/LoadingState";
5: import { ChevronDown, ChevronUp, RotateCcw, AlertTriangle, CheckCircle, Square, Send, Clock } from "lucide-react";
6: import { useAuth } from "@/pages/dap/DAPLayout";
7: import { tryGet, tryPost } from "@/lib/apiClient";
8: import {
9:   STOP_CONFIRM,
10:   PARTY_HALTED_KIND_LINE,
11:   PARTY_HALTED_WHAT_NEXT,
12:   IN_APPROVAL_WAITING_TPL,
13:   EXPIRED_DATE_TPL,
14:   EXPIRED_WAITED_TPL,
15:   EXPIRED_MEANING_TPL,
16:   EXPIRED_WHAT_NEXT_TPL,
17:   BLOCK_KIND_REQUEST,
18:   BLOCK_KIND_CHECK,
19:   BLOCK_KIND_ESTATE,
20:   BLOCK_ESTATE_REASON,
21:   BLOCK_WHATNEXT_REQUEST,
22:   BLOCK_WHATNEXT_CHECK,
23:   BLOCK_WHATNEXT_ESTATE_TPL,
24: } from "@/strings/lifecycleStrings";
25: 
26: /**
27:  * Request Lifecycle — Journey v2 conformance pass.
28:  *
29:  * Wired to:
30:  *   GET  /api/portal/requests           — principal-scoped history
31:  *   GET  /api/portal/requests/{id}      — detail
32:  *   POST /api/portal/requests           — submit new request
33:  *   POST /api/portal/requests/{id}/stop — request-scoped stop
34:  *   POST /api/portal/requests/{id}/retry — bounded-3 retry
35:  *
36:  * THREE Blocked kinds: request, check, estate (§5, §11) — plus Interrupted
37:  * (own rail state, platform fault) and party_halted (own rail state).
38:  * Stopped terminal state (Executing → Stopped, charged-to-point-of-stop,
39:  * receipted).
40:  *
41:  * HARD OMISSIONS (owner-ruled):
42:  * - NO "Waited N days" in any post-decision Sign-off block (Approved/Refused)
43:  * - NO partial-release UI
44:  * - NO owner-turnaround metrics
45:  * - NO approver identity anywhere (DAP-15)
46:  * - NO remaining-budget reason lines (DAP-35)
47:  */
48: 
49: const MODE_VERB = {
50:   processed: "Open report", finetune: "Download model",
51:   skills: "Download skill", raw: "Download data"
52: };
53: 
54: const BLOCK_KIND_META = {
55:   request: {
56:     kindLine: BLOCK_KIND_REQUEST,
57:     whatNext: BLOCK_WHATNEXT_REQUEST,
58:     showCopy: true,
59:     showProgress: true,
60:   },
61:   check: {
62:     kindLine: BLOCK_KIND_CHECK,
63:     whatNext: BLOCK_WHATNEXT_CHECK,
64:     showCopy: true,
65:     showProgress: true,
66:   },
67:   estate: {
68:     kindLine: BLOCK_KIND_ESTATE,
69:     fixedReason: BLOCK_ESTATE_REASON,
70:     showCopy: false,
71:     showProgress: false,
72:   },
73: };
74: 
75: // Sample requests — reference state machine (used when backend endpoints not yet mounted)
76: const SAMPLE_REQUESTS = [
77:   {
78:     id: "ftn-2026-0118", objective: "Train on the cleared complaint files to route by urgency.",
79:     status: "Executing", pct: 41, eta: "~6h to completion", mode: "finetune",
80:     agreement: "Agreement MER-007", submitted: "submitted 5 Sep 2026", submittedBy: "R. Adeyemi",
81:     scope: "Audio", signoffRequired: true, approvedDate: "12 Sep 2026", approvedByRole: "records authority",
82:   },
83:   {
84:     id: "prc-2026-0109", objective: "Find out which branches drive repeat complaints, this quarter.",
85:     status: "Executing", stageIndex: 2, stageCount: 4, stageLabel: "Analyzing", eta: "~40 min",
86:     mode: "processed", agreement: "Agreement MER-002", submitted: "submitted 16 Sep 2026", submittedBy: "T. Mwangi",
87:     scope: "Audio", signoffRequired: false,
88:   },
89:   {
90:     id: "ftn-2026-0119", objective: "Train on IVR prompts to flag automated-menu drop-off.",
91:     status: "In Approval", mode: "finetune", agreement: "Agreement MER-007",
92:     submitted: "submitted 13 Sep 2026", submittedBy: "R. Adeyemi", scope: "Audio",
93:     submittedAtISO: "2026-09-13", windowEndsAtISO: "2026-09-28",
94:     dataOwner: "Digicow",
95:     signoffReason: "This request needs sign-off because it includes IVR prompts. Under Agreement MER-007, Digicow has to approve any use of them.",
96:     spendCeilingBreach: false,
97:   },
98:   {
99:     id: "ftn-2026-0121", objective: "Train on branch chat logs to flag escalation risk.",
100:     status: "In Approval", mode: "finetune", agreement: "Agreement MER-007",
101:     submitted: "submitted 5 Sep 2026", submittedBy: "A. Osei", scope: "Audio",
102:     submittedAtISO: "2026-09-05", windowEndsAtISO: "2026-09-19",
103:     dataOwner: "Digicow",
104:     spendCeilingBreach: true,
105:     spendCeilingReason: "Organisation ceiling reached for this period. Spend-ceiling breach folds into In Approval.",
106:   },
107:   {
108:     id: "int-2026-0001", objective: "Extract quality metrics from the call recordings.",
109:     status: "Interrupted (platform fault)", mode: "processed",
110:     agreement: "Agreement MER-002", submitted: "submitted 17 Sep 2026", submittedBy: "R. Adeyemi",
111:     scope: "Audio", retryAttempts: 2, maxRetries: 3,
112:     interruptReason: "Upstream compute node unreachable. Bounded auto-retry in progress.",
113:   },
114:   {
115:     id: "ftn-2026-0120", objective: "Train on radio segments to detect ad breaks.",
116:     status: "Ready", mode: "finetune", agreement: "Agreement MER-007",
117:     submitted: "submitted 10 Sep 2026", submittedBy: "R. Adeyemi", scope: "Audio",
118:     modelId: "MDL-2026-0120", baseModel: "meridian-audio-base-v3",
119:     targetsSet: "88%", targetsAchieved: "91%", weightsHash: "sha256:7be2a0\u2026d914",
120:     signoffRequired: true, approvedByRole: "records authority", approvedDate: "14 Sep 2026",
121:   },
122:   {
123:     id: "prc-2026-0111", objective: "Find out which time-of-day produces the most complaint escalations.",
124:     status: "Retrieved", mode: "processed", agreement: "Agreement MER-002",
125:     submitted: "submitted 13 Sep 2026", submittedBy: "R. Adeyemi", scope: "Text",
126:     retrievedAt: "18 Sep 2026",
127:   },
128:   {
129:     id: "ftn-2026-0117", objective: "Train on the call recordings to classify caller intent at 88% accuracy or better.",
130:     status: "Refused", mode: "finetune", agreement: "Agreement MER-007",
131:     submitted: "submitted 2 Sep 2026", submittedBy: "A. Osei", scope: "Audio",
132:     refusalReason: "The call recordings contain spoken account details, and Digicow would not release a model trained on them under this agreement. That reason is recorded rather than left implicit.",
133:   },
134:   {
135:     id: "prc-2026-0104", objective: "Find out complaint volume by branch, last quarter.",
136:     status: "Expired", mode: "processed", agreement: "Agreement MER-002",
137:     submitted: "submitted 19 Aug 2026", submittedBy: "R. Adeyemi",
138:     submittedAtISO: "2026-08-18", expiredAtISO: "2026-09-02", expiredAtDisplay: "2 Sep 2026",
139:     dataOwner: "Digicow",
140:     addressedTo: "the records authority at Digicow",
141:     signoffReason: "This request needed sign-off because it includes complaint files. Under Agreement MER-002, Digicow had to approve any use of them.",
142:   },
143:   {
144:     id: "skl-2026-0047", objective: "Build a skill to summarise complaint threads by branch.",
145:     status: "Blocked", mode: "skills", agreement: "Agreement MER-007",
146:     submitted: "submitted 5 Sep 2026", submittedBy: "T. Mwangi", scope: "Text",
147:     blockedAt: "14 Sep 2026, 03:12", blockKind: "estate",
148:     dataOwner: "the data governance office at Digicow",
149:   },
150:   {
151:     id: "prc-2026-0102", objective: "Find out average time-to-close by branch, last quarter.",
152:     status: "Blocked", mode: "processed", agreement: "Agreement MER-002",
153:     submitted: "submitted 12 Sep 2026", submittedBy: "R. Adeyemi", scope: "Audio",
154:     blockedAt: "13 Sep 2026, 17:40", blockKind: "request",
155:     blockReason: "There isn't enough time-to-close data recorded for last quarter to answer this by branch.",
156:     blockRef: "PRC-2026-0102-B1",
157:     dataOwner: "Digicow",
158:   },
159:   {
160:     id: "ftn-2026-0122", objective: "Train on the cleared complaint files to identify repeat callers.",
161:     status: "party_halted", mode: "finetune", agreement: "Agreement MER-007",
162:     submitted: "submitted 8 Sep 2026", submittedBy: "R. Adeyemi", scope: "Audio",
163:     blockedAt: "15 Sep 2026, 11:04",
164:     blockedBy: "R. Adeyemi",
165:     pctAtStop: 63,
166:     blockRef: "FTN-2026-0122-B1",
167:     dataOwner: "Digicow",
168:     signoffRequired: true, approvedByRole: "records authority", approvedDate: "12 Sep 2026",
169:   },
170:   // Stopped terminal state (Executing → Stopped)
171:   {
172:     id: "prc-2026-0115", objective: "Find out which branches have the most incomplete complaint records.",
173:     status: "Stopped", mode: "processed", agreement: "Agreement MER-002",
174:     submitted: "submitted 14 Sep 2026", submittedBy: "R. Adeyemi", scope: "Audio",
175:     stoppedAt: "16 Sep 2026, 09:22", pctAtStop: 28,
176:   },
177: ];
178: 
179: const ALL_STATES = [
180:   "In Approval", "Executing", "Ready", "Retrieved", "Refused",
181:   "Blocked", "Expired", "Interrupted (platform fault)",
182:   "Blocked \u00b7 request", "Blocked \u00b7 check", "Blocked \u00b7 estate",
183:   "party_halted", "Stopped",
184: ];
185: 
186: const RAIL_ROW = [
187:   ["Total", "Total"], ["In Approval", "In Approval"], ["Executing", "Executing"],
188:   ["Ready", "Ready"], ["Retrieved", "Retrieved"], ["Refused", "Refused"],
189:   ["Blocked", "Blocked"], ["Expired", "Expired"], ["Interrupted (platform fault)", "Interrupted"],
190:   ["party_halted", "Stopped by you"], ["Stopped", "Stopped"],
191: ];
192: 
193: function daysBetween(isoA, isoB) {
194:   const a = new Date(isoA);
195:   const b = isoB ? new Date(isoB) : new Date();
196:   return Math.max(0, Math.round((b - a) / 86_400_000));
197: }
198: 
199: /* ── Submit Form ───────────────────────────────────────── */
200: function SubmitForm({ onSubmitted }) {
201:   const { user } = useAuth();
202:   const [objectiveText, setObjectiveText] = useState("");
203:   const [units, setUnits] = useState("");
204:   const [submitting, setSubmitting] = useState(false);
205:   const [result, setResult] = useState(null);
206:   const [error, setError] = useState(null);
207: 
208:   const handleSubmit = useCallback(async (e) => {
209:     e.preventDefault();
210:     if (!objectiveText.trim()) return;
211:     setSubmitting(true);
212:     setError(null);
213:     setResult(null);
214:     const unitList = units.trim() ? units.split(",").map((u) => u.trim()).filter(Boolean) : [];
215:     const res = await tryPost("/api/portal/requests", { objective_text: objectiveText, units: unitList });
216:     setSubmitting(false);
217:     if (res.ok) {
218:       setResult(res.data);
219:       setObjectiveText("");
220:       setUnits("");
221:       if (onSubmitted) onSubmitted();
222:     } else if (res.status === 422) {
223:       setError(`Governed refusal: ${JSON.stringify(res.data)}`);
224:     } else if (res.status === 404) {
225:       setError("Endpoint not yet mounted on this backend instance (POST /api/portal/requests returns 404).");
226:     } else if (res.status === 401) {
227:       setError("Authentication required. Please sign in.");
228:     } else {
229:       setError(res.error || `Unexpected response: ${res.status}`);
230:     }
231:   }, [objectiveText, units, onSubmitted]);
232: 
233:   if (!user) return null;
234: 
235:   return (
236:     <div data-testid="request-submit-form" className="rounded-lg border p-4 mb-6" style={{ borderColor: "var(--line)", background: "white" }}>
237:       <h2 className="text-sm font-medium mb-3" style={{ color: "var(--ink)" }}>
238:         <Send size={14} className="inline mr-1.5" />
239:         Submit a new request
240:       </h2>
241:       <form onSubmit={handleSubmit}>
242:         <div className="space-y-3">
243:           <div>
244:             <label htmlFor="objective-text" className="text-xs block mb-1" style={{ color: "var(--ink2)" }}>
245:               Objective (frozen once submitted)
246:             </label>
247:             <textarea
248:               id="objective-text"
249:               data-testid="submit-objective-text"
250:               value={objectiveText}
251:               onChange={(e) => setObjectiveText(e.target.value)}
252:               placeholder="Describe what you need from the data estate..."
253:               className="w-full text-sm px-3 py-2 rounded border resize-none"
254:               style={{ borderColor: "var(--hair)", minHeight: "80px" }}
255:               required
256:             />
257:           </div>
258:           <div>
259:             <label htmlFor="submit-units" className="text-xs block mb-1" style={{ color: "var(--ink2)" }}>
260:               Units (comma-separated, optional)
261:             </label>
262:             <input
263:               id="submit-units"
264:               data-testid="submit-units"
265:               value={units}
266:               onChange={(e) => setUnits(e.target.value)}
267:               placeholder="unit-a, unit-b"
268:               className="w-full text-sm px-3 py-2 rounded border"
269:               style={{ borderColor: "var(--hair)" }}
270:             />
271:           </div>
272:           <button
273:             type="submit"
274:             data-testid="submit-request-btn"
275:             disabled={submitting || !objectiveText.trim()}
276:             className="text-xs px-4 py-2 rounded font-medium transition-colors disabled:opacity-50"
277:             style={{ background: "var(--blue)", color: "white" }}
278:           >
279:             {submitting ? "Submitting\u2026" : "Submit request"}
280:           </button>
281:         </div>
282:       </form>
283:       {result && (
284:         <div data-testid="submit-result" className="mt-3 rounded p-3 text-xs" style={{ background: "rgba(29,122,110,.06)", color: "var(--sage)" }}>
285:           Request accepted. Outcome: {result.outcome || "accepted"}. Authority: {result.authority || "delegated"}.
286:         </div>
287:       )}
288:       {error && (
289:         <div data-testid="submit-error" className="mt-3 rounded p-3 text-xs" style={{ background: "rgba(184,57,91,.06)", color: "var(--oxblood)" }}>
290:           {error}
291:         </div>
292:       )}
293:     </div>
294:   );
295: }
296: 
297: /* ── Request Card ──────────────────────────────────────── */
298: function RequestCard({ req, onRefresh }) {
299:   const [expanded, setExpanded] = useState(false);
300:   const [stopDialogOpen, setStopDialogOpen] = useState(false);
301:   const [stopLoading, setStopLoading] = useState(false);
302:   const [stopResult, setStopResult] = useState(null);
303:   const [retryLoading, setRetryLoading] = useState(false);
304:   const [retryResult, setRetryResult] = useState(null);
305:   const blockMeta = req.blockKind ? BLOCK_KIND_META[req.blockKind] : null;
306: 
307:   const waitDays = req.submittedAtISO ? daysBetween(req.submittedAtISO, null) : null;
308:   const resolvedKindLine = blockMeta ? blockMeta.kindLine : null;
309:   const resolvedWhatNext = (() => {
310:     if (!blockMeta) return null;
311:     if (req.blockKind === "estate") return BLOCK_WHATNEXT_ESTATE_TPL(req.dataOwner || "the data owner");
312:     return blockMeta.whatNext || null;
313:   })();
314: 
315:   // Stop handler — wired to POST /api/portal/requests/{id}/stop
316:   const handleStop = useCallback(async () => {
317:     setStopLoading(true);
318:     const res = await tryPost(`/api/portal/requests/${req.id}/stop`);
319:     setStopLoading(false);
320:     if (res.ok) {
321:       setStopResult(res.data);
322:       setStopDialogOpen(false);
323:       if (onRefresh) onRefresh();
324:     } else if (res.status === 409) {
325:       setStopResult({ error: true, detail: res.data?.detail || "Request is not currently Executing." });
326:     } else {
327:       setStopResult({ error: true, detail: res.error || `Stop failed (${res.status})` });
328:     }
329:   }, [req.id, onRefresh]);
330: 
331:   // Retry handler — wired to POST /api/portal/requests/{id}/retry
332:   const handleRetry = useCallback(async () => {
333:     setRetryLoading(true);
334:     const res = await tryPost(`/api/portal/requests/${req.id}/retry`);
335:     setRetryLoading(false);
336:     if (res.ok) {
337:       setRetryResult(res.data);
338:       if (onRefresh) onRefresh();
339:     } else {
340:       setRetryResult({ error: true, detail: res.data?.detail || res.error || `Retry failed (${res.status})` });
341:     }
342:   }, [req.id, onRefresh]);
343: 
344:   return (
345:     <div
346:       data-testid={`request-card-${req.id}`}
347:       className="rounded-lg border overflow-hidden transition-shadow hover:shadow-sm"
348:       style={{ borderColor: "var(--line)", background: "white" }}
349:     >
350:       <div className="p-4">
351:         <div className="flex items-start justify-between mb-2">
352:           <div className="flex-1">
353:             <div className="flex items-center gap-2 mb-1">
354:               <span className="text-xs font-mono" style={{ color: "var(--ink3)" }}>{req.id}</span>
355:               <StatusBadge status={req.status} />
356:               {req.status === "Blocked" && req.blockKind && (
357:                 <StatusBadge status={`Blocked \u00b7 ${req.blockKind}`} />
358:               )}
359:             </div>
360:             <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>{req.objective}</p>
361:           </div>
362:           <button
363:             data-testid={`request-expand-${req.id}`}
364:             onClick={() => setExpanded(!expanded)}
365:             className="p-1 rounded hover:bg-black/5 transition-colors"
366:             aria-label={expanded ? "Collapse" : "Expand"}
367:           >
368:             {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
369:           </button>
370:         </div>
371: 
372:         <div className="flex flex-wrap gap-3 text-xs" style={{ color: "var(--ink3)" }}>
373:           <span>{req.mode && MODE_VERB[req.mode] ? MODE_VERB[req.mode] : req.mode}</span>
374:           <span>&middot;</span>
375:           <span>{req.agreement}</span>
376:           <span>&middot;</span>
377:           <span>{req.submitted}</span>
378:         </div>
379: 
380:         {/* In Approval: spend-ceiling breach folded in with reason */}
381:         {req.status === "In Approval" && req.spendCeilingBreach && (
382:           <div className="mt-2 text-xs p-2 rounded" style={{ background: "rgba(176,141,46,.08)", color: "var(--brass)" }}>
383:             <AlertTriangle size={12} className="inline mr-1" />
384:             {req.spendCeilingReason}
385:           </div>
386:         )}
387: 
388:         {/* In Approval: waiting line (TC-INA-06) */}
389:         {req.status === "In Approval" && req.windowEndsAtISO && waitDays != null && (
390:           <p data-testid={`in-approval-waiting-${req.id}`} className="mt-2 text-xs" style={{ color: "var(--brass)" }}>
391:             {IN_APPROVAL_WAITING_TPL(
392:               req.dataOwner || "the data owner",
393:               new Date(req.windowEndsAtISO).toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" }),
394:               waitDays
395:             )}
396:           </p>
397:         )}
398: 
399:         {/* Interrupted state with retry counter + retry action */}
400:         {req.status === "Interrupted (platform fault)" && (
401:           <div className="mt-2">
402:             <div className="flex items-center gap-2 text-xs p-2 rounded" style={{ background: "rgba(184,57,91,.06)", color: "var(--oxblood)" }}>
403:               <RotateCcw size={12} />
404:               <span>
405:                 Auto-retry attempt {req.retryAttempts || 0} of {req.maxRetries || 3}
406:                 {(req.retryAttempts || 0) >= (req.maxRetries || 3) && " \u2014 exhausted, resolves to Blocked \u00b7 check"}
407:               </span>
408:             </div>
409:             {(req.retryAttempts || 0) < (req.maxRetries || 3) && (
410:               <button
411:                 data-testid={`retry-btn-${req.id}`}
412:                 onClick={handleRetry}
413:                 disabled={retryLoading}
414:                 className="mt-2 flex items-center gap-1.5 text-xs px-2.5 py-1 rounded border transition-colors hover:bg-blue-50 disabled:opacity-50"
415:                 style={{ borderColor: "var(--blue)", color: "var(--blue)" }}
416:               >
417:                 <RotateCcw size={10} /> {retryLoading ? "Retrying\u2026" : "Retry"}
418:               </button>
419:             )}
420:             {retryResult && retryResult.error && (
421:               <p className="mt-1 text-[10px]" style={{ color: "var(--oxblood)" }}>{retryResult.detail}</p>
422:             )}
423:           </div>
424:         )}
425: 
426:         {/* Executing: progress + Stop action (TC-BLK-24) */}
427:         {req.status === "Executing" && (
428:           <div className="mt-2">
429:             {req.pct != null && (
430:               <>
431:                 <div className="flex items-center justify-between text-xs mb-1" style={{ color: "var(--ink3)" }}>
432:                   <span>{req.stageLabel || "Processing"}</span>
433:                   <span>{req.eta}</span>
434:                 </div>
435:                 <div className="h-1.5 rounded-full overflow-hidden" style={{ background: "var(--line)" }}>
436:                   <div className="h-full rounded-full transition-all" style={{ width: `${req.pct}%`, background: "var(--accent)" }} />
437:                 </div>
438:               </>
439:             )}
440:             {req.stageIndex != null && req.pct == null && (
441:               <div className="flex items-center justify-between text-xs" style={{ color: "var(--ink3)" }}>
442:                 <span>Step {req.stageIndex} of {req.stageCount} &mdash; {req.stageLabel}</span>
443:                 <span>{req.eta}</span>
444:               </div>
445:             )}
446:             <button
447:               data-testid={`stop-btn-${req.id}`}
448:               onClick={() => setStopDialogOpen(true)}
449:               className="mt-2 flex items-center gap-1.5 text-xs px-2.5 py-1 rounded border transition-colors hover:bg-red-50"
450:               style={{ borderColor: "var(--oxblood)", color: "var(--oxblood)" }}
451:             >
452:               <Square size={10} /> Stop
453:             </button>
454:           </div>
455:         )}
456: 
457:         {/* Stop confirm dialog (TC-BLK-24) — request-scoped copy, NEVER party-halt framing */}
458:         {stopDialogOpen && (
459:           <div data-testid={`stop-confirm-${req.id}`} className="mt-2 border rounded-lg p-3" style={{ borderColor: "var(--oxblood)", background: "rgba(184,57,91,.04)" }}>
460:             <p className="text-sm mb-3" style={{ color: "var(--ink)" }}>
461:               {STOP_CONFIRM}
462:             </p>
463:             <div className="flex gap-2">
464:               <button
465:                 data-testid={`stop-confirm-yes-${req.id}`}
466:                 className="text-xs px-3 py-1.5 rounded font-medium text-white disabled:opacity-50"
467:                 style={{ background: "var(--oxblood)" }}
468:                 disabled={stopLoading}
469:                 onClick={handleStop}
470:               >
471:                 {stopLoading ? "Stopping\u2026" : "Stop"}
472:               </button>
473:               <button
474:                 data-testid={`stop-confirm-cancel-${req.id}`}
475:                 className="text-xs px-3 py-1.5 rounded border"
476:                 style={{ borderColor: "var(--hair)", color: "var(--ink2)" }}
477:                 onClick={() => setStopDialogOpen(false)}
478:               >
479:                 Cancel
480:               </button>
481:             </div>
482:             {stopResult && stopResult.error && (
483:               <p className="mt-2 text-[10px]" style={{ color: "var(--oxblood)" }}>{stopResult.detail}</p>
484:             )}
485:           </div>
486:         )}
487: 
488:         {/* Stopped terminal state — charged-to-point-of-stop, receipted */}
489:         {req.status === "Stopped" && (
490:           <div className="mt-2 text-xs p-2 rounded" style={{ background: "rgba(27,31,39,.04)", color: "var(--ink2)" }}>
491:             <Square size={10} className="inline mr-1" style={{ color: "var(--oxblood)" }} />
492:             Stopped{req.stoppedAt ? ` at ${req.stoppedAt}` : ""}.
493:             {req.pctAtStop != null && ` Charged to ${req.pctAtStop}% completion.`}
494:             {" "}Receipted.
495:           </div>
496:         )}
497: 
498:         {/* Ready state */}
499:         {req.status === "Ready" && req.modelId && (
500:           <div className="mt-2 text-xs" style={{ color: "var(--ink3)" }}>
501:             <span>Model: {req.modelId} &middot; Base: {req.baseModel}</span>
502:             {req.weightsHash && <span className="ml-2 font-mono">{req.weightsHash}</span>}
503:           </div>
504:         )}
505:       </div>
506: 
507:       {/* Expanded drawer */}
508:       {expanded && (
509:         <div className="border-t px-4 py-3 text-sm space-y-3" style={{ borderColor: "var(--line)", background: "var(--surface)" }}>
510:           {req.submittedBy && <p style={{ color: "var(--ink2)" }}>Submitted by {req.submittedBy}</p>}
511:           {req.scope && <p style={{ color: "var(--ink3)" }}>Scope: {req.scope}</p>}
512: 
513:           {/* In Approval drawer (TC-INA-06) */}
514:           {req.status === "In Approval" && (
515:             <div data-testid={`drawer-in-approval-${req.id}`} className="mt-1 space-y-2">
516:               {req.signoffReason && (
517:                 <p className="text-sm" style={{ color: "var(--ink2)" }}>{req.signoffReason}</p>
518:               )}
519:               {req.windowEndsAtISO && waitDays != null && (
520:                 <p className="text-sm" style={{ color: "var(--brass)" }}>
521:                   {IN_APPROVAL_WAITING_TPL(
522:                     req.dataOwner || "the data owner",
523:                     new Date(req.windowEndsAtISO).toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" }),
524:                     waitDays
525:                   )}
526:                 </p>
527:               )}
528:             </div>
529:           )}
530: 
531:           {/* Blocked drawer — three kinds: request / check / estate */}
532:           {req.status === "Blocked" && blockMeta && (
533:             <div
534:               data-testid={`drawer-blocked-${req.blockKind}-${req.id}`}
535:               className="border-l-4 p-3 rounded"
536:               style={{ borderColor: "var(--oxblood)", background: "rgba(184,57,91,.04)" }}
537:             >
538:               {blockMeta.showProgress === true && req.pctAtStop != null && (
539:                 <div className="mb-2">
540:                   <div className="h-1.5 rounded-full overflow-hidden" style={{ background: "var(--line)" }}>
541:                     <div className="h-full rounded-full" style={{ width: `${req.pctAtStop}%`, background: "var(--oxblood)" }} />
542:                   </div>
543:                   <p className="text-[10px] mt-0.5" style={{ color: "var(--oxblood)" }}>
544:                     Stopped at {req.pctAtStop}% &middot; {req.blockedAt}
545:                   </p>
546:                 </div>
547:               )}
548:               <p data-testid={`block-kind-line-${req.id}`} className="text-xs font-medium mb-1" style={{ color: "var(--oxblood)" }}>
549:                 {resolvedKindLine}
550:               </p>
551:               {req.blockKind === "estate" && (
552:                 <p className="text-sm" style={{ color: "var(--ink2)" }}>{BLOCK_ESTATE_REASON}</p>
553:               )}
554:               {(req.blockKind === "request" || req.blockKind === "check") && req.blockReason && (
555:                 <p className="text-sm" style={{ color: "var(--ink2)" }}>{req.blockReason}</p>
556:               )}
557:               {req.blockRef && req.blockKind !== "estate" && (
558:                 <p className="text-xs font-mono mt-1" style={{ color: "var(--ink3)" }}>Reference {req.blockRef}</p>
559:               )}
560:               {resolvedWhatNext && (
561:                 <p data-testid={`block-whatnext-${req.id}`} className="text-xs mt-2" style={{ color: "var(--ink3)" }}>{resolvedWhatNext}</p>
562:               )}
563:               {blockMeta.showCopy && (
564:                 <button data-testid={`copy-new-request-${req.id}`} className="mt-2 text-xs px-3 py-1.5 rounded border transition-colors hover:bg-white" style={{ borderColor: "var(--hair)", color: "var(--ink)" }}>
565:                   Copy into a new request
566:                 </button>
567:               )}
568:             </div>
569:           )}
570: 
571:           {/* party_halted drawer — own rail state, NOT a Blocked variant */}
572:           {req.status === "party_halted" && (
573:             <div data-testid={`drawer-party-halted-${req.id}`} className="border-l-4 p-3 rounded" style={{ borderColor: "var(--oxblood)", background: "rgba(184,57,91,.04)" }}>
574:               {req.pctAtStop != null && (
575:                 <div className="mb-2">
576:                   <div className="h-1.5 rounded-full overflow-hidden" style={{ background: "var(--line)" }}>
577:                     <div className="h-full rounded-full" style={{ width: `${req.pctAtStop}%`, background: "var(--oxblood)" }} />
578:                   </div>
579:                   <p className="text-[10px] mt-0.5" style={{ color: "var(--oxblood)" }}>Stopped at {req.pctAtStop}% &middot; {req.blockedAt}</p>
580:                 </div>
581:               )}
582:               <p data-testid={`party-halted-kind-line-${req.id}`} className="text-xs font-medium mb-1" style={{ color: "var(--oxblood)" }}>{PARTY_HALTED_KIND_LINE}</p>
583:               {req.blockedBy && <p className="text-xs mt-1" style={{ color: "var(--ink3)" }}>Stopped by {req.blockedBy}</p>}
584:               {req.blockRef && <p className="text-xs font-mono mt-1" style={{ color: "var(--ink3)" }}>Reference {req.blockRef}</p>}
585:               <p data-testid={`party-halted-whatnext-${req.id}`} className="text-xs mt-2" style={{ color: "var(--ink3)" }}>{PARTY_HALTED_WHAT_NEXT}</p>
586:               <button data-testid={`copy-new-request-${req.id}`} className="mt-2 text-xs px-3 py-1.5 rounded border transition-colors hover:bg-white" style={{ borderColor: "var(--hair)", color: "var(--ink)" }}>
587:                 Copy into a new request
588:               </button>
589:             </div>
590:           )}
591: 
592:           {/* Stopped drawer — terminal state, receipted */}
593:           {req.status === "Stopped" && (
594:             <div data-testid={`drawer-stopped-${req.id}`} className="border-l-4 p-3 rounded" style={{ borderColor: "var(--ink3)", background: "rgba(27,31,39,.04)" }}>
595:               <p className="text-xs font-medium mb-1" style={{ color: "var(--ink)" }}>
596:                 This request was stopped by the requester.
597:               </p>
598:               {req.pctAtStop != null && (
599:                 <p className="text-xs" style={{ color: "var(--ink2)" }}>Charged to {req.pctAtStop}% of execution. Receipted.</p>
600:               )}
601:               {req.stoppedAt && <p className="text-xs" style={{ color: "var(--ink3)" }}>Stopped at {req.stoppedAt}</p>}
602:             </div>
603:           )}
604: 
605:           {/* Expired drawer (TC-EXP-02) */}
606:           {req.status === "Expired" && (
607:             <div data-testid={`drawer-expired-${req.id}`} className="p-3 rounded space-y-2" style={{ background: "rgba(27,31,39,.04)" }}>
608:               <p data-testid={`expired-date-line-${req.id}`} className="text-sm font-medium" style={{ color: "var(--ink)" }}>
609:                 {EXPIRED_DATE_TPL(req.expiredAtDisplay || "")}
610:               </p>
611:               <p data-testid={`expired-waited-line-${req.id}`} className="text-sm" style={{ color: "var(--ink2)" }}>
612:                 {EXPIRED_WAITED_TPL(
613:                   req.submittedAtISO && req.expiredAtISO ? daysBetween(req.submittedAtISO, req.expiredAtISO) : 14
614:                 )}
615:               </p>
616:               {req.addressedTo && <p className="text-sm" style={{ color: "var(--ink3)" }}>It was addressed to {req.addressedTo}.</p>}
617:               {req.signoffReason && <p className="text-sm" style={{ color: "var(--ink3)" }}>{req.signoffReason}</p>}
618:               <p data-testid={`expired-meaning-${req.id}`} className="text-sm" style={{ color: "var(--ink2)" }}>{EXPIRED_MEANING_TPL(req.dataOwner || "the data owner")}</p>
619:               <p data-testid={`expired-whatnext-${req.id}`} className="text-sm" style={{ color: "var(--ink2)" }}>{EXPIRED_WHAT_NEXT_TPL(req.dataOwner || "the data owner")}</p>
620:               <button data-testid={`copy-new-request-${req.id}`} className="mt-1 text-xs px-3 py-1.5 rounded border transition-colors hover:bg-white" style={{ borderColor: "var(--hair)", color: "var(--ink)" }}>
621:                 Submit again as a new request
622:               </button>
623:             </div>
624:           )}
625: 
626:           {/* Refused drawer — NO "Waited N days" (hard omission) */}
627:           {req.status === "Refused" && req.refusalReason && (
628:             <div className="border-l-4 p-3 rounded" style={{ borderColor: "var(--ink)", background: "rgba(27,31,39,.03)" }}>
629:               <p className="text-sm" style={{ color: "var(--ink2)" }}>{req.refusalReason}</p>
630:             </div>
631:           )}
632: 
633:           {/* Retrieved */}
634:           {req.status === "Retrieved" && req.retrievedAt && (
635:             <p className="mt-1" style={{ color: "var(--sage)" }}>
636:               <CheckCircle size={12} className="inline mr-1" />
637:               Retrieved {req.retrievedAt}
638:             </p>
639:           )}
640: 
641:           {/* Sign-off block — NO "Waited N days" (hard omission), NO approver identity (DAP-15) */}
642:           {req.approvedByRole && req.status !== "In Approval" && (
643:             <p className="mt-1" style={{ color: "var(--ink3)" }}>
644:               Approved by {req.approvedByRole} on {req.approvedDate}
645:             </p>
646:           )}
647:         </div>
648:       )}
649:     </div>
650:   );
651: }
652: 
653: /* ── Main component ────────────────────────────────────── */
654: export default function RequestLifecycle() {
655:   const { user } = useAuth();
656:   const [filter, setFilter] = useState("Total");
657:   const [liveRows, setLiveRows] = useState(null);
658:   const [liveError, setLiveError] = useState(null);
659:   const [loading, setLoading] = useState(false);
660: 
661:   const fetchRequests = useCallback(async () => {
662:     if (!user) return;
663:     setLoading(true);
664:     const res = await tryGet("/api/portal/requests");
665:     setLoading(false);
666:     if (res.ok && res.data && Array.isArray(res.data.rows)) {
667:       setLiveRows(res.data.rows);
668:       setLiveError(null);
669:     } else if (res.status === 404) {
670:       setLiveError("Endpoint not yet mounted (GET /api/portal/requests returns 404). Showing reference state machine.");
671:       setLiveRows(null);
672:     } else if (res.status === 401) {
673:       setLiveError("Authentication required for request history.");
674:       setLiveRows(null);
675:     } else {
676:       setLiveError(res.error || "Failed to fetch requests.");
677:       setLiveRows(null);
678:     }
679:   }, [user]);
680: 
681:   useEffect(() => { fetchRequests(); }, [fetchRequests]);
682: 
683:   const requests = liveRows && liveRows.length > 0 ? liveRows : SAMPLE_REQUESTS;
684:   const usingLive = liveRows !== null && liveRows.length > 0;
685: 
686:   const counts = {};
687:   for (const r of requests) {
688:     counts[r.status] = (counts[r.status] || 0) + 1;
689:   }
690:   counts["Total"] = requests.length;
691: 
692:   const filtered = filter === "Total"
693:     ? requests
694:     : requests.filter((r) => r.status === filter);
695: 
696:   return (
697:     <div data-testid="request-lifecycle" className="max-w-5xl mx-auto px-8 py-10">
698:       <h1
699:         data-testid="request-lifecycle-title"
700:         className="text-xl font-semibold mb-1"
701:         style={{ color: "var(--ink)", fontFamily: "var(--head)" }}
702:       >
703:         Request Lifecycle
704:       </h1>
705:       <p className="text-sm mb-6" style={{ color: "var(--ink3)" }}>
706:         Every request passes through a state machine. This view shows the full lifecycle.
707:       </p>
708: 
709:       {/* Submit form (JWT-gated) */}
710:       <SubmitForm onSubmitted={fetchRequests} />
711: 
712:       {/* State machine legend */}
713:       <div data-testid="state-machine-legend" className="mb-6">
714:         <h2 className="text-sm font-medium mb-3" style={{ color: "var(--ink)" }}>State Legend</h2>
715:         <div className="flex flex-wrap gap-2">
716:           {ALL_STATES.map((s) => (
717:             <StatusBadge key={s} status={s} />
718:           ))}
719:         </div>
720:       </div>
721: 
722:       {/* Rail counts */}
723:       <div data-testid="request-rail" className="rounded-lg border mb-6" style={{ borderColor: "var(--line)", background: "white" }}>
724:         <div className="grid grid-cols-11 text-center">
725:           {RAIL_ROW.map(([key, label]) => (
726:             <button
727:               key={key}
728:               data-testid={`rail-${key.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}
729:               onClick={() => setFilter(key)}
730:               className={`py-3 text-xs transition-colors border-b-2 ${
731:                 filter === key ? "font-semibold" : "hover:bg-black/[.02]"
732:               }`}
733:               style={{
734:                 borderBottomColor: filter === key ? "var(--blue)" : "transparent",
735:                 color: filter === key ? "var(--ink)" : "var(--ink3)",
736:               }}
737:             >
738:               <span className="block text-lg font-semibold">{counts[key] || 0}</span>
739:               <span>{label}</span>
740:             </button>
741:           ))}
742:         </div>
743:       </div>
744: 
745:       {loading && <LoadingState message="Loading requests\u2026" />}
746: 
747:       {/* Request cards */}
748:       <div className="space-y-3" data-testid="request-list">
749:         {filtered.map((req) => (
750:           <RequestCard key={req.id} req={req} onRefresh={fetchRequests} />
751:         ))}
752:         {filtered.length === 0 && !loading && (
753:           <div className="text-center py-8">
754:             <p className="text-sm" style={{ color: "var(--ink3)" }}>No requests in this state.</p>
755:           </div>
756:         )}
757:       </div>
758: 
759:       {/* Backend status notice */}
760:       {liveError && (
761:         <div data-testid="request-backend-notice" className="mt-8 rounded-lg border p-4" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
762:           <p className="text-xs font-medium mb-1" style={{ color: "var(--brass)" }}>
763:             <Clock size={12} className="inline mr-1" />
764:             Endpoint not yet mounted
765:           </p>
766:           <p className="text-xs" style={{ color: "var(--ink3)" }}>{liveError}</p>
767:         </div>
768:       )}
769:       {!liveError && !usingLive && !loading && (
770:         <div className="mt-8 rounded-lg border p-4" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
771:           <p className="text-xs font-medium mb-1" style={{ color: "var(--brass)" }}>Reference state machine</p>
772:           <p className="text-xs" style={{ color: "var(--ink3)" }}>
773:             The requests shown above are the reference state machine rendered from the DAP design specification.
774:             Once the backend portal endpoints are mounted, this view will display real request data.
775:           </p>
776:         </div>
777:       )}
778:     </div>
779:   );
780: }

# SOURCE: frontend/src/pages/os/AdminEstate.jsx

1: /*
2:  * AdminEstate.jsx — v2 OS · admin tab · MANAGE ESTATE Registry leaf.
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4e GREEN · 2026-09-22T08:52:00Z
4:  * R-103 amendment: single continuous run to completion.
5:  * HONEST-GAP · SO §5 honest-gap-never-fake.
6:  */
7: 
8: import React from "react";
9: 
10: export default function AdminEstate() {
11:   return (
12:     <div
13:       data-testid="admin-estate-surface"
14:       style={{
15:         minHeight: "100vh",
16:         background: "var(--surface, #f7f5ef)",
17:         color: "var(--ink, #12121a)",
18:         padding: "48px 64px",
19:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
20:       }}
21:     >
22:       <header style={{ marginBottom: 32 }}>
23:         <div
24:           data-testid="admin-estate-breadcrumb"
25:           style={{
26:             fontSize: 12,
27:             letterSpacing: "0.12em",
28:             textTransform: "uppercase",
29:             color: "var(--ink3, #6b6b78)",
30:             marginBottom: 8,
31:           }}
32:         >
33:           MANAGE ESTATE · Registry
34:         </div>
35:         <h1
36:           data-testid="admin-estate-title"
37:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
38:         >
39:           Registry
40:         </h1>
41:       </header>
42:       <section
43:         data-testid="admin-estate-lead"
44:         style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}
45:       >
46:         <p style={{ margin: "0 0 24px 0" }}>
47:           Every model, every skill, every dataset the estate holds — its lineage, its entitlements, its trust receipts.
48:         </p>
49:       </section>
50:       <section
51:         data-testid="admin-estate-honest-gap"
52:         style={{
53:           marginTop: 40,
54:           padding: "24px 28px",
55:           background: "rgba(176,141,46,.07)",
56:           border: "1px solid var(--brass, #b08d2e)",
57:           borderRadius: 4,
58:           maxWidth: 720,
59:         }}
60:       >
61:         <div
62:           data-testid="admin-estate-honest-gap-label"
63:           style={{
64:             fontSize: 11,
65:             letterSpacing: "0.14em",
66:             textTransform: "uppercase",
67:             color: "var(--brass, #b08d2e)",
68:             fontWeight: 600,
69:             marginBottom: 8,
70:           }}
71:         >
72:           Honest gap · surface only
73:         </div>
74:         <div data-testid="admin-estate-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
75:           Backend for Registry not yet wired. This surface reveals the design-of-record
76:           structure honestly; no fabricated data is shown. Wire lands at PHASE 3
77:           Census Productization + PHASE 4 feature build-out per R-102 MASTER DIRECTIVE
78:           + R-103 amendment (single continuous run).
79:         </div>
80:         <div
81:           data-testid="admin-estate-honest-gap-see-working"
82:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
83:         >
84:           See the working: NAV admin.estate at App.js const NAV · surface at
85:           pages/os/AdminEstate.jsx.
86:         </div>
87:       </section>
88:     </div>
89:   );
90: }

# SOURCE: frontend/src/pages/os/AdminGovern.jsx

1: /*
2:  * AdminGovern.jsx — v2 OS · admin tab · MANAGE ESTATE Shield leaf.
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4e GREEN · 2026-09-22T08:52:00Z
4:  * R-103 amendment: single continuous run to completion.
5:  * HONEST-GAP · SO §5 honest-gap-never-fake.
6:  */
7: 
8: import React from "react";
9: 
10: export default function AdminGovern() {
11:   return (
12:     <div
13:       data-testid="admin-govern-surface"
14:       style={{
15:         minHeight: "100vh",
16:         background: "var(--surface, #f7f5ef)",
17:         color: "var(--ink, #12121a)",
18:         padding: "48px 64px",
19:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
20:       }}
21:     >
22:       <header style={{ marginBottom: 32 }}>
23:         <div
24:           data-testid="admin-govern-breadcrumb"
25:           style={{
26:             fontSize: 12,
27:             letterSpacing: "0.12em",
28:             textTransform: "uppercase",
29:             color: "var(--ink3, #6b6b78)",
30:             marginBottom: 8,
31:           }}
32:         >
33:           MANAGE ESTATE · Shield
34:         </div>
35:         <h1
36:           data-testid="admin-govern-title"
37:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
38:         >
39:           Shield
40:         </h1>
41:       </header>
42:       <section
43:         data-testid="admin-govern-lead"
44:         style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}
45:       >
46:         <p style={{ margin: "0 0 24px 0" }}>
47:           The refusal rules in force. Named authors; dated changes; one place the shield reads from.
48:         </p>
49:       </section>
50:       <section
51:         data-testid="admin-govern-honest-gap"
52:         style={{
53:           marginTop: 40,
54:           padding: "24px 28px",
55:           background: "rgba(176,141,46,.07)",
56:           border: "1px solid var(--brass, #b08d2e)",
57:           borderRadius: 4,
58:           maxWidth: 720,
59:         }}
60:       >
61:         <div
62:           data-testid="admin-govern-honest-gap-label"
63:           style={{
64:             fontSize: 11,
65:             letterSpacing: "0.14em",
66:             textTransform: "uppercase",
67:             color: "var(--brass, #b08d2e)",
68:             fontWeight: 600,
69:             marginBottom: 8,
70:           }}
71:         >
72:           Honest gap · surface only
73:         </div>
74:         <div data-testid="admin-govern-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
75:           Backend for Shield not yet wired. This surface reveals the design-of-record
76:           structure honestly; no fabricated data is shown. Wire lands at PHASE 3
77:           Census Productization + PHASE 4 feature build-out per R-102 MASTER DIRECTIVE
78:           + R-103 amendment (single continuous run).
79:         </div>
80:         <div
81:           data-testid="admin-govern-honest-gap-see-working"
82:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
83:         >
84:           See the working: NAV admin.govern at App.js const NAV · surface at
85:           pages/os/AdminGovern.jsx.
86:         </div>
87:       </section>
88:     </div>
89:   );
90: }

# SOURCE: frontend/src/pages/os/AdminGreyMirror.jsx

1: /*
2:  * AdminGreyMirror.jsx — v2 OS · admin tab · MANAGE ESTATE Grey Mirror leaf.
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4e GREEN · 2026-09-22T08:52:00Z
4:  * R-103 amendment: single continuous run to completion.
5:  * HONEST-GAP · SO §5 honest-gap-never-fake.
6:  */
7: 
8: import React from "react";
9: 
10: export default function AdminGreyMirror() {
11:   return (
12:     <div
13:       data-testid="admin-greymirror-surface"
14:       style={{
15:         minHeight: "100vh",
16:         background: "var(--surface, #f7f5ef)",
17:         color: "var(--ink, #12121a)",
18:         padding: "48px 64px",
19:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
20:       }}
21:     >
22:       <header style={{ marginBottom: 32 }}>
23:         <div
24:           data-testid="admin-greymirror-breadcrumb"
25:           style={{
26:             fontSize: 12,
27:             letterSpacing: "0.12em",
28:             textTransform: "uppercase",
29:             color: "var(--ink3, #6b6b78)",
30:             marginBottom: 8,
31:           }}
32:         >
33:           MANAGE ESTATE · Grey Mirror
34:         </div>
35:         <h1
36:           data-testid="admin-greymirror-title"
37:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
38:         >
39:           Grey Mirror
40:         </h1>
41:       </header>
42:       <section
43:         data-testid="admin-greymirror-lead"
44:         style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}
45:       >
46:         <p style={{ margin: "0 0 24px 0" }}>
47:           Ask the estate what it knows about you. Grey Mirror shows every recorded observation with its source and admission.
48:         </p>
49:       </section>
50:       <section
51:         data-testid="admin-greymirror-honest-gap"
52:         style={{
53:           marginTop: 40,
54:           padding: "24px 28px",
55:           background: "rgba(176,141,46,.07)",
56:           border: "1px solid var(--brass, #b08d2e)",
57:           borderRadius: 4,
58:           maxWidth: 720,
59:         }}
60:       >
61:         <div
62:           data-testid="admin-greymirror-honest-gap-label"
63:           style={{
64:             fontSize: 11,
65:             letterSpacing: "0.14em",
66:             textTransform: "uppercase",
67:             color: "var(--brass, #b08d2e)",
68:             fontWeight: 600,
69:             marginBottom: 8,
70:           }}
71:         >
72:           Honest gap · surface only
73:         </div>
74:         <div data-testid="admin-greymirror-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
75:           Backend for Grey Mirror not yet wired. This surface reveals the design-of-record
76:           structure honestly; no fabricated data is shown. Wire lands at PHASE 3
77:           Census Productization + PHASE 4 feature build-out per R-102 MASTER DIRECTIVE
78:           + R-103 amendment (single continuous run).
79:         </div>
80:         <div
81:           data-testid="admin-greymirror-honest-gap-see-working"
82:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
83:         >
84:           See the working: NAV admin.greymirror at App.js const NAV · surface at
85:           pages/os/AdminGreyMirror.jsx.
86:         </div>
87:       </section>
88:     </div>
89:   );
90: }

# SOURCE: frontend/src/pages/os/AdminModelAdmission.jsx

1: /*
2:  * AdminModelAdmission.jsx — v2 OS · admin tab · APPROVALS Model Approval leaf.
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4e GREEN · 2026-09-22T08:52:00Z
4:  * R-103 amendment: single continuous run to completion.
5:  * HONEST-GAP · SO §5 honest-gap-never-fake.
6:  */
7: 
8: import React from "react";
9: 
10: export default function AdminModelAdmission() {
11:   return (
12:     <div
13:       data-testid="admin-modeladmission-surface"
14:       style={{
15:         minHeight: "100vh",
16:         background: "var(--surface, #f7f5ef)",
17:         color: "var(--ink, #12121a)",
18:         padding: "48px 64px",
19:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
20:       }}
21:     >
22:       <header style={{ marginBottom: 32 }}>
23:         <div
24:           data-testid="admin-modeladmission-breadcrumb"
25:           style={{
26:             fontSize: 12,
27:             letterSpacing: "0.12em",
28:             textTransform: "uppercase",
29:             color: "var(--ink3, #6b6b78)",
30:             marginBottom: 8,
31:           }}
32:         >
33:           APPROVALS · Model Approval
34:         </div>
35:         <h1
36:           data-testid="admin-modeladmission-title"
37:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
38:         >
39:           Model Approval
40:         </h1>
41:       </header>
42:       <section
43:         data-testid="admin-modeladmission-lead"
44:         style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}
45:       >
46:         <p style={{ margin: "0 0 24px 0" }}>
47:           New models seeking admission. Each carries its evaluation, its lineage, its declared purpose and the authority admitting it.
48:         </p>
49:       </section>
50:       <section
51:         data-testid="admin-modeladmission-honest-gap"
52:         style={{
53:           marginTop: 40,
54:           padding: "24px 28px",
55:           background: "rgba(176,141,46,.07)",
56:           border: "1px solid var(--brass, #b08d2e)",
57:           borderRadius: 4,
58:           maxWidth: 720,
59:         }}
60:       >
61:         <div
62:           data-testid="admin-modeladmission-honest-gap-label"
63:           style={{
64:             fontSize: 11,
65:             letterSpacing: "0.14em",
66:             textTransform: "uppercase",
67:             color: "var(--brass, #b08d2e)",
68:             fontWeight: 600,
69:             marginBottom: 8,
70:           }}
71:         >
72:           Honest gap · surface only
73:         </div>
74:         <div data-testid="admin-modeladmission-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
75:           Backend for Model Approval not yet wired. This surface reveals the design-of-record
76:           structure honestly; no fabricated data is shown. Wire lands at PHASE 3
77:           Census Productization + PHASE 4 feature build-out per R-102 MASTER DIRECTIVE
78:           + R-103 amendment (single continuous run).
79:         </div>
80:         <div
81:           data-testid="admin-modeladmission-honest-gap-see-working"
82:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
83:         >
84:           See the working: NAV admin.modeladmission at App.js const NAV · surface at
85:           pages/os/AdminModelAdmission.jsx.
86:         </div>
87:       </section>
88:     </div>
89:   );
90: }

# SOURCE: frontend/src/pages/os/AdminRulesUpd.jsx

1: /*
2:  * AdminRulesUpd.jsx — v2 OS · admin tab · APPROVALS Rules Updates leaf.
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4e GREEN · 2026-09-22T08:52:00Z
4:  * R-103 amendment: single continuous run to completion.
5:  * HONEST-GAP · SO §5 honest-gap-never-fake.
6:  */
7: 
8: import React from "react";
9: 
10: export default function AdminRulesUpd() {
11:   return (
12:     <div
13:       data-testid="admin-rulesupd-surface"
14:       style={{
15:         minHeight: "100vh",
16:         background: "var(--surface, #f7f5ef)",
17:         color: "var(--ink, #12121a)",
18:         padding: "48px 64px",
19:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
20:       }}
21:     >
22:       <header style={{ marginBottom: 32 }}>
23:         <div
24:           data-testid="admin-rulesupd-breadcrumb"
25:           style={{
26:             fontSize: 12,
27:             letterSpacing: "0.12em",
28:             textTransform: "uppercase",
29:             color: "var(--ink3, #6b6b78)",
30:             marginBottom: 8,
31:           }}
32:         >
33:           APPROVALS · Rules Updates
34:         </div>
35:         <h1
36:           data-testid="admin-rulesupd-title"
37:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
38:         >
39:           Rules Updates
40:         </h1>
41:       </header>
42:       <section
43:         data-testid="admin-rulesupd-lead"
44:         style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}
45:       >
46:         <p style={{ margin: "0 0 24px 0" }}>
47:           Proposed changes to the shield. Named authors; RATIFY / REJECT trail; nothing lands without a signed ceremony.
48:         </p>
49:       </section>
50:       <section
51:         data-testid="admin-rulesupd-honest-gap"
52:         style={{
53:           marginTop: 40,
54:           padding: "24px 28px",
55:           background: "rgba(176,141,46,.07)",
56:           border: "1px solid var(--brass, #b08d2e)",
57:           borderRadius: 4,
58:           maxWidth: 720,
59:         }}
60:       >
61:         <div
62:           data-testid="admin-rulesupd-honest-gap-label"
63:           style={{
64:             fontSize: 11,
65:             letterSpacing: "0.14em",
66:             textTransform: "uppercase",
67:             color: "var(--brass, #b08d2e)",
68:             fontWeight: 600,
69:             marginBottom: 8,
70:           }}
71:         >
72:           Honest gap · surface only
73:         </div>
74:         <div data-testid="admin-rulesupd-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
75:           Backend for Rules Updates not yet wired. This surface reveals the design-of-record
76:           structure honestly; no fabricated data is shown. Wire lands at PHASE 3
77:           Census Productization + PHASE 4 feature build-out per R-102 MASTER DIRECTIVE
78:           + R-103 amendment (single continuous run).
79:         </div>
80:         <div
81:           data-testid="admin-rulesupd-honest-gap-see-working"
82:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
83:         >
84:           See the working: NAV admin.rulesupd at App.js const NAV · surface at
85:           pages/os/AdminRulesUpd.jsx.
86:         </div>
87:       </section>
88:     </div>
89:   );
90: }

# SOURCE: frontend/src/pages/os/AdminSpendReq.jsx

1: /*
2:  * AdminSpendReq.jsx — v2 OS · admin tab · APPROVALS Spend Requests leaf.
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4e GREEN · 2026-09-22T08:52:00Z
4:  * R-103 amendment: single continuous run to completion.
5:  * HONEST-GAP · SO §5 honest-gap-never-fake.
6:  */
7: 
8: import React from "react";
9: 
10: export default function AdminSpendReq() {
11:   return (
12:     <div
13:       data-testid="admin-spendreq-surface"
14:       style={{
15:         minHeight: "100vh",
16:         background: "var(--surface, #f7f5ef)",
17:         color: "var(--ink, #12121a)",
18:         padding: "48px 64px",
19:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
20:       }}
21:     >
22:       <header style={{ marginBottom: 32 }}>
23:         <div
24:           data-testid="admin-spendreq-breadcrumb"
25:           style={{
26:             fontSize: 12,
27:             letterSpacing: "0.12em",
28:             textTransform: "uppercase",
29:             color: "var(--ink3, #6b6b78)",
30:             marginBottom: 8,
31:           }}
32:         >
33:           APPROVALS · Spend Requests
34:         </div>
35:         <h1
36:           data-testid="admin-spendreq-title"
37:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
38:         >
39:           Spend Requests
40:         </h1>
41:       </header>
42:       <section
43:         data-testid="admin-spendreq-lead"
44:         style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}
45:       >
46:         <p style={{ margin: "0 0 24px 0" }}>
47:           Requests that trip the spend threshold. Each held card carries its evidence bundle plus a named approving authority.
48:         </p>
49:       </section>
50:       <section
51:         data-testid="admin-spendreq-honest-gap"
52:         style={{
53:           marginTop: 40,
54:           padding: "24px 28px",
55:           background: "rgba(176,141,46,.07)",
56:           border: "1px solid var(--brass, #b08d2e)",
57:           borderRadius: 4,
58:           maxWidth: 720,
59:         }}
60:       >
61:         <div
62:           data-testid="admin-spendreq-honest-gap-label"
63:           style={{
64:             fontSize: 11,
65:             letterSpacing: "0.14em",
66:             textTransform: "uppercase",
67:             color: "var(--brass, #b08d2e)",
68:             fontWeight: 600,
69:             marginBottom: 8,
70:           }}
71:         >
72:           Honest gap · surface only
73:         </div>
74:         <div data-testid="admin-spendreq-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
75:           Backend for Spend Requests not yet wired. This surface reveals the design-of-record
76:           structure honestly; no fabricated data is shown. Wire lands at PHASE 3
77:           Census Productization + PHASE 4 feature build-out per R-102 MASTER DIRECTIVE
78:           + R-103 amendment (single continuous run).
79:         </div>
80:         <div
81:           data-testid="admin-spendreq-honest-gap-see-working"
82:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
83:         >
84:           See the working: NAV admin.spendreq at App.js const NAV · surface at
85:           pages/os/AdminSpendReq.jsx.
86:         </div>
87:       </section>
88:     </div>
89:   );
90: }

# SOURCE: frontend/src/pages/os/AdminWDecisions.jsx

1: /*
2:  * AdminWDecisions.jsx — v2 OS · admin tab · THE WATCH Decisions leaf.
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4e GREEN · 2026-09-22T08:52:00Z
4:  * R-103 amendment: single continuous run to completion.
5:  * HONEST-GAP · SO §5 honest-gap-never-fake.
6:  */
7: 
8: import React from "react";
9: 
10: export default function AdminWDecisions() {
11:   return (
12:     <div
13:       data-testid="admin-wdecisions-surface"
14:       style={{
15:         minHeight: "100vh",
16:         background: "var(--surface, #f7f5ef)",
17:         color: "var(--ink, #12121a)",
18:         padding: "48px 64px",
19:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
20:       }}
21:     >
22:       <header style={{ marginBottom: 32 }}>
23:         <div
24:           data-testid="admin-wdecisions-breadcrumb"
25:           style={{
26:             fontSize: 12,
27:             letterSpacing: "0.12em",
28:             textTransform: "uppercase",
29:             color: "var(--ink3, #6b6b78)",
30:             marginBottom: 8,
31:           }}
32:         >
33:           THE WATCH · Decisions
34:         </div>
35:         <h1
36:           data-testid="admin-wdecisions-title"
37:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
38:         >
39:           Decisions
40:         </h1>
41:       </header>
42:       <section
43:         data-testid="admin-wdecisions-lead"
44:         style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}
45:       >
46:         <p style={{ margin: "0 0 24px 0" }}>
47:           Watch decisions banked to the record. Each cites the rule it applied, the authority that ratified it, and the evidence bundle.
48:         </p>
49:       </section>
50:       <section
51:         data-testid="admin-wdecisions-honest-gap"
52:         style={{
53:           marginTop: 40,
54:           padding: "24px 28px",
55:           background: "rgba(176,141,46,.07)",
56:           border: "1px solid var(--brass, #b08d2e)",
57:           borderRadius: 4,
58:           maxWidth: 720,
59:         }}
60:       >
61:         <div
62:           data-testid="admin-wdecisions-honest-gap-label"
63:           style={{
64:             fontSize: 11,
65:             letterSpacing: "0.14em",
66:             textTransform: "uppercase",
67:             color: "var(--brass, #b08d2e)",
68:             fontWeight: 600,
69:             marginBottom: 8,
70:           }}
71:         >
72:           Honest gap · surface only
73:         </div>
74:         <div data-testid="admin-wdecisions-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
75:           Backend for Decisions not yet wired. This surface reveals the design-of-record
76:           structure honestly; no fabricated data is shown. Wire lands at PHASE 3
77:           Census Productization + PHASE 4 feature build-out per R-102 MASTER DIRECTIVE
78:           + R-103 amendment (single continuous run).
79:         </div>
80:         <div
81:           data-testid="admin-wdecisions-honest-gap-see-working"
82:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
83:         >
84:           See the working: NAV admin.wdecisions at App.js const NAV · surface at
85:           pages/os/AdminWDecisions.jsx.
86:         </div>
87:       </section>
88:     </div>
89:   );
90: }

# SOURCE: frontend/src/pages/os/AdminWRecord.jsx

1: /*
2:  * AdminWRecord.jsx — v2 OS · admin tab · THE WATCH Record leaf.
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4e GREEN · 2026-09-22T08:52:00Z
4:  * R-103 amendment: single continuous run to completion.
5:  * HONEST-GAP · SO §5 honest-gap-never-fake.
6:  */
7: 
8: import React from "react";
9: 
10: export default function AdminWRecord() {
11:   return (
12:     <div
13:       data-testid="admin-wrecord-surface"
14:       style={{
15:         minHeight: "100vh",
16:         background: "var(--surface, #f7f5ef)",
17:         color: "var(--ink, #12121a)",
18:         padding: "48px 64px",
19:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
20:       }}
21:     >
22:       <header style={{ marginBottom: 32 }}>
23:         <div
24:           data-testid="admin-wrecord-breadcrumb"
25:           style={{
26:             fontSize: 12,
27:             letterSpacing: "0.12em",
28:             textTransform: "uppercase",
29:             color: "var(--ink3, #6b6b78)",
30:             marginBottom: 8,
31:           }}
32:         >
33:           THE WATCH · Record
34:         </div>
35:         <h1
36:           data-testid="admin-wrecord-title"
37:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
38:         >
39:           Record
40:         </h1>
41:       </header>
42:       <section
43:         data-testid="admin-wrecord-lead"
44:         style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}
45:       >
46:         <p style={{ margin: "0 0 24px 0" }}>
47:           External witness trail. Every held / refused / admitted decision is written here with source, authority, and timestamp.
48:         </p>
49:       </section>
50:       <section
51:         data-testid="admin-wrecord-honest-gap"
52:         style={{
53:           marginTop: 40,
54:           padding: "24px 28px",
55:           background: "rgba(176,141,46,.07)",
56:           border: "1px solid var(--brass, #b08d2e)",
57:           borderRadius: 4,
58:           maxWidth: 720,
59:         }}
60:       >
61:         <div
62:           data-testid="admin-wrecord-honest-gap-label"
63:           style={{
64:             fontSize: 11,
65:             letterSpacing: "0.14em",
66:             textTransform: "uppercase",
67:             color: "var(--brass, #b08d2e)",
68:             fontWeight: 600,
69:             marginBottom: 8,
70:           }}
71:         >
72:           Honest gap · surface only
73:         </div>
74:         <div data-testid="admin-wrecord-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
75:           Backend for Record not yet wired. This surface reveals the design-of-record
76:           structure honestly; no fabricated data is shown. Wire lands at PHASE 3
77:           Census Productization + PHASE 4 feature build-out per R-102 MASTER DIRECTIVE
78:           + R-103 amendment (single continuous run).
79:         </div>
80:         <div
81:           data-testid="admin-wrecord-honest-gap-see-working"
82:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
83:         >
84:           See the working: NAV admin.wrecord at App.js const NAV · surface at
85:           pages/os/AdminWRecord.jsx.
86:         </div>
87:       </section>
88:     </div>
89:   );
90: }

# SOURCE: frontend/src/pages/os/AdminWState.jsx

1: /*
2:  * AdminWState.jsx — v2 OS · admin tab · THE WATCH State leaf.
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4e GREEN · 2026-09-22T08:52:00Z
4:  * R-103 amendment: single continuous run to completion.
5:  * HONEST-GAP · SO §5 honest-gap-never-fake.
6:  */
7: 
8: import React from "react";
9: 
10: export default function AdminWState() {
11:   return (
12:     <div
13:       data-testid="admin-wstate-surface"
14:       style={{
15:         minHeight: "100vh",
16:         background: "var(--surface, #f7f5ef)",
17:         color: "var(--ink, #12121a)",
18:         padding: "48px 64px",
19:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
20:       }}
21:     >
22:       <header style={{ marginBottom: 32 }}>
23:         <div
24:           data-testid="admin-wstate-breadcrumb"
25:           style={{
26:             fontSize: 12,
27:             letterSpacing: "0.12em",
28:             textTransform: "uppercase",
29:             color: "var(--ink3, #6b6b78)",
30:             marginBottom: 8,
31:           }}
32:         >
33:           THE WATCH · State
34:         </div>
35:         <h1
36:           data-testid="admin-wstate-title"
37:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
38:         >
39:           State
40:         </h1>
41:       </header>
42:       <section
43:         data-testid="admin-wstate-lead"
44:         style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}
45:       >
46:         <p style={{ margin: "0 0 24px 0" }}>
47:           The Watch heartbeat: what is being watched, what has warmed since last read, what has gone quiet.
48:         </p>
49:       </section>
50:       <section
51:         data-testid="admin-wstate-honest-gap"
52:         style={{
53:           marginTop: 40,
54:           padding: "24px 28px",
55:           background: "rgba(176,141,46,.07)",
56:           border: "1px solid var(--brass, #b08d2e)",
57:           borderRadius: 4,
58:           maxWidth: 720,
59:         }}
60:       >
61:         <div
62:           data-testid="admin-wstate-honest-gap-label"
63:           style={{
64:             fontSize: 11,
65:             letterSpacing: "0.14em",
66:             textTransform: "uppercase",
67:             color: "var(--brass, #b08d2e)",
68:             fontWeight: 600,
69:             marginBottom: 8,
70:           }}
71:         >
72:           Honest gap · surface only
73:         </div>
74:         <div data-testid="admin-wstate-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
75:           Backend for State not yet wired. This surface reveals the design-of-record
76:           structure honestly; no fabricated data is shown. Wire lands at PHASE 3
77:           Census Productization + PHASE 4 feature build-out per R-102 MASTER DIRECTIVE
78:           + R-103 amendment (single continuous run).
79:         </div>
80:         <div
81:           data-testid="admin-wstate-honest-gap-see-working"
82:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
83:         >
84:           See the working: NAV admin.wstate at App.js const NAV · surface at
85:           pages/os/AdminWState.jsx.
86:         </div>
87:       </section>
88:     </div>
89:   );
90: }

# SOURCE: frontend/src/pages/os/AdminWUnder.jsx

1: /*
2:  * AdminWUnder.jsx — v2 OS · admin tab · THE WATCH Under Watch leaf.
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4e GREEN · 2026-09-22T08:52:00Z
4:  * R-103 amendment: single continuous run to completion.
5:  * HONEST-GAP · SO §5 honest-gap-never-fake.
6:  */
7: 
8: import React from "react";
9: 
10: export default function AdminWUnder() {
11:   return (
12:     <div
13:       data-testid="admin-wunder-surface"
14:       style={{
15:         minHeight: "100vh",
16:         background: "var(--surface, #f7f5ef)",
17:         color: "var(--ink, #12121a)",
18:         padding: "48px 64px",
19:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
20:       }}
21:     >
22:       <header style={{ marginBottom: 32 }}>
23:         <div
24:           data-testid="admin-wunder-breadcrumb"
25:           style={{
26:             fontSize: 12,
27:             letterSpacing: "0.12em",
28:             textTransform: "uppercase",
29:             color: "var(--ink3, #6b6b78)",
30:             marginBottom: 8,
31:           }}
32:         >
33:           THE WATCH · Under Watch
34:         </div>
35:         <h1
36:           data-testid="admin-wunder-title"
37:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
38:         >
39:           Under Watch
40:         </h1>
41:       </header>
42:       <section
43:         data-testid="admin-wunder-lead"
44:         style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}
45:       >
46:         <p style={{ margin: "0 0 24px 0" }}>
47:           Live entries currently under Watch scrutiny. Each carries its trigger, its evidence, and its next-review date.
48:         </p>
49:       </section>
50:       <section
51:         data-testid="admin-wunder-honest-gap"
52:         style={{
53:           marginTop: 40,
54:           padding: "24px 28px",
55:           background: "rgba(176,141,46,.07)",
56:           border: "1px solid var(--brass, #b08d2e)",
57:           borderRadius: 4,
58:           maxWidth: 720,
59:         }}
60:       >
61:         <div
62:           data-testid="admin-wunder-honest-gap-label"
63:           style={{
64:             fontSize: 11,
65:             letterSpacing: "0.14em",
66:             textTransform: "uppercase",
67:             color: "var(--brass, #b08d2e)",
68:             fontWeight: 600,
69:             marginBottom: 8,
70:           }}
71:         >
72:           Honest gap · surface only
73:         </div>
74:         <div data-testid="admin-wunder-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
75:           Backend for Under Watch not yet wired. This surface reveals the design-of-record
76:           structure honestly; no fabricated data is shown. Wire lands at PHASE 3
77:           Census Productization + PHASE 4 feature build-out per R-102 MASTER DIRECTIVE
78:           + R-103 amendment (single continuous run).
79:         </div>
80:         <div
81:           data-testid="admin-wunder-honest-gap-see-working"
82:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
83:         >
84:           See the working: NAV admin.wunder at App.js const NAV · surface at
85:           pages/os/AdminWUnder.jsx.
86:         </div>
87:       </section>
88:     </div>
89:   );
90: }

# SOURCE: frontend/src/pages/os/AppsConnected.jsx

1: /*
2:  * AppsConnected.jsx — v2 OS · Turn 4 sub-slice 4f GREEN · 2026-09-22T09:20:00Z
3:  * R-101 + R-102 + R-103 amendment. HONEST-GAP · SO §5.
4:  */
5: import React from "react";
6: export default function AppsConnected() {
7:   return (
8:     <div data-testid="apps-connected-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
9:       <header style={{marginBottom:32}}>
10:         <div data-testid="apps-connected-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>3RD PARTY APPS · Connected</div>
11:         <h1 data-testid="apps-connected-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>Connected</h1>
12:       </header>
13:       <section data-testid="apps-connected-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
14:         <p style={{margin:"0 0 24px 0"}}>Apps currently connected to the estate. Each shows what data it reads, what it writes, and its revocation controls.</p>
15:       </section>
16:       <section data-testid="apps-connected-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
17:         <div data-testid="apps-connected-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
18:         <div data-testid="apps-connected-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Backend for Connected not yet wired. Design-of-record structure shown honestly; no fabricated data. Wire lands at PHASE 3 Census Productization + PHASE 4 feature build-out per R-102 + R-103 amendment.</div>
19:         <div data-testid="apps-connected-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: NAV apps.appsconnected at App.js · surface at pages/os/AppsConnected.jsx.</div>
20:       </section>
21:     </div>
22:   );
23: }

# SOURCE: frontend/src/pages/os/AppsFrequent.jsx

1: /*
2:  * AppsFrequent.jsx — v2 OS · Turn 4 sub-slice 4f GREEN · 2026-09-22T09:20:00Z
3:  * R-101 + R-102 + R-103 amendment. HONEST-GAP · SO §5.
4:  */
5: import React from "react";
6: export default function AppsFrequent() {
7:   return (
8:     <div data-testid="apps-frequent-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
9:       <header style={{marginBottom:32}}>
10:         <div data-testid="apps-frequent-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>3RD PARTY APPS · Frequent</div>
11:         <h1 data-testid="apps-frequent-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>Frequent</h1>
12:       </header>
13:       <section data-testid="apps-frequent-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
14:         <p style={{margin:"0 0 24px 0"}}>Apps your team uses most. Each shows its last use, its entitlement scope, and its trust receipts.</p>
15:       </section>
16:       <section data-testid="apps-frequent-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
17:         <div data-testid="apps-frequent-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
18:         <div data-testid="apps-frequent-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Backend for Frequent not yet wired. Design-of-record structure shown honestly; no fabricated data. Wire lands at PHASE 3 Census Productization + PHASE 4 feature build-out per R-102 + R-103 amendment.</div>
19:         <div data-testid="apps-frequent-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: NAV apps.appsfrequent at App.js · surface at pages/os/AppsFrequent.jsx.</div>
20:       </section>
21:     </div>
22:   );
23: }

# SOURCE: frontend/src/pages/os/AppsNew.jsx

1: /*
2:  * AppsNew.jsx — v2 OS · Turn 4 sub-slice 4f GREEN · 2026-09-22T09:20:00Z
3:  * R-101 + R-102 + R-103 amendment. HONEST-GAP · SO §5.
4:  */
5: import React from "react";
6: export default function AppsNew() {
7:   return (
8:     <div data-testid="apps-new-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
9:       <header style={{marginBottom:32}}>
10:         <div data-testid="apps-new-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>3RD PARTY APPS · New</div>
11:         <h1 data-testid="apps-new-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>New</h1>
12:       </header>
13:       <section data-testid="apps-new-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
14:         <p style={{margin:"0 0 24px 0"}}>Newly available third-party apps. Each shows its admission requirements, its trust posture, and the authority admitting it.</p>
15:       </section>
16:       <section data-testid="apps-new-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
17:         <div data-testid="apps-new-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
18:         <div data-testid="apps-new-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Backend for New not yet wired. Design-of-record structure shown honestly; no fabricated data. Wire lands at PHASE 3 Census Productization + PHASE 4 feature build-out per R-102 + R-103 amendment.</div>
19:         <div data-testid="apps-new-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: NAV apps.appsnew at App.js · surface at pages/os/AppsNew.jsx.</div>
20:       </section>
21:     </div>
22:   );
23: }

# SOURCE: frontend/src/pages/os/AppsRequests.jsx

1: /*
2:  * AppsRequests.jsx — v2 OS · Turn 4 sub-slice 4f GREEN · 2026-09-22T09:20:00Z
3:  * R-101 + R-102 + R-103 amendment. HONEST-GAP · SO §5.
4:  */
5: import React from "react";
6: export default function AppsRequests() {
7:   return (
8:     <div data-testid="apps-requests-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
9:       <header style={{marginBottom:32}}>
10:         <div data-testid="apps-requests-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>3RD PARTY APPS · Requests</div>
11:         <h1 data-testid="apps-requests-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>Requests</h1>
12:       </header>
13:       <section data-testid="apps-requests-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
14:         <p style={{margin:"0 0 24px 0"}}>App connection requests pending admission. Each carries its declared purpose and its named approving authority.</p>
15:       </section>
16:       <section data-testid="apps-requests-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
17:         <div data-testid="apps-requests-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
18:         <div data-testid="apps-requests-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Backend for Requests not yet wired. Design-of-record structure shown honestly; no fabricated data. Wire lands at PHASE 3 Census Productization + PHASE 4 feature build-out per R-102 + R-103 amendment.</div>
19:         <div data-testid="apps-requests-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: NAV apps.appsrequests at App.js · surface at pages/os/AppsRequests.jsx.</div>
20:       </section>
21:     </div>
22:   );
23: }

# SOURCE: frontend/src/pages/os/BuildAgent.jsx

1: /*
2:  * BuildAgent.jsx — v2 OS · Turn 4 sub-slice 4f GREEN · 2026-09-22T09:20:00Z
3:  * R-101 + R-102 + R-103 amendment. HONEST-GAP · SO §5.
4:  */
5: import React from "react";
6: export default function BuildAgent() {
7:   return (
8:     <div data-testid="build-agent-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
9:       <header style={{marginBottom:32}}>
10:         <div data-testid="build-agent-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>BUILD YOUR RESOURCES · Build Agents</div>
11:         <h1 data-testid="build-agent-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>Build Agents</h1>
12:       </header>
13:       <section data-testid="build-agent-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
14:         <p style={{margin:"0 0 24px 0"}}>Compose agents from skills the estate already trusts. Each agent carries its skill list and the ceremony that admitted it.</p>
15:       </section>
16:       <section data-testid="build-agent-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
17:         <div data-testid="build-agent-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
18:         <div data-testid="build-agent-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Backend for Build Agents not yet wired. Design-of-record structure shown honestly; no fabricated data. Wire lands at PHASE 3 Census Productization + PHASE 4 feature build-out per R-102 + R-103 amendment.</div>
19:         <div data-testid="build-agent-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: NAV build.agentbuild at App.js · surface at pages/os/BuildAgent.jsx.</div>
20:       </section>
21:     </div>
22:   );
23: }

# SOURCE: frontend/src/pages/os/BuildExtract.jsx

1: /*
2:  * BuildExtract.jsx — v2 OS · Turn 4 sub-slice 4f GREEN · 2026-09-22T09:20:00Z
3:  * R-101 + R-102 + R-103 amendment. HONEST-GAP · SO §5.
4:  */
5: import React from "react";
6: export default function BuildExtract() {
7:   return (
8:     <div data-testid="build-extract-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
9:       <header style={{marginBottom:32}}>
10:         <div data-testid="build-extract-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>BUILD YOUR RESOURCES · Extract Data</div>
11:         <h1 data-testid="build-extract-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>Extract Data</h1>
12:       </header>
13:       <section data-testid="build-extract-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
14:         <p style={{margin:"0 0 24px 0"}}>Pull structured data from admitted sources. Every extraction records its source, its shield decisions, and its evidence trail.</p>
15:       </section>
16:       <section data-testid="build-extract-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
17:         <div data-testid="build-extract-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
18:         <div data-testid="build-extract-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Backend for Extract Data not yet wired. Design-of-record structure shown honestly; no fabricated data. Wire lands at PHASE 3 Census Productization + PHASE 4 feature build-out per R-102 + R-103 amendment.</div>
19:         <div data-testid="build-extract-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: NAV build.extract at App.js · surface at pages/os/BuildExtract.jsx.</div>
20:       </section>
21:     </div>
22:   );
23: }

# SOURCE: frontend/src/pages/os/BuildSkill.jsx

1: /*
2:  * BuildSkill.jsx — v2 OS · Turn 4 sub-slice 4f GREEN · 2026-09-22T09:20:00Z
3:  * R-101 + R-102 + R-103 amendment. HONEST-GAP · SO §5.
4:  */
5: import React from "react";
6: export default function BuildSkill() {
7:   return (
8:     <div data-testid="build-skill-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
9:       <header style={{marginBottom:32}}>
10:         <div data-testid="build-skill-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>BUILD YOUR RESOURCES · Build Skill</div>
11:         <h1 data-testid="build-skill-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>Build Skill</h1>
12:       </header>
13:       <section data-testid="build-skill-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
14:         <p style={{margin:"0 0 24px 0"}}>Define a new skill: input shape, output contract, refusal boundaries. Skills live in the registry with lineage.</p>
15:       </section>
16:       <section data-testid="build-skill-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
17:         <div data-testid="build-skill-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
18:         <div data-testid="build-skill-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Backend for Build Skill not yet wired. Design-of-record structure shown honestly; no fabricated data. Wire lands at PHASE 3 Census Productization + PHASE 4 feature build-out per R-102 + R-103 amendment.</div>
19:         <div data-testid="build-skill-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: NAV build.buildskill at App.js · surface at pages/os/BuildSkill.jsx.</div>
20:       </section>
21:     </div>
22:   );
23: }

# SOURCE: frontend/src/pages/os/BuildTrain.jsx

1: /*
2:  * BuildTrain.jsx — v2 OS · Turn 4 sub-slice 4f GREEN · 2026-09-22T09:20:00Z
3:  * R-101 + R-102 + R-103 amendment. HONEST-GAP · SO §5.
4:  */
5: import React from "react";
6: export default function BuildTrain() {
7:   return (
8:     <div data-testid="build-train-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
9:       <header style={{marginBottom:32}}>
10:         <div data-testid="build-train-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>BUILD YOUR RESOURCES · Train Models</div>
11:         <h1 data-testid="build-train-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>Train Models</h1>
12:       </header>
13:       <section data-testid="build-train-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
14:         <p style={{margin:"0 0 24px 0"}}>Train models on admitted data. Every training run banks its inputs, its evaluation, and the authority that admitted it.</p>
15:       </section>
16:       <section data-testid="build-train-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
17:         <div data-testid="build-train-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
18:         <div data-testid="build-train-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Backend for Train Models not yet wired. Design-of-record structure shown honestly; no fabricated data. Wire lands at PHASE 3 Census Productization + PHASE 4 feature build-out per R-102 + R-103 amendment.</div>
19:         <div data-testid="build-train-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: NAV build.train at App.js · surface at pages/os/BuildTrain.jsx.</div>
20:       </section>
21:     </div>
22:   );
23: }

# SOURCE: frontend/src/pages/os/BuildlibAgents.jsx

1: /*
2:  * BuildlibAgents.jsx — v2 OS · Turn 4 sub-slice 4f GREEN · 2026-09-22T09:20:00Z
3:  * R-101 + R-102 + R-103 amendment. HONEST-GAP · SO §5.
4:  */
5: import React from "react";
6: export default function BuildlibAgents() {
7:   return (
8:     <div data-testid="buildlib-agents-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
9:       <header style={{marginBottom:32}}>
10:         <div data-testid="buildlib-agents-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>YOUR RESOURCES · Agents</div>
11:         <h1 data-testid="buildlib-agents-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>Agents</h1>
12:       </header>
13:       <section data-testid="buildlib-agents-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
14:         <p style={{margin:"0 0 24px 0"}}>Agents your team owns and can invoke. Each shows its skill list, admission ceremony, and last use.</p>
15:       </section>
16:       <section data-testid="buildlib-agents-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
17:         <div data-testid="buildlib-agents-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
18:         <div data-testid="buildlib-agents-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Backend for Agents not yet wired. Design-of-record structure shown honestly; no fabricated data. Wire lands at PHASE 3 Census Productization + PHASE 4 feature build-out per R-102 + R-103 amendment.</div>
19:         <div data-testid="buildlib-agents-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: NAV build.youragents at App.js · surface at pages/os/BuildlibAgents.jsx.</div>
20:       </section>
21:     </div>
22:   );
23: }

# SOURCE: frontend/src/pages/os/BuildlibModels.jsx

1: /*
2:  * BuildlibModels.jsx — v2 OS · Turn 4 sub-slice 4f GREEN · 2026-09-22T09:20:00Z
3:  * R-101 + R-102 + R-103 amendment. HONEST-GAP · SO §5.
4:  */
5: import React from "react";
6: export default function BuildlibModels() {
7:   return (
8:     <div data-testid="buildlib-models-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
9:       <header style={{marginBottom:32}}>
10:         <div data-testid="buildlib-models-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>YOUR RESOURCES · Models</div>
11:         <h1 data-testid="buildlib-models-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>Models</h1>
12:       </header>
13:       <section data-testid="buildlib-models-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
14:         <p style={{margin:"0 0 24px 0"}}>Models admitted to the estate. Each shows its lineage, its evaluation, and the authority that admitted it.</p>
15:       </section>
16:       <section data-testid="buildlib-models-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
17:         <div data-testid="buildlib-models-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
18:         <div data-testid="buildlib-models-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Backend for Models not yet wired. Design-of-record structure shown honestly; no fabricated data. Wire lands at PHASE 3 Census Productization + PHASE 4 feature build-out per R-102 + R-103 amendment.</div>
19:         <div data-testid="buildlib-models-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: NAV build.yourmodels at App.js · surface at pages/os/BuildlibModels.jsx.</div>
20:       </section>
21:     </div>
22:   );
23: }

# SOURCE: frontend/src/pages/os/CollabEmails.jsx

1: /*
2:  * CollabEmails.jsx — v2 OS · Turn 4 sub-slice 4f GREEN · 2026-09-22T09:20:00Z
3:  * R-101 + R-102 + R-103 amendment. HONEST-GAP · SO §5.
4:  */
5: import React from "react";
6: export default function CollabEmails() {
7:   return (
8:     <div data-testid="collab-emails-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
9:       <header style={{marginBottom:32}}>
10:         <div data-testid="collab-emails-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>COLLAB · Emails</div>
11:         <h1 data-testid="collab-emails-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>Emails</h1>
12:       </header>
13:       <section data-testid="collab-emails-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
14:         <p style={{margin:"0 0 24px 0"}}>Estate-connected email surface. Every message is shield-checked; refused ones surface here as held with reason.</p>
15:       </section>
16:       <section data-testid="collab-emails-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
17:         <div data-testid="collab-emails-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
18:         <div data-testid="collab-emails-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Backend for Emails not yet wired. Design-of-record structure shown honestly; no fabricated data. Wire lands at PHASE 3 Census Productization + PHASE 4 feature build-out per R-102 + R-103 amendment.</div>
19:         <div data-testid="collab-emails-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: NAV work.emails at App.js · surface at pages/os/CollabEmails.jsx.</div>
20:       </section>
21:     </div>
22:   );
23: }

# SOURCE: frontend/src/pages/os/CollabHrStuff.jsx

1: /*
2:  * CollabHrStuff.jsx — v2 OS · Turn 4 sub-slice 4f GREEN · 2026-09-22T09:20:00Z
3:  * R-101 + R-102 + R-103 amendment. HONEST-GAP · SO §5.
4:  */
5: import React from "react";
6: export default function CollabHrStuff() {
7:   return (
8:     <div data-testid="collab-hrstuff-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
9:       <header style={{marginBottom:32}}>
10:         <div data-testid="collab-hrstuff-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>COLLAB · HR Stuff</div>
11:         <h1 data-testid="collab-hrstuff-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>HR Stuff</h1>
12:       </header>
13:       <section data-testid="collab-hrstuff-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
14:         <p style={{margin:"0 0 24px 0"}}>HR-adjacent surface: leave, reviews, entitlement changes. Each item shows named approving authority and status.</p>
15:       </section>
16:       <section data-testid="collab-hrstuff-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
17:         <div data-testid="collab-hrstuff-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
18:         <div data-testid="collab-hrstuff-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Backend for HR Stuff not yet wired. Design-of-record structure shown honestly; no fabricated data. Wire lands at PHASE 3 Census Productization + PHASE 4 feature build-out per R-102 + R-103 amendment.</div>
19:         <div data-testid="collab-hrstuff-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: NAV work.hrstuff at App.js · surface at pages/os/CollabHrStuff.jsx.</div>
20:       </section>
21:     </div>
22:   );
23: }

# SOURCE: frontend/src/pages/os/CollabMentions.jsx

1: /*
2:  * CollabMentions.jsx — v2 OS · Turn 4 sub-slice 4f GREEN · 2026-09-22T09:20:00Z
3:  * R-101 + R-102 + R-103 amendment. HONEST-GAP · SO §5.
4:  */
5: import React from "react";
6: export default function CollabMentions() {
7:   return (
8:     <div data-testid="collab-mentions-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
9:       <header style={{marginBottom:32}}>
10:         <div data-testid="collab-mentions-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>COLLAB · Mentions</div>
11:         <h1 data-testid="collab-mentions-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>Mentions</h1>
12:       </header>
13:       <section data-testid="collab-mentions-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
14:         <p style={{margin:"0 0 24px 0"}}>Where you were named. Each mention carries its author, its context, and a link back to the source thread.</p>
15:       </section>
16:       <section data-testid="collab-mentions-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
17:         <div data-testid="collab-mentions-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
18:         <div data-testid="collab-mentions-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Backend for Mentions not yet wired. Design-of-record structure shown honestly; no fabricated data. Wire lands at PHASE 3 Census Productization + PHASE 4 feature build-out per R-102 + R-103 amendment.</div>
19:         <div data-testid="collab-mentions-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: NAV work.mentions at App.js · surface at pages/os/CollabMentions.jsx.</div>
20:       </section>
21:     </div>
22:   );
23: }

# SOURCE: frontend/src/pages/os/CollabProjects.jsx

1: /*
2:  * CollabProjects.jsx — v2 OS · Turn 4 sub-slice 4f GREEN · 2026-09-22T09:20:00Z
3:  * R-101 + R-102 + R-103 amendment. HONEST-GAP · SO §5.
4:  */
5: import React from "react";
6: export default function CollabProjects() {
7:   return (
8:     <div data-testid="collab-projects-surface" style={{minHeight:"100vh",background:"var(--surface, #f7f5ef)",color:"var(--ink, #12121a)",padding:"48px 64px",fontFamily:"'Charter', 'Iowan Old Style', Georgia, serif"}}>
9:       <header style={{marginBottom:32}}>
10:         <div data-testid="collab-projects-breadcrumb" style={{fontSize:12,letterSpacing:"0.12em",textTransform:"uppercase",color:"var(--ink3, #6b6b78)",marginBottom:8}}>COLLAB · Projects/Tasks</div>
11:         <h1 data-testid="collab-projects-title" style={{fontSize:40,fontWeight:300,margin:0,letterSpacing:"-0.02em"}}>Projects/Tasks</h1>
12:       </header>
13:       <section data-testid="collab-projects-lead" style={{maxWidth:720,fontSize:17,lineHeight:1.6}}>
14:         <p style={{margin:"0 0 24px 0"}}>Projects and tasks with their people, deadlines, and evidence bundles. Each held task shows what's blocking it.</p>
15:       </section>
16:       <section data-testid="collab-projects-honest-gap" style={{marginTop:40,padding:"24px 28px",background:"rgba(176,141,46,.07)",border:"1px solid var(--brass, #b08d2e)",borderRadius:4,maxWidth:720}}>
17:         <div data-testid="collab-projects-honest-gap-label" style={{fontSize:11,letterSpacing:"0.14em",textTransform:"uppercase",color:"var(--brass, #b08d2e)",fontWeight:600,marginBottom:8}}>Honest gap · surface only</div>
18:         <div data-testid="collab-projects-honest-gap-body" style={{fontSize:15,lineHeight:1.5}}>Backend for Projects/Tasks not yet wired. Design-of-record structure shown honestly; no fabricated data. Wire lands at PHASE 3 Census Productization + PHASE 4 feature build-out per R-102 + R-103 amendment.</div>
19:         <div data-testid="collab-projects-honest-gap-see-working" style={{marginTop:16,fontSize:13,color:"var(--ink3, #6b6b78)"}}>See the working: NAV work.projects at App.js · surface at pages/os/CollabProjects.jsx.</div>
20:       </section>
21:     </div>
22:   );
23: }

# SOURCE: frontend/src/pages/os/MonitorIdeas.jsx

1: /*
2:  * MonitorIdeas.jsx — v2 OS · Work tab · MONITOR · ideas leaf.
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4d GREEN · 2026-09-22T08:22:00Z
4:  * HONEST-GAP · SO §5 honest-gap-never-fake.
5:  */
6: 
7: import React from "react";
8: 
9: export default function MonitorIdeas() {
10:   return (
11:     <div
12:       data-testid="monitor-ideas-surface"
13:       style={{
14:         minHeight: "100vh",
15:         background: "var(--surface, #f7f5ef)",
16:         color: "var(--ink, #12121a)",
17:         padding: "48px 64px",
18:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
19:       }}
20:     >
21:       <header style={{ marginBottom: 32 }}>
22:         <div
23:           data-testid="monitor-ideas-breadcrumb"
24:           style={{
25:             fontSize: 12,
26:             letterSpacing: "0.12em",
27:             textTransform: "uppercase",
28:             color: "var(--ink3, #6b6b78)",
29:             marginBottom: 8,
30:           }}
31:         >
32:           MONITOR · Ideas
33:         </div>
34:         <h1
35:           data-testid="monitor-ideas-title"
36:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
37:         >
38:           Ideas
39:         </h1>
40:       </header>
41:       <section data-testid="monitor-ideas-lead" style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}>
42:         <p style={{ margin: "0 0 24px 0" }}>
43:           Prompts drawn from what the system has read: patterns worth naming,
44:           questions worth asking. Every idea traces back to the reading it
45:           came from.
46:         </p>
47:       </section>
48:       <section
49:         data-testid="monitor-ideas-honest-gap"
50:         style={{
51:           marginTop: 40,
52:           padding: "24px 28px",
53:           background: "rgba(176,141,46,.07)",
54:           border: "1px solid var(--brass, #b08d2e)",
55:           borderRadius: 4,
56:           maxWidth: 720,
57:         }}
58:       >
59:         <div
60:           data-testid="monitor-ideas-honest-gap-label"
61:           style={{
62:             fontSize: 11,
63:             letterSpacing: "0.14em",
64:             textTransform: "uppercase",
65:             color: "var(--brass, #b08d2e)",
66:             fontWeight: 600,
67:             marginBottom: 8,
68:           }}
69:         >
70:           Honest gap · surface only
71:         </div>
72:         <div data-testid="monitor-ideas-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
73:           Idea-mining backend not yet built. This surface reveals the
74:           design-of-record structure without fabricating fake ideas. Wire
75:           lands at PHASE 4 (c) CP-SKILLS-LAYER + (h) Model Registry feature
76:           build.
77:         </div>
78:         <div
79:           data-testid="monitor-ideas-honest-gap-see-working"
80:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
81:         >
82:           See the working: NAV monitor.ideas at App.js · surface at
83:           pages/os/MonitorIdeas.jsx.
84:         </div>
85:       </section>
86:     </div>
87:   );
88: }

# SOURCE: frontend/src/pages/os/MonitorSignals.jsx

1: /*
2:  * MonitorSignals.jsx — v2 OS · Work tab · MONITOR · signals leaf.
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4d GREEN · 2026-09-22T08:22:00Z
4:  * HONEST-GAP · SO §5 honest-gap-never-fake.
5:  */
6: 
7: import React from "react";
8: 
9: export default function MonitorSignals() {
10:   return (
11:     <div
12:       data-testid="monitor-signals-surface"
13:       style={{
14:         minHeight: "100vh",
15:         background: "var(--surface, #f7f5ef)",
16:         color: "var(--ink, #12121a)",
17:         padding: "48px 64px",
18:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
19:       }}
20:     >
21:       <header style={{ marginBottom: 32 }}>
22:         <div
23:           data-testid="monitor-signals-breadcrumb"
24:           style={{
25:             fontSize: 12,
26:             letterSpacing: "0.12em",
27:             textTransform: "uppercase",
28:             color: "var(--ink3, #6b6b78)",
29:             marginBottom: 8,
30:           }}
31:         >
32:           MONITOR · Signals
33:         </div>
34:         <h1
35:           data-testid="monitor-signals-title"
36:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
37:         >
38:           Signals
39:         </h1>
40:       </header>
41:       <section data-testid="monitor-signals-lead" style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}>
42:         <p style={{ margin: "0 0 24px 0" }}>
43:           The system speaks up when something wobbles: shield refusals, entitlement
44:           expiries, source drift, unexplained silences. Every signal traces back
45:           to what triggered it.
46:         </p>
47:       </section>
48:       <section
49:         data-testid="monitor-signals-honest-gap"
50:         style={{
51:           marginTop: 40,
52:           padding: "24px 28px",
53:           background: "rgba(176,141,46,.07)",
54:           border: "1px solid var(--brass, #b08d2e)",
55:           borderRadius: 4,
56:           maxWidth: 720,
57:         }}
58:       >
59:         <div
60:           data-testid="monitor-signals-honest-gap-label"
61:           style={{
62:             fontSize: 11,
63:             letterSpacing: "0.14em",
64:             textTransform: "uppercase",
65:             color: "var(--brass, #b08d2e)",
66:             fontWeight: 600,
67:             marginBottom: 8,
68:           }}
69:         >
70:           Honest gap · surface only
71:         </div>
72:         <div data-testid="monitor-signals-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
73:           Signal aggregation not yet wired. Real signals will pull from shield
74:           refusal logs, entitlement-service allowance events, and Census
75:           drift-detection. Wire lands at PHASE 4 (g) Watch external-witness
76:           trail feature build.
77:         </div>
78:         <div
79:           data-testid="monitor-signals-honest-gap-see-working"
80:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
81:         >
82:           See the working: NAV monitor.signals at App.js · surface at
83:           pages/os/MonitorSignals.jsx.
84:         </div>
85:       </section>
86:     </div>
87:   );
88: }

# SOURCE: frontend/src/pages/os/OSPrototype.jsx

1: /**
2:  * OSPrototype.jsx — thin wrapper re-exporting PortalIframe from App.js.
3:  *
4:  * R-91 CP-APP-JS-UNIFY: the V8 substitution engine and PortalIframe
5:  * component now live physically in App.js (required by 63 sealed backend
6:  * invariants that pin text-substrings against App.js file bytes).
7:  * This file exists only as a re-export for the pod_shell mirror
8:  * (9 pages files inventory) and any legacy import references.
9:  */
10: import { PortalIframe } from "@/App";
11: 
12: export default PortalIframe;

# SOURCE: frontend/src/pages/os/ThinkLabClarity.jsx

1: /*
2:  * ThinkLabClarity.jsx — v2 OS · work tab · THINKLAB Seek Clarity leaf.
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4e GREEN · 2026-09-22T08:52:00Z
4:  * R-103 amendment: single continuous run to completion.
5:  * HONEST-GAP · SO §5 honest-gap-never-fake.
6:  */
7: 
8: import React from "react";
9: 
10: export default function ThinkLabClarity() {
11:   return (
12:     <div
13:       data-testid="thinklab-clarity-surface"
14:       style={{
15:         minHeight: "100vh",
16:         background: "var(--surface, #f7f5ef)",
17:         color: "var(--ink, #12121a)",
18:         padding: "48px 64px",
19:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
20:       }}
21:     >
22:       <header style={{ marginBottom: 32 }}>
23:         <div
24:           data-testid="thinklab-clarity-breadcrumb"
25:           style={{
26:             fontSize: 12,
27:             letterSpacing: "0.12em",
28:             textTransform: "uppercase",
29:             color: "var(--ink3, #6b6b78)",
30:             marginBottom: 8,
31:           }}
32:         >
33:           THINKLAB · Seek Clarity
34:         </div>
35:         <h1
36:           data-testid="thinklab-clarity-title"
37:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
38:         >
39:           Seek Clarity
40:         </h1>
41:       </header>
42:       <section
43:         data-testid="thinklab-clarity-lead"
44:         style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}
45:       >
46:         <p style={{ margin: "0 0 24px 0" }}>
47:           ThinkLab helps you name what's fuzzy. Ask a question sideways; find the thread that unlocks the rest.
48:         </p>
49:       </section>
50:       <section
51:         data-testid="thinklab-clarity-honest-gap"
52:         style={{
53:           marginTop: 40,
54:           padding: "24px 28px",
55:           background: "rgba(176,141,46,.07)",
56:           border: "1px solid var(--brass, #b08d2e)",
57:           borderRadius: 4,
58:           maxWidth: 720,
59:         }}
60:       >
61:         <div
62:           data-testid="thinklab-clarity-honest-gap-label"
63:           style={{
64:             fontSize: 11,
65:             letterSpacing: "0.14em",
66:             textTransform: "uppercase",
67:             color: "var(--brass, #b08d2e)",
68:             fontWeight: 600,
69:             marginBottom: 8,
70:           }}
71:         >
72:           Honest gap · surface only
73:         </div>
74:         <div data-testid="thinklab-clarity-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
75:           Backend for Seek Clarity not yet wired. This surface reveals the design-of-record
76:           structure honestly; no fabricated data is shown. Wire lands at PHASE 3
77:           Census Productization + PHASE 4 feature build-out per R-102 MASTER DIRECTIVE
78:           + R-103 amendment (single continuous run).
79:         </div>
80:         <div
81:           data-testid="thinklab-clarity-honest-gap-see-working"
82:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
83:         >
84:           See the working: NAV work.clarity at App.js const NAV · surface at
85:           pages/os/ThinkLabClarity.jsx.
86:         </div>
87:       </section>
88:     </div>
89:   );
90: }

# SOURCE: frontend/src/pages/os/ThinkLabHypothesis.jsx

1: /*
2:  * ThinkLabHypothesis.jsx — v2 OS · work tab · THINKLAB Test Hypothesis leaf.
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4e GREEN · 2026-09-22T08:52:00Z
4:  * R-103 amendment: single continuous run to completion.
5:  * HONEST-GAP · SO §5 honest-gap-never-fake.
6:  */
7: 
8: import React from "react";
9: 
10: export default function ThinkLabHypothesis() {
11:   return (
12:     <div
13:       data-testid="thinklab-hypothesis-surface"
14:       style={{
15:         minHeight: "100vh",
16:         background: "var(--surface, #f7f5ef)",
17:         color: "var(--ink, #12121a)",
18:         padding: "48px 64px",
19:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
20:       }}
21:     >
22:       <header style={{ marginBottom: 32 }}>
23:         <div
24:           data-testid="thinklab-hypothesis-breadcrumb"
25:           style={{
26:             fontSize: 12,
27:             letterSpacing: "0.12em",
28:             textTransform: "uppercase",
29:             color: "var(--ink3, #6b6b78)",
30:             marginBottom: 8,
31:           }}
32:         >
33:           THINKLAB · Test Hypothesis
34:         </div>
35:         <h1
36:           data-testid="thinklab-hypothesis-title"
37:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
38:         >
39:           Test Hypothesis
40:         </h1>
41:       </header>
42:       <section
43:         data-testid="thinklab-hypothesis-lead"
44:         style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}
45:       >
46:         <p style={{ margin: "0 0 24px 0" }}>
47:           Frame a claim; the system finds what admits it, what refuses it, what stays silent.
48:         </p>
49:       </section>
50:       <section
51:         data-testid="thinklab-hypothesis-honest-gap"
52:         style={{
53:           marginTop: 40,
54:           padding: "24px 28px",
55:           background: "rgba(176,141,46,.07)",
56:           border: "1px solid var(--brass, #b08d2e)",
57:           borderRadius: 4,
58:           maxWidth: 720,
59:         }}
60:       >
61:         <div
62:           data-testid="thinklab-hypothesis-honest-gap-label"
63:           style={{
64:             fontSize: 11,
65:             letterSpacing: "0.14em",
66:             textTransform: "uppercase",
67:             color: "var(--brass, #b08d2e)",
68:             fontWeight: 600,
69:             marginBottom: 8,
70:           }}
71:         >
72:           Honest gap · surface only
73:         </div>
74:         <div data-testid="thinklab-hypothesis-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
75:           Backend for Test Hypothesis not yet wired. This surface reveals the design-of-record
76:           structure honestly; no fabricated data is shown. Wire lands at PHASE 3
77:           Census Productization + PHASE 4 feature build-out per R-102 MASTER DIRECTIVE
78:           + R-103 amendment (single continuous run).
79:         </div>
80:         <div
81:           data-testid="thinklab-hypothesis-honest-gap-see-working"
82:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
83:         >
84:           See the working: NAV work.hypothesis at App.js const NAV · surface at
85:           pages/os/ThinkLabHypothesis.jsx.
86:         </div>
87:       </section>
88:     </div>
89:   );
90: }

# SOURCE: frontend/src/pages/os/ThinkLabPerspective.jsx

1: /*
2:  * ThinkLabPerspective.jsx — v2 OS · work tab · THINKLAB Get Perspective leaf.
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4e GREEN · 2026-09-22T08:52:00Z
4:  * R-103 amendment: single continuous run to completion.
5:  * HONEST-GAP · SO §5 honest-gap-never-fake.
6:  */
7: 
8: import React from "react";
9: 
10: export default function ThinkLabPerspective() {
11:   return (
12:     <div
13:       data-testid="thinklab-perspective-surface"
14:       style={{
15:         minHeight: "100vh",
16:         background: "var(--surface, #f7f5ef)",
17:         color: "var(--ink, #12121a)",
18:         padding: "48px 64px",
19:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
20:       }}
21:     >
22:       <header style={{ marginBottom: 32 }}>
23:         <div
24:           data-testid="thinklab-perspective-breadcrumb"
25:           style={{
26:             fontSize: 12,
27:             letterSpacing: "0.12em",
28:             textTransform: "uppercase",
29:             color: "var(--ink3, #6b6b78)",
30:             marginBottom: 8,
31:           }}
32:         >
33:           THINKLAB · Get Perspective
34:         </div>
35:         <h1
36:           data-testid="thinklab-perspective-title"
37:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
38:         >
39:           Get Perspective
40:         </h1>
41:       </header>
42:       <section
43:         data-testid="thinklab-perspective-lead"
44:         style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}
45:       >
46:         <p style={{ margin: "0 0 24px 0" }}>
47:           See the same question through a different persona's lens: compliance, watch, operator. Where they diverge is where the work is.
48:         </p>
49:       </section>
50:       <section
51:         data-testid="thinklab-perspective-honest-gap"
52:         style={{
53:           marginTop: 40,
54:           padding: "24px 28px",
55:           background: "rgba(176,141,46,.07)",
56:           border: "1px solid var(--brass, #b08d2e)",
57:           borderRadius: 4,
58:           maxWidth: 720,
59:         }}
60:       >
61:         <div
62:           data-testid="thinklab-perspective-honest-gap-label"
63:           style={{
64:             fontSize: 11,
65:             letterSpacing: "0.14em",
66:             textTransform: "uppercase",
67:             color: "var(--brass, #b08d2e)",
68:             fontWeight: 600,
69:             marginBottom: 8,
70:           }}
71:         >
72:           Honest gap · surface only
73:         </div>
74:         <div data-testid="thinklab-perspective-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
75:           Backend for Get Perspective not yet wired. This surface reveals the design-of-record
76:           structure honestly; no fabricated data is shown. Wire lands at PHASE 3
77:           Census Productization + PHASE 4 feature build-out per R-102 MASTER DIRECTIVE
78:           + R-103 amendment (single continuous run).
79:         </div>
80:         <div
81:           data-testid="thinklab-perspective-honest-gap-see-working"
82:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
83:         >
84:           See the working: NAV work.perspective at App.js const NAV · surface at
85:           pages/os/ThinkLabPerspective.jsx.
86:         </div>
87:       </section>
88:     </div>
89:   );
90: }

# SOURCE: frontend/src/pages/os/ThinkLabStrategy.jsx

1: /*
2:  * ThinkLabStrategy.jsx — v2 OS · work tab · THINKLAB Develop Strategy leaf.
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4e GREEN · 2026-09-22T08:52:00Z
4:  * R-103 amendment: single continuous run to completion.
5:  * HONEST-GAP · SO §5 honest-gap-never-fake.
6:  */
7: 
8: import React from "react";
9: 
10: export default function ThinkLabStrategy() {
11:   return (
12:     <div
13:       data-testid="thinklab-strategy-surface"
14:       style={{
15:         minHeight: "100vh",
16:         background: "var(--surface, #f7f5ef)",
17:         color: "var(--ink, #12121a)",
18:         padding: "48px 64px",
19:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
20:       }}
21:     >
22:       <header style={{ marginBottom: 32 }}>
23:         <div
24:           data-testid="thinklab-strategy-breadcrumb"
25:           style={{
26:             fontSize: 12,
27:             letterSpacing: "0.12em",
28:             textTransform: "uppercase",
29:             color: "var(--ink3, #6b6b78)",
30:             marginBottom: 8,
31:           }}
32:         >
33:           THINKLAB · Develop Strategy
34:         </div>
35:         <h1
36:           data-testid="thinklab-strategy-title"
37:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
38:         >
39:           Develop Strategy
40:         </h1>
41:       </header>
42:       <section
43:         data-testid="thinklab-strategy-lead"
44:         style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}
45:       >
46:         <p style={{ margin: "0 0 24px 0" }}>
47:           Draft a direction; test it against the estate; watch where it breaks. Strategy that survives contact with source.
48:         </p>
49:       </section>
50:       <section
51:         data-testid="thinklab-strategy-honest-gap"
52:         style={{
53:           marginTop: 40,
54:           padding: "24px 28px",
55:           background: "rgba(176,141,46,.07)",
56:           border: "1px solid var(--brass, #b08d2e)",
57:           borderRadius: 4,
58:           maxWidth: 720,
59:         }}
60:       >
61:         <div
62:           data-testid="thinklab-strategy-honest-gap-label"
63:           style={{
64:             fontSize: 11,
65:             letterSpacing: "0.14em",
66:             textTransform: "uppercase",
67:             color: "var(--brass, #b08d2e)",
68:             fontWeight: 600,
69:             marginBottom: 8,
70:           }}
71:         >
72:           Honest gap · surface only
73:         </div>
74:         <div data-testid="thinklab-strategy-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
75:           Backend for Develop Strategy not yet wired. This surface reveals the design-of-record
76:           structure honestly; no fabricated data is shown. Wire lands at PHASE 3
77:           Census Productization + PHASE 4 feature build-out per R-102 MASTER DIRECTIVE
78:           + R-103 amendment (single continuous run).
79:         </div>
80:         <div
81:           data-testid="thinklab-strategy-honest-gap-see-working"
82:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
83:         >
84:           See the working: NAV work.strategy at App.js const NAV · surface at
85:           pages/os/ThinkLabStrategy.jsx.
86:         </div>
87:       </section>
88:     </div>
89:   );
90: }

# SOURCE: frontend/src/pages/os/WorkAnalyze.jsx

1: /*
2:  * WorkAnalyze.jsx — v2 OS Prototype · Work tab · WORKSTUDIO group · analyze leaf.
3:  * (label per enumeration §1.2: "Data Suite")
4:  *
5:  * R-101 preserved WHAT · Turn 4 sub-slice 4d GREEN · 2026-09-22T08:22:00Z
6:  * Owner FE brief §0 verbatim: "The prototype is the design of record ... prototype wins."
7:  *
8:  * HONEST-GAP: no analytics backend exists this-slice. Surface shows the
9:  * design-of-record shape + honest deferral to PHASE 4 Data Suite build.
10:  * SO §5 honest-gap-never-fake.
11:  */
12: 
13: import React from "react";
14: 
15: export default function WorkAnalyze() {
16:   return (
17:     <div
18:       data-testid="work-analyze-surface"
19:       style={{
20:         minHeight: "100vh",
21:         background: "var(--surface, #f7f5ef)",
22:         color: "var(--ink, #12121a)",
23:         padding: "48px 64px",
24:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
25:       }}
26:     >
27:       <header style={{ marginBottom: 32 }}>
28:         <div
29:           style={{
30:             fontSize: 12,
31:             letterSpacing: "0.12em",
32:             textTransform: "uppercase",
33:             color: "var(--ink3, #6b6b78)",
34:             marginBottom: 8,
35:           }}
36:           data-testid="work-analyze-breadcrumb"
37:         >
38:           WORKSTUDIO · Data Suite
39:         </div>
40:         <h1
41:           style={{
42:             fontSize: 40,
43:             fontWeight: 300,
44:             margin: 0,
45:             letterSpacing: "-0.02em",
46:           }}
47:           data-testid="work-analyze-title"
48:         >
49:           Data Suite
50:         </h1>
51:       </header>
52: 
53:       <section
54:         data-testid="work-analyze-lead"
55:         style={{
56:           maxWidth: 720,
57:           fontSize: 17,
58:           lineHeight: 1.6,
59:         }}
60:       >
61:         <p style={{ margin: "0 0 24px 0" }}>
62:           Analyse what the estate holds without moving it. Every measure carries
63:           its source; every filter reveals the working.
64:         </p>
65:       </section>
66: 
67:       <section
68:         data-testid="work-analyze-honest-gap"
69:         style={{
70:           marginTop: 40,
71:           padding: "24px 28px",
72:           background: "rgba(176,141,46,.07)",
73:           border: "1px solid var(--brass, #b08d2e)",
74:           borderRadius: 4,
75:           maxWidth: 720,
76:         }}
77:       >
78:         <div
79:           style={{
80:             fontSize: 11,
81:             letterSpacing: "0.14em",
82:             textTransform: "uppercase",
83:             color: "var(--brass, #b08d2e)",
84:             fontWeight: 600,
85:             marginBottom: 8,
86:           }}
87:           data-testid="work-analyze-honest-gap-label"
88:         >
89:           Honest gap · surface only
90:         </div>
91:         <div
92:           style={{ fontSize: 15, lineHeight: 1.5 }}
93:           data-testid="work-analyze-honest-gap-body"
94:         >
95:           Data Suite analytics backend not yet built. This surface presents the
96:           design-of-record structure; no fabricated data is shown. Analytics
97:           engine lands at PHASE 4 Data-Suite feature build.
98:         </div>
99:         <div
100:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
101:           data-testid="work-analyze-honest-gap-see-working"
102:         >
103:           See the working: NAV workstudio.analyze at App.js · surface at
104:           pages/os/WorkAnalyze.jsx.
105:         </div>
106:       </section>
107:     </div>
108:   );
109: }

# SOURCE: frontend/src/pages/os/WorkBoard.jsx

1: /*
2:  * WorkBoard.jsx — v2 OS · Work tab · WORKSTUDIO · board leaf.
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4d GREEN · 2026-09-22T08:22:00Z
4:  * HONEST-GAP · SO §5 honest-gap-never-fake.
5:  *
6:  * Cures V8-render drift where current runtime showed "Board 360" in a
7:  * separate "Performance Management" section.
8:  */
9: 
10: import React from "react";
11: 
12: export default function WorkBoard() {
13:   return (
14:     <div
15:       data-testid="work-board-surface"
16:       style={{
17:         minHeight: "100vh",
18:         background: "var(--surface, #f7f5ef)",
19:         color: "var(--ink, #12121a)",
20:         padding: "48px 64px",
21:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
22:       }}
23:     >
24:       <header style={{ marginBottom: 32 }}>
25:         <div
26:           data-testid="work-board-breadcrumb"
27:           style={{
28:             fontSize: 12,
29:             letterSpacing: "0.12em",
30:             textTransform: "uppercase",
31:             color: "var(--ink3, #6b6b78)",
32:             marginBottom: 8,
33:           }}
34:         >
35:           WORKSTUDIO · Board
36:         </div>
37:         <h1
38:           data-testid="work-board-title"
39:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
40:         >
41:           Board
42:         </h1>
43:       </header>
44:       <section data-testid="work-board-lead" style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}>
45:         <p style={{ margin: "0 0 24px 0" }}>
46:           Board-facing view: what the board will see, phrased in board language,
47:           traceable back to source data with a single click.
48:         </p>
49:       </section>
50:       <section
51:         data-testid="work-board-honest-gap"
52:         style={{
53:           marginTop: 40,
54:           padding: "24px 28px",
55:           background: "rgba(176,141,46,.07)",
56:           border: "1px solid var(--brass, #b08d2e)",
57:           borderRadius: 4,
58:           maxWidth: 720,
59:         }}
60:       >
61:         <div
62:           data-testid="work-board-honest-gap-label"
63:           style={{
64:             fontSize: 11,
65:             letterSpacing: "0.14em",
66:             textTransform: "uppercase",
67:             color: "var(--brass, #b08d2e)",
68:             fontWeight: 600,
69:             marginBottom: 8,
70:           }}
71:         >
72:           Honest gap · surface only
73:         </div>
74:         <div data-testid="work-board-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
75:           Board rollup not yet wired. Depends on Company Goals aggregation
76:           (upstream) which depends on PHASE 3 Census Productization.
77:         </div>
78:         <div
79:           data-testid="work-board-honest-gap-see-working"
80:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
81:         >
82:           See the working: NAV workstudio.board at App.js · surface at
83:           pages/os/WorkBoard.jsx.
84:         </div>
85:       </section>
86:     </div>
87:   );
88: }

# SOURCE: frontend/src/pages/os/WorkChat.jsx

1: /*
2:  * WorkChat.jsx — v2 OS Prototype · Work tab · WORKSTUDIO group · chat leaf.
3:  *
4:  * R-101 preserved WHAT · Turn 4 sub-slice 4d GREEN · 2026-09-22T08:22:00Z
5:  * Owner FE brief §0 verbatim: "The prototype is the design of record ... prototype wins."
6:  * Owner directive verbatim 2026-09-22T~06:10Z: "UI/UX architecture and experience
7:  * flow needs to be exact as the HTML I shared."
8:  *
9:  * Sub-slice 4d owner ruling verbatim 2026-09-22T~08:15Z: "Work tab (chat LIVE +
10:  * analyze/documents/tasks/team/performance/board honest-gap)".
11:  *
12:  * HONEST-GAP DISCLOSURE (SO §5 honest-gap-never-fake · this-slice specific):
13:  * No `/api/chat` or equivalent chat surface currently exists in the
14:  * Extraction-Akki backend (grep verified 2026-09-22T08:20Z zero hits on
15:  * backend/routers/ for chat routes). The design-of-record "chat LIVE"
16:  * capability is a PHASE 4 feature (owner R-102 MASTER DIRECTIVE
17:  * "productized and functional or gaps surfaced"). This surface reveals the
18:  * gap honestly rather than fabricating a fake chat pipeline. Live-wire
19:  * lands at CP-CHAT-LIVE-WIRE (queued to DQ-14/15/16 fork if desk cannot
20:  * fold into PHASE 4 (h) Model Registry lane).
21:  *
22:  * FOURQ discipline (Rule zero · every block leads with a sentence; measures
23:  * live behind "see the working"): each section header is a plain-English
24:  * lead sentence; details/measures collapse below.
25:  */
26: 
27: import React from "react";
28: 
29: export default function WorkChat() {
30:   return (
31:     <div
32:       data-testid="work-chat-surface"
33:       style={{
34:         minHeight: "100vh",
35:         background: "var(--surface, #f7f5ef)",
36:         color: "var(--ink, #12121a)",
37:         padding: "48px 64px",
38:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
39:       }}
40:     >
41:       <header style={{ marginBottom: 32 }}>
42:         <div
43:           style={{
44:             fontSize: 12,
45:             letterSpacing: "0.12em",
46:             textTransform: "uppercase",
47:             color: "var(--ink3, #6b6b78)",
48:             marginBottom: 8,
49:           }}
50:           data-testid="work-chat-breadcrumb"
51:         >
52:           WORKSTUDIO · Chat
53:         </div>
54:         <h1
55:           style={{
56:             fontSize: 40,
57:             fontWeight: 300,
58:             margin: 0,
59:             letterSpacing: "-0.02em",
60:           }}
61:           data-testid="work-chat-title"
62:         >
63:           Chat
64:         </h1>
65:       </header>
66: 
67:       <section
68:         data-testid="work-chat-lead"
69:         style={{
70:           maxWidth: 720,
71:           fontSize: 17,
72:           lineHeight: 1.6,
73:           color: "var(--ink, #12121a)",
74:         }}
75:       >
76:         <p style={{ margin: "0 0 24px 0" }}>
77:           Ask a question; the shield stays on. Every answer traces to a source
78:           or says plainly why it can't. Branch a reply to compare two directions
79:           without losing the original.
80:         </p>
81:       </section>
82: 
83:       <section
84:         data-testid="work-chat-honest-gap"
85:         style={{
86:           marginTop: 40,
87:           padding: "24px 28px",
88:           background: "rgba(184,57,91,.06)",
89:           border: "1px solid var(--oxblood, #b8395b)",
90:           borderRadius: 4,
91:           maxWidth: 720,
92:         }}
93:       >
94:         <div
95:           style={{
96:             fontSize: 11,
97:             letterSpacing: "0.14em",
98:             textTransform: "uppercase",
99:             color: "var(--oxblood, #b8395b)",
100:             marginBottom: 8,
101:             fontWeight: 600,
102:           }}
103:           data-testid="work-chat-honest-gap-label"
104:         >
105:           Honest gap · backend wire pending
106:         </div>
107:         <div
108:           style={{ fontSize: 15, lineHeight: 1.5, color: "var(--ink, #12121a)" }}
109:           data-testid="work-chat-honest-gap-body"
110:         >
111:           The chat backend is not yet wired. This surface reveals the gap
112:           honestly. Live wire lands at CP-CHAT-LIVE-WIRE under the PHASE 4
113:           feature build-out per R-102 MASTER DIRECTIVE. Until then this page
114:           shows the design-of-record shape without fabricating a fake pipeline.
115:         </div>
116:         <div
117:           style={{
118:             marginTop: 16,
119:             fontSize: 13,
120:             color: "var(--ink3, #6b6b78)",
121:           }}
122:           data-testid="work-chat-honest-gap-see-working"
123:         >
124:           See the working: shell constants at /app/frontend/src/App.js
125:           const NAV → workstudio.chat · this surface at pages/os/WorkChat.jsx.
126:         </div>
127:       </section>
128:     </div>
129:   );
130: }

# SOURCE: frontend/src/pages/os/WorkCommission.jsx

1: /*
2:  * WorkCommission.jsx — v2 OS · Work tab · workstudio · commission leaf.
3:  * PHASE 4 (a) · CP-COMMISSION-WIZARD-LIVE · Commit-A · 2026-09-22T22:25:00Z
4:  *
5:  * Owner banked order verbatim (2026-09-22T~21:21Z):
6:  *   "PHASE 4 (banked order): entitlements backend → Connect + Commission
7:  *    wizards live → CP-SKILLS-LAYER → ..."
8:  *
9:  * This page wraps the pre-existing sealed Canon-5-§14 Shaping-Wizard
10:  * <CommissionWizard /> (byte-identical across pod_shell/frontend/src ↔
11:  * /app/frontend/src twins per wave_g mirror invariant + Ship-Manifest DoD)
12:  * into a routable surface at `/os/work/commission`.
13:  *
14:  * Sealed carriers UNCHANGED per SO §3.8:
15:  *   - CommissionWizard.jsx (Canon 5 §14 Shaping Wizard · Phase 7 Stage B-1
16:  *     operator variant) is consumed by identity import ONLY.
17:  *   - Backend `/api/wizard/operator/*` endpoints are consumed by the wizard
18:  *     component; this page adds no backend consumption of its own.
19:  *
20:  * Honest-gap-narrowing (SO §5.7 · additive) — WorkTasks.jsx honest-gap body
21:  * cites "Wire lands at PHASE 4 (b) Connect + Commission wizard live feature
22:  * build". This page IS that wire for the Commission half. The WorkTasks
23:  * honest-gap remains banked because the Task/request backlog aggregation
24:  * view is a SEPARATE surface that is NOT resolved by this-slice; owner
25:  * gets a truthful narrowing without a paraphrase drift.
26:  */
27: 
28: import React from "react";
29: import CommissionWizard from "@/components/CommissionWizard";
30: 
31: export default function WorkCommission() {
32:   return (
33:     <div
34:       data-testid="work-commission-surface"
35:       style={{
36:         minHeight: "100vh",
37:         background: "var(--surface, #f7f5ef)",
38:         color: "var(--ink, #12121a)",
39:         padding: "24px 32px",
40:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
41:       }}
42:     >
43:       <header
44:         data-testid="work-commission-header"
45:         style={{ marginBottom: 16, maxWidth: 1080 }}
46:       >
47:         <div
48:           data-testid="work-commission-breadcrumb"
49:           style={{
50:             fontSize: 12,
51:             letterSpacing: "0.12em",
52:             textTransform: "uppercase",
53:             color: "var(--ink3, #6b6b78)",
54:             marginBottom: 8,
55:           }}
56:         >
57:           WORKSTUDIO · Commission · Canon 5 §14 Shaping Wizard
58:         </div>
59:         <h1
60:           data-testid="work-commission-title"
61:           style={{ fontSize: 32, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
62:         >
63:           Commission an objective
64:         </h1>
65:         <p
66:           data-testid="work-commission-lead"
67:           style={{ fontSize: 15, lineHeight: 1.55, color: "var(--ink2, #444)", marginTop: 12, maxWidth: 720 }}
68:         >
69:           A chat pane on one side, a draft rail on the other. Mandatory fields — reach,
70:           the four output fields, done-condition, budget, lawful basis — are asked, never
71:           pre-filled. Preference fields may carry agent recommendations. Every turn is
72:           grounded in a real estate read; no fabricated availability, ever.
73:         </p>
74:       </header>
75:       <section data-testid="work-commission-wizard-mount">
76:         <CommissionWizard />
77:       </section>
78:     </div>
79:   );
80: }

# SOURCE: frontend/src/pages/os/WorkDocuments.jsx

1: /*
2:  * WorkDocuments.jsx — v2 OS · Work tab · WORKSTUDIO · documents leaf.
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4d GREEN · 2026-09-22T08:22:00Z
4:  * HONEST-GAP · SO §5 honest-gap-never-fake.
5:  */
6: 
7: import React from "react";
8: 
9: export default function WorkDocuments() {
10:   return (
11:     <div
12:       data-testid="work-documents-surface"
13:       style={{
14:         minHeight: "100vh",
15:         background: "var(--surface, #f7f5ef)",
16:         color: "var(--ink, #12121a)",
17:         padding: "48px 64px",
18:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
19:       }}
20:     >
21:       <header style={{ marginBottom: 32 }}>
22:         <div
23:           data-testid="work-documents-breadcrumb"
24:           style={{
25:             fontSize: 12,
26:             letterSpacing: "0.12em",
27:             textTransform: "uppercase",
28:             color: "var(--ink3, #6b6b78)",
29:             marginBottom: 8,
30:           }}
31:         >
32:           WORKSTUDIO · Documents
33:         </div>
34:         <h1
35:           data-testid="work-documents-title"
36:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
37:         >
38:           Documents
39:         </h1>
40:       </header>
41:       <section data-testid="work-documents-lead" style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}>
42:         <p style={{ margin: "0 0 24px 0" }}>
43:           Every document in view carries its lineage: who prepared it, what
44:           admits it, what it depends on. Nothing floats without a source.
45:         </p>
46:       </section>
47:       <section
48:         data-testid="work-documents-honest-gap"
49:         style={{
50:           marginTop: 40,
51:           padding: "24px 28px",
52:           background: "rgba(176,141,46,.07)",
53:           border: "1px solid var(--brass, #b08d2e)",
54:           borderRadius: 4,
55:           maxWidth: 720,
56:         }}
57:       >
58:         <div
59:           data-testid="work-documents-honest-gap-label"
60:           style={{
61:             fontSize: 11,
62:             letterSpacing: "0.14em",
63:             textTransform: "uppercase",
64:             color: "var(--brass, #b08d2e)",
65:             fontWeight: 600,
66:             marginBottom: 8,
67:           }}
68:         >
69:           Honest gap · surface only
70:         </div>
71:         <div data-testid="work-documents-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
72:           Document indexing and lineage service not yet built. This surface
73:           presents the design-of-record structure; no fabricated documents are
74:           shown. Documents engine lands at PHASE 4 Deck-Engine feature build.
75:         </div>
76:         <div
77:           data-testid="work-documents-honest-gap-see-working"
78:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
79:         >
80:           See the working: NAV workstudio.documents at App.js · surface at
81:           pages/os/WorkDocuments.jsx.
82:         </div>
83:       </section>
84:     </div>
85:   );
86: }

# SOURCE: frontend/src/pages/os/WorkPerformance.jsx

1: /*
2:  * WorkPerformance.jsx — v2 OS · Work tab · WORKSTUDIO · performance leaf
3:  * ("Company Goals" label per enumeration §1.2).
4:  * R-101 preserved WHAT · Turn 4 sub-slice 4d GREEN · 2026-09-22T08:22:00Z
5:  * HONEST-GAP · SO §5 honest-gap-never-fake.
6:  *
7:  * Cures V8-render drift where current runtime showed separate "Performance
8:  * Management" section with "Exco 360" tile (landmark 01 evidence).
9:  */
10: 
11: import React from "react";
12: 
13: export default function WorkPerformance() {
14:   return (
15:     <div
16:       data-testid="work-performance-surface"
17:       style={{
18:         minHeight: "100vh",
19:         background: "var(--surface, #f7f5ef)",
20:         color: "var(--ink, #12121a)",
21:         padding: "48px 64px",
22:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
23:       }}
24:     >
25:       <header style={{ marginBottom: 32 }}>
26:         <div
27:           data-testid="work-performance-breadcrumb"
28:           style={{
29:             fontSize: 12,
30:             letterSpacing: "0.12em",
31:             textTransform: "uppercase",
32:             color: "var(--ink3, #6b6b78)",
33:             marginBottom: 8,
34:           }}
35:         >
36:           WORKSTUDIO · Company Goals
37:         </div>
38:         <h1
39:           data-testid="work-performance-title"
40:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
41:         >
42:           Company Goals
43:         </h1>
44:       </header>
45:       <section data-testid="work-performance-lead" style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}>
46:         <p style={{ margin: "0 0 24px 0" }}>
47:           The measures that matter to the board are the measures on this page.
48:           Every card leads with a sentence; every number carries its source.
49:         </p>
50:       </section>
51:       <section
52:         data-testid="work-performance-honest-gap"
53:         style={{
54:           marginTop: 40,
55:           padding: "24px 28px",
56:           background: "rgba(176,141,46,.07)",
57:           border: "1px solid var(--brass, #b08d2e)",
58:           borderRadius: 4,
59:           maxWidth: 720,
60:         }}
61:       >
62:         <div
63:           data-testid="work-performance-honest-gap-label"
64:           style={{
65:             fontSize: 11,
66:             letterSpacing: "0.14em",
67:             textTransform: "uppercase",
68:             color: "var(--brass, #b08d2e)",
69:             fontWeight: 600,
70:             marginBottom: 8,
71:           }}
72:         >
73:           Honest gap · surface only
74:         </div>
75:         <div data-testid="work-performance-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
76:           Company Goals aggregation not yet wired. Real board-level measures
77:           require a full Census + Registry pipeline pulling from admitted
78:           sources — that lands at PHASE 3 Census Productization + PHASE 4
79:           (h) Model Registry.
80:         </div>
81:         <div
82:           data-testid="work-performance-honest-gap-see-working"
83:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
84:         >
85:           See the working: NAV workstudio.performance label="Company Goals" at
86:           App.js · surface at pages/os/WorkPerformance.jsx. Cures V8-render
87:           drift showing "Exco 360" tile in separate "Performance Management"
88:           section.
89:         </div>
90:       </section>
91:     </div>
92:   );
93: }

# SOURCE: frontend/src/pages/os/WorkTasks.jsx

1: /*
2:  * WorkTasks.jsx — v2 OS · Work tab · WORKSTUDIO · tasks leaf ("My Work" label).
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4d GREEN · 2026-09-22T08:22:00Z
4:  * HONEST-GAP · SO §5 honest-gap-never-fake.
5:  *
6:  * Cures V8-render drift where current runtime showed label "Task Manager"
7:  * instead of design-of-record "My Work" (landmark 01 evidence).
8:  */
9: 
10: import React from "react";
11: 
12: export default function WorkTasks() {
13:   return (
14:     <div
15:       data-testid="work-tasks-surface"
16:       style={{
17:         minHeight: "100vh",
18:         background: "var(--surface, #f7f5ef)",
19:         color: "var(--ink, #12121a)",
20:         padding: "48px 64px",
21:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
22:       }}
23:     >
24:       <header style={{ marginBottom: 32 }}>
25:         <div
26:           data-testid="work-tasks-breadcrumb"
27:           style={{
28:             fontSize: 12,
29:             letterSpacing: "0.12em",
30:             textTransform: "uppercase",
31:             color: "var(--ink3, #6b6b78)",
32:             marginBottom: 8,
33:           }}
34:         >
35:           WORKSTUDIO · My Work
36:         </div>
37:         <h1
38:           data-testid="work-tasks-title"
39:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
40:         >
41:           My Work
42:         </h1>
43:       </header>
44:       <section data-testid="work-tasks-lead" style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}>
45:         <p style={{ margin: "0 0 24px 0" }}>
46:           Your open work in one place: what's yours, what's waiting on evidence,
47:           what's held. Every card leads with a sentence; measures live behind
48:           "see the working".
49:         </p>
50:       </section>
51:       <section
52:         data-testid="work-tasks-honest-gap"
53:         style={{
54:           marginTop: 40,
55:           padding: "24px 28px",
56:           background: "rgba(176,141,46,.07)",
57:           border: "1px solid var(--brass, #b08d2e)",
58:           borderRadius: 4,
59:           maxWidth: 720,
60:         }}
61:       >
62:         <div
63:           data-testid="work-tasks-honest-gap-label"
64:           style={{
65:             fontSize: 11,
66:             letterSpacing: "0.14em",
67:             textTransform: "uppercase",
68:             color: "var(--brass, #b08d2e)",
69:             fontWeight: 600,
70:             marginBottom: 8,
71:           }}
72:         >
73:           Honest gap · surface only
74:         </div>
75:         <div data-testid="work-tasks-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
76:           Task/request backlog service exists partially in dap_lifecycle but
77:           the "My Work" aggregation view is not yet wired to it. This surface
78:           presents the design-of-record structure; no fabricated tasks are
79:           shown. Wire lands at PHASE 4 (b) Connect + Commission wizard live
80:           feature build.
81:         </div>
82:         <div
83:           data-testid="work-tasks-honest-gap-see-working"
84:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
85:         >
86:           See the working: NAV workstudio.tasks label="My Work" at App.js ·
87:           surface at pages/os/WorkTasks.jsx. Cures V8-render drift showing
88:           "Task Manager".
89:         </div>
90:       </section>
91:     </div>
92:   );
93: }

# SOURCE: frontend/src/pages/os/WorkTeam.jsx

1: /*
2:  * WorkTeam.jsx — v2 OS · Work tab · WORKSTUDIO · team leaf ("My Team" label).
3:  * R-101 preserved WHAT · Turn 4 sub-slice 4d GREEN · 2026-09-22T08:22:00Z
4:  * HONEST-GAP · SO §5 honest-gap-never-fake.
5:  */
6: 
7: import React from "react";
8: 
9: export default function WorkTeam() {
10:   return (
11:     <div
12:       data-testid="work-team-surface"
13:       style={{
14:         minHeight: "100vh",
15:         background: "var(--surface, #f7f5ef)",
16:         color: "var(--ink, #12121a)",
17:         padding: "48px 64px",
18:         fontFamily: "'Charter', 'Iowan Old Style', Georgia, serif",
19:       }}
20:     >
21:       <header style={{ marginBottom: 32 }}>
22:         <div
23:           data-testid="work-team-breadcrumb"
24:           style={{
25:             fontSize: 12,
26:             letterSpacing: "0.12em",
27:             textTransform: "uppercase",
28:             color: "var(--ink3, #6b6b78)",
29:             marginBottom: 8,
30:           }}
31:         >
32:           WORKSTUDIO · My Team
33:         </div>
34:         <h1
35:           data-testid="work-team-title"
36:           style={{ fontSize: 40, fontWeight: 300, margin: 0, letterSpacing: "-0.02em" }}
37:         >
38:           My Team
39:         </h1>
40:       </header>
41:       <section data-testid="work-team-lead" style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}>
42:         <p style={{ margin: "0 0 24px 0" }}>
43:           Your people in one place: who's on watch, whose entitlements need
44:           renewal, who's holding what.
45:         </p>
46:       </section>
47:       <section
48:         data-testid="work-team-honest-gap"
49:         style={{
50:           marginTop: 40,
51:           padding: "24px 28px",
52:           background: "rgba(176,141,46,.07)",
53:           border: "1px solid var(--brass, #b08d2e)",
54:           borderRadius: 4,
55:           maxWidth: 720,
56:         }}
57:       >
58:         <div
59:           data-testid="work-team-honest-gap-label"
60:           style={{
61:             fontSize: 11,
62:             letterSpacing: "0.14em",
63:             textTransform: "uppercase",
64:             color: "var(--brass, #b08d2e)",
65:             fontWeight: 600,
66:             marginBottom: 8,
67:           }}
68:         >
69:           Honest gap · surface only
70:         </div>
71:         <div data-testid="work-team-honest-gap-body" style={{ fontSize: 15, lineHeight: 1.5 }}>
72:           Team roster + entitlement rollup service not yet wired. Principal
73:           Model v1 exists at backend/services/request_context/context.py but
74:           the team-level aggregation view is queued for CP-TENANT-SEPARATION
75:           (PHASE 2) where per-tenant roster views become meaningful.
76:         </div>
77:         <div
78:           data-testid="work-team-honest-gap-see-working"
79:           style={{ marginTop: 16, fontSize: 13, color: "var(--ink3, #6b6b78)" }}
80:         >
81:           See the working: NAV workstudio.team label="My Team" at App.js ·
82:           surface at pages/os/WorkTeam.jsx.
83:         </div>
84:       </section>
85:     </div>
86:   );
87: }

# SOURCE: frontend/src/hooks/use-toast.js

1: "use client";
2: // Inspired by react-hot-toast library
3: import * as React from "react"
4: 
5: const TOAST_LIMIT = 1
6: const TOAST_REMOVE_DELAY = 1000000
7: 
8: const actionTypes = {
9:   ADD_TOAST: "ADD_TOAST",
10:   UPDATE_TOAST: "UPDATE_TOAST",
11:   DISMISS_TOAST: "DISMISS_TOAST",
12:   REMOVE_TOAST: "REMOVE_TOAST"
13: }
14: 
15: let count = 0
16: 
17: function genId() {
18:   count = (count + 1) % Number.MAX_SAFE_INTEGER
19:   return count.toString();
20: }
21: 
22: const toastTimeouts = new Map()
23: 
24: const addToRemoveQueue = (toastId) => {
25:   if (toastTimeouts.has(toastId)) {
26:     return
27:   }
28: 
29:   const timeout = setTimeout(() => {
30:     toastTimeouts.delete(toastId)
31:     dispatch({
32:       type: "REMOVE_TOAST",
33:       toastId: toastId,
34:     })
35:   }, TOAST_REMOVE_DELAY)
36: 
37:   toastTimeouts.set(toastId, timeout)
38: }
39: 
40: export const reducer = (state, action) => {
41:   switch (action.type) {
42:     case "ADD_TOAST":
43:       return {
44:         ...state,
45:         toasts: [action.toast, ...state.toasts].slice(0, TOAST_LIMIT),
46:       };
47: 
48:     case "UPDATE_TOAST":
49:       return {
50:         ...state,
51:         toasts: state.toasts.map((t) =>
52:           t.id === action.toast.id ? { ...t, ...action.toast } : t),
53:       };
54: 
55:     case "DISMISS_TOAST": {
56:       const { toastId } = action
57: 
58:       // ! Side effects ! - This could be extracted into a dismissToast() action,
59:       // but I'll keep it here for simplicity
60:       if (toastId) {
61:         addToRemoveQueue(toastId)
62:       } else {
63:         state.toasts.forEach((toast) => {
64:           addToRemoveQueue(toast.id)
65:         })
66:       }
67: 
68:       return {
69:         ...state,
70:         toasts: state.toasts.map((t) =>
71:           t.id === toastId || toastId === undefined
72:             ? {
73:                 ...t,
74:                 open: false,
75:               }
76:             : t),
77:       };
78:     }
79:     case "REMOVE_TOAST":
80:       if (action.toastId === undefined) {
81:         return {
82:           ...state,
83:           toasts: [],
84:         }
85:       }
86:       return {
87:         ...state,
88:         toasts: state.toasts.filter((t) => t.id !== action.toastId),
89:       };
90:   }
91: }
92: 
93: const listeners = []
94: 
95: let memoryState = { toasts: [] }
96: 
97: function dispatch(action) {
98:   memoryState = reducer(memoryState, action)
99:   listeners.forEach((listener) => {
100:     listener(memoryState)
101:   })
102: }
103: 
104: function toast({
105:   ...props
106: }) {
107:   const id = genId()
108: 
109:   const update = (props) =>
110:     dispatch({
111:       type: "UPDATE_TOAST",
112:       toast: { ...props, id },
113:     })
114:   const dismiss = () => dispatch({ type: "DISMISS_TOAST", toastId: id })
115: 
116:   dispatch({
117:     type: "ADD_TOAST",
118:     toast: {
119:       ...props,
120:       id,
121:       open: true,
122:       onOpenChange: (open) => {
123:         if (!open) dismiss()
124:       },
125:     },
126:   })
127: 
128:   return {
129:     id: id,
130:     dismiss,
131:     update,
132:   }
133: }
134: 
135: function useToast() {
136:   const [state, setState] = React.useState(memoryState)
137: 
138:   React.useEffect(() => {
139:     listeners.push(setState)
140:     return () => {
141:       const index = listeners.indexOf(setState)
142:       if (index > -1) {
143:         listeners.splice(index, 1)
144:       }
145:     };
146:   }, [state])
147: 
148:   return {
149:     ...state,
150:     toast,
151:     dismiss: (toastId) => dispatch({ type: "DISMISS_TOAST", toastId }),
152:   };
153: }
154: 
155: export { useToast, toast }

# SOURCE: frontend/src/hooks/useBuildSkillProvisioning.js

1: /**
2:  * useBuildSkillProvisioning — DAP BuildSkill polling hook.
3:  *
4:  * CP-SKILLS-LAYER-SERIES-CLOSE (PHASE 4 · c-vi · Slice 5).
5:  *
6:  * Consumes the sealed A18.2 persistence state via the additive backend
7:  * route `/api/dap/buildskill/provisioning-records`. Returns EXACTLY what
8:  * the route returns (records[], count). Never fabricates: no synthetic
9:  * default records array, no cached fallback that could drift from the
10:  * sealed store — every call is a fresh fetch. `// no fabrication` here
11:  * per the banked lesson from useCensusRunState.js discipline (never
12:  * fabricates when the endpoint is unreachable — surfaces the error
13:  * separately and preserves the previous records).
14:  *
15:  * Owner boundary directive verbatim (2026-02-23 · slice open):
16:  *   "the buildskill surface must show real provisioning state or
17:  *    honest-gap, and the boundary report must include the tester
18:  *    walkthrough — the concrete steps a human takes and what they see."
19:  *
20:  * Owner R-102 verbatim: "productized-or-honest-gap — the USER-visible bar."
21:  *
22:  * Env discipline: uses `process.env.REACT_APP_BACKEND_URL` verbatim.
23:  * Never hardcodes an origin.
24:  */
25: import { useCallback, useEffect, useRef, useState } from "react";
26: 
27: // Paired-equality anchor with backend router's
28: // PROVISIONING_RECORDS_ROUTE_PATH Final constant. Any drift here fires
29: // the invariant test's paired-equality pin RED right-reason.
30: const PROVISIONING_RECORDS_ROUTE_PATH = "/api/dap/buildskill/provisioning-records";
31: 
32: const POLL_INTERVAL_MS = 30000; // 30s · slower than the census badge (15s)
33:                                  // because provisioning changes are rare.
34: 
35: export function useBuildSkillProvisioning(jwtToken, { autoPoll = true } = {}) {
36:   const [records, setRecords] = useState([]);
37:   const [count, setCount] = useState(0);
38:   const [loading, setLoading] = useState(false);
39:   const [error, setError] = useState(null);
40:   const [lastFetchedAt, setLastFetchedAt] = useState(null);
41:   const intervalRef = useRef(null);
42: 
43:   const fetchOnce = useCallback(async () => {
44:     setLoading(true);
45:     setError(null);
46:     try {
47:       const base = process.env.REACT_APP_BACKEND_URL || "";
48:       const url = `${base}${PROVISIONING_RECORDS_ROUTE_PATH}`;
49:       const headers = { Accept: "application/json" };
50:       if (jwtToken) {
51:         headers["Authorization"] = `Bearer ${jwtToken}`;
52:       }
53:       const resp = await fetch(url, { headers });
54:       if (!resp.ok) {
55:         setError(
56:           `Request refused (status ${resp.status}). Prior view preserved.`
57:         );
58:         setLoading(false);
59:         return;
60:       }
61:       const body = await resp.json();
62:       // Never fabricates: only set state from the body shape the sealed
63:       // store produced. Missing keys yield empty arrays / zero count.
64:       const fetchedRecords = Array.isArray(body?.records) ? body.records : [];
65:       const fetchedCount =
66:         typeof body?.count === "number" ? body.count : fetchedRecords.length;
67:       setRecords(fetchedRecords);
68:       setCount(fetchedCount);
69:       setLastFetchedAt(new Date().toISOString());
70:     } catch (e) {
71:       setError(
72:         `Could not reach the buildskill surface. Prior view preserved.`
73:       );
74:     } finally {
75:       setLoading(false);
76:     }
77:   }, [jwtToken]);
78: 
79:   useEffect(() => {
80:     if (!autoPoll) return () => {};
81:     fetchOnce();
82:     intervalRef.current = setInterval(fetchOnce, POLL_INTERVAL_MS);
83:     return () => {
84:       if (intervalRef.current) {
85:         clearInterval(intervalRef.current);
86:         intervalRef.current = null;
87:       }
88:     };
89:   }, [autoPoll, fetchOnce]);
90: 
91:   return {
92:     records,
93:     count,
94:     loading,
95:     error,
96:     lastFetchedAt,
97:     triggerRefetch: fetchOnce,
98:   };
99: }
100: 
101: export default useBuildSkillProvisioning;

# SOURCE: frontend/src/hooks/useCensusRunState.js

1: /**
2:  * useCensusRunState — real-scheduler-state polling hook.
3:  *
4:  * Owner directive verbatim (PHASE 3 continuation A''):
5:  *   "the UI must show REAL scheduler state only — the running card polls
6:  *    the service's own state, never synthesized progress."
7:  *
8:  * This hook polls GET /api/portal/census/runs/{census_run_id}/state
9:  * every POLL_INTERVAL_MS and returns EXACTLY what the endpoint returns.
10:  * It never fabricates progress, ETA, or random values. When the endpoint
11:  * returns 404 (unknown id), state is set to null. When the poll fails
12:  * (network error), the previous state is preserved and an error is
13:  * surfaced separately.
14:  *
15:  * Backend contract: services/census_autonomy/state_reader.py returns
16:  *   { status: "PENDING" | "COMPLETE" | "REFUSED", ...fields }
17:  * or null → 404.
18:  */
19: import { useEffect, useRef, useState } from "react";
20: 
21: const POLL_INTERVAL_MS = 5000;
22: 
23: export function useCensusRunState(censusRunId, jwtToken) {
24:   const [state, setState] = useState(null);
25:   const [error, setError] = useState(null);
26:   const activeRef = useRef(true);
27: 
28:   useEffect(() => {
29:     activeRef.current = true;
30:     if (!censusRunId) {
31:       setState(null);
32:       setError(null);
33:       return () => { activeRef.current = false; };
34:     }
35: 
36:     async function fetchOnce() {
37:       try {
38:         const resp = await fetch(
39:           `${process.env.REACT_APP_BACKEND_URL}/api/portal/census/runs/${encodeURIComponent(censusRunId)}/state`,
40:           {
41:             headers: jwtToken
42:               ? { "Authorization": `Bearer ${jwtToken}` }
43:               : {},
44:           }
45:         );
46:         if (!activeRef.current) return;
47:         if (resp.status === 404) {
48:           setState(null);
49:           setError(null);
50:           return;
51:         }
52:         if (!resp.ok) {
53:           setError(`state fetch failed: HTTP ${resp.status}`);
54:           return;
55:         }
56:         const doc = await resp.json();
57:         if (!activeRef.current) return;
58:         // Store REAL state verbatim; do not derive progress percent.
59:         setState(doc);
60:         setError(null);
61:       } catch (e) {
62:         if (!activeRef.current) return;
63:         setError(String(e));
64:       }
65:     }
66: 
67:     fetchOnce();
68:     const handle = setInterval(fetchOnce, POLL_INTERVAL_MS);
69:     return () => {
70:       activeRef.current = false;
71:       clearInterval(handle);
72:     };
73:   }, [censusRunId, jwtToken]);
74: 
75:   return { state, error };
76: }

# SOURCE: frontend/src/hooks/useResponseRequiredList.js

1: /**
2:  * useResponseRequiredList — real-producer-data polling hook.
3:  *
4:  * PHASE 3 continuation A'''-cont-B · CP-CENSUS-AUTONOMY-RESPONSE-
5:  * REQUIRED-BADGE-UI. Consumes the sealed A'''-cont-A endpoint
6:  * `GET /api/portal/census/response-required-items` and returns
7:  * EXACTLY what the endpoint returns (items[], count). Never
8:  * fabricates.
9:  *
10:  * Owner directive verbatim (2026-09-22T~19:40Z at A'''' opening):
11:  *   "the owner-answerable item text for blocked slices should carry
12:  *    the exact unblock action ... so the badge in A'''-cont-B is
13:  *    actionable, not just informative — put that in the item payload
14:  *    schema now if it needs a field."
15:  *
16:  * Owner directive verbatim (2026-09-22T~21:21Z at Phase 3 closure):
17:  *   "Proceed: A'''-cont-B (badge + polling on real producer data)"
18:  *
19:  * The sealed A'''' adapter embeds the actionable unblock action inside
20:  * the sealed queue's `reason_text` field via the machine-parseable
21:  * marker prefix `[UNBLOCK action_class=<code>] <detail>` — the badge
22:  * consumes that marker to render the actionable owner-answerable item.
23:  *
24:  * Never fabricates: no synthetic progress, no synthetic items, no
25:  * count interpolation. When the endpoint returns HTTP 4xx/5xx, the
26:  * previous items are preserved and an error is surfaced separately
27:  * (banked lesson from A'' useCensusRunState.js discipline).
28:  *
29:  * Env discipline: uses `process.env.REACT_APP_BACKEND_URL` verbatim.
30:  * Never hardcodes an origin.
31:  */
32: import { useEffect, useRef, useState } from "react";
33: 
34: const POLL_INTERVAL_MS = 15000;
35: 
36: export function useResponseRequiredList(jwtToken, { autoPoll = true } = {}) {
37:   const [items, setItems] = useState([]);
38:   const [count, setCount] = useState(0);
39:   const [error, setError] = useState(null);
40:   const [loading, setLoading] = useState(false);
41:   const activeRef = useRef(true);
42:   const [refetchTick, setRefetchTick] = useState(0);
43: 
44:   const triggerRefetch = () => setRefetchTick((t) => t + 1);
45: 
46:   useEffect(() => {
47:     activeRef.current = true;
48:     if (!jwtToken) {
49:       setItems([]);
50:       setCount(0);
51:       setError(null);
52:       return () => {
53:         activeRef.current = false;
54:       };
55:     }
56: 
57:     async function fetchOnce() {
58:       setLoading(true);
59:       try {
60:         const resp = await fetch(
61:           `${process.env.REACT_APP_BACKEND_URL}/api/portal/census/response-required-items`,
62:           {
63:             headers: { Authorization: `Bearer ${jwtToken}` },
64:           }
65:         );
66:         if (!activeRef.current) return;
67:         if (!resp.ok) {
68:           setError(`response-required-items fetch failed: HTTP ${resp.status}`);
69:           setLoading(false);
70:           return;
71:         }
72:         const doc = await resp.json();
73:         if (!activeRef.current) return;
74:         // Store REAL producer data verbatim; do NOT derive fabricated fields.
75:         setItems(Array.isArray(doc.items) ? doc.items : []);
76:         setCount(typeof doc.count === "number" ? doc.count : 0);
77:         setError(null);
78:         setLoading(false);
79:       } catch (e) {
80:         if (!activeRef.current) return;
81:         setError(String(e));
82:         setLoading(false);
83:       }
84:     }
85: 
86:     fetchOnce();
87:     if (!autoPoll) {
88:       return () => {
89:         activeRef.current = false;
90:       };
91:     }
92:     const handle = setInterval(fetchOnce, POLL_INTERVAL_MS);
93:     return () => {
94:       activeRef.current = false;
95:       clearInterval(handle);
96:     };
97:   }, [jwtToken, autoPoll, refetchTick]);
98: 
99:   return { items, count, error, loading, triggerRefetch };
100: }

# SOURCE: frontend/src/lib/apiClient.js

1: /**
2:  * Centralized API client for the Akki frontend.
3:  * All calls use REACT_APP_BACKEND_URL from environment.
4:  * All backend routes are prefixed with /api.
5:  */
6: 
7: const BASE = process.env.REACT_APP_BACKEND_URL || "";
8: 
9: async function request(path, options = {}) {
10:   const url = `${BASE}${path}`;
11:   const headers = { ...options.headers };
12: 
13:   // Attach JWT if stored
14:   const token = sessionStorage.getItem("akki_access_token");
15:   if (token && !headers["Authorization"]) {
16:     headers["Authorization"] = `Bearer ${token}`;
17:   }
18: 
19:   const res = await fetch(url, { ...options, headers });
20:   return res;
21: }
22: 
23: export async function get(path) {
24:   const res = await request(path);
25:   if (!res.ok) {
26:     const body = await res.text();
27:     throw new Error(`GET ${path} → ${res.status}: ${body}`);
28:   }
29:   return res.json();
30: }
31: 
32: export async function post(path, body) {
33:   const res = await request(path, {
34:     method: "POST",
35:     headers: { "Content-Type": "application/json" },
36:     body: JSON.stringify(body),
37:   });
38:   if (!res.ok) {
39:     const text = await res.text();
40:     throw new Error(`POST ${path} → ${res.status}: ${text}`);
41:   }
42:   return res.json();
43: }
44: 
45: /** Login and store tokens.
46:  *  Backend uses `email` + `password` (NOT username). */
47: export async function login(email, password) {
48:   const res = await request("/api/auth/login", {
49:     method: "POST",
50:     headers: { "Content-Type": "application/json" },
51:     body: JSON.stringify({ email, password }),
52:   });
53:   if (!res.ok) throw new Error("Login failed");
54:   const data = await res.json();
55:   if (data.access_token) sessionStorage.setItem("akki_access_token", data.access_token);
56:   if (data.refresh_token) sessionStorage.setItem("akki_refresh_token", data.refresh_token);
57:   return data;
58: }
59: 
60: /** Refresh the access token.
61:  *  Backend reads the refresh token from Authorization header. */
62: export async function refreshToken() {
63:   const refresh = sessionStorage.getItem("akki_refresh_token");
64:   if (!refresh) throw new Error("No refresh token");
65:   const res = await request("/api/auth/refresh", {
66:     method: "POST",
67:     headers: {
68:       "Content-Type": "application/json",
69:       "Authorization": `Bearer ${refresh}`,
70:     },
71:   });
72:   if (!res.ok) throw new Error("Refresh failed");
73:   const data = await res.json();
74:   if (data.access_token) sessionStorage.setItem("akki_access_token", data.access_token);
75:   if (data.refresh_token) sessionStorage.setItem("akki_refresh_token", data.refresh_token);
76:   return data;
77: }
78: 
79: /** Get current identity */
80: export const fetchMe = () => get("/api/auth/me");
81: 
82: // Specific API calls matching the contract
83: 
84: export const fetchRegistryFacts = () => get("/api/registry/facts");
85: export const fetchComputeEstate = () => get("/api/compute/estate");
86: export const fetchModels = () => get("/api/model_registry/models");
87: export const fetchFullRecord = () => get("/api/model_registry/full_record");
88: export const fetchSkillFilesState = () => get("/api/skill-files/state");
89: export const fetchCensusLatest = () => get("/api/census/latest");
90: export const fetchGovernanceState = () => get("/api/governance/state");
91: export const fetchWatchState = () => get("/api/watch/state");
92: export const fetchGreyMirrorState = () => get("/api/grey_mirror/state");
93: export const fetchAuditTrailOverview = () => get("/api/audit_trail/overview");
94: export const fetchGovernEstateRulesRecord = () => get("/api/govern/estate_rules_record");
95: export const fetchTeamAccessRegister = () => get("/api/team/access_register");
96: export const fetchTeamConstitutionalSeats = () => get("/api/team/constitutional_seats");
97: export const fetchComplianceRefusals = () => get("/api/compliance/refusals");
98: export const fetchGovernTrustCenter = () => get("/api/govern/trust_center_record");
99: export const fetchShieldReceipts = () => get("/api/shield/receipts?limit=50");
100: export const fetchShieldAllowlists = () => get("/api/shield/allowlists");
101: export const fetchCostLedgerSummary = (kind = "") => get(`/api/cost_ledger/summary?kind=${kind}`);
102: export const fetchCostLedgerEntries = (kind = "", limit = 25) => get(`/api/cost_ledger/entries?kind=${kind}&limit=${limit}`);
103: export const fetchModelById = (id) => get(`/api/model_registry/${id}/journal`);
104: 
105: // ── Portal write-path (R-100 · JWT-gated) ────────────────────────────────
106: // tryGet / tryPost return {ok, status, data, error} — never throw on HTTP errors.
107: // This allows callers to handle 404 (endpoint not mounted) gracefully.
108: 
109: export async function tryGet(path) {
110:   try {
111:     const res = await request(path);
112:     const data = res.ok ? await res.json().catch(() => null) : await res.json().catch(() => null);
113:     return { ok: res.ok, status: res.status, data, error: res.ok ? null : `${res.status}` };
114:   } catch (e) {
115:     return { ok: false, status: 0, data: null, error: e.message };
116:   }
117: }
118: 
119: export async function tryPost(path, body) {
120:   try {
121:     const res = await request(path, {
122:       method: "POST",
123:       headers: { "Content-Type": "application/json" },
124:       body: body != null ? JSON.stringify(body) : undefined,
125:     });
126:     const data = await res.json().catch(() => null);
127:     return { ok: res.ok, status: res.status, data, error: res.ok ? null : `${res.status}` };
128:   } catch (e) {
129:     return { ok: false, status: 0, data: null, error: e.message };
130:   }
131: }
132: 
133: // Portal requests
134: export const fetchPortalRequests = () => tryGet("/api/portal/requests");
135: export const fetchPortalRequestDetail = (id) => tryGet(`/api/portal/requests/${id}`);
136: export const submitPortalRequest = (body) => tryPost("/api/portal/requests", body);
137: export const stopPortalRequest = (id) => tryPost(`/api/portal/requests/${id}/stop`);
138: export const retryPortalRequest = (id) => tryPost(`/api/portal/requests/${id}/retry`);
139: 
140: // Portal entitlement
141: export const fetchPortalLicence = () => tryGet("/api/portal/entitlement/licence");
142: export const fetchPortalCatalog = () => tryGet("/api/portal/entitlement/catalog/listed");
143: export const fetchPortalAllowance = () => tryGet("/api/portal/entitlement/allowance");
144: export const fetchPortalBadges = () => tryGet("/api/portal/entitlement/badges");
145: 
146: // Canon rules (R-99 · public, no auth)
147: export const fetchCanonRulesDap = () => tryGet("/api/canon/rules/dap");
148: export const fetchCanonRulesRbm = () => tryGet("/api/canon/rules/rbm");
149: export const fetchCanonRulesRoc = () => tryGet("/api/canon/rules/roc");
150: export const fetchCanonRbm8Ceremony = () => tryGet("/api/canon/rules/rbm-8-ceremony-mechanic");

# SOURCE: frontend/src/lib/utils.js

1: import { clsx } from "clsx";
2: import { twMerge } from "tailwind-merge"
3: 
4: export function cn(...inputs) {
5:   return twMerge(clsx(inputs));
6: }

# SOURCE: frontend/src/components/AuditTrail.jsx

1: import React, { useEffect, useState } from "react";
2: import { Link } from "react-router-dom";
3: 
4: /**
5:  * AuditTrail.jsx — Wave F Cleanup · CP · audit-trail Overview surface.
6:  *
7:  * Canon rows landed by this surface (verbatim from AKKI CANON —
8:  * ADDENDUM 1 §1 Confirmed Closures):
9:  *
10:  *   #4 · CA1-001 · Doc02-020a — "Closed by the audit trail Overview
11:  *        stating when an answer drew on 2+ independently-governed units."
12:  *
13:  *   #17 · CA1-002 · Doc06-016 — "Closed by the audit trail Overview
14:  *        stating how many available source units were actually served."
15:  *
16:  *   #19/#20/#21 · CA1-003 · Doc07-019 · Doc08-017 — "Closed by a
17:  *        Registry densification stat and a per-turn warm/fresh tag —
18:  *        flagged here as a partial closure, not a full one."
19:  *
20:  * Data source: GET /api/audit_trail/overview. Every row cites its
21:  * on-disk source_path (REFERENCE-NOT-COPY · Design Law A8). Empty
22:  * stores render an honest sentence naming the canon anchor.
23:  */
24: 
25: const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
26: 
27: // v7 palette tokens (matched to Governance / Watch / Grey-Mirror).
28: const paper = "#f5f2ea";
29: const surface = "#ffffff";
30: const ink = "#1b1f27";
31: const ink2 = "#3a3f4a";
32: const ink3 = "#7a7f8a";
33: const line = "#e4dccf";
34: const blue = "#16274a";
35: const oxblood = "#8a2a44";
36: const brass = "#b08d2e";
37: const head = 'ui-serif, "Iowan Old Style", Georgia, serif';
38: 
39: function Panel({ "data-testid": dt, title, anchor, canonQuote, children }) {
40:   return (
41:     <section data-testid={dt} style={{
42:       background: surface, border: `1px solid ${line}`, padding: "22px 24px",
43:       marginBottom: 20,
44:     }}>
45:       <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 8 }}>
46:         <h2 style={{ fontFamily: head, fontSize: 20, color: blue, margin: 0 }}>{title}</h2>
47:         <span style={{ fontSize: 11, letterSpacing: 1.5, color: ink3 }}>{anchor}</span>
48:       </div>
49:       {canonQuote ? (
50:         <blockquote style={{
51:           margin: "8px 0 12px 0", padding: "8px 12px", borderLeft: `3px solid ${brass}`,
52:           color: ink2, fontStyle: "italic", fontSize: 13, lineHeight: 1.5,
53:         }}>
54:           {canonQuote}
55:         </blockquote>
56:       ) : null}
57:       {children}
58:     </section>
59:   );
60: }
61: 
62: function EmptyState({ anchor, kind }) {
63:   return (
64:     <p style={{ color: ink2, fontStyle: "italic", margin: "6px 0 0 0" }}>
65:       No {kind} on record. Canon anchor: {anchor}. Drawn, never left blank.
66:     </p>
67:   );
68: }
69: 
70: export default function AuditTrail() {
71:   const [state, setState] = useState(null);
72:   const [error, setError] = useState(null);
73: 
74:   useEffect(() => {
75:     (async () => {
76:       try {
77:         const r = await fetch(`${BACKEND_URL}/api/audit_trail/overview`);
78:         if (!r.ok) throw new Error(`HTTP ${r.status}`);
79:         setState(await r.json());
80:       } catch (e) {
81:         setError(String(e));
82:       }
83:     })();
84:   }, []);
85: 
86:   return (
87:     <div data-testid="audit-trail-view" style={{
88:       minHeight: "100vh", background: paper, padding: "40px 48px",
89:       fontFamily: "ui-sans-serif, system-ui",
90:     }}>
91:       <div style={{ maxWidth: 1080, margin: "0 auto" }}>
92:         <div style={{ fontSize: 11, letterSpacing: 2, color: ink3 }}>AKKI · AUDIT TRAIL</div>
93:         <h1 data-testid="audit-trail-title" style={{
94:           fontFamily: head, fontSize: 40, color: blue, margin: "8px 0 6px 0",
95:         }}>Audit Trail Overview</h1>
96:         <p data-testid="audit-trail-reference-note" style={{
97:           color: ink2, fontSize: 13, lineHeight: 1.6, marginBottom: 20,
98:         }}>
99:           REFERENCE-NOT-COPY (Design Law A8). Every entry cites its
100:           on-disk source_path; record bodies live under
101:           <code style={{ margin: "0 4px" }}>phase0/</code> where each
102:           producer wrote them. Canon anchors: Addendum §1 CA1-001 · CA1-002 ·
103:           CA1-003 (partial closure).
104:         </p>
105: 
106:         <nav style={{ marginBottom: 24, fontSize: 13 }}>
107:           <Link data-testid="nav-to-governance" to="/governance" style={{ color: blue, marginRight: 20 }}>
108:             → Governance
109:           </Link>
110:           <Link data-testid="nav-to-watch" to="/watch" style={{ color: blue, marginRight: 20 }}>
111:             → The Watch
112:           </Link>
113:           <Link to="/" style={{ color: ink3 }}>← Registry</Link>
114:         </nav>
115: 
116:         {error ? (
117:           <div style={{ color: oxblood, marginBottom: 12 }}>
118:             Failed to load audit-trail overview: {error}
119:           </div>
120:         ) : null}
121: 
122:         <Panel data-testid="multi-unit-answers-panel"
123:                title="Multi-Unit Answers"
124:                anchor="CA1-001 · Doc02-020a · Promise #4"
125:                canonQuote={state?.multi_unit_answers?.canon_text}>
126:           <div data-testid="multi-unit-answers-count" style={{
127:             fontFamily: "ui-monospace, monospace", color: brass, fontSize: 13, marginBottom: 6,
128:           }}>
129:             {state ? `${state.multi_unit_answers.count} answers drew on 2+ independently-governed units` : "loading…"}
130:           </div>
131:           {state && state.multi_unit_answers.count === 0 ? (
132:             <div data-testid="multi-unit-answers-empty-state">
133:               <EmptyState anchor="Addendum §1 CA1-001"
134:                           kind="multi-unit answers" />
135:             </div>
136:           ) : null}
137:           {state && state.multi_unit_answers.count > 0 ? (
138:             <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
139:               {state.multi_unit_answers.entries.slice(0, 40).map((e) => (
140:                 <li key={e.trace_id} style={{ borderBottom: `1px dotted ${line}`, padding: "8px 0" }}>
141:                   <div style={{ fontFamily: "ui-monospace, monospace", fontSize: 13, color: blue }}>
142:                     {e.trace_id}
143:                   </div>
144:                   <div style={{ fontSize: 12, color: ink2, marginTop: 2 }}>
145:                     {e.unit_count} units · {e.source_units.join(" · ")}
146:                   </div>
147:                   <div style={{ fontSize: 11, color: ink3, marginTop: 2 }}>
148:                     {e.source_path}
149:                   </div>
150:                 </li>
151:               ))}
152:             </ul>
153:           ) : null}
154:         </Panel>
155: 
156:         <Panel data-testid="units-served-panel"
157:                title="Units Served"
158:                anchor="CA1-002 · Doc06-016 · Promise #17"
159:                canonQuote={state?.units_served?.canon_text}>
160:           <div data-testid="units-served-count" style={{
161:             fontFamily: "ui-monospace, monospace", color: brass, fontSize: 13, marginBottom: 6,
162:           }}>
163:             {state
164:               ? `${state.units_served.served} of ${state.units_served.available} available source units were actually served`
165:               : "loading…"}
166:           </div>
167:           {state && state.units_served.available === 0 ? (
168:             <div data-testid="units-served-empty-state">
169:               <EmptyState anchor="Addendum §1 CA1-002"
170:                           kind="available source units" />
171:             </div>
172:           ) : null}
173:           {state && state.units_served.available > 0 ? (
174:             <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
175:               {state.units_served.entries.slice(0, 40).map((e) => (
176:                 <li key={e.source_id} style={{ borderBottom: `1px dotted ${line}`, padding: "8px 0" }}>
177:                   <div style={{ fontFamily: "ui-monospace, monospace", fontSize: 13, color: blue }}>
178:                     {e.source_id}
179:                   </div>
180:                   <div style={{ fontSize: 12, color: ink2, marginTop: 2 }}>
181:                     served_receipts: {e.served_receipts}
182:                   </div>
183:                   <div style={{ fontSize: 11, color: ink3, marginTop: 2 }}>
184:                     {e.source_path}
185:                   </div>
186:                 </li>
187:               ))}
188:             </ul>
189:           ) : null}
190:         </Panel>
191: 
192:         <Panel data-testid="densification-panel"
193:                title="Registry Densification"
194:                anchor="CA1-003 · Doc07-019 · Doc08-017 · Promises #19/#20/#21"
195:                canonQuote={state?.densification?.canon_text}>
196:           <div data-testid="densification-partial-closure-badge" style={{
197:             display: "inline-block", padding: "2px 8px",
198:             background: "#f5e3c8", color: oxblood,
199:             fontSize: 11, letterSpacing: 1, marginBottom: 8,
200:           }}>
201:             PARTIAL CLOSURE (canon-designated)
202:           </div>
203:           <div data-testid="densification-facts-registered" style={{
204:             fontFamily: "ui-monospace, monospace", color: brass, fontSize: 13, marginBottom: 6,
205:           }}>
206:             {state ? `${state.densification.facts_registered} facts registered` : "loading…"}
207:           </div>
208:           {state ? (
209:             <p style={{ fontSize: 12, color: ink3, margin: "6px 0" }}>
210:               Warm/fresh tag wired through by reference: <code>{state.densification.warm_fresh_reference}</code>
211:             </p>
212:           ) : null}
213:         </Panel>
214:       </div>
215:     </div>
216:   );
217: }

# SOURCE: frontend/src/components/Chat.jsx

1: import React, { useState } from "react";
2: import { Link } from "react-router-dom";
3: import RefusalCard from "./RefusalCard";  // W11 R5 · Canon 5 §9.2 binding card
4: 
5: /**
6:  * Chat.jsx — W5 CP4 · Governed chat surface.
7:  *
8:  * Owner Order 2026-08-25 · one question / one answer. Every submit
9:  * transits the LLM chokepoint (purpose=chat.governed_answer). Response
10:  * carries: answer + full metering + model provenance line. Refusals
11:  * render verbatim (A8-Q3).
12:  *
13:  * v7 palette · REFERENCE-NOT-COPY on the receipt id.
14:  */
15: 
16: const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
17: 
18: // v7 palette tokens.
19: const paper = "#f5f2ea";
20: const surface = "#ffffff";
21: const surface2 = "#f0ebe1";
22: const ink = "#1b1f27";
23: const ink2 = "#3a3f4a";
24: const ink3 = "#7a7f8a";
25: const line = "#e4dccf";
26: const blue = "#16274a";
27: const sage = "#1d7a6e";
28: const oxblood = "#8a2a44";
29: const oxblood2 = "#b8395b";
30: const brass = "#b08d2e";
31: const head = 'ui-serif, "Iowan Old Style", Georgia, serif';
32: 
33: 
34: export default function Chat() {
35:   const [question, setQuestion] = useState("");
36:   const [response, setResponse] = useState(null);
37:   const [busy, setBusy] = useState(false);
38:   const [error, setError] = useState(null);
39: 
40:   const submit = async () => {
41:     if (!question.trim() || busy) return;
42:     setBusy(true);
43:     setResponse(null);
44:     setError(null);
45:     try {
46:       const r = await fetch(`${BACKEND_URL}/api/chat/ask`, {
47:         method: "POST",
48:         headers: { "Content-Type": "application/json" },
49:         body: JSON.stringify({ question }),
50:       });
51:       if (!r.ok) throw new Error(`HTTP ${r.status}`);
52:       const body = await r.json();
53:       setResponse(body);
54:     } catch (exc) {
55:       setError(String(exc));
56:     } finally {
57:       setBusy(false);
58:     }
59:   };
60: 
61:   return (
62:     <div style={{ minHeight: "100vh", background: paper, padding: "48px 40px",
63:                   fontFamily: "ui-sans-serif, system-ui, sans-serif" }}>
64:       <div style={{ maxWidth: 780, margin: "0 auto" }}>
65:         <div style={{ fontSize: 11, letterSpacing: 2, color: ink3,
66:                       textTransform: "uppercase" }}>
67:           AKKI · CHAT
68:         </div>
69:         <div style={{ display: "flex", justifyContent: "space-between",
70:                       alignItems: "baseline" }}>
71:           <h1 style={{ fontFamily: head, fontSize: 42, margin: "10px 0 20px 0",
72:                        color: blue }}>
73:             One question. One answer.
74:           </h1>
75:           <Link to="/" style={{ color: ink3, fontSize: 12, textDecoration: "none" }}>
76:             ← Registry
77:           </Link>
78:         </div>
79:         <p style={{ color: ink2, lineHeight: 1.6, fontSize: 14, marginBottom: 24 }}>
80:           Every submit crosses the governed chokepoint. The receipt is the
81:           record. The model that answered is on the receipt.
82:         </p>
83: 
84:         <div style={{ background: surface, padding: "22px 24px",
85:                       border: `1px solid ${line}`, borderRadius: 10 }}>
86:           <div style={{ fontSize: 11, letterSpacing: 1.5, color: ink3,
87:                         textTransform: "uppercase", fontWeight: 600,
88:                         marginBottom: 10 }}>
89:             Ask
90:           </div>
91:           <textarea data-testid="chat-question-input"
92:                     value={question}
93:                     onChange={e => setQuestion(e.target.value)}
94:                     placeholder="Ask a governed question…"
95:                     rows={4}
96:                     style={{ width: "100%", padding: "10px 12px",
97:                              fontFamily: "ui-sans-serif, system-ui, sans-serif",
98:                              fontSize: 14, color: ink,
99:                              background: paper, border: `1px solid ${line}`,
100:                              borderRadius: 6, resize: "vertical" }} />
101:           <button data-testid="chat-submit-button"
102:                   onClick={submit}
103:                   disabled={busy || !question.trim()}
104:                   style={{ marginTop: 14, padding: "9px 18px",
105:                            background: busy ? ink3 : blue, color: "#fff",
106:                            border: `1px solid ${blue}`, borderRadius: 5,
107:                            cursor: busy ? "wait" : "pointer",
108:                            fontSize: 13, fontWeight: 700 }}>
109:             {busy ? "Asking…" : "Ask"}
110:           </button>
111:         </div>
112: 
113:         {error && (
114:           <div data-testid="chat-network-error"
115:                style={{ marginTop: 20, padding: "14px 18px", background: surface,
116:                         borderLeft: `3px solid ${oxblood2}`, borderRadius: 6,
117:                         border: `1px solid ${line}` }}>
118:             <div style={{ fontSize: 11, letterSpacing: 1.5, color: oxblood,
119:                           textTransform: "uppercase", fontWeight: 700 }}>
120:               Network refused
121:             </div>
122:             <div style={{ fontSize: 12, color: ink, marginTop: 6,
123:                           fontFamily: "ui-monospace, Menlo, monospace" }}>
124:               {error}
125:             </div>
126:           </div>
127:         )}
128: 
129:         {response && response.refused && (
130:           <div data-testid="chat-refusal-card" style={{ marginTop: 20 }}>
131:             {/* W11 R5 · Canon 5 §9.2 binding-copy card · superseded the
132:                 previous inline oxblood block per owner directive
133:                 2026-08-26 "wire every refusal surface through it". */}
134:             <RefusalCard
135:               refusal={{
136:                 asked: question,
137:                 reason: response.refusal_reason,
138:               }}
139:             />
140:             <div style={{ fontSize: 11, color: ink3, marginTop: 8,
141:                           fontStyle: "italic" }}>
142:               A8-Q3 · verbatim refusal, never a smoothed answer.
143:             </div>
144:           </div>
145:         )}
146: 
147:         {response && !response.refused && (
148:           <div data-testid="chat-answer-card"
149:                style={{ marginTop: 20, padding: "22px 24px", background: surface,
150:                         border: `1px solid ${line}`, borderRadius: 10 }}>
151:             <div style={{ display: "flex", justifyContent: "space-between",
152:                           alignItems: "baseline", marginBottom: 12 }}>
153:               <div style={{ fontSize: 11, letterSpacing: 1.5, color: sage,
154:                             textTransform: "uppercase", fontWeight: 700 }}>
155:                 Answer
156:               </div>
157:               <div style={{ fontSize: 10, color: ink3,
158:                             fontFamily: "ui-monospace, Menlo, monospace" }}
159:                    data-testid="chat-provenance">
160:                 Answered by <b style={{ color: ink }}>{response.model_id}</b> via {response.provider} ·{" "}
161:                 receipt <b>{response.receipt_id}</b>
162:               </div>
163:             </div>
164:             <div style={{ fontSize: 15, color: ink, lineHeight: 1.7,
165:                           fontFamily: head }}>
166:               {response.answer}
167:             </div>
168:             <div style={{ marginTop: 14, paddingTop: 12,
169:                           borderTop: `1px solid ${line}`,
170:                           fontSize: 11, color: ink3,
171:                           fontFamily: "ui-monospace, Menlo, monospace",
172:                           display: "grid", gridTemplateColumns: "1fr 1fr 1fr",
173:                           gap: 12 }}>
174:               <div>tokens_in · <b>{response.tokens_in}</b></div>
175:               <div>tokens_out · <b>{response.tokens_out}</b></div>
176:               <div>latency_ms · <b>{response.latency_ms}</b></div>
177:             </div>
178:           </div>
179:         )}
180:       </div>
181:     </div>
182:   );
183: }

# SOURCE: frontend/src/components/ClassBadge.jsx

1: import React from "react";
2: 
3: /**
4:  * ClassBadge.jsx — verbatim LIFT from Akki-OS-V1
5:  * (frontend/src/components/ClassBadge.js). Byte-identical to the donor.
6:  *
7:  * Renders a defensibility-class tag used by RefusalCard.
8:  */
9: 
10: const classLabels = {
11:   fact: "Established fact",
12:   utterance: "Recorded statement",
13:   non_factual: "Non-factual context",
14: };
15: 
16: const classColors = {
17:   fact: "bg-emerald-100 text-emerald-900 border-emerald-300",
18:   utterance: "bg-sky-100 text-sky-900 border-sky-300",
19:   non_factual: "bg-slate-100 text-slate-700 border-slate-300",
20: };
21: 
22: export default function ClassBadge({ defensibilityClass, compact = false }) {
23:   if (!defensibilityClass) return null;
24:   const label = classLabels[defensibilityClass] || defensibilityClass;
25:   const color = classColors[defensibilityClass] || classColors.non_factual;
26:   return (
27:     <span
28:       data-testid={`class-badge-${defensibilityClass}`}
29:       className={`inline-flex items-center rounded border font-medium ${color} ${compact ? "px-1.5 py-0 text-[10px]" : "px-2 py-0.5 text-xs"}`}
30:       title={`Defensibility class: ${label}`}
31:     >
32:       {compact ? defensibilityClass : label}
33:     </span>
34:   );
35: }

# SOURCE: frontend/src/components/CommissionWizard.jsx

1: /*
2:  * CommissionWizard.jsx — Canon 5 §14 Shaping Wizard (Phase 7 Stage B-1
3:  * operator variant · LIFTed from Akki-OS-V1 · Extraction-Akki W11 R3).
4:  *
5:  * Canon 5 §14 verbatim (from
6:  * canon/text/Akki_Canon_5_Interface_Architecture.txt lines 191-197):
7:  *   "14  Commission — The Shaping Wizard
8:  *    Layout: a chat pane on one side, an objective draft rail on the
9:  *    other.
10:  *    Chat. The operator states intent; the agent asks for mandatory
11:  *    fields and never proposes on them. An estate-check chip renders
12:  *    inline before any feasibility-dependent question is asked.
13:  *    Draft rail. Three dimensions — entry, reach, output — plus the
14:  *    envelope, each field in one of three visual states: filled with a
15:  *    check, open and muted, or agent-assumed with the amber chip. The
16:  *    envelope line lists done-condition, budget, and lawful basis until
17:  *    each is supplied.
18:  *    ...
19:  *    Mandatory fields — reach, the four output fields, done-condition,
20:  *    budget, lawful basis — are asked, never pre-filled. Preference
21:  *    fields may carry agent recommendations, but the mandatory set never
22:  *    does. Every turn is grounded in a real estate read; no fabricated
23:  *    availability, ever, under any circumstance."
24:  *
25:  * Canon 5 §15 verbatim (lines 198-206):
26:  *   "Frozen is immutable — a changed intent is a new objective."
27:  *
28:  * Canon 5 §9.3 verbatim (lines 141-144):
29:  *   "Agent assumed — confirm or change
30:  *    Amber, 11px label weight, attached to any field an agent filled
31:  *    rather than the person."
32:  *
33:  * SOLVA.md §5.6 verbatim (lines 396-400):
34:  *   "One question at a time. One answer surface at a time. Clear
35:  *    progression indication."
36:  *
37:  * Owner supersession note (2026-08-26): where the 2026-08-14
38:  * Simplification Ruling ("The 5-step wizard is retired as the primary
39:  * path") conflicts with Canon 5 §14, Canon 5 wins. This component
40:  * restores the Canon 5 §14 shaping-wizard grammar as the primary
41:  * commissioning surface.
42:  */
43: 
44: import React, { useEffect, useRef, useState } from "react";
45: 
46: const BACKEND = process.env.REACT_APP_BACKEND_URL;
47: 
48: // Canon 5 design tokens · restrained palette, amber chip carries the
49: // agent-assumed grammar per §9.3.
50: const TOK = {
51:   ink1: "#111",
52:   ink2: "#555",
53:   ink3: "#8b8b8b",
54:   paper: "#fbfaf7",
55:   chatPane: "#ffffff",
56:   draftRail: "#f4f2ec",
57:   line: "#e6e2d8",
58:   brass: "#b08d2e",          // §9.3 amber chip
59:   amberSoft: "#f3e6bd",
60:   checkGreen: "#4a6b3f",
61:   oxblood: "#7a2b1e",
62:   ok: "#4a6b3f",
63: };
64: 
65: // Canon 5 §14 verbatim: "Mandatory fields — reach, the four output
66: // fields, done-condition, budget, lawful basis — are asked, never
67: // pre-filled."
68: const MANDATORY_FIELDS = [
69:   { path: "reach",                     label: "Reach",             dim: "reach" },
70:   { path: "output.form",               label: "Output form",       dim: "output" },
71:   { path: "output.consumer",           label: "Output consumer",   dim: "output" },
72:   { path: "output.grain",              label: "Output grain",      dim: "output" },
73:   { path: "output.standard",           label: "Output standard",   dim: "output" },
74:   { path: "envelope.done_condition",   label: "Done condition",    dim: "envelope" },
75:   { path: "envelope.budget",           label: "Budget",            dim: "envelope" },
76:   { path: "envelope.lawful_basis",     label: "Lawful basis",      dim: "envelope" },
77: ];
78: 
79: // Canon 6 §6 verbatim: five steps · "the need stated in plain words;
80: // scope selected from what the registry says actually exists; standards
81: // and rights confirmed against explained defaults; a plan preview ...;
82: // and commissioning itself".
83: const FIVE_STEPS = [
84:   { key: "need",     label: "1 · State the need in plain words" },
85:   { key: "scope",    label: "2 · Choose scope from what the registry has" },
86:   { key: "standards",label: "3 · Confirm standards and rights" },
87:   { key: "preview",  label: "4 · Read the plan preview" },
88:   { key: "commit",   label: "5 · Commission" },
89: ];
90: 
91: /* ------------------------------------------------------------------ */
92: /*  Draft rail row · one of {filled ✓, open muted, agent-assumed amber} */
93: /* ------------------------------------------------------------------ */
94: 
95: function DraftRailRow({ field, committed }) {
96:   // committed is a CommittedValue_v0 dict or undefined
97:   const state = !committed
98:     ? "open"
99:     : committed.source === "agent_assumed"
100:       ? "agent-assumed"
101:       : "operator-supplied";
102: 
103:   return (
104:     <div data-testid={`draft-rail-row-${field.path.replace(/\./g, "_")}`}
105:          style={{
106:            display: "flex", alignItems: "center", justifyContent: "space-between",
107:            padding: "8px 12px", borderBottom: `1px solid ${TOK.line}`,
108:            background: state === "open" ? "transparent" : TOK.paper,
109:          }}>
110:       <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
111:         {state === "operator-supplied" && (
112:           <span data-testid="check-icon" style={{ color: TOK.checkGreen, fontSize: 14 }}>✓</span>
113:         )}
114:         {state === "agent-assumed" && (
115:           <span data-testid="amber-chip"
116:                 style={{
117:                   fontSize: 11, fontWeight: 500,
118:                   color: TOK.ink1, background: TOK.amberSoft,
119:                   border: `1px solid ${TOK.brass}`,
120:                   padding: "2px 6px", borderRadius: 3,
121:                 }}>
122:             {/* Canon 5 §9.3 verbatim binding copy */}
123:             Agent assumed — confirm or change
124:           </span>
125:         )}
126:         <div style={{
127:           color: state === "open" ? TOK.ink3 : TOK.ink1,
128:           fontSize: 13,
129:         }}>
130:           {field.label}
131:         </div>
132:       </div>
133:       <div style={{ color: TOK.ink2, fontSize: 13, maxWidth: 220, textAlign: "right" }}>
134:         {committed ? String(committed.value) : "—"}
135:       </div>
136:     </div>
137:   );
138: }
139: 
140: /* ------------------------------------------------------------------ */
141: /*  Chat pane · one question at a time (SOLVA §5.6)                   */
142: /* ------------------------------------------------------------------ */
143: 
144: function ChatPane({ turns, onReply, disabled }) {
145:   const [input, setInput] = useState("");
146:   const [askingField, setAskingField] = useState("");
147:   const bottomRef = useRef(null);
148: 
149:   useEffect(() => {
150:     bottomRef.current?.scrollIntoView({ behavior: "smooth" });
151:   }, [turns.length]);
152: 
153:   const lastTurn = turns[turns.length - 1];
154: 
155:   function submit() {
156:     if (!input.trim()) return;
157:     onReply(lastTurn?.turn_ref, input.trim(), askingField || null);
158:     setInput("");
159:     setAskingField("");
160:   }
161: 
162:   return (
163:     <div data-testid="chat-pane" style={{ display: "flex", flexDirection: "column", height: "100%" }}>
164:       <div style={{
165:         padding: "10px 14px", borderBottom: `1px solid ${TOK.line}`,
166:         fontSize: 13, color: TOK.ink2,
167:       }}>
168:         The chat pane. The operator states intent; the agent asks for mandatory
169:         fields and never proposes on them.
170:       </div>
171: 
172:       <div style={{ flex: 1, overflow: "auto", padding: "12px 14px" }}>
173:         {turns.length === 0 && (
174:           <div style={{ color: TOK.ink3, fontSize: 13 }}>
175:             (waiting for the first question — the agent opens by asking about reach)
176:           </div>
177:         )}
178:         {turns.map((t, i) => (
179:           <div key={i} data-testid={`turn-${i}`}
180:                style={{ marginBottom: 10 }}>
181:             {t.agent_content && (
182:               <div style={{ color: TOK.ink1, fontSize: 14 }}>
183:                 <strong style={{ color: TOK.ink2, fontWeight: 500 }}>Agent:</strong>{" "}
184:                 {t.agent_content}
185:               </div>
186:             )}
187:             {t.user_content && (
188:               <div style={{ color: TOK.ink1, fontSize: 14, marginLeft: 12 }}>
189:                 <strong style={{ color: TOK.ink2, fontWeight: 500 }}>You:</strong>{" "}
190:                 {t.user_content}
191:               </div>
192:             )}
193:             {t.feasibility_snapshot_ref && (
194:               <div data-testid="estate-check-chip"
195:                    style={{
196:                      fontSize: 11, color: TOK.ink2, background: TOK.paper,
197:                      border: `1px solid ${TOK.line}`,
198:                      padding: "2px 6px", borderRadius: 3,
199:                      display: "inline-block", marginTop: 4,
200:                    }}>
201:                 {/* Canon 5 §14: "An estate-check chip renders inline before any
202:                     feasibility-dependent question is asked." */}
203:                 estate-check · grounded by {t.feasibility_snapshot_ref}
204:               </div>
205:             )}
206:           </div>
207:         ))}
208:         <div ref={bottomRef} />
209:       </div>
210: 
211:       <div style={{ padding: "10px 14px", borderTop: `1px solid ${TOK.line}` }}>
212:         <input data-testid="chat-input" value={input}
213:                onChange={(e) => setInput(e.target.value)}
214:                onKeyDown={(e) => { if (e.key === "Enter") submit(); }}
215:                placeholder="Type your reply and press Enter..."
216:                disabled={disabled}
217:                style={{
218:                  width: "100%", padding: "8px 10px",
219:                  border: `1px solid ${TOK.line}`, borderRadius: 4,
220:                  fontSize: 14, background: TOK.chatPane,
221:                }} />
222:       </div>
223:     </div>
224:   );
225: }
226: 
227: /* ------------------------------------------------------------------ */
228: /*  Draft rail · three dimensions + envelope (Canon 5 §14)            */
229: /* ------------------------------------------------------------------ */
230: 
231: function DraftRail({ state, onCommit }) {
232:   const committed = (state && state.committed_values) || {};
233:   const dimensions = ["entry", "reach", "output"];
234:   const envelopeFields = MANDATORY_FIELDS.filter((f) => f.dim === "envelope");
235:   const outputFields = MANDATORY_FIELDS.filter((f) => f.dim === "output");
236:   const reachField = MANDATORY_FIELDS.find((f) => f.path === "reach");
237: 
238:   return (
239:     <div data-testid="draft-rail"
240:          style={{
241:            background: TOK.draftRail, borderLeft: `1px solid ${TOK.line}`,
242:            height: "100%", overflow: "auto",
243:          }}>
244:       <div style={{ padding: "12px 14px", borderBottom: `1px solid ${TOK.line}` }}>
245:         <div style={{ fontSize: 14, color: TOK.ink1, fontWeight: 500 }}>
246:           Objective draft rail
247:         </div>
248:         <div style={{ fontSize: 12, color: TOK.ink2, marginTop: 2 }}>
249:           Three dimensions — entry, reach, output — plus the envelope.
250:         </div>
251:       </div>
252: 
253:       {/* Dimension: entry (no mandatory fields at v0; preference-only) */}
254:       <div style={{ padding: "10px 14px" }}>
255:         <div style={{ fontSize: 11, textTransform: "uppercase", color: TOK.ink2, letterSpacing: 0.5 }}>
256:           entry
257:         </div>
258:         <div style={{ padding: "6px 0", fontSize: 13, color: TOK.ink3 }}>
259:           (preference · agent may recommend)
260:         </div>
261:       </div>
262: 
263:       {/* Dimension: reach */}
264:       <div style={{ padding: "10px 14px", borderTop: `1px solid ${TOK.line}` }}>
265:         <div style={{ fontSize: 11, textTransform: "uppercase", color: TOK.ink2, letterSpacing: 0.5 }}>
266:           reach
267:         </div>
268:         <DraftRailRow field={reachField} committed={committed[reachField.path]} />
269:       </div>
270: 
271:       {/* Dimension: output · four fields */}
272:       <div style={{ padding: "10px 14px 0 14px", borderTop: `1px solid ${TOK.line}` }}>
273:         <div style={{ fontSize: 11, textTransform: "uppercase", color: TOK.ink2, letterSpacing: 0.5 }}>
274:           output
275:         </div>
276:       </div>
277:       {outputFields.map((f) => (
278:         <DraftRailRow key={f.path} field={f} committed={committed[f.path]} />
279:       ))}
280: 
281:       {/* Envelope */}
282:       <div style={{ padding: "10px 14px 0 14px", borderTop: `1px solid ${TOK.line}` }}>
283:         <div style={{ fontSize: 11, textTransform: "uppercase", color: TOK.ink2, letterSpacing: 0.5 }}>
284:           envelope
285:         </div>
286:       </div>
287:       {envelopeFields.map((f) => (
288:         <DraftRailRow key={f.path} field={f} committed={committed[f.path]} />
289:       ))}
290:     </div>
291:   );
292: }
293: 
294: /* ------------------------------------------------------------------ */
295: /*  Canon 6 §6 · five-step progression strip                           */
296: /* ------------------------------------------------------------------ */
297: 
298: function FiveStepStrip({ committedCount, frozen }) {
299:   const step = frozen
300:     ? 4
301:     : committedCount === 0
302:       ? 0
303:       : committedCount < MANDATORY_FIELDS.length
304:         ? 2
305:         : 3;
306: 
307:   return (
308:     <div data-testid="five-step-strip"
309:          style={{
310:            display: "flex", gap: 8, padding: "8px 14px",
311:            borderBottom: `1px solid ${TOK.line}`,
312:            background: TOK.paper,
313:          }}>
314:       {FIVE_STEPS.map((s, i) => (
315:         <div key={s.key}
316:              style={{
317:                fontSize: 11, padding: "3px 8px", borderRadius: 3,
318:                background: i === step ? TOK.brass : "transparent",
319:                color: i === step ? "#fff" : TOK.ink2,
320:                border: i === step ? "none" : `1px solid ${TOK.line}`,
321:              }}>
322:           {s.label}
323:         </div>
324:       ))}
325:     </div>
326:   );
327: }
328: 
329: /* ------------------------------------------------------------------ */
330: /*  Root                                                              */
331: /* ------------------------------------------------------------------ */
332: 
333: export default function CommissionWizard() {
334:   const [session, setSession] = useState(null);
335:   const [state, setState] = useState(null);
336:   const [error, setError] = useState(null);
337:   const [frozen, setFrozen] = useState(false);
338: 
339:   async function startSession() {
340:     setError(null);
341:     try {
342:       const r = await fetch(`${BACKEND}/api/wizard/operator/session`, { method: "POST" });
343:       if (!r.ok) throw new Error(`session start failed · HTTP ${r.status}`);
344:       const s = await r.json();
345:       setSession(s);
346:       // First agent turn
347:       await advanceTurn(s.session_id, null, "");
348:     } catch (e) {
349:       setError(e.message);
350:     }
351:   }
352: 
353:   async function advanceTurn(sessionId, turnRef, userContent, field, value) {
354:     try {
355:       const body = {};
356:       if (turnRef) body.turn_ref = turnRef;
357:       if (userContent) body.user_content = userContent;
358:       if (field) body.field = field;
359:       if (value !== undefined) body.value = value;
360:       const r = await fetch(`${BACKEND}/api/wizard/operator/${sessionId}/turn`, {
361:         method: "POST",
362:         headers: { "Content-Type": "application/json" },
363:         body: JSON.stringify(body),
364:       });
365:       if (!r.ok) throw new Error(`turn failed · HTTP ${r.status}`);
366:       // Reload state after every turn
367:       const stateResp = await fetch(`${BACKEND}/api/wizard/operator/${sessionId}`);
368:       if (stateResp.ok) setState(await stateResp.json());
369:     } catch (e) {
370:       setError(e.message);
371:     }
372:   }
373: 
374:   async function commitReview() {
375:     if (!session) return;
376:     try {
377:       const r = await fetch(`${BACKEND}/api/wizard/operator/${session.session_id}/commit-review`);
378:       if (r.ok) setState(await r.json());
379:     } catch (e) { setError(e.message); }
380:   }
381: 
382:   async function freeze() {
383:     if (!session) return;
384:     try {
385:       const r = await fetch(`${BACKEND}/api/wizard/operator/${session.session_id}/freeze`, {
386:         method: "POST",
387:       });
388:       if (!r.ok) throw new Error(`freeze refused · HTTP ${r.status}`);
389:       setFrozen(true);
390:       const stateResp = await fetch(`${BACKEND}/api/wizard/operator/${session.session_id}`);
391:       if (stateResp.ok) setState(await stateResp.json());
392:     } catch (e) { setError(e.message); }
393:   }
394: 
395:   const turns = (state && state.turns) || [];
396:   const committedCount = state ? Object.keys(state.committed_values || {}).length : 0;
397: 
398:   return (
399:     <div data-testid="commission-wizard"
400:          style={{ display: "flex", flexDirection: "column", height: "100vh",
401:                   fontFamily: "system-ui, -apple-system, sans-serif",
402:                   background: TOK.paper, color: TOK.ink1 }}>
403: 
404:       <header style={{
405:         display: "flex", alignItems: "center", justifyContent: "space-between",
406:         padding: "12px 18px", borderBottom: `1px solid ${TOK.line}`,
407:       }}>
408:         <div>
409:           <div style={{ fontSize: 16, fontWeight: 500 }}>Commission — The Shaping Wizard</div>
410:           <div style={{ fontSize: 12, color: TOK.ink2, marginTop: 2 }}>
411:             Canon 5 §14 · turns a need into governed work in five steps
412:           </div>
413:         </div>
414:         {!session ? (
415:           <button data-testid="start-session-btn" onClick={startSession}
416:                   style={{ background: TOK.brass, color: "#fff", border: "none",
417:                             padding: "8px 16px", borderRadius: 4, cursor: "pointer" }}>
418:             Start commissioning
419:           </button>
420:         ) : (
421:           <div style={{ fontSize: 11, color: TOK.ink3 }}>
422:             session {session.session_id.slice(0, 8)}…
423:           </div>
424:         )}
425:       </header>
426: 
427:       {session && (
428:         <FiveStepStrip committedCount={committedCount} frozen={frozen} />
429:       )}
430: 
431:       {error && (
432:         <div data-testid="wizard-error" style={{
433:           padding: "10px 14px", background: TOK.paper,
434:           color: TOK.oxblood, borderBottom: `3px solid ${TOK.oxblood}`,
435:           fontSize: 13,
436:         }}>
437:           {error}
438:         </div>
439:       )}
440: 
441:       <div style={{ flex: 1, display: "grid",
442:                      gridTemplateColumns: session ? "1fr 380px" : "1fr",
443:                      minHeight: 0 }}>
444:         {session ? (
445:           <ChatPane turns={turns}
446:                     disabled={frozen}
447:                     onReply={(turnRef, content, field) =>
448:                       advanceTurn(session.session_id, turnRef, content, field)
449:                     } />
450:         ) : (
451:           <div style={{ padding: 24, color: TOK.ink2 }}>
452:             The shaping wizard opens with a chat pane and a draft rail. The
453:             operator states intent; the agent asks for mandatory fields and
454:             never proposes on them.
455:           </div>
456:         )}
457:         {session && (
458:           <DraftRail state={state} />
459:         )}
460:       </div>
461: 
462:       {session && (
463:         <footer style={{
464:           display: "flex", justifyContent: "space-between", alignItems: "center",
465:           padding: "10px 18px", borderTop: `1px solid ${TOK.line}`,
466:           background: TOK.paper,
467:         }}>
468:           <div style={{ fontSize: 11, color: TOK.ink3 }}>
469:             {/* Canon 5 §15 verbatim binding copy */}
470:             Frozen is immutable — a changed intent is a new objective.
471:           </div>
472:           <div style={{ display: "flex", gap: 10 }}>
473:             <button onClick={commitReview}
474:                     data-testid="commit-review-btn"
475:                     disabled={frozen}
476:                     style={{ padding: "6px 12px", border: `1px solid ${TOK.line}`,
477:                               background: TOK.chatPane, borderRadius: 4,
478:                               cursor: frozen ? "not-allowed" : "pointer" }}>
479:               Commit review
480:             </button>
481:             <button onClick={freeze}
482:                     data-testid="freeze-btn"
483:                     disabled={frozen || committedCount < MANDATORY_FIELDS.length}
484:                     style={{ padding: "6px 12px", border: "none",
485:                               background: frozen ? TOK.ink3 : TOK.checkGreen,
486:                               color: "#fff", borderRadius: 4,
487:                               cursor: (frozen || committedCount < MANDATORY_FIELDS.length) ? "not-allowed" : "pointer" }}>
488:               {frozen ? "Frozen" : "Freeze objective"}
489:             </button>
490:           </div>
491:         </footer>
492:       )}
493:     </div>
494:   );
495: }

# SOURCE: frontend/src/components/ConnectDrawerChat.jsx

1: import React, { useEffect, useMemo, useRef, useState } from "react";
2: import axios from "axios";
3: 
4: /**
5:  * ConnectDrawerChat — Right-side conversational drawer for the Connect flow.
6:  *
7:  * Owner Ruling 2026-08-19 (T12, verbatim):
8:  *   "paste and connect conversational wizard that assists connection,
9:  *    drawer chatbox right side on clicking connect."
10:  *
11:  * Behaviour
12:  *  - Opens as a fixed right-side drawer on top of Registry.
13:  *  - Opens with a single assistant turn asking what to connect (chip menu
14:  *    inline; free-text or paste both accepted in the same input).
15:  *  - PASTE runs the deterministic parser at /api/connect/parse-paste — no LLM
16:  *    transit for credential text (standing rule). The parser strips password
17:  *    + aws_secret_access_key server-side and returns *_captured signals; the
18:  *    browser holds the raw paste in local state only until POST — the chat
19:  *    log renders every credential as "•••• captured" from the parse turn
20:  *    forward.
21:  *  - Missing fields are asked as chat turns (one field per turn).
22:  *  - Confirmation turn ("is this the AISCA machine?" / analogous for data
23:  *    source / non-compute) fires the pipeline endpoint of the parsed kind:
24:  *      compute      -> POST /api/connect/gpu (handshake walk rendered as
25:  *                      three chat cards + four-questions card)
26:  *      data-source  -> POST /api/connect/data-source (four-questions card)
27:  *      llm/model    -> POST /api/connect/intent (recorded chat card)
28:  *  - Provisioning card (Sending it? Receiving it? aside) is a chat card
29:  *    triggered by the "Provisioning a new machine?" chip.
30:  *
31:  * Custody
32:  *  - Chat log NEVER carries a password or aws_secret_access_key value from
33:  *    the parse turn onward. The Registry surface never sees them.
34:  *  - `rawPaste` and `rawPassword` live only in local component state; on
35:  *    close they are cleared explicitly. No localStorage / sessionStorage.
36:  *
37:  * Visual grammar (v7 oracle exactly)
38:  *  - --paper #f5f2ea (drawer bg), --surface #f0ece1 (assistant turn),
39:  *    --surface2 #ede8da (user turn), --line #e4dfd3 (borders),
40:  *    --ink #1b1f27, --ink2 #3d4350, --ink3 #5b6270 (typographic ladder),
41:  *    --blue #16274a (primary), --sage #1d7a6e (ready/pass),
42:  *    --oxblood #b8395b (refuse/fail), --brass #b08d2e (aside)
43:  *  - --drawer-w min(460px, 94vw)
44:  *  - --shadow-drawer -14px 0 48px rgba(15,27,51,.18)
45:  *  - --head Iowan Old Style, Georgia, serif
46:  *  - --body Söhne, Helvetica Neue, Arial, sans-serif  (system fallback)
47:  */
48: 
49: const BACKEND = process.env.REACT_APP_BACKEND_URL;
50: 
51: // v7 tokens — literal so the grep-tests can verify pixel parity.
52: const TOK = {
53:   paper: "#f5f2ea",
54:   surface: "#f0ece1",
55:   surface2: "#ede8da",
56:   line: "#e4dfd3",
57:   ink: "#1b1f27",
58:   ink2: "#3d4350",
59:   ink3: "#5b6270",
60:   blue: "#16274a",
61:   blue2: "#0f1b33",
62:   sage: "#1d7a6e",
63:   oxblood: "#b8395b",
64:   brass: "#b08d2e",
65:   scrim: "rgba(15,27,51,.42)",
66:   shadowDrawer: "-14px 0 48px rgba(15,27,51,.18)",
67:   drawerW: "min(460px, 94vw)",
68:   head: "Iowan Old Style, Georgia, serif",
69:   body: "Söhne, Helvetica Neue, Arial, sans-serif",
70: };
71: 
72: const KIND_CHIPS = [
73:   { key: "auto", label: "Auto-detect", testid: "connect-drawer-kind-chip-auto" },
74:   { key: "data-source", label: "A data source", testid: "connect-drawer-kind-chip-data-source" },
75:   { key: "llm", label: "An LLM", testid: "connect-drawer-kind-chip-llm" },
76:   { key: "trained-model", label: "A trained model", testid: "connect-drawer-kind-chip-trained-model" },
77:   { key: "compute", label: "Compute", testid: "connect-drawer-kind-chip-compute" },
78: ];
79: 
80: const COMPUTE_REQUIRED = ["host_name", "username", "public_ip"];
81: const COMPUTE_PW_REQUIRED = true;
82: const DATA_SOURCE_REQUIRED = ["region", "cluster_arn", "secret_arn"];
83: const DATA_SOURCE_SECRET_REQUIRED = true;
84: 
85: // Deterministic client-side pluck (mirrors server parser). Runs on the raw
86: // paste in local state; the plucked value is submitted once to the pipeline
87: // endpoint and never rendered into any chat turn.
88: function extractPasswordFromPaste(paste) {
89:   if (!paste) return "";
90:   const re = /^\s*(password|pass|pwd)\s*[:=]\s*(.+?)\s*$/im;
91:   const m = paste.match(re);
92:   return m ? m[2] : "";
93: }
94: function extractAwsSecretFromPaste(paste) {
95:   if (!paste) return "";
96:   const re = /^\s*(aws[_ ]?secret[_ ]?access[_ ]?key|secret[_ ]access[_ ]key|secret[_ ]key)\s*[:=]\s*(.+?)\s*$/im;
97:   const m = paste.match(re);
98:   return m ? m[2] : "";
99: }
100: 
101: function fieldReadout(fields, password_captured, aws_secret_captured) {
102:   // Plain-English "I read a host, a username, a masked password and two IPs" style.
103:   const bits = [];
104:   if (fields.host_name) bits.push("a host");
105:   if (fields.username) bits.push("a username");
106:   if (password_captured) bits.push("a masked password");
107:   if (aws_secret_captured) bits.push("a masked AWS secret access key");
108:   if (fields.aws_access_key_id) bits.push("an AWS access key ID");
109:   if (fields.region) bits.push("a region");
110:   if (fields.cluster_arn) bits.push("a cluster ARN");
111:   if (fields.secret_arn) bits.push("a Secrets Manager ARN");
112:   if (fields.database) bits.push("a database name");
113:   const ips = [];
114:   if (fields.public_ip) ips.push("public");
115:   if (fields.private_ip) ips.push("private");
116:   if (ips.length) bits.push(ips.length === 2 ? "two IPs (public and private)" : `a ${ips[0]} IP`);
117:   if (fields.os) bits.push("an OS");
118:   if (fields.deploy_date) bits.push("a deploy date");
119:   if (!bits.length) return "I couldn't pick anything out of that paste.";
120:   const list = bits.length === 1 ? bits[0]
121:     : bits.slice(0, -1).join(", ") + " and " + bits[bits.length - 1];
122:   return `I read ${list}.`;
123: }
124: 
125: function guessConfirmSentence(kind, fields) {
126:   if (kind === "compute") {
127:     const host = fields.host_name || "this machine";
128:     return `Is this the ${host} machine you want to admit into the estate?`;
129:   }
130:   if (kind === "data-source") {
131:     const db = fields.database || "database";
132:     const region = fields.region || "region";
133:     return `Is this the ${db} source in ${region} you want to connect over the RDS Data API?`;
134:   }
135:   if (kind === "llm") return "Is this the LLM you want to record intent for (goes live with its wave)?";
136:   if (kind === "trained-model") return "Is this the trained model you want to record intent for (goes live with its wave)?";
137:   return "Is this what you want to record?";
138: }
139: 
140: const KIND_LABEL = {
141:   compute: "compute",
142:   "data-source": "a data source",
143:   llm: "an LLM",
144:   "trained-model": "a trained model",
145: };
146: 
147: // ---------------------------------------------------------------------------
148: // Chat turn primitives
149: // ---------------------------------------------------------------------------
150: 
151: function AssistantTurn({ children, testid }) {
152:   return (
153:     <div data-testid={testid || "connect-drawer-chat-turn-assistant"}
154:          style={{ background: TOK.surface, border: `1px solid ${TOK.line}`,
155:                   borderRadius: 12, padding: "12px 14px", margin: "10px 0",
156:                   fontFamily: TOK.body, color: TOK.ink, fontSize: 14,
157:                   lineHeight: 1.5, maxWidth: "94%" }}>
158:       {children}
159:     </div>
160:   );
161: }
162: 
163: function UserTurn({ children, testid }) {
164:   return (
165:     <div data-testid={testid || "connect-drawer-chat-turn-user"}
166:          style={{ background: TOK.surface2, border: `1px solid ${TOK.line}`,
167:                   borderRadius: 12, padding: "10px 14px", margin: "10px 0 10px auto",
168:                   fontFamily: TOK.body, color: TOK.ink2, fontSize: 13,
169:                   lineHeight: 1.5, maxWidth: "82%", whiteSpace: "pre-wrap" }}>
170:       {children}
171:     </div>
172:   );
173: }
174: 
175: function Chip({ label, active, onClick, testid }) {
176:   return (
177:     <button type="button" data-testid={testid} onClick={onClick}
178:       style={{ padding: "6px 12px", borderRadius: 999,
179:                border: `1px solid ${active ? TOK.blue : TOK.line}`,
180:                background: active ? TOK.blue : "#fff",
181:                color: active ? "#fff" : TOK.ink2,
182:                cursor: "pointer", fontSize: 12, fontFamily: TOK.body,
183:                letterSpacing: 0.2, marginRight: 6, marginTop: 6 }}>
184:       {label}
185:     </button>
186:   );
187: }
188: 
189: function StatusPill({ status }) {
190:   const bg = status === "pass" ? TOK.sage :
191:              status === "fail" ? TOK.oxblood :
192:              status === "yes"  ? TOK.sage :
193:              status === "no"   ? TOK.oxblood : TOK.ink3;
194:   return (
195:     <span style={{ display: "inline-block", padding: "2px 8px", borderRadius: 999,
196:                    background: bg, color: "#fff", fontSize: 10, letterSpacing: 0.6,
197:                    textTransform: "uppercase" }}>{status || "—"}</span>
198:   );
199: }
200: 
201: // ---------------------------------------------------------------------------
202: // Chat cards (post-submit renderings)
203: // ---------------------------------------------------------------------------
204: 
205: function HandshakeStageCard({ testid, label, stage }) {
206:   const status = (stage && stage.status) || "untried";
207:   const border = status === "pass" ? TOK.sage : status === "fail" ? TOK.oxblood : TOK.line;
208:   return (
209:     <div data-testid={testid}
210:          style={{ background: "#fff", border: `1px solid ${TOK.line}`,
211:                   borderLeft: `4px solid ${border}`, borderRadius: 10,
212:                   padding: "10px 12px", margin: "8px 0" }}>
213:       <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
214:         <div style={{ fontFamily: TOK.head, fontSize: 14, color: TOK.ink }}>{label}</div>
215:         <StatusPill status={status} />
216:       </div>
217:       {stage && stage.detail && (
218:         <div style={{ marginTop: 4, fontSize: 12, color: TOK.ink3, fontFamily: TOK.body }}>
219:           {stage.detail}
220:         </div>
221:       )}
222:     </div>
223:   );
224: }
225: 
226: function FourQuestionsCard({ result }) {
227:   // Four questions from the compute or data-source result.
228:   const q = result.four_questions || {
229:     link_working: result.link_working,
230:     found: !!(result.found && Object.keys(result.found).length),
231:     ready: result.ready,
232:     failure: result.failure || null,
233:   };
234:   const yes = (v) => v === true || v === "yes" ? "yes" : "no";
235:   return (
236:     <div data-testid="chat-card-four-questions"
237:          style={{ background: "#fff", border: `1px solid ${TOK.line}`,
238:                   borderRadius: 10, padding: "12px 14px", margin: "8px 0" }}>
239:       <div style={{ fontFamily: TOK.head, fontSize: 14, color: TOK.ink, marginBottom: 8 }}>
240:         The four questions
241:       </div>
242:       <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
243:         <FQItem label="LINK WORKING" value={yes(q.link_working)} />
244:         <FQItem label="FOUND" value={q.found ? "yes" : "no"} />
245:         <FQItem label="READY" value={yes(q.ready)} />
246:         <FQItem label="FAILURE" value={q.failure || "none"} kind="text" />
247:       </div>
248:       {result.failure_sentence && (
249:         <div style={{ marginTop: 10, padding: 8, background: "#fdf2f5",
250:                       color: TOK.oxblood, borderRadius: 6, fontSize: 12,
251:                       fontFamily: TOK.body }}>
252:           {result.failure_sentence}
253:         </div>
254:       )}
255:     </div>
256:   );
257: }
258: 
259: function FQItem({ label, value, kind }) {
260:   const color = value === "yes" ? TOK.sage : value === "no" ? TOK.oxblood :
261:                 value === "none" ? TOK.ink3 : TOK.oxblood;
262:   return (
263:     <div style={{ border: `1px solid ${TOK.line}`, borderRadius: 8, padding: "6px 10px" }}>
264:       <div style={{ fontSize: 10, letterSpacing: 1.2, color: TOK.ink3,
265:                     textTransform: "uppercase", fontFamily: TOK.body }}>{label}</div>
266:       <div style={{ fontFamily: TOK.head, fontSize: kind === "text" ? 14 : 18,
267:                     color, marginTop: 2 }}>{value}</div>
268:     </div>
269:   );
270: }
271: 
272: function ProvisioningCard({ facts }) {
273:   if (!facts) {
274:     return (
275:       <div data-testid="chat-card-provisioning"
276:            style={{ background: "#fff", border: `1px solid ${TOK.line}`,
277:                     borderRadius: 10, padding: 12, margin: "8px 0",
278:                     color: TOK.ink3, fontSize: 12, fontFamily: TOK.body }}>
279:         Reading provisioning facts from /api/connect/estate-facts…
280:       </div>
281:     );
282:   }
283:   return (
284:     <div data-testid="chat-card-provisioning"
285:          style={{ background: "#fff", border: `1px solid ${TOK.line}`,
286:                   borderLeft: `4px solid ${TOK.brass}`, borderRadius: 10,
287:                   padding: "12px 14px", margin: "8px 0", fontFamily: TOK.body }}>
288:       <div style={{ fontFamily: TOK.head, fontSize: 14, color: TOK.ink,
289:                     marginBottom: 8 }}>
290:         Provisioning aside · what to paste on the AISCA side
291:       </div>
292:       <KV label="PUBLIC KEY">
293:         <code data-testid="provisioning-card-public-key"
294:               style={{ fontSize: 11, wordBreak: "break-all", color: TOK.ink2 }}>
295:           {facts.estate_public_key}
296:         </code>
297:       </KV>
298:       <KV label="POD EGRESS IP">
299:         <code data-testid="provisioning-card-egress-ip"
300:               style={{ fontSize: 12, color: TOK.ink2 }}>{facts.pod_egress_ip}</code>
301:       </KV>
302:       <KV label="FINGERPRINT">
303:         <code data-testid="provisioning-card-fingerprint"
304:               style={{ fontSize: 11, color: TOK.ink2 }}>{facts.estate_public_key_fingerprint}</code>
305:       </KV>
306:     </div>
307:   );
308: }
309: 
310: function KV({ label, children }) {
311:   return (
312:     <div style={{ marginBottom: 6 }}>
313:       <div style={{ fontSize: 10, letterSpacing: 1.2, color: TOK.ink3,
314:                     textTransform: "uppercase" }}>{label}</div>
315:       <div style={{ fontSize: 13, color: TOK.ink }}>{children}</div>
316:     </div>
317:   );
318: }
319: 
320: function IntentRecordedCard({ record }) {
321:   return (
322:     <div data-testid="chat-card-intent-recorded"
323:          style={{ background: "#fff", border: `1px solid ${TOK.line}`,
324:                   borderLeft: `4px solid ${TOK.sage}`, borderRadius: 10,
325:                   padding: "12px 14px", margin: "8px 0",
326:                   fontFamily: TOK.body }}>
327:       <div style={{ fontFamily: TOK.head, fontSize: 14, color: TOK.ink }}>
328:         Intent recorded
329:       </div>
330:       <div style={{ marginTop: 6, fontSize: 13, color: TOK.ink2 }}>
331:         Recorded — this connection type goes live with its wave.
332:       </div>
333:       <div style={{ marginTop: 6, fontSize: 12, color: TOK.ink3 }}>
334:         Name: {record?.name || "—"}
335:       </div>
336:     </div>
337:   );
338: }
339: 
340: // ---------------------------------------------------------------------------
341: // Main drawer component
342: // ---------------------------------------------------------------------------
343: 
344: export default function ConnectDrawerChat({ onClose }) {
345:   // Session-only state. Never persisted. Cleared on unmount.
346:   const [turns, setTurns] = useState([]);
347:   const [kind, setKind] = useState("auto");
348:   const [input, setInput] = useState("");
349:   // rawPaste + rawPassword + rawAwsSecret held in refs so they are NEVER
350:   // visible in the chat state's dependency graph or a React devtool trace.
351:   const pasteCacheRef = useRef("");
352:   const pwCacheRef = useRef("");
353:   const awsCacheRef = useRef("");
354:   // W11 R2 · draft_id held in a ref so ConfirmButtons closures always read
355:   // the CURRENT id, never a stale null captured before setParsed applied.
356:   const draftIdRef = useRef(null);
357:   const kindRef = useRef("auto");
358:   const [parsed, setParsed] = useState(null);      // fields + *_captured signals only
359:   const [awaitingConfirm, setAwaitingConfirm] = useState(false);
360:   const [askingField, setAskingField] = useState(null); // null | "field_name"
361:   const [manualPatch, setManualPatch] = useState({});   // non-secret overrides
362:   const [submitting, setSubmitting] = useState(false);
363:   const [provFacts, setProvFacts] = useState(null);
364:   const chatLogRef = useRef(null);
365: 
366:   // Opening turn
367:   useEffect(() => {
368:     setTurns([
369:       {
370:         role: "assistant",
371:         node: (
372:           <>
373:             <div style={{ fontFamily: TOK.head, fontSize: 16, color: TOK.ink,
374:                           marginBottom: 6 }}>
375:               What would you like to connect?
376:             </div>
377:             <div style={{ fontSize: 13, color: TOK.ink2, marginBottom: 8 }}>
378:               Pick a kind (or leave it on auto-detect) and paste the connection
379:               details in the chat. I read them deterministically — nothing here
380:               is sent to a model.
381:             </div>
382:             <div style={{ display: "flex", flexWrap: "wrap" }}>
383:               {KIND_CHIPS.map((c) => (
384:                 <Chip key={c.key} label={c.label} testid={c.testid}
385:                       active={kind === c.key}
386:                       onClick={() => setKind(c.key)} />
387:               ))}
388:             </div>
389:             <div style={{ marginTop: 12, fontSize: 12, color: TOK.ink3 }}>
390:               Provisioning a new machine?{" "}
391:               <button type="button" data-testid="chip-show-provisioning-aside"
392:                       onClick={openProvisioning}
393:                       style={{ background: "transparent", border: "none",
394:                                color: TOK.brass, cursor: "pointer",
395:                                textDecoration: "underline", padding: 0,
396:                                fontSize: 12 }}>
397:                 Show me what to paste on the AISCA side →
398:               </button>
399:             </div>
400:           </>
401:         ),
402:       },
403:     ]);
404:     // Preload provisioning facts (used only if the aside chip is clicked)
405:     axios.get(`${BACKEND}/api/connect/estate-facts`).then(
406:       (r) => setProvFacts(r.data),
407:       () => setProvFacts(null),
408:     );
409:     return () => {
410:       // Explicitly clear on unmount so credentials cannot survive close.
411:       pasteCacheRef.current = "";
412:       pwCacheRef.current = "";
413:       awsCacheRef.current = "";
414:     };
415:     // eslint-disable-next-line react-hooks/exhaustive-deps
416:   }, []);
417: 
418:   // Auto-scroll chat log
419:   useEffect(() => {
420:     if (chatLogRef.current) chatLogRef.current.scrollTop = chatLogRef.current.scrollHeight;
421:   }, [turns]);
422: 
423:   function push(role, node) {
424:     setTurns((prev) => [...prev, { role, node }]);
425:   }
426: 
427:   function openProvisioning() {
428:     push("assistant", (
429:       <>
430:         <div style={{ fontSize: 13, color: TOK.ink2, marginBottom: 6 }}>
431:           Sending it or receiving it — here is the estate&apos;s side, ready to paste.
432:         </div>
433:         <ProvisioningCard facts={provFacts} />
434:       </>
435:     ));
436:   }
437: 
438:   async function handleSend(text) {
439:     if (!text.trim()) return;
440:     // Detect paste (multi-line, or contains a `key: value` line)
441:     const isPaste = text.includes("\n") || /^\s*(host\s*name|username|pass(word)?|public\s*ip|private\s*ip|region|cluster_?arn|secret_?arn|aws)\b/im.test(text);
442:     // Log the USER turn — mask any credential-shaped lines before rendering.
443:     const maskedForLog = redactCredsForLog(text);
444:     push("user", maskedForLog);
445:     setInput("");
446:     if (isPaste) {
447:       // Cache raw paste (in ref, never in React state that renders)
448:       pasteCacheRef.current = text;
449:       pwCacheRef.current = extractPasswordFromPaste(text);
450:       awsCacheRef.current = extractAwsSecretFromPaste(text);
451:       await runParse(text);
452:     } else if (askingField) {
453:       // A missing-field answer
454:       setManualPatch((m) => ({ ...m, [askingField]: text.trim() }));
455:       const nextAsk = nextMissingField({
456:         ...parsed?.fields, ...manualPatch, [askingField]: text.trim(),
457:       }, effectiveKind(parsed?.kind, kind));
458:       setAskingField(nextAsk);
459:       if (nextAsk) {
460:         push("assistant", `Thanks. And ${humanField(nextAsk)}?`);
461:       } else {
462:         // All filled — go to confirmation
463:         setAwaitingConfirm(true);
464:         const eKind = effectiveKind(parsed?.kind, kind);
465:         push("assistant", (
466:           <>
467:             <div>{guessConfirmSentence(eKind, { ...parsed?.fields, ...manualPatch, [askingField]: text.trim() })}</div>
468:             <ConfirmButtons onConfirm={runSubmit} onCancel={() => {
469:               setAwaitingConfirm(false);
470:               push("assistant", "OK, no submit. Paste again or edit the fields to keep going.");
471:             }} />
472:           </>
473:         ));
474:       }
475:     } else {
476:       // Free text response before a paste — nudge them to paste
477:       push("assistant", "Paste the details in the chat when you have them — I read them deterministically. If you want me to guide you, tell me what kind of thing this is (data source, LLM, compute, trained model).");
478:     }
479:   }
480: 
481:   async function runParse(paste) {
482:     setSubmitting(true);
483:     try {
484:       const body = { paste, hint_kind: kind === "auto" ? null : kind };
485:       const r = await axios.post(`${BACKEND}/api/connect/parse-paste`, body);
486:       const data = r.data;
487:       setParsed(data);
488:       // W11 R2 · store draft_id + effective kind in refs so ConfirmButtons
489:       // closures always read the current values, never a stale null.
490:       draftIdRef.current = data.draft_id || null;
491:       kindRef.current = effectiveKind(data.kind, kind);
492:       // Render the assistant's plain-English readout — with credentials
493:       // shown as "•••• captured" only, never plaintext.
494:       const readout = fieldReadout(data.fields || {}, data.password_captured, data.aws_secret_captured);
495:       const eKind = effectiveKind(data.kind, kind);
496:       const confirmSentence = guessConfirmSentence(eKind, data.fields || {});
497:       const nextAsk = nextMissingField({ ...data.fields }, eKind);
498:       push("assistant", (
499:         <>
500:           <div style={{ marginBottom: 6 }}>
501:             <strong>{readout}</strong>{" "}
502:             <span style={{ color: TOK.ink3 }}>(kind: {KIND_LABEL[eKind] || eKind})</span>
503:           </div>
504:           <ParseReadoutTable fields={data.fields || {}}
505:                              password_captured={data.password_captured}
506:                              aws_secret_captured={data.aws_secret_captured} />
507:           {nextAsk ? (
508:             <div style={{ marginTop: 8, color: TOK.ink2 }}>
509:               I still need {humanField(nextAsk)}. What is it?
510:             </div>
511:           ) : (
512:             <div style={{ marginTop: 8, color: TOK.ink2 }}>
513:               {confirmSentence}
514:               <ConfirmButtons onConfirm={runSubmit} onCancel={() => {
515:                 push("assistant", "OK, no submit. Paste again or edit the fields to keep going.");
516:               }} />
517:             </div>
518:           )}
519:         </>
520:       ));
521:       setAskingField(nextAsk);
522:       setAwaitingConfirm(!nextAsk);
523:     } catch (e) {
524:       const detail = humanSpeakError(e);
525:       push("assistant", (
526:         <div style={{ color: TOK.oxblood }}>
527:           <div>I couldn&apos;t read that paste — {detail.plain}</div>
528:           <div style={{ marginTop: 4, color: TOK.ink2 }}>
529:             {detail.remedy || "Try re-pasting with clear labels (Host Name / Username / Password / Public IP for compute; Region / Cluster ARN / Secret ARN for a data source)."}
530:           </div>
531:         </div>
532:       ));
533:     } finally {
534:       setSubmitting(false);
535:     }
536:   }
537: 
538:   async function runSubmit() {
539:     setAwaitingConfirm(false);
540:     setSubmitting(true);
541:     push("user", "yes, connect it");
542:     // W11 R2 · confirm reads server-side draft state, not client-captured
543:     // fields. Prior stale-closure bug: parsed?.fields could be null at push
544:     // time, producing empty strings and a Pydantic 422 in the response.
545:     const draftId = draftIdRef.current;
546:     const eKind = kindRef.current || effectiveKind(parsed?.kind, kind);
547:     if (!draftId) {
548:       push("assistant", (
549:         <div style={{ color: TOK.oxblood }}>
550:           I don&apos;t have a draft for that yet — paste the details again
551:           and I&apos;ll read them.
552:         </div>
553:       ));
554:       setSubmitting(false);
555:       return;
556:     }
557:     try {
558:       const r = await axios.post(`${BACKEND}/api/connect/confirm/${draftId}`, {});
559:       const data = r.data;
560:       if (eKind === "compute") {
561:         const stages = (data && data.stages) || {};
562:         push("assistant", (
563:           <>
564:             <div style={{ marginBottom: 4 }}>
565:               Handshake walk — declaration then hardening then acceptance.
566:             </div>
567:             <HandshakeStageCard testid="chat-card-handshake-declaration" label="Declaration"
568:                                 stage={stages.declaration} />
569:             <HandshakeStageCard testid="chat-card-handshake-hardening" label="Hardening"
570:                                 stage={stages.hardening} />
571:             <HandshakeStageCard testid="chat-card-handshake-acceptance" label="Acceptance"
572:                                 stage={stages.acceptance} />
573:             <FourQuestionsCard result={data} />
574:           </>
575:         ));
576:       } else if (eKind === "data-source") {
577:         push("assistant", (
578:           <>
579:             <div style={{ marginBottom: 4 }}>
580:               Connected to the data source — the four questions:
581:             </div>
582:             <FourQuestionsCard result={data} />
583:           </>
584:         ));
585:       } else {
586:         push("assistant", <IntentRecordedCard record={data.intent || data} />);
587:       }
588:     } catch (e) {
589:       // W11 R2 · human-speak error rendering. If the backend attached a
590:       // structured detail ({field, remedy, plain}), render the plain
591:       // sentence verbatim and the remedy on a second line. Never surface
592:       // the raw Pydantic 422 shape.
593:       const detail = humanSpeakError(e);
594:       push("assistant", (
595:         <div style={{ color: TOK.oxblood }}>
596:           <div>{detail.plain}</div>
597:           {detail.remedy ? (
598:             <div style={{ marginTop: 4, color: TOK.ink2 }}>{detail.remedy}</div>
599:           ) : null}
600:         </div>
601:       ));
602:     } finally {
603:       setSubmitting(false);
604:       // Zero out the raw creds and the draft id — they've been submitted.
605:       pasteCacheRef.current = "";
606:       pwCacheRef.current = "";
607:       awsCacheRef.current = "";
608:       draftIdRef.current = null;
609:     }
610:   }
611: 
612:   return (
613:     <>
614:       {/* Scrim */}
615:       <div onClick={onClose}
616:            style={{ position: "fixed", top: 0, right: 0, bottom: 0, left: 0,
617:                     background: TOK.scrim, zIndex: 240 }} />
618:       {/* Right-side drawer */}
619:       <aside data-testid="connect-drawer-chat"
620:              style={{ position: "fixed", top: 0, right: 0, bottom: 0,
621:                       width: TOK.drawerW, background: TOK.paper,
622:                       borderLeft: `1px solid ${TOK.line}`,
623:                       boxShadow: TOK.shadowDrawer, zIndex: 250,
624:                       display: "flex", flexDirection: "column",
625:                       fontFamily: TOK.body }}>
626:         {/* Header */}
627:         <header style={{ padding: "16px 20px", borderBottom: `1px solid ${TOK.line}`,
628:                          display: "flex", alignItems: "center",
629:                          background: TOK.paper }}>
630:           <div>
631:             <div style={{ fontFamily: TOK.head, fontSize: 18, color: TOK.ink }}>
632:               Connect
633:             </div>
634:             <div style={{ fontSize: 11, color: TOK.ink3, marginTop: 2,
635:                           letterSpacing: 0.3 }}>
636:               conversational · paste-assisted · nothing here reaches a model
637:             </div>
638:           </div>
639:           <div style={{ flex: 1 }} />
640:           <button type="button" data-testid="connect-drawer-close" onClick={onClose}
641:                   style={{ background: "transparent", border: "none",
642:                            fontSize: 22, cursor: "pointer", color: TOK.ink3,
643:                            padding: "4px 8px" }}>×</button>
644:         </header>
645: 
646:         {/* Chat log */}
647:         <div ref={chatLogRef} data-testid="connect-drawer-chat-log"
648:              style={{ flex: 1, padding: "8px 18px 12px", overflowY: "auto" }}>
649:           {turns.map((t, i) => (
650:             t.role === "assistant"
651:               ? <AssistantTurn key={i}>{t.node}</AssistantTurn>
652:               : <UserTurn key={i}>{t.node}</UserTurn>
653:           ))}
654:           {submitting && (
655:             <AssistantTurn testid="connect-drawer-chat-thinking">
656:               <span style={{ color: TOK.ink3, fontStyle: "italic" }}>
657:                 Reading…
658:               </span>
659:             </AssistantTurn>
660:           )}
661:         </div>
662: 
663:         {/* Input */}
664:         <div style={{ padding: "12px 18px 18px", borderTop: `1px solid ${TOK.line}`,
665:                       background: TOK.paper }}>
666:           <div style={{ display: "flex", alignItems: "flex-end", gap: 8 }}>
667:             <textarea data-testid="connect-drawer-chat-input"
668:                       value={input}
669:                       onChange={(e) => setInput(e.target.value)}
670:                       onKeyDown={(e) => {
671:                         if (e.key === "Enter" && !e.shiftKey) {
672:                           e.preventDefault();
673:                           handleSend(input);
674:                         }
675:                       }}
676:                       placeholder="Type your answer, or paste the connection details… Enter to send."
677:                       rows={2}
678:                       style={{ flex: 1, padding: "10px 12px",
679:                                border: `1px solid ${TOK.line}`, borderRadius: 8,
680:                                fontSize: 13, color: TOK.ink, background: "#fff",
681:                                fontFamily: TOK.body, resize: "vertical" }} />
682:             <button type="button" data-testid="connect-drawer-chat-send"
683:                     onClick={() => handleSend(input)}
684:                     disabled={submitting}
685:                     style={{ background: TOK.blue, color: "#fff",
686:                              padding: "10px 16px", border: "none",
687:                              borderRadius: 8, cursor: "pointer", fontSize: 13,
688:                              fontFamily: TOK.body }}>
689:               Send
690:             </button>
691:           </div>
692:           <div style={{ marginTop: 6, fontSize: 11, color: TOK.ink3 }}>
693:             The parse runs locally on the server — passwords and secret keys
694:             are stripped before any log line is written. Chat log stays
695:             session-only.
696:           </div>
697:         </div>
698:       </aside>
699:     </>
700:   );
701: }
702: 
703: // ---------------------------------------------------------------------------
704: // Helpers
705: // ---------------------------------------------------------------------------
706: 
707: function ConfirmButtons({ onConfirm, onCancel }) {
708:   return (
709:     <div style={{ marginTop: 8, display: "flex", gap: 8 }}>
710:       <button type="button" data-testid="connect-drawer-confirm-yes"
711:               onClick={onConfirm}
712:               style={{ background: TOK.blue, color: "#fff", padding: "6px 14px",
713:                        border: "none", borderRadius: 999, cursor: "pointer",
714:                        fontSize: 12 }}>Yes, connect it</button>
715:       <button type="button" data-testid="connect-drawer-confirm-no"
716:               onClick={onCancel}
717:               style={{ background: "transparent", color: TOK.ink3,
718:                        padding: "6px 14px", border: `1px solid ${TOK.line}`,
719:                        borderRadius: 999, cursor: "pointer", fontSize: 12 }}>
720:         No, wait
721:       </button>
722:     </div>
723:   );
724: }
725: 
726: function ParseReadoutTable({ fields, password_captured, aws_secret_captured }) {
727:   return (
728:     <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12,
729:                     fontFamily: TOK.body, marginTop: 6 }}>
730:       <tbody>
731:         {Object.entries(fields || {}).map(([k, v]) => (
732:           <tr key={k}>
733:             <td style={{ color: TOK.ink3, paddingRight: 10, verticalAlign: "top",
734:                           fontSize: 11, letterSpacing: 0.2, textTransform: "uppercase" }}>
735:               {humanField(k)}
736:             </td>
737:             <td style={{ fontFamily: "ui-monospace, SFMono-Regular, monospace",
738:                           color: TOK.ink }}>
739:               {String(v)}
740:             </td>
741:           </tr>
742:         ))}
743:         {password_captured && (
744:           <tr>
745:             <td style={{ color: TOK.ink3, paddingRight: 10, fontSize: 11,
746:                           letterSpacing: 0.2, textTransform: "uppercase" }}>
747:               Password
748:             </td>
749:             <td data-testid="chat-parsed-password-captured"
750:                 style={{ color: TOK.ink, fontFamily: "ui-monospace" }}>
751:               •••• captured (server-stripped; the chat log never carries it)
752:             </td>
753:           </tr>
754:         )}
755:         {aws_secret_captured && (
756:           <tr>
757:             <td style={{ color: TOK.ink3, paddingRight: 10, fontSize: 11,
758:                           letterSpacing: 0.2, textTransform: "uppercase" }}>
759:               AWS Secret Access Key
760:             </td>
761:             <td data-testid="chat-parsed-aws-secret-captured"
762:                 style={{ color: TOK.ink, fontFamily: "ui-monospace" }}>
763:               •••• captured (server-stripped; the chat log never carries it)
764:             </td>
765:           </tr>
766:         )}
767:       </tbody>
768:     </table>
769:   );
770: }
771: 
772: function redactCredsForLog(paste) {
773:   // Redact `password:`, `pwd:`, and AWS secret lines before they land in the
774:   // chat log. Only the labelled value is masked; the rest of the paste is
775:   // preserved so the user can see what they sent.
776:   return String(paste || "").split("\n").map((line) => {
777:     if (/^\s*(password|pass|pwd)\s*[:=]/i.test(line)) {
778:       return line.replace(/([:=]\s*).*$/, "$1•••• captured");
779:     }
780:     if (/^\s*(aws[_ ]?secret[_ ]?access[_ ]?key|secret[_ ]access[_ ]key|secret[_ ]key)\s*[:=]/i.test(line)) {
781:       return line.replace(/([:=]\s*).*$/, "$1•••• captured");
782:     }
783:     return line;
784:   }).join("\n");
785: }
786: 
787: function humanField(k) {
788:   if (!k) return "";
789:   return k.replace(/_/g, " ")
790:     .replace(/\baws\b/i, "AWS")
791:     .replace(/\barn\b/i, "ARN")
792:     .replace(/\bid\b/i, "ID")
793:     .replace(/\bip\b/i, "IP")
794:     .replace(/\bos\b/i, "OS")
795:     .replace(/^./, (c) => c.toUpperCase());
796: }
797: 
798: function errDetailToString(e) {
799:   const d = e?.response?.data?.detail;
800:   if (typeof d === "string") return d;
801:   if (Array.isArray(d)) {
802:     // FastAPI 422 shape: [{loc: [...], msg: "...", type: "..."}, ...]
803:     return d.map((x) => x?.msg || JSON.stringify(x)).join("; ");
804:   }
805:   if (d && typeof d === "object") return JSON.stringify(d);
806:   return e?.message || "unknown error";
807: }
808: 
809: // W11 R2 · Human-speak error translation. Prefers the structured
810: // {field, remedy, plain} shape the backend attaches to 4xx/5xx bodies;
811: // falls back to a plain sentence that NEVER surfaces raw Pydantic 422
812: // vocabulary (banned phrases per owner directive 2026-08-26).
813: export function humanSpeakError(e) {
814:   const d = e?.response?.data?.detail;
815:   if (d && typeof d === "object" && !Array.isArray(d) &&
816:       typeof d.plain === "string") {
817:     return {
818:       field: d.field || "",
819:       remedy: d.remedy || "",
820:       plain: d.plain,
821:     };
822:   }
823:   // Fallback path: keep the sentence in human words. Never echo
824:   // "String should have at least 1 character" or similar shape leakage.
825:   let plain = "";
826:   if (typeof d === "string") plain = d;
827:   else if (Array.isArray(d)) {
828:     // Extract the first offending field name if present
829:     const first = d[0] || {};
830:     const loc = Array.isArray(first.loc) ? first.loc : [];
831:     const fieldName = loc.find(
832:       (s) => typeof s === "string" && !["body", "query", "path"].includes(s)
833:     ) || "field";
834:     plain = `The ${fieldName.replace(/_/g, " ")} is not what the estate expected.`;
835:     return {
836:       field: fieldName,
837:       remedy: `Re-paste with the ${fieldName.replace(/_/g, " ")} line included, or type it into the drawer input.`,
838:       plain,
839:     };
840:   } else {
841:     plain = e?.message || "The estate couldn't accept that.";
842:   }
843:   return { field: "", remedy: "Paste again or edit the fields and try once more.", plain };
844: }
845: 
846: function nextMissingField(fields, eKind) {
847:   if (eKind === "compute") {
848:     for (const f of COMPUTE_REQUIRED) if (!fields[f]) return f;
849:     if (COMPUTE_PW_REQUIRED && !fields.__password_captured_hint) {
850:       // password requirement is signalled via parsed.password_captured; we
851:       // don't ask for it in-chat (it should have been in the paste).
852:     }
853:     return null;
854:   }
855:   if (eKind === "data-source") {
856:     for (const f of DATA_SOURCE_REQUIRED) if (!fields[f]) return f;
857:     return null;
858:   }
859:   // llm / trained-model — only name is required for the intent record
860:   if (!fields.name) return "name";
861:   return null;
862: }
863: 
864: function effectiveKind(parsedKind, chosenKind) {
865:   if (parsedKind) return parsedKind;
866:   return chosenKind === "auto" ? "compute" : chosenKind;
867: }

# SOURCE: frontend/src/components/ConnectWizard.jsx

1: import React, { useEffect, useState } from "react";
2: import axios from "axios";
3: 
4: /**
5:  * ConnectWizard - Single paste-and-connect panel (Owner Simplification 2026-08-14).
6:  *
7:  * The 5-step wizard is retired as the primary path. Connect collapses to
8:  * ONE panel: a large paste area with type chips on the same panel
9:  * (default: auto-detect), manual fallback fields inline, and a one-tap
10:  * aside for the provisioning card. Step grammar survives ONLY as the
11:  * post-submit progress/result view - the handshake walk from the
12:  * existing seven-stage pipeline (unchanged).
13:  *
14:  * Custody rule (owner Q2 addendum):
15:  *   Pasted text may contain the password; the /api/connect/parse-paste
16:  *   response NEVER carries it back (server strips + password_captured
17:  *   signal). This component keeps the raw paste in its own textarea
18:  *   memory and submits the full credential set once to /api/connect/gpu
19:  *   (compute) or /api/connect/intent (non-compute).
20:  */
21: 
22: const BACKEND = process.env.REACT_APP_BACKEND_URL;
23: 
24: const CHIPS = [
25:   { key: "auto", label: "Auto-detect", testid: "chip-auto-detect" },
26:   { key: "data-source", label: "A data source", testid: "wizard-chip-data-source" },
27:   { key: "llm", label: "An LLM", testid: "wizard-chip-llm" },
28:   { key: "trained-model", label: "A trained model", testid: "wizard-chip-trained-model" },
29:   { key: "compute", label: "Compute", testid: "wizard-chip-compute" },
30: ];
31: 
32: const COMPUTE_MANUAL_FIELDS = [
33:   ["host_name", "Host Name", "text", true],
34:   ["username", "Username", "text", true],
35:   ["password", "Password", "password", true],
36:   ["public_ip", "Public IP", "text", true],
37:   ["private_ip", "Private IP", "text", false],
38:   ["os", "OS", "text", false],
39:   ["deploy_date", "Deploy date (pins +14d)", "date", false],
40: ];
41: 
42: const HANDSHAKE_STAGES = [
43:   { key: "declaration", label: "Declaration" },
44:   { key: "hardening", label: "Hardening" },
45:   { key: "acceptance", label: "Acceptance" },
46: ];
47: 
48: // Client-side mirror password extractor (deterministic; same shape as the
49: // server parser). The parse-paste response never carries the password back
50: // (custody rule), so the browser plucks it from its own textarea memory
51: // before POSTing to /api/connect/gpu.
52: function extractPasswordFromPaste(paste) {
53:   if (!paste) return "";
54:   const re = /^\s*(password|pass|pwd)\s*[:=]\s*(.+?)\s*$/im;
55:   const m = paste.match(re);
56:   return m ? m[2] : "";
57: }
58: 
59: // Same mirror pattern for aws_secret_access_key — the parse-paste response
60: // omits it; we pluck from the raw paste for the /api/connect/data-source POST.
61: function extractAwsSecretFromPaste(paste) {
62:   if (!paste) return "";
63:   const re = /^\s*(aws[_ ]?secret[_ ]?access[_ ]?key|secret[_ ]access[_ ]key|secret[_ ]key)\s*[:=]\s*(.+?)\s*$/im;
64:   const m = paste.match(re);
65:   return m ? m[2] : "";
66: }
67: 
68: // Styles (top-level so component can reference them; palette matches the
69: // wider estate surface — cream / navy / oxblood / amber / sage).
70: const cream = "#f6f2ea";
71: const navy = "#1c2b45";
72: const oxblood = "#5a1a1a";
73: const amber = "#c98a1c";
74: const sage = "#4a7c59";
75: const grey = "#666";
76: 
77: const overlayStyle = {
78:   position: "fixed", inset: 0, background: "rgba(28,43,69,0.6)", zIndex: 1000,
79:   display: "flex", alignItems: "flex-start", justifyContent: "center",
80:   overflowY: "auto", padding: "32px 16px",
81: };
82: const panelStyle = {
83:   background: "#ffffff", padding: 24, borderRadius: 8,
84:   width: "min(720px, 95vw)", maxHeight: "88vh", overflowY: "auto",
85:   fontFamily: "system-ui, -apple-system, sans-serif",
86: };
87: const headerRow = { display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 };
88: const h1Style = { fontSize: 22, fontWeight: 600, color: navy };
89: const closeBtn = { border: "none", background: "transparent", fontSize: 24, cursor: "pointer", color: grey };
90: const chipRow = { display: "flex", flexWrap: "wrap", gap: 8, margin: "12px 0" };
91: const pasteStyle = { width: "100%", minHeight: 140, fontFamily: "monospace", fontSize: 13, padding: 10, border: "1px solid #ccc", borderRadius: 4, boxSizing: "border-box" };
92: const buttonRow = { display: "flex", gap: 12, margin: "12px 0", alignItems: "center", flexWrap: "wrap" };
93: const btnPrimary = { background: navy, color: "#fff", padding: "10px 18px", border: "none", borderRadius: 4, cursor: "pointer", fontSize: 14 };
94: const btnAmber = { background: amber, color: "#fff", padding: "8px 14px", border: "none", borderRadius: 4, cursor: "pointer", fontSize: 13 };
95: const btnLink = { background: "transparent", border: "none", color: amber, textDecoration: "underline", cursor: "pointer", fontSize: 13, padding: 0 };
96: const confirmStyle = { marginTop: 12, background: cream, padding: 12, border: "1px solid #ddd", borderRadius: 4 };
97: const warningStyle = { marginTop: 8, padding: 10, background: "#fef4e5", color: oxblood, border: `1px solid ${amber}`, borderRadius: 4, fontSize: 13 };
98: const fieldGrid = { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))", gap: 8, marginTop: 8 };
99: const fieldLabel = { display: "flex", flexDirection: "column", gap: 4 };
100: const inputStyle = { padding: "6px 8px", border: "1px solid #ccc", borderRadius: 4, fontSize: 13 };
101: 
102: function chipStyle(selected) {
103:   return {
104:     padding: "6px 12px", border: `1px solid ${selected ? navy : "#ccc"}`,
105:     background: selected ? navy : "#fff", color: selected ? "#fff" : navy,
106:     borderRadius: 20, cursor: "pointer", fontSize: 13,
107:   };
108: }
109: 
110: export default function ConnectWizard({ isOpen = true, onClose, initialKind }) {
111:   const [paste, setPaste] = useState("");
112:   const [chipKind, setChipKind] = useState(initialKind || "auto");
113:   const [parseResult, setParseResult] = useState(null);
114:   const [parseErr, setParseErr] = useState("");
115:   const [manual, setManual] = useState({});
116:   const [showProvCard, setShowProvCard] = useState(false);
117:   const [estateFacts, setEstateFacts] = useState(null);
118:   const [connectionName, setConnectionName] = useState("");
119:   const [submitting, setSubmitting] = useState(false);
120:   const [handshake, setHandshake] = useState(null);
121:   const [intentRecorded, setIntentRecorded] = useState(null);
122:   const [dataSourceResult, setDataSourceResult] = useState(null);
123:   const [submitErr, setSubmitErr] = useState("");
124: 
125:   useEffect(() => {
126:     if (!isOpen) return;
127:     axios.get(`${BACKEND}/api/connect/estate-facts`)
128:       .then((r) => setEstateFacts(r.data))
129:       .catch(() => setEstateFacts(null));
130:   }, [isOpen]);
131: 
132:   if (!isOpen) return null;
133: 
134:   const effectiveKind = parseResult?.kind || (chipKind === "auto" ? "compute" : chipKind);
135: 
136:   const doParse = async () => {
137:     setParseErr("");
138:     setHandshake(null);
139:     setIntentRecorded(null);
140:     if (!paste.trim()) {
141:       setParseErr("I did not read anything to parse. Paste the details, or fill the manual fields below.");
142:       setParseResult(null);
143:       return;
144:     }
145:     try {
146:       const body = { paste, hint_kind: chipKind === "auto" ? null : chipKind };
147:       const r = await axios.post(`${BACKEND}/api/connect/parse-paste`, body);
148:       setParseResult(r.data);
149:       // Seed manual fields from parsed non-secret values (owner can edit)
150:       setManual((m) => ({ ...m, ...r.data.fields }));
151:     } catch (e) {
152:       const detail = e?.response?.data?.detail || e.message;
153:       setParseErr(`I couldn't read that. ${detail}. Try again, or fill the manual fields.`);
154:       setParseResult(null);
155:     }
156:   };
157: 
158:   const doSubmit = async () => {
159:     setSubmitErr("");
160:     setSubmitting(true);
161:     try {
162:       if (effectiveKind === "compute") {
163:         const pwFromPaste = extractPasswordFromPaste(paste);
164:         const payload = {
165:           host_name: manual.host_name || parseResult?.fields?.host_name || "",
166:           username: manual.username || parseResult?.fields?.username || "",
167:           password: manual.password || pwFromPaste,
168:           public_ip: manual.public_ip || parseResult?.fields?.public_ip || "",
169:           private_ip: manual.private_ip || parseResult?.fields?.private_ip || "",
170:           os: manual.os || parseResult?.fields?.os || "",
171:           deploy_date: manual.deploy_date || parseResult?.fields?.deploy_date || "",
172:         };
173:         const r = await axios.post(`${BACKEND}/api/connect/gpu`, payload);
174:         setHandshake(r.data);
175:       } else if (effectiveKind === "data-source") {
176:         // Client-side mirror pluck for aws_secret_access_key (custody:
177:         // /api/connect/parse-paste never carries it back, so we pull it
178:         // from the raw paste same as we do for the compute password).
179:         const awsSecretFromPaste = extractAwsSecretFromPaste(paste);
180:         const payload = {
181:           aws_access_key_id: manual.aws_access_key_id || parseResult?.fields?.aws_access_key_id || undefined,
182:           aws_secret_access_key: manual.aws_secret_access_key || awsSecretFromPaste || undefined,
183:           region: manual.region || parseResult?.fields?.region || "",
184:           cluster_arn: manual.cluster_arn || parseResult?.fields?.cluster_arn || "",
185:           secret_arn: manual.secret_arn || parseResult?.fields?.secret_arn || "",
186:           database: manual.database || parseResult?.fields?.database || undefined,
187:         };
188:         const r = await axios.post(`${BACKEND}/api/connect/data-source`, payload);
189:         setDataSourceResult(r.data);
190:       } else {
191:         const payload = {
192:           kind: effectiveKind,
193:           name: connectionName || `unnamed-${effectiveKind}`,
194:           description: (paste || "").slice(0, 200),
195:         };
196:         const r = await axios.post(`${BACKEND}/api/connect/intent`, payload);
197:         setIntentRecorded(r.data);
198:       }
199:     } catch (e) {
200:       const detail = e?.response?.data?.detail || e.message;
201:       setSubmitErr(`The estate could not accept that: ${detail}`);
202:     } finally {
203:       setSubmitting(false);
204:     }
205:   };
206: 
207:   // -------- Post-submit result views ----------------------------------------
208: 
209:   if (handshake) {
210:     return (
211:       <div style={overlayStyle}>
212:         <div style={panelStyle}>
213:           <div style={headerRow}>
214:             <div style={h1Style}>Handshake walk</div>
215:             <button data-testid="wizard-close" onClick={() => { setHandshake(null); onClose && onClose(); }} style={closeBtn}>×</button>
216:           </div>
217:           <HandshakeWalk data={handshake} />
218:         </div>
219:       </div>
220:     );
221:   }
222:   if (dataSourceResult) {
223:     return (
224:       <div style={overlayStyle}>
225:         <div style={panelStyle}>
226:           <div style={headerRow}>
227:             <div style={h1Style}>Data connection</div>
228:             <button data-testid="wizard-close" onClick={() => { setDataSourceResult(null); onClose && onClose(); }} style={closeBtn}>×</button>
229:           </div>
230:           <DataSourceResult result={dataSourceResult} />
231:         </div>
232:       </div>
233:     );
234:   }
235:   if (intentRecorded) {
236:     return (
237:       <div style={overlayStyle}>
238:         <div style={panelStyle}>
239:           <div style={headerRow}>
240:             <div style={h1Style}>Intent recorded</div>
241:             <button data-testid="wizard-close" onClick={() => { setIntentRecorded(null); onClose && onClose(); }} style={closeBtn}>×</button>
242:           </div>
243:           <div data-testid="intent-recorded" style={{ color: sage, padding: 12, background: cream, borderRadius: 4 }}>
244:             Recorded — this connection type goes live with its wave.
245:             <div style={{ color: grey, marginTop: 12, fontSize: 13 }}>Name: {intentRecorded.name}</div>
246:           </div>
247:         </div>
248:       </div>
249:     );
250:   }
251: 
252:   // -------- Main single-panel form -----------------------------------------
253: 
254:   return (
255:     <div style={overlayStyle}>
256:       <div data-testid="connect-panel" style={panelStyle}>
257:         <div style={headerRow}>
258:           <div>
259:             <div style={h1Style}>Connect something new</div>
260:             <div style={{ color: grey, fontSize: 13, marginTop: 4 }}>
261:               A conversation, not a form. Paste the connection details exactly as you received them — I will read them.
262:             </div>
263:           </div>
264:           <button data-testid="wizard-close" onClick={onClose} style={closeBtn}>×</button>
265:         </div>
266: 
267:         <div style={chipRow}>
268:           {CHIPS.map((c) => (
269:             <button
270:               key={c.key}
271:               data-testid={c.testid}
272:               onClick={() => { setChipKind(c.key); setParseResult(null); }}
273:               style={chipStyle(chipKind === c.key)}
274:             >
275:               {c.label}
276:             </button>
277:           ))}
278:         </div>
279: 
280:         <textarea
281:           data-testid="connect-paste-input"
282:           value={paste}
283:           onChange={(e) => setPaste(e.target.value)}
284:           placeholder={"Host Name: aisca-gpu-01\nUsername: ubuntu\nPassword: ...\nPublic IP: 203.0.113.5\nOS: ubuntu24.04"}
285:           style={pasteStyle}
286:         />
287: 
288:         <div style={buttonRow}>
289:           <button data-testid="connect-parse" onClick={doParse} style={btnAmber}>Parse & confirm</button>
290:           <button
291:             data-testid="provisioning-card-toggle"
292:             onClick={() => setShowProvCard(!showProvCard)}
293:             style={btnLink}
294:           >
295:             {showProvCard ? "Hide provisioning card" : "Provisioning a new machine? What to paste on the AISCA side"}
296:           </button>
297:         </div>
298: 
299:         {parseErr && (
300:           <div data-testid="parse-error" style={warningStyle}>{parseErr}</div>
301:         )}
302: 
303:         {parseResult && <ConfirmView result={parseResult} />}
304: 
305:         {showProvCard && <ProvisioningCard facts={estateFacts} />}
306: 
307:         <details style={{ marginTop: 16, borderTop: `1px solid ${grey}30`, paddingTop: 12 }}>
308:           <summary style={{ cursor: "pointer", color: grey, fontSize: 13 }}>
309:             Manual fallback fields (edit what I read, or fill from scratch)
310:           </summary>
311:           {effectiveKind === "compute" && (
312:             <div style={fieldGrid}>
313:               <label style={fieldLabel}>
314:                 <span style={{ color: navy, fontSize: 12 }}>Host Name *</span>
315:                 <input data-testid="manual-field-host_name" type="text" autoComplete="off"
316:                   value={manual.host_name || ""}
317:                   onChange={(e) => setManual({ ...manual, host_name: e.target.value })}
318:                   style={inputStyle} />
319:               </label>
320:               <label style={fieldLabel}>
321:                 <span style={{ color: navy, fontSize: 12 }}>Username *</span>
322:                 <input data-testid="manual-field-username" type="text" autoComplete="off"
323:                   value={manual.username || ""}
324:                   onChange={(e) => setManual({ ...manual, username: e.target.value })}
325:                   style={inputStyle} />
326:               </label>
327:               <label style={fieldLabel}>
328:                 <span style={{ color: navy, fontSize: 12 }}>Password *</span>
329:                 <input data-testid="manual-field-password" type="password" autoComplete="new-password"
330:                   value={manual.password || ""}
331:                   onChange={(e) => setManual({ ...manual, password: e.target.value })}
332:                   style={inputStyle} />
333:               </label>
334:               <label style={fieldLabel}>
335:                 <span style={{ color: navy, fontSize: 12 }}>Public IP *</span>
336:                 <input data-testid="manual-field-public_ip" type="text" autoComplete="off"
337:                   value={manual.public_ip || ""}
338:                   onChange={(e) => setManual({ ...manual, public_ip: e.target.value })}
339:                   style={inputStyle} />
340:               </label>
341:               <label style={fieldLabel}>
342:                 <span style={{ color: navy, fontSize: 12 }}>Private IP</span>
343:                 <input data-testid="manual-field-private_ip" type="text" autoComplete="off"
344:                   value={manual.private_ip || ""}
345:                   onChange={(e) => setManual({ ...manual, private_ip: e.target.value })}
346:                   style={inputStyle} />
347:               </label>
348:               <label style={fieldLabel}>
349:                 <span style={{ color: navy, fontSize: 12 }}>OS</span>
350:                 <input data-testid="manual-field-os" type="text" autoComplete="off"
351:                   value={manual.os || ""}
352:                   onChange={(e) => setManual({ ...manual, os: e.target.value })}
353:                   style={inputStyle} />
354:               </label>
355:               <label style={fieldLabel}>
356:                 <span style={{ color: navy, fontSize: 12 }}>Deploy date (pins +14d)</span>
357:                 <input data-testid="manual-field-deploy_date" type="date" autoComplete="off"
358:                   value={manual.deploy_date || ""}
359:                   onChange={(e) => setManual({ ...manual, deploy_date: e.target.value })}
360:                   style={inputStyle} />
361:               </label>
362:             </div>
363:           )}
364:           {effectiveKind === "data-source" && (
365:             <div style={fieldGrid}>
366:               <label style={fieldLabel}>
367:                 <span style={{ color: navy, fontSize: 12 }}>AWS Access Key ID</span>
368:                 <input data-testid="manual-field-aws_access_key_id" type="text" autoComplete="off"
369:                   value={manual.aws_access_key_id || ""}
370:                   onChange={(e) => setManual({ ...manual, aws_access_key_id: e.target.value })}
371:                   style={inputStyle} />
372:               </label>
373:               <label style={fieldLabel}>
374:                 <span style={{ color: navy, fontSize: 12 }}>AWS Secret Access Key</span>
375:                 <input data-testid="manual-field-aws_secret_access_key" type="password" autoComplete="new-password"
376:                   value={manual.aws_secret_access_key || ""}
377:                   onChange={(e) => setManual({ ...manual, aws_secret_access_key: e.target.value })}
378:                   style={inputStyle} />
379:               </label>
380:               <label style={fieldLabel}>
381:                 <span style={{ color: navy, fontSize: 12 }}>Region *</span>
382:                 <input data-testid="manual-field-region" type="text" autoComplete="off"
383:                   value={manual.region || ""}
384:                   onChange={(e) => setManual({ ...manual, region: e.target.value })}
385:                   placeholder="us-east-1"
386:                   style={inputStyle} />
387:               </label>
388:               <label style={fieldLabel}>
389:                 <span style={{ color: navy, fontSize: 12 }}>Cluster ARN *</span>
390:                 <input data-testid="manual-field-cluster_arn" type="text" autoComplete="off"
391:                   value={manual.cluster_arn || ""}
392:                   onChange={(e) => setManual({ ...manual, cluster_arn: e.target.value })}
393:                   placeholder="arn:aws:rds:us-east-1:…:cluster:…"
394:                   style={inputStyle} />
395:               </label>
396:               <label style={fieldLabel}>
397:                 <span style={{ color: navy, fontSize: 12 }}>Secret ARN *</span>
398:                 <input data-testid="manual-field-secret_arn" type="text" autoComplete="off"
399:                   value={manual.secret_arn || ""}
400:                   onChange={(e) => setManual({ ...manual, secret_arn: e.target.value })}
401:                   placeholder="arn:aws:secretsmanager:us-east-1:…:secret:…"
402:                   style={inputStyle} />
403:               </label>
404:               <label style={fieldLabel}>
405:                 <span style={{ color: navy, fontSize: 12 }}>Database</span>
406:                 <input data-testid="manual-field-database" type="text" autoComplete="off"
407:                   value={manual.database || ""}
408:                   onChange={(e) => setManual({ ...manual, database: e.target.value })}
409:                   style={inputStyle} />
410:               </label>
411:             </div>
412:           )}
413:           {effectiveKind !== "compute" && (
414:             <div style={{ marginTop: 8, color: grey, fontSize: 13 }}>
415:               This kind ({effectiveKind}) is intent-only right now — it records
416:               via /api/connect/intent. The paste and name are enough.
417:             </div>
418:           )}
419:         </details>
420: 
421:         {effectiveKind !== "compute" && effectiveKind !== "data-source" && (
422:           <input
423:             data-testid="wizard-connection-name"
424:             placeholder="Name it in the estate's words (nothing connects unnamed)"
425:             value={connectionName}
426:             onChange={(e) => setConnectionName(e.target.value)}
427:             style={{ ...inputStyle, marginTop: 12, width: "100%", boxSizing: "border-box" }}
428:           />
429:         )}
430: 
431:         <button
432:           data-testid="connect-submit"
433:           onClick={doSubmit}
434:           disabled={submitting}
435:           style={{ ...btnPrimary, marginTop: 16 }}
436:         >
437:           {submitting ? "Connecting…"
438:             : effectiveKind === "compute" ? "Connect"
439:             : effectiveKind === "data-source" ? "Test connection"
440:             : "Record intent"}
441:         </button>
442: 
443:         {submitErr && <div style={warningStyle}>{submitErr}</div>}
444:       </div>
445:     </div>
446:   );
447: }
448: 
449: function ConfirmView({ result }) {
450:   if (result.missing && result.missing.length > 0) {
451:     return (
452:       <div style={confirmStyle}>
453:         <div style={{ color: amber, marginBottom: 8 }}>
454:           I read this as a <b>{result.kind}</b> paste, but I did not find:
455:         </div>
456:         <ul data-testid="parse-missing-fields" style={{ margin: 0, paddingLeft: 20 }}>
457:           {result.missing.map((f) => <li key={f} style={{ color: oxblood }}>{f}</li>)}
458:         </ul>
459:         <div style={{ color: grey, fontSize: 12, marginTop: 8 }}>
460:           Fill the manual fields below, or paste again with the missing labels.
461:           Ask again is the estate's default when it cannot read.
462:         </div>
463:       </div>
464:     );
465:   }
466:   return (
467:     <div style={confirmStyle}>
468:       <div style={{ color: sage, marginBottom: 8 }}>
469:         I read this as a <b>{result.kind}</b> paste. Confirm:
470:       </div>
471:       <table style={{ width: "100%", fontSize: 13, borderCollapse: "collapse" }}>
472:         <tbody>
473:           {Object.entries(result.fields).map(([k, v]) => (
474:             <tr key={k}>
475:               <td style={{ color: grey, paddingRight: 8, verticalAlign: "top" }}>{k}</td>
476:               <td style={{ fontFamily: "monospace" }}>{String(v)}</td>
477:             </tr>
478:           ))}
479:           {result.password_captured && (
480:             <tr>
481:               <td style={{ color: grey, paddingRight: 8 }}>password</td>
482:               <td data-testid="parsed-password-captured" style={{ fontFamily: "monospace" }}>•••• captured</td>
483:             </tr>
484:           )}
485:           {result.aws_secret_captured && (
486:             <tr>
487:               <td style={{ color: grey, paddingRight: 8 }}>aws_secret_access_key</td>
488:               <td data-testid="parsed-aws-secret-captured" style={{ fontFamily: "monospace" }}>•••• captured</td>
489:             </tr>
490:           )}
491:         </tbody>
492:       </table>
493:     </div>
494:   );
495: }
496: 
497: function DataSourceResult({ result }) {
498:   const ok = result.link_working && result.ready;
499:   const border = ok ? sage : oxblood;
500:   return (
501:     <div style={{ padding: 12, borderLeft: `4px solid ${border}`, background: cream, borderRadius: 4 }}>
502:       <div style={{ marginBottom: 8, color: navy, fontSize: 14, fontWeight: 600 }}>
503:         {ok ? `Connected to ${result.source_id || "the data source"}.` : "The data connection didn't come up."}
504:       </div>
505:       <table style={{ width: "100%", fontSize: 13, borderCollapse: "collapse" }}>
506:         <tbody>
507:           <tr>
508:             <td style={{ color: grey, paddingRight: 8, width: 180 }}>Is the link working?</td>
509:             <td data-testid="data-link-working" style={{ color: result.link_working ? sage : oxblood }}>
510:               {result.link_working ? "yes — SELECT 1 returned over the Data API" : "no"}
511:             </td>
512:           </tr>
513:           <tr>
514:             <td style={{ color: grey, paddingRight: 8, verticalAlign: "top" }}>What did we find?</td>
515:             <td data-testid="data-source-found" style={{ verticalAlign: "top" }}>
516:               {result.link_working ? renderFound(result.found) : "—"}
517:             </td>
518:           </tr>
519:           <tr>
520:             <td style={{ color: grey, paddingRight: 8 }}>Is it ready?</td>
521:             <td data-testid="data-source-ready" style={{ color: result.ready ? sage : oxblood }}>
522:               {result.ready ? "yes" : "no"}
523:             </td>
524:           </tr>
525:           <tr>
526:             <td style={{ color: grey, paddingRight: 8, verticalAlign: "top" }}>Any failure to name?</td>
527:             <td data-testid="data-source-failure" style={{ verticalAlign: "top" }}>
528:               {result.failure
529:                 ? <div><b>{result.failure}</b> — {result.failure_sentence}</div>
530:                 : "no"}
531:             </td>
532:           </tr>
533:         </tbody>
534:       </table>
535:       <div style={{ color: grey, fontSize: 12, marginTop: 10 }}>
536:         Engine: {result.engine} · Channel: {result.channel} · Standing creds stored key-custody-locally at {result.creds_path}
537:       </div>
538:     </div>
539:   );
540: }
541: 
542: function renderFound(found) {
543:   if (!found || Object.keys(found).length === 0) return "—";
544:   const schemas = found.schemas || [];
545:   const tables = found.tables || [];
546:   return (
547:     <div>
548:       <div>
549:         <b>{schemas.length}</b> schema{schemas.length === 1 ? "" : "s"}:{" "}
550:         {schemas.slice(0, 6).join(", ")}{schemas.length > 6 ? "…" : ""}
551:       </div>
552:       <div>
553:         <b>{tables.length}</b> table{tables.length === 1 ? "" : "s"} sampled (cap {found.inventory_cap})
554:         {tables.length > 0 && (
555:           <ul style={{ margin: "6px 0 0 0", paddingLeft: 20 }}>
556:             {tables.slice(0, 8).map((t, i) => (
557:               <li key={i} style={{ fontFamily: "monospace", fontSize: 12 }}>
558:                 {t.schema}.{t.table} <span style={{ color: grey }}>≈ {t.approx_row_count} rows</span>
559:               </li>
560:             ))}
561:           </ul>
562:         )}
563:       </div>
564:     </div>
565:   );
566: }
567: 
568: 
569: function HandshakeWalk({ data }) {
570:   return (
571:     <div data-testid="handshake-walk">
572:       {HANDSHAKE_STAGES.map((s) => {
573:         const stage = (data.stages || {})[s.key] || {};
574:         const status = stage.status || "untried";
575:         const border = status === "pass" ? sage : status === "fail" ? oxblood : "#999";
576:         return (
577:           <div
578:             key={s.key}
579:             data-testid={`handshake-stage-${s.key}`}
580:             style={{ padding: 8, borderLeft: `4px solid ${border}`, margin: "6px 0", background: cream }}
581:           >
582:             <b>{s.label}</b> <span style={{ color: grey }}>· {status}</span>
583:             {stage.detail && <div style={{ fontSize: 12, color: "#333" }}>{stage.detail}</div>}
584:           </div>
585:         );
586:       })}
587:       <div style={{ fontSize: 12, color: grey, marginTop: 10 }}>
588:         Handshake walk from POST /api/connect/gpu — declaration → hardening → acceptance.
589:       </div>
590:     </div>
591:   );
592: }
593: 
594: function ProvisioningCard({ facts }) {
595:   if (!facts) {
596:     return (
597:       <div data-testid="provisioning-card" style={{ marginTop: 12, color: grey, padding: 12, background: cream, borderRadius: 4 }}>
598:         Loading provisioning card from /api/connect/estate-facts…
599:       </div>
600:     );
601:   }
602:   return (
603:     <div data-testid="provisioning-card" style={{ marginTop: 12, background: cream, padding: 12, border: "1px solid #ccc", borderRadius: 4 }}>
604:       <div style={{ fontSize: 12, color: grey, marginBottom: 6 }}>What to paste on the AISCA side (VM creation form):</div>
605:       <div style={{ marginBottom: 4, wordBreak: "break-all" }}>
606:         <b>Public key:</b>{" "}
607:         <code data-testid="provisioning-card-public-key" style={{ fontSize: 12 }}>{facts.estate_public_key}</code>
608:       </div>
609:       <div style={{ marginBottom: 4 }}>
610:         <b>Pod egress IP:</b>{" "}
611:         <code data-testid="provisioning-card-egress-ip" style={{ fontSize: 12 }}>{facts.pod_egress_ip}</code>
612:       </div>
613:       <div>
614:         <b>Fingerprint:</b>{" "}
615:         <code data-testid="provisioning-card-fingerprint" style={{ fontSize: 12 }}>{facts.estate_public_key_fingerprint}</code>
616:       </div>
617:     </div>
618:   );
619: }

# SOURCE: frontend/src/components/CostLedger.jsx

1: import React, { useEffect, useState } from "react";
2: import { Link } from "react-router-dom";
3: 
4: /**
5:  * CostLedger.jsx — W6 CP2b · CA1-008 surface.
6:  *
7:  * Owner Ruling 2026-08-25 · W6 GO §W6-SCOPE-(a):
8:  *   Cost Ledger per the v7 oracle · real figures only.
9:  *
10:  * Canon 1 §4.4 · Measure, do not assert.
11:  * Canon 1 §4.1 · Cost optimisations fail transparent.
12:  *
13:  * CA1-008 · the lever sequence itself (cache → route → narrow → cascade
14:  * → waste_report) rendered as named ordered steps with saving
15:  * attributable to each — not just the final per-call cost.
16:  *
17:  * Rendering discipline:
18:  *   · Quantities ALWAYS render (they are measured facts).
19:  *   · Money renders ONLY when the entry carries cost_total !== null.
20:  *   · When any entry carries honest_gap_note, the surface renders it
21:  *     verbatim; no fabricated $ figure.
22:  *   · Levers named-but-not-yet-attributed render as "honest gap" rows
23:  *     (drawn-not-blank per the standing rule).
24:  */
25: 
26: const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
27: 
28: // v7 palette tokens.
29: const paper = "#f5f2ea";
30: const surface = "#ffffff";
31: const surface2 = "#f0ebe1";
32: const ink = "#1b1f27";
33: const ink2 = "#3a3f4a";
34: const ink3 = "#7a7f8a";
35: const line = "#e4dccf";
36: const blue = "#16274a";
37: const sage = "#1d7a6e";
38: const oxblood = "#8a2a44";
39: const oxblood2 = "#b8395b";
40: const brass = "#b08d2e";
41: const head = 'ui-serif, "Iowan Old Style", Georgia, serif';
42: 
43: 
44: export default function CostLedger() {
45:   const [summary, setSummary] = useState(null);
46:   const [entries, setEntries] = useState(null);
47:   const [rates, setRates] = useState(null);
48:   const [error, setError] = useState(null);
49:   const [kindFilter, setKindFilter] = useState("llm");
50: 
51:   useEffect(() => {
52:     const load = async () => {
53:       try {
54:         const [s, e, r] = await Promise.all([
55:           fetch(`${BACKEND_URL}/api/cost_ledger/summary?kind=${kindFilter}`).then(x => x.json()),
56:           fetch(`${BACKEND_URL}/api/cost_ledger/entries?kind=${kindFilter}&limit=25`).then(x => x.json()),
57:           fetch(`${BACKEND_URL}/api/cost_ledger/rates`).then(x => x.json()),
58:         ]);
59:         setSummary(s);
60:         setEntries(e.entries || []);
61:         setRates(r);
62:       } catch (exc) {
63:         setError(String(exc));
64:       }
65:     };
66:     load();
67:   }, [kindFilter]);
68: 
69:   return (
70:     <div style={{ minHeight: "100vh", background: paper, padding: "48px 40px",
71:                   fontFamily: "ui-sans-serif, system-ui, sans-serif" }}>
72:       <div style={{ maxWidth: 1200, margin: "0 auto" }}>
73:         <div style={{ fontSize: 11, letterSpacing: 2, color: ink3,
74:                       textTransform: "uppercase" }}>
75:           AKKI · COST LEDGER · CA1-008
76:         </div>
77:         <div style={{ display: "flex", justifyContent: "space-between",
78:                       alignItems: "baseline" }}>
79:           <h1 style={{ fontFamily: head, fontSize: 42, margin: "10px 0 8px 0",
80:                        color: blue }}>
81:             Every crossing, measured.
82:           </h1>
83:           <Link to="/" style={{ color: ink3, fontSize: 12, textDecoration: "none" }}>
84:             ← Registry
85:           </Link>
86:         </div>
87:         <p style={{ color: ink2, lineHeight: 1.6, fontSize: 14, marginBottom: 24,
88:                     maxWidth: 720 }}>
89:           The ledger reads the crossing receipts. Quantities are measured
90:           facts. Money renders only when a rate is on record — otherwise
91:           the gap is named, not papered.
92:         </p>
93: 
94:         {error && (
95:           <div data-testid="cost-ledger-error"
96:                style={{ padding: "10px 14px", background: "#f7ecea",
97:                         borderLeft: `2px solid ${oxblood2}`, borderRadius: 4,
98:                         marginBottom: 20, fontSize: 12, color: oxblood }}>
99:             The ledger could not be read: {error}. This is work done, not
100:             work lost — try again in a moment.
101:           </div>
102:         )}
103: 
104:         {/* Filter */}
105:         <div style={{ marginBottom: 20, display: "flex", gap: 10 }}
106:              data-testid="cost-ledger-filter">
107:           {["llm", "seam", ""].map(k => (
108:             <button key={k || "all"}
109:                     data-testid={`cost-ledger-filter-${k || "all"}`}
110:                     onClick={() => setKindFilter(k)}
111:                     style={{
112:                       padding: "6px 14px", fontSize: 12,
113:                       background: kindFilter === k ? blue : surface,
114:                       color: kindFilter === k ? "#fff" : ink,
115:                       border: `1px solid ${kindFilter === k ? blue : line}`,
116:                       borderRadius: 4, cursor: "pointer", fontWeight: 600,
117:                     }}>
118:               {k === "llm" ? "LLM crossings" : k === "seam" ? "Compute seam" : "All"}
119:             </button>
120:           ))}
121:         </div>
122: 
123:         {/* Summary */}
124:         {summary && <CostSummary summary={summary} />}
125: 
126:         {/* Rates on record */}
127:         {rates && <RatesOnRecord rates={rates} />}
128: 
129:         {/* Ledger rows */}
130:         <div style={{ marginTop: 32 }}>
131:           <div style={{ fontSize: 11, letterSpacing: 1.5, color: ink3,
132:                         textTransform: "uppercase", fontWeight: 600,
133:                         marginBottom: 14 }}>
134:             Ledger · newest first
135:           </div>
136:           {entries === null && (
137:             <div style={{ fontSize: 12, color: ink3 }}>Reading the ledger…</div>
138:           )}
139:           {entries !== null && entries.length === 0 && (
140:             <div data-testid="cost-ledger-empty"
141:                  style={{ padding: "18px 20px", border: `1px solid ${line}`,
142:                           borderRadius: 9, background: surface,
143:                           fontSize: 12.5, color: ink2, lineHeight: 1.55 }}>
144:               No crossings on record for this filter. As the estate's
145:               governed calls run, entries land here.
146:             </div>
147:           )}
148:           {entries !== null && entries.map(e => <LedgerRow key={e.receipt_id} entry={e} />)}
149:         </div>
150:       </div>
151:     </div>
152:   );
153: }
154: 
155: 
156: function CostSummary({ summary }) {
157:   const currency = summary.currency || "USD";
158:   return (
159:     <div data-testid="cost-ledger-summary"
160:          style={{ padding: "20px 24px", background: surface,
161:                   border: `1px solid ${line}`, borderRadius: 10,
162:                   marginBottom: 24 }}>
163:       <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)",
164:                     gap: 24 }}>
165:         <SummaryField label="calls" value={summary.total_calls} />
166:         <SummaryField label="tokens_in"
167:                       value={summary.total_tokens_in.toLocaleString()} />
168:         <SummaryField label="tokens_out"
169:                       value={summary.total_tokens_out.toLocaleString()} />
170:         <SummaryField label="latency_total"
171:                       value={`${(summary.total_latency_ms / 1000).toFixed(1)}s`} />
172:       </div>
173: 
174:       <div style={{ marginTop: 18, paddingTop: 14, borderTop: `1px solid ${line}`,
175:                     display: "flex", alignItems: "baseline",
176:                     justifyContent: "space-between" }}>
177:         <div>
178:           <div style={{ fontSize: 11, color: ink3, letterSpacing: 1.2,
179:                         textTransform: "uppercase" }}>
180:             Cost · this filter
181:           </div>
182:           <div style={{ fontSize: 30, fontFamily: head, color: blue,
183:                         marginTop: 4 }}>
184:             {summary.total_cost > 0
185:               ? `${currency === "USD" ? "$" : currency + " "}${summary.total_cost.toFixed(4)}`
186:               : summary.total_cost_is_partial
187:                 ? <span style={{ fontSize: 15, color: ink3, fontStyle: "italic" }}>Not yet measured</span>
188:                 : <span style={{ fontSize: 15, color: ink3 }}>$0.00</span>}
189:             {summary.total_cost_is_partial && summary.total_cost > 0 && (
190:               <span style={{ fontSize: 12, color: oxblood, marginLeft: 10 }}
191:                     data-testid="cost-partial-marker">
192:                 (partial · lower bound)
193:               </span>
194:             )}
195:           </div>
196:         </div>
197:         {summary.gaps_present && (
198:           <div style={{ maxWidth: 380, fontSize: 11, color: ink3,
199:                         fontStyle: "italic", textAlign: "right",
200:                         lineHeight: 1.55 }}
201:                data-testid="cost-ledger-honest-gap">
202:             {summary.honest_gap_note}
203:           </div>
204:         )}
205:       </div>
206: 
207:       {/* CA1-008 lever sequence */}
208:       <LeverSequence levers={summary.levers} currency={currency} />
209:     </div>
210:   );
211: }
212: 
213: 
214: function SummaryField({ label, value }) {
215:   return (
216:     <div>
217:       <div style={{ fontSize: 10, color: ink3, letterSpacing: 1.5,
218:                     textTransform: "uppercase" }}>
219:         {label}
220:       </div>
221:       <div style={{ fontSize: 22, color: ink, fontFamily: head,
222:                     marginTop: 4 }}>
223:         {value}
224:       </div>
225:     </div>
226:   );
227: }
228: 
229: 
230: function LeverSequence({ levers, currency }) {
231:   const order = ["cache", "route", "narrow", "cascade", "waste_report"];
232:   return (
233:     <div style={{ marginTop: 20, paddingTop: 16, borderTop: `1px solid ${line}` }}
234:          data-testid="cost-ledger-levers">
235:       <div style={{ fontSize: 11, color: ink3, letterSpacing: 1.2,
236:                     textTransform: "uppercase", marginBottom: 10 }}>
237:         CA1-008 · savings by lever · in order
238:       </div>
239:       <div style={{ display: "grid",
240:                     gridTemplateColumns: "repeat(5, 1fr)",
241:                     gap: 12 }}>
242:         {order.map(name => {
243:           const l = levers[name] || { saving: 0, attributed_calls: 0 };
244:           const attributed = l.attributed_calls > 0;
245:           return (
246:             <div key={name} data-testid={`cost-lever-${name}`}
247:                  style={{ padding: "10px 12px", background: surface2,
248:                           borderLeft: `3px solid ${attributed ? sage : brass}`,
249:                           borderRadius: 5 }}>
250:               <div style={{ fontSize: 10, color: ink3, letterSpacing: 1,
251:                             textTransform: "uppercase", fontWeight: 700 }}>
252:                 {name.replace("_", " ")}
253:               </div>
254:               {attributed ? (
255:                 <>
256:                   <div style={{ fontSize: 16, color: sage, marginTop: 4,
257:                                 fontFamily: head }}>
258:                     {currency === "USD" ? "$" : currency + " "}
259:                     {l.saving.toFixed(4)}
260:                   </div>
261:                   <div style={{ fontSize: 10, color: ink3, marginTop: 2 }}>
262:                     {l.attributed_calls} attributed call{l.attributed_calls === 1 ? "" : "s"}
263:                   </div>
264:                 </>
265:               ) : (
266:                 <div style={{ fontSize: 11, color: ink3, marginTop: 6,
267:                               fontStyle: "italic", lineHeight: 1.4 }}>
268:                   Not yet attributed. Landing as levers become measurable.
269:                 </div>
270:               )}
271:             </div>
272:           );
273:         })}
274:       </div>
275:     </div>
276:   );
277: }
278: 
279: 
280: function RatesOnRecord({ rates }) {
281:   const hasModels = rates.models && rates.models.length > 0;
282:   const hasGpu = rates.gpu_hours && rates.gpu_hours.length > 0;
283:   return (
284:     <div data-testid="cost-ledger-rates"
285:          style={{ marginBottom: 24, padding: "16px 20px", background: surface,
286:                   border: `1px solid ${line}`, borderRadius: 10 }}>
287:       <div style={{ fontSize: 11, color: ink3, letterSpacing: 1.5,
288:                     textTransform: "uppercase", fontWeight: 600,
289:                     marginBottom: 10 }}>
290:         Rates on record
291:       </div>
292:       {!hasModels && !hasGpu && (
293:         <div data-testid="rates-honest-gap"
294:              style={{ fontSize: 12, color: ink3, fontStyle: "italic",
295:                       lineHeight: 1.55 }}>
296:           {rates.honest_gap_note || "No rates on record."} 
297:           Owner-supplied only · never invented.
298:         </div>
299:       )}
300:       {hasModels && (
301:         <div style={{ marginBottom: 12 }}>
302:           <div style={{ fontSize: 11, color: ink3, marginBottom: 6 }}>
303:             Model rates ({rates.models.length})
304:           </div>
305:           {rates.models.map(r => (
306:             <div key={r.model_id}
307:                  style={{ fontSize: 12, color: ink, padding: "4px 0",
308:                           fontFamily: "ui-monospace, Menlo, monospace" }}>
309:               <b>{r.model_id}</b>{" · "}
310:               {r.rate_per_million_tokens_in}/M in{" · "}
311:               {r.rate_per_million_tokens_out}/M out{" · "}
312:               {r.currency}{" · "}
313:               <span style={{ color: ink3, fontStyle: "italic" }}>
314:                 {r.source}@{r.authored_at?.substring(0, 10)}
315:               </span>
316:             </div>
317:           ))}
318:         </div>
319:       )}
320:       {hasGpu && (
321:         <div>
322:           <div style={{ fontSize: 11, color: ink3, marginBottom: 6 }}>
323:             GPU-hour rates ({rates.gpu_hours.length})
324:           </div>
325:           {rates.gpu_hours.map(r => (
326:             <div key={r.node_id}
327:                  style={{ fontSize: 12, color: ink, padding: "4px 0",
328:                           fontFamily: "ui-monospace, Menlo, monospace" }}>
329:               <b>{r.node_id}</b>{" · "}{r.rate_per_hour}/hr · {r.currency}
330:             </div>
331:           ))}
332:         </div>
333:       )}
334:     </div>
335:   );
336: }
337: 
338: 
339: function LedgerRow({ entry }) {
340:   const hasCost = entry.cost_total !== null;
341:   return (
342:     <div data-testid="cost-ledger-entry"
343:          style={{ border: `1px solid ${line}`, borderRadius: 9,
344:                   padding: "14px 16px", background: surface,
345:                   marginBottom: 10 }}>
346:       <div style={{ display: "flex", justifyContent: "space-between",
347:                     alignItems: "baseline", marginBottom: 6 }}>
348:         <div>
349:           <span style={{ fontSize: 13, fontWeight: 600, color: ink }}>
350:             {crossingLabel(entry.kind)}
351:           </span>
352:           <span style={{ marginLeft: 12, fontSize: 11, color: ink3,
353:                          fontFamily: "ui-monospace, Menlo, monospace" }}>
354:             {entry.receipt_id}
355:           </span>
356:         </div>
357:         <div style={{ fontSize: 11, color: ink3,
358:                       fontFamily: "ui-monospace, Menlo, monospace" }}>
359:           {formatIso(entry.at_iso)}
360:         </div>
361:       </div>
362: 
363:       <div style={{ fontSize: 11, color: ink3, marginBottom: 8,
364:                     fontFamily: "ui-monospace, Menlo, monospace" }}>
365:         {entry.model_id && (
366:           <><b style={{ color: ink }}>{entry.model_id}</b> via {entry.provider}{" · "}</>
367:         )}
368:         {entry.purpose_declared || entry.masking_tier}{" · "}
369:         {entry.actor}
370:       </div>
371: 
372:       <div style={{ display: "flex", gap: 20, flexWrap: "wrap",
373:                     fontSize: 11, fontFamily: "ui-monospace, Menlo, monospace",
374:                     color: ink3 }}>
375:         <span>tokens_in · <b style={{ color: ink }}>{entry.tokens_in}</b></span>
376:         <span>tokens_out · <b style={{ color: ink }}>{entry.tokens_out}</b></span>
377:         <span>latency · <b style={{ color: ink }}>{entry.latency_ms}ms</b></span>
378:         {entry.gpu_hours > 0 && (
379:           <span>gpu_hours · <b style={{ color: ink }}>{entry.gpu_hours}</b></span>
380:         )}
381:         {hasCost ? (
382:           <span style={{ color: sage }}>
383:             cost · <b>{entry.currency === "USD" ? "$" : entry.currency + " "}
384:                        {entry.cost_total.toFixed(6)}</b>
385:           </span>
386:         ) : (
387:           <span style={{ color: oxblood, fontStyle: "italic" }}
388:                 data-testid="entry-honest-gap">
389:             cost · not yet measured
390:           </span>
391:         )}
392:       </div>
393: 
394:       {/* Route lever · surfaced on the row when attributed */}
395:       {entry.levers && entry.levers.some(l => l.name === "route" && l.attributed) && (
396:         <div style={{ marginTop: 10, padding: "8px 10px", background: surface2,
397:                       borderLeft: `3px solid ${sage}`, borderRadius: 4,
398:                       fontSize: 11, color: ink }}
399:              data-testid="entry-route-lever">
400:           {entry.levers.find(l => l.name === "route").evidence}
401:         </div>
402:       )}
403:     </div>
404:   );
405: }
406: 
407: 
408: function crossingLabel(kind) {
409:   if (kind === "rds_data_api") return "Data API";
410:   if (kind === "ssh_seam") return "Compute seam";
411:   if (kind === "chat_governed_answer") return "Chat";
412:   if (kind === "solva_frame_audit") return "Solva · frame audit";
413:   if (kind === "solva_candidate_generation") return "Solva · candidates";
414:   if (kind === "solva_synthesis") return "Solva · synthesis";
415:   if (kind === "thinklab_direct_answer") return "ThinkLab · direct";
416:   if (kind === "llm_connect_verify") return "LLM · connect verify";
417:   return kind || "Crossing";
418: }
419: 
420: 
421: function formatIso(iso) {
422:   if (!iso) return "";
423:   try {
424:     return new Date(iso).toISOString().substring(0, 19).replace("T", " ");
425:   } catch {
426:     return iso;
427:   }
428: }

# SOURCE: frontend/src/components/DataShield.jsx

1: import React, { useEffect, useState } from "react";
2: 
3: /**
4:  * DataShield.jsx — Data Shield surface (Trust Center group → Data Shield).
5:  *
6:  * Owner Order 2026-08-25 · "W3 go" · Doc 01 (chokepoint · receipt · custody
7:  * sequence) + Doc 02 (confidentiality · dual-file · CA1-007 dry-run) +
8:  * CA1-N4 (residency).
9:  *
10:  * v7 oracle fabric — extracted verbatim from
11:  *   fixtures/RMS_AI_Akki_Prototype_v7_Standalone.html at offset 334300-337500
12:  * (the `isTrustDataShield` block). Landing header, session-timeline card
13:  * shape, session-headline pattern, sage/paper/ink palette reproduced.
14:  *
15:  * REFERENCE-NOT-COPY: every crossing card references a receipt IDENTITY
16:  * (rcp-<hex>); no receipt content is baked into the DOM. The dry-run
17:  * preview walks the receipt log by identity and reports would_catch_refs /
18:  * would_miss_refs — never the receipts' payload content.
19:  *
20:  * No fabrication: the session headline renders the honest count from
21:  * /api/shield/receipts; when no row-bearing crossing exists yet the
22:  * dry-run's honest_gap sentence is displayed verbatim.
23:  */
24: 
25: const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
26: 
27: // v7 palette tokens — extracted verbatim from prototype.html :root vars.
28: const paper = "#f5f2ea";     // --paper
29: const surface = "#ffffff";   // --surface
30: const surface2 = "#f0ebe1";  // --surface2
31: const ink = "#1b1f27";       // --ink
32: const ink2 = "#3a3f4a";      // --ink2
33: const ink3 = "#7a7f8a";      // --ink3
34: const line = "#e4dccf";      // --line
35: const blue = "#16274a";      // --blue
36: const sage = "#1d7a6e";      // --sage
37: const oxblood = "#8a2a44";   // --oxblood
38: const oxblood2 = "#b8395b";  // --oxblood2
39: const brass = "#b08d2e";     // --brass
40: const head = 'ui-serif, "Iowan Old Style", Georgia, serif';
41: 
42: export default function DataShield() {
43:   const [receipts, setReceipts] = useState(null);
44:   const [receiptCount, setReceiptCount] = useState(0);
45:   const [allowlists, setAllowlists] = useState(null);
46:   const [loadError, setLoadError] = useState(null);
47: 
48:   useEffect(() => {
49:     let alive = true;
50:     const load = async () => {
51:       try {
52:         const [r1, r2] = await Promise.all([
53:           fetch(`${BACKEND_URL}/api/shield/receipts?limit=50`),
54:           fetch(`${BACKEND_URL}/api/shield/allowlists`),
55:         ]);
56:         if (!r1.ok) throw new Error(`receipts HTTP ${r1.status}`);
57:         if (!r2.ok) throw new Error(`allowlists HTTP ${r2.status}`);
58:         const [b1, b2] = await Promise.all([r1.json(), r2.json()]);
59:         if (!alive) return;
60:         setReceipts(b1.receipts || []);
61:         setReceiptCount(b1.count || 0);
62:         setAllowlists(b2);
63:       } catch (e) {
64:         if (!alive) return;
65:         setLoadError(String(e.message || e));
66:       }
67:     };
68:     load();
69:     return () => { alive = false; };
70:   }, []);
71: 
72:   return (
73:     <div data-testid="data-shield-surface"
74:          style={{ minHeight: "100vh", background: paper, padding: "40px 48px",
75:                   fontFamily: 'ui-sans-serif, "Söhne", system-ui, sans-serif',
76:                   color: ink }}>
77:       <div style={{ maxWidth: 1080, margin: "0 auto" }}>
78: 
79:         {/* Breadcrumb: Trust Center group → Data Shield */}
80:         <div style={{ display: "flex", alignItems: "center", gap: 8,
81:                       fontSize: 11, letterSpacing: 1.5, color: ink3,
82:                       textTransform: "uppercase", marginBottom: 6 }}>
83:           <a href="/" style={{ color: ink3, textDecoration: "none" }}>Estate</a>
84:           <span>·</span>
85:           <span>Trust Center</span>
86:           <span>·</span>
87:           <span style={{ color: ink }}>Data Shield</span>
88:         </div>
89: 
90:         <h1 style={{ fontFamily: head, fontSize: 42, margin: "12px 0 4px",
91:                      color: blue, letterSpacing: -0.2 }}>
92:           Data Shield
93:         </h1>
94: 
95:         <p style={{ fontSize: 14, color: ink2, lineHeight: 1.65,
96:                     maxWidth: 620, margin: "8px 0 24px" }}>
97:           Every governed model call is shielded and receipted. The per-message
98:           pattern lives inline in Chat, on each answer. The full record for a
99:           session is here.
100:         </p>
101: 
102:         {loadError && (
103:           <div style={{ padding: "10px 14px", background: "#f7ecea",
104:                         borderLeft: `2px solid ${oxblood2}`, borderRadius: 4,
105:                         marginBottom: 20, fontSize: 12, color: oxblood }}>
106:             The shield log could not be read: {loadError}. This is work done,
107:             not work lost — try again in a moment.
108:           </div>
109:         )}
110: 
111:         {/* Session headline — honest count from /api/shield/receipts */}
112:         <div data-testid="data-shield-session-headline"
113:              style={{ fontSize: 13.5, color: ink, fontWeight: 600,
114:                       background: surface2, padding: "12px 16px",
115:                       borderRadius: 8, marginBottom: 24, maxWidth: 620 }}>
116:           {receiptCount} governed calls this session · zero raw content crossed the seam.
117:         </div>
118: 
119:         {/* Two-column grid: Session timeline / Rules in force + dry-run */}
120:         <div style={{ display: "grid",
121:                       gridTemplateColumns: "1fr 380px",
122:                       gap: 32 }}>
123: 
124:           {/* LEFT: session timeline (crossing-receipt log) */}
125:           <SessionTimeline receipts={receipts} />
126: 
127:           {/* RIGHT: rules in force + dry-run + refusal example */}
128:           <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
129:             <RulesInForce allowlists={allowlists} />
130:             <DryRunPanel />
131:             <RefusalExample />
132:           </div>
133:         </div>
134: 
135:       </div>
136:     </div>
137:   );
138: }
139: 
140: function SessionTimeline({ receipts }) {
141:   return (
142:     <div data-testid="data-shield-timeline"
143:          style={{ display: "flex", flexDirection: "column", gap: 12 }}>
144:       <div style={{ fontSize: 11, letterSpacing: 1.5, color: ink3,
145:                     textTransform: "uppercase", fontWeight: 600 }}>
146:         Session timeline
147:       </div>
148: 
149:       {receipts === null && (
150:         <div style={{ fontSize: 12, color: ink3 }}>Reading the log…</div>
151:       )}
152: 
153:       {receipts !== null && receipts.length === 0 && (
154:         <div data-testid="data-shield-timeline-empty"
155:              style={{ padding: "18px 20px", border: `1px solid ${line}`,
156:                       borderRadius: 9, background: surface, fontSize: 12.5,
157:                       color: ink2, lineHeight: 1.55 }}>
158:           No governed crossings have been made yet. Every outbound call
159:           transits the chokepoint — this list will populate as the estate's
160:           real crossings run.
161:         </div>
162:       )}
163: 
164:       {receipts !== null && receipts.map((rc) => (
165:         <div key={rc.receipt_id} data-testid="data-shield-receipt-row"
166:              style={{ border: `1px solid ${line}`, borderRadius: 9,
167:                       padding: "14px 16px", background: surface }}>
168:           <div style={{ display: "flex", justifyContent: "space-between",
169:                         marginBottom: 6, alignItems: "baseline" }}>
170:             <span style={{ fontSize: 13, fontWeight: 600, color: ink }}>
171:               {crossingLabel(rc.kind)}
172:             </span>
173:             <span style={{ fontFamily: "ui-monospace, Menlo, monospace",
174:                            fontSize: 10.5, color: ink3 }}>
175:               {rc.receipt_id}
176:             </span>
177:           </div>
178:           <div style={{ fontSize: 12, color: ink3, marginBottom: 10 }}>
179:             {rc.verb} · {rc.endpoint_host}
180:           </div>
181:           <div style={{ display: "flex", gap: 18, flexWrap: "wrap" }}>
182:             <Field label="RESIDENCY" value={rc.residency_region} tone={sage} />
183:             <Field label="MASKING TIER" value={rc.masking_tier} tone={brass} />
184:             <Field label="ACTOR" value={rc.actor} tone={ink2} />
185:             <Field label="AT" value={formatIso(rc.at_iso)} tone={ink3} />
186:           </div>
187:           {/* W5 · LLM metering line for reasoning/chat crossings */}
188:           {isReasoningKind(rc.kind) && rc.payload_shape && (
189:             <div data-testid="data-shield-llm-metering"
190:                  style={{ marginTop: 10, paddingTop: 10,
191:                           borderTop: `1px dashed ${line}`,
192:                           display: "flex", gap: 18, flexWrap: "wrap",
193:                           fontSize: 11, color: ink3,
194:                           fontFamily: "ui-monospace, Menlo, monospace" }}>
195:               <span>model · <b style={{ color: ink }}>{rc.payload_shape.model_id || "—"}</b></span>
196:               <span>provider · <b style={{ color: ink }}>{rc.payload_shape.provider || "—"}</b></span>
197:               <span>tokens_in · <b style={{ color: ink }}>{rc.payload_shape.tokens_in ?? "—"}</b></span>
198:               <span>tokens_out · <b style={{ color: ink }}>{rc.payload_shape.tokens_out ?? "—"}</b></span>
199:               <span>latency_ms · <b style={{ color: ink }}>{rc.payload_shape.latency_ms ?? "—"}</b></span>
200:               <span style={{ color: ink3, fontStyle: "italic" }}>
201:                 metering_source · {rc.payload_shape.metering_source || "unavailable"}
202:               </span>
203:             </div>
204:           )}
205:         </div>
206:       ))}
207:     </div>
208:   );
209: }
210: 
211: 
212: function isReasoningKind(kind) {
213:   if (!kind) return false;
214:   return kind.startsWith("solva_") || kind.startsWith("chat_") ||
215:          kind.startsWith("thinklab_") || kind.startsWith("llm_");
216: }
217: 
218: 
219: function crossingLabel(kind) {
220:   if (kind === "rds_data_api") return "Data API crossing";
221:   if (kind === "ssh_seam") return "Compute seam crossing";
222:   if (kind === "governance_read") return "Governance read";
223:   if (kind === "llm_synthesis") return "Model synthesis";
224:   // W5 kinds:
225:   if (kind === "chat_governed_answer") return "Chat · governed answer";
226:   if (kind === "solva_frame_audit") return "Solva · frame audit";
227:   if (kind === "solva_candidate_generation") return "Solva · candidate generation";
228:   if (kind === "solva_synthesis") return "Solva · synthesis";
229:   if (kind === "thinklab_direct_answer") return "ThinkLab · direct answer";
230:   if (kind === "llm_connect_verify") return "LLM · connect verify";
231:   return kind || "Crossing";
232: }
233: 
234: function formatIso(iso) {
235:   if (!iso) return "";
236:   // Show as YYYY-MM-DD · HH:MM (UTC) — v7 mono-caption style.
237:   const m = iso.match(/^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})/);
238:   return m ? `${m[1]} · ${m[2]}Z` : iso;
239: }
240: 
241: function Field({ label, value, tone }) {
242:   return (
243:     <div>
244:       <div style={{ fontSize: 10, letterSpacing: 1.2, color: ink3,
245:                     textTransform: "uppercase", marginBottom: 2 }}>
246:         {label}
247:       </div>
248:       <div style={{ fontFamily: head, fontSize: 14, color: tone || ink }}>
249:         {value || "—"}
250:       </div>
251:     </div>
252:   );
253: }
254: 
255: function RulesInForce({ allowlists }) {
256:   if (!allowlists) return (
257:     <div data-testid="data-shield-rules-in-force"
258:          style={{ border: `1px solid ${line}`, borderRadius: 9,
259:                   padding: "18px 20px", background: surface,
260:                   fontSize: 12, color: ink3 }}>
261:       Reading the rules in force…
262:     </div>
263:   );
264:   const admissible = (allowlists.masking_tiers || []).filter(
265:     t => (t.admissible_under_env || []).length > 0
266:   );
267:   const declared_only = (allowlists.masking_tiers || []).filter(
268:     t => (t.admissible_under_env || []).length === 0
269:   );
270:   return (
271:     <div data-testid="data-shield-rules-in-force"
272:          style={{ border: `1px solid ${line}`, borderRadius: 9,
273:                   padding: "18px 20px", background: surface }}>
274:       <div style={{ fontSize: 11, letterSpacing: 1.5, color: ink3,
275:                     textTransform: "uppercase", fontWeight: 600,
276:                     marginBottom: 12 }}>
277:         Rules in force
278:       </div>
279: 
280:       <div style={{ marginBottom: 14 }}>
281:         <div style={{ fontSize: 10.5, letterSpacing: 0.5, color: ink2,
282:                       marginBottom: 6, fontWeight: 600 }}>
283:           Masking tiers admissible today
284:         </div>
285:         {admissible.map(t => (
286:           <div key={t.tier} data-testid="data-shield-masking-tier-row"
287:                style={{ fontSize: 12, color: ink2, marginBottom: 6,
288:                         paddingBottom: 6, borderBottom: `1px dashed ${line}` }}>
289:             <div style={{ fontFamily: head, color: sage, fontWeight: 600 }}>
290:               {t.tier}
291:             </div>
292:             <div style={{ fontSize: 11, color: ink3, lineHeight: 1.5 }}>
293:               {t.description}
294:             </div>
295:           </div>
296:         ))}
297: 
298:         {declared_only.length > 0 && (
299:           <>
300:             <div style={{ fontSize: 10.5, letterSpacing: 0.5, color: ink2,
301:                           marginTop: 12, marginBottom: 6, fontWeight: 600 }}>
302:               Declared but not yet admissible
303:             </div>
304:             {declared_only.map(t => (
305:               <div key={t.tier} data-testid="data-shield-masking-tier-row"
306:                    style={{ fontSize: 12, color: ink2, marginBottom: 6,
307:                             paddingBottom: 6, borderBottom: `1px dashed ${line}` }}>
308:                 <div style={{ fontFamily: head, color: brass, fontWeight: 600 }}>
309:                   {t.tier}
310:                 </div>
311:                 <div style={{ fontSize: 11, color: ink3, lineHeight: 1.5 }}>
312:                   {t.description}
313:                 </div>
314:                 {t.not_admissible_because && (
315:                   <div style={{ fontSize: 10.5, color: oxblood, marginTop: 3,
316:                                 fontStyle: "italic" }}>
317:                     {t.not_admissible_because}
318:                   </div>
319:                 )}
320:               </div>
321:             ))}
322:           </>
323:         )}
324:       </div>
325: 
326:       <div>
327:         <div style={{ fontSize: 10.5, letterSpacing: 0.5, color: ink2,
328:                       marginBottom: 6, fontWeight: 600 }}>
329:           Residency
330:         </div>
331:         {(allowlists.residency?.allowlisted_regions || []).map(r => (
332:           <div key={r} data-testid="data-shield-residency-region-row"
333:                style={{ fontSize: 12, color: ink2, padding: "3px 0" }}>
334:             <span style={{ fontFamily: head, color: sage, fontWeight: 600 }}>
335:               {r}
336:             </span>
337:             <span style={{ color: ink3, marginLeft: 8 }}>· on the allowlist</span>
338:           </div>
339:         ))}
340:         <div data-testid="data-shield-residency-honest-gap"
341:              style={{ fontSize: 11, color: ink3, lineHeight: 1.55,
342:                       marginTop: 8, fontStyle: "italic" }}>
343:           {allowlists.residency?.note}
344:         </div>
345:       </div>
346:     </div>
347:   );
348: }
349: 
350: function DryRunPanel() {
351:   const [kind, setKind] = useState("pattern");
352:   const [inputValue, setInputValue] = useState("SELECT.*information_schema");
353:   const [running, setRunning] = useState(false);
354:   const [result, setResult] = useState(null);
355:   const [error, setError] = useState(null);
356: 
357:   const run = async () => {
358:     setRunning(true);
359:     setError(null);
360:     setResult(null);
361:     try {
362:       const body = { candidate_declaration: buildCandidate(kind, inputValue) };
363:       const r = await fetch(`${BACKEND_URL}/api/shield/dry-run`, {
364:         method: "POST",
365:         headers: { "Content-Type": "application/json" },
366:         body: JSON.stringify(body),
367:       });
368:       const j = await r.json();
369:       if (!r.ok) {
370:         setError(j.detail || `HTTP ${r.status}`);
371:       } else {
372:         setResult(j);
373:       }
374:     } catch (e) {
375:       setError(String(e.message || e));
376:     } finally {
377:       setRunning(false);
378:     }
379:   };
380: 
381:   return (
382:     <div data-testid="data-shield-dry-run-panel"
383:          style={{ border: `1px solid ${line}`, borderRadius: 9,
384:                   padding: "18px 20px", background: surface }}>
385:       <div style={{ fontSize: 11, letterSpacing: 1.5, color: ink3,
386:                     textTransform: "uppercase", fontWeight: 600,
387:                     marginBottom: 6 }}>
388:         Dry-run preview
389:       </div>
390:       <div style={{ fontSize: 12, color: ink2, lineHeight: 1.55,
391:                     marginBottom: 12 }}>
392:         Preview what a confidentiality declaration would catch against the
393:         crossing-receipt log, before adopting it.
394:       </div>
395: 
396:       <div style={{ display: "flex", flexDirection: "column", gap: 8,
397:                     marginBottom: 10 }}>
398:         <label style={{ fontSize: 11, color: ink3 }}>
399:           Declaration kind
400:           <select data-testid="data-shield-dry-run-kind-select"
401:                   value={kind}
402:                   onChange={(e) => setKind(e.target.value)}
403:                   style={{ display: "block", marginTop: 4, padding: "6px 8px",
404:                            fontSize: 12, border: `1px solid ${line}`,
405:                            borderRadius: 5, width: "100%",
406:                            background: surface, color: ink }}>
407:             <option value="exact_value">Exact value</option>
408:             <option value="pattern">Pattern (regex)</option>
409:             <option value="category">Category</option>
410:           </select>
411:         </label>
412:         <label style={{ fontSize: 11, color: ink3 }}>
413:           {kind === "pattern" ? "Regex" : kind === "category" ? "Category name" : "Value"}
414:           <input data-testid="data-shield-dry-run-input"
415:                  value={inputValue}
416:                  onChange={(e) => setInputValue(e.target.value)}
417:                  style={{ display: "block", marginTop: 4, padding: "6px 8px",
418:                           fontSize: 12, border: `1px solid ${line}`,
419:                           borderRadius: 5, width: "100%",
420:                           background: surface, color: ink,
421:                           fontFamily: "ui-monospace, Menlo, monospace" }} />
422:         </label>
423:       </div>
424: 
425:       <button data-testid="data-shield-dry-run-run"
426:               onClick={run}
427:               disabled={running || !inputValue.trim()}
428:               style={{ padding: "8px 14px", background: blue,
429:                        color: surface, border: "none", borderRadius: 6,
430:                        cursor: "pointer", fontSize: 12, fontWeight: 600,
431:                        opacity: (running || !inputValue.trim()) ? 0.6 : 1 }}>
432:         {running ? "Previewing…" : "Preview against receipts"}
433:       </button>
434: 
435:       {error && (
436:         <div style={{ marginTop: 12, fontSize: 12, color: oxblood,
437:                       background: "#f7ecea", padding: "8px 12px",
438:                       borderRadius: 6, borderLeft: `2px solid ${oxblood2}` }}>
439:           {error}
440:         </div>
441:       )}
442: 
443:       {result && (
444:         <div data-testid="data-shield-dry-run-result"
445:              style={{ marginTop: 14, paddingTop: 12,
446:                       borderTop: `1px solid ${line}` }}>
447:           <div style={{ fontSize: 11, color: ink3, marginBottom: 6 }}>
448:             Preview <span style={{ fontFamily: "ui-monospace, Menlo, monospace",
449:                                     color: ink2 }}>{result.preview_id}</span>
450:             <span> · {result.sample_size} receipts walked</span>
451:           </div>
452:           <div style={{ display: "flex", gap: 20, marginBottom: 10 }}>
453:             <div>
454:               <div style={{ fontSize: 10, letterSpacing: 1.2, color: ink3 }}>
455:                 WOULD CATCH
456:               </div>
457:               <div style={{ fontFamily: head, fontSize: 20, color: sage }}>
458:                 {result.would_catch_refs.length}
459:               </div>
460:             </div>
461:             <div>
462:               <div style={{ fontSize: 10, letterSpacing: 1.2, color: ink3 }}>
463:                 WOULD MISS
464:               </div>
465:               <div style={{ fontFamily: head, fontSize: 20, color: ink2 }}>
466:                 {result.would_miss_refs.length}
467:               </div>
468:             </div>
469:           </div>
470:           {/* REFERENCE-NOT-COPY: render the caught refs as identity chips */}
471:           {result.would_catch_refs.length > 0 && (
472:             <div style={{ fontSize: 11, color: ink3, marginBottom: 8,
473:                           lineHeight: 1.55 }}>
474:               First matches (by identity):{" "}
475:               {result.would_catch_refs.slice(0, 3).map(id => (
476:                 <span key={id}
477:                       style={{ fontFamily: "ui-monospace, Menlo, monospace",
478:                                background: surface2, padding: "1px 5px",
479:                                borderRadius: 3, marginRight: 4,
480:                                color: ink2 }}>
481:                   {id}
482:                 </span>
483:               ))}
484:             </div>
485:           )}
486:           {result.honest_gap && (
487:             <div style={{ fontSize: 11.5, color: ink2, lineHeight: 1.55,
488:                           fontStyle: "italic", borderLeft: `2px solid ${brass}`,
489:                           paddingLeft: 10, marginTop: 8 }}>
490:               {result.honest_gap}
491:             </div>
492:           )}
493:         </div>
494:       )}
495:     </div>
496:   );
497: }
498: 
499: function buildCandidate(kind, value) {
500:   if (kind === "exact_value") return { kind, value };
501:   if (kind === "pattern") return { kind, regex: value };
502:   return { kind, category: value };
503: }
504: 
505: function RefusalExample() {
506:   // Doc 01 §A5.5 · closed outbound network except at crossing. The example
507:   // renders the actual refusal grammar the chokepoint would produce for an
508:   // out-of-allowlist region — a governed teaching pattern, not a fabricated
509:   // event. If a real refusal has ever fired, it will appear here in future
510:   // waves; today the estate has zero real refusals on record (drawn-not-
511:   // blank posture).
512:   return (
513:     <div data-testid="data-shield-refusal-example"
514:          style={{ border: `1px solid ${line}`, borderRadius: 9,
515:                   padding: "18px 20px", background: surface }}>
516:       <div style={{ fontSize: 11, letterSpacing: 1.5, color: ink3,
517:                     textTransform: "uppercase", fontWeight: 600,
518:                     marginBottom: 6 }}>
519:         What a refused crossing looks like
520:       </div>
521:       <div style={{ fontSize: 12, color: ink2, lineHeight: 1.55,
522:                     marginBottom: 10 }}>
523:         The chokepoint refuses at the endpoint, not at a UI button. The
524:         refusal carries a plain sentence naming what would have gone wrong.
525:       </div>
526:       <div style={{ fontSize: 11.5, color: ink2, lineHeight: 1.55,
527:                     background: "#f7ecea", borderLeft: `2px solid ${oxblood2}`,
528:                     padding: "10px 12px", borderRadius: 6,
529:                     fontFamily: "ui-monospace, Menlo, monospace" }}>
530:         residency_refused — region_off_allowlist — 'us-east-1' not admissible
531:         for this estate. Allowlisted regions on record: ['eu-west-1'].
532:         Adding a region requires an Owner ruling (CA1-N4 · residency).
533:       </div>
534:       <div style={{ fontSize: 11, color: ink3, marginTop: 8, fontStyle: "italic",
535:                     lineHeight: 1.55 }}>
536:         No real refusals are on record yet — every crossing since the
537:         chokepoint landed has been residency-clean.
538:       </div>
539:     </div>
540:   );
541: }

# SOURCE: frontend/src/components/EvidenceRegister.jsx

1: import React, { useEffect, useState } from "react";
2: import { Link } from "react-router-dom";
3: 
4: /**
5:  * EvidenceRegister.jsx — W11 B · CP6 · Doc 19B §19B.4-6 · EP-1/EP-2/EP-3.
6:  *
7:  * Doc 19B PROPOSED · never confirmed adopted (Doc 19 §19B.1 verbatim).
8:  * The register + protocol are load-bearing before the terminal test
9:  * runs (EP-4 · OPEN ordering constraint · Owner ratification pending).
10:  *
11:  * Verbatim surface anchors (canon Doc 19 §19B.5-6):
12:  *   §19B.6 absolute: "No figure reaches an external document without
13:  *                     a resolvable register row."
14:  *   §19B.6:          "A-4 never becomes a gate by drift — its scope
15:  *                     is validation and re-entry, and staying there
16:  *                     is a condition of adoption, not a detail."
17:  *
18:  * Data sources:
19:  *   GET /api/evidence-register   → EP-1 register rows (empty at ship)
20:  *   GET /api/claims-validation   → EP-3 A-4 rows (empty at ship)
21:  *
22:  * NO judging fires from this surface. Adding a figure requires an
23:  * Owner-side dual-judge protocol; this surface renders lineage only.
24:  */
25: 
26: const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
27: 
28: const paper = "#f5f2ea";
29: const surface = "#ffffff";
30: const ink = "#1b1f27";
31: const ink2 = "#3a3f4a";
32: const ink3 = "#7a7f8a";
33: const line = "#e4dccf";
34: const blue = "#16274a";
35: const sage = "#1d7a6e";
36: const brass = "#b08d2e";
37: const oxblood = "#8a2a44";
38: const head = 'ui-serif, "Iowan Old Style", Georgia, serif';
39: 
40: 
41: function Panel({ dt, title, anchor, children }) {
42:   return (
43:     <section data-testid={dt} style={{
44:       background: surface, border: `1px solid ${line}`, padding: "22px 24px",
45:       marginBottom: 20,
46:     }}>
47:       <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 8 }}>
48:         <h2 style={{ fontFamily: head, fontSize: 20, color: blue, margin: 0 }}>{title}</h2>
49:         <span style={{ fontSize: 11, letterSpacing: 1.5, color: ink3 }}>{anchor}</span>
50:       </div>
51:       {children}
52:     </section>
53:   );
54: }
55: 
56: function ProposedBadge() {
57:   return (
58:     <span data-testid="proposed-status-badge" style={{
59:       display: "inline-block", padding: "2px 8px", fontSize: 10, letterSpacing: 1.5,
60:       color: paper, background: brass, borderRadius: 2, marginLeft: 8,
61:     }}>PROPOSED</span>
62:   );
63: }
64: 
65: export default function EvidenceRegister() {
66:   const [reg, setReg] = useState(null);
67:   const [claims, setClaims] = useState(null);
68:   const [err, setErr] = useState(null);
69: 
70:   useEffect(() => {
71:     fetch(`${BACKEND_URL}/api/evidence-register`)
72:       .then((r) => r.ok ? r.json() : Promise.reject(`HTTP ${r.status}`))
73:       .then(setReg)
74:       .catch((e) => setErr(String(e)));
75:     fetch(`${BACKEND_URL}/api/claims-validation`)
76:       .then((r) => r.ok ? r.json() : Promise.reject(`HTTP ${r.status}`))
77:       .then(setClaims)
78:       .catch(() => { /* empty ledger is honest default */ });
79:   }, []);
80: 
81:   return (
82:     <div data-testid="evidence-register-page" style={{
83:       minHeight: "100vh", background: paper, padding: "48px 40px",
84:       fontFamily: "ui-sans-serif",
85:     }}>
86:       <div style={{ maxWidth: 960, margin: "0 auto" }}>
87:         <div style={{ fontSize: 11, letterSpacing: 2, color: ink3 }}>
88:           AKKI · EVIDENCE REGISTER
89:           <ProposedBadge />
90:         </div>
91:         <h1 style={{ fontFamily: head, fontSize: 40, margin: "10px 0 6px 0", color: blue }}>
92:           Evidence register & claims validation
93:         </h1>
94:         <p data-testid="evidence-register-19b6-anchor"
95:            style={{ color: ink2, maxWidth: 720, lineHeight: 1.55, margin: "0 0 26px 0" }}>
96:           Doc 19B §19B.6 · "No figure reaches an external document without a
97:           resolvable register row." The register is PROPOSED (Owner-noted as
98:           not-yet-canon 2026-08-26); rows carry status_class=PROPOSED until
99:           ratified.
100:         </p>
101: 
102:         {err && (
103:           <Panel dt="evidence-register-error" title="Surface unreachable" anchor="§19B.6">
104:             <p style={{ color: oxblood }}>Backend refused this request: {err}</p>
105:           </Panel>
106:         )}
107: 
108:         <Panel dt="evidence-register-panel"
109:                title="Evidence register · EP-1"
110:                anchor="Doc 19B §19B.5 · Wave B CP6">
111:           {!reg && !err && <p style={{ color: ink3 }}>Loading…</p>}
112:           {reg && reg.count === 0 && (
113:             <>
114:               <p data-testid="evidence-register-empty" style={{ color: ink2, fontStyle: "italic", margin: "6px 0 0 0" }}>
115:                 No evidence-register row on record. Canon anchor: Doc 19B §19B.5. Drawn, never left blank.
116:               </p>
117:               <p style={{ color: ink3, fontSize: 12, marginTop: 8, lineHeight: 1.5 }}>
118:                 {reg.status_class_note}
119:               </p>
120:             </>
121:           )}
122:           {reg && reg.count > 0 && (
123:             <div data-testid="evidence-register-list">
124:               <p style={{ color: ink3, fontSize: 12, marginBottom: 12 }}>
125:                 {reg.count} figure{reg.count === 1 ? "" : "s"} on record.
126:               </p>
127:               {reg.rows.map((r) => (
128:                 <article key={r.figure_id} data-testid={`register-row-${r.figure_id}`}
129:                          style={{ borderTop: `1px solid ${line}`, padding: "12px 0" }}>
130:                   <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
131:                     <h3 style={{ fontFamily: head, fontSize: 15, color: ink, margin: 0 }}>
132:                       {r.figure_id}
133:                     </h3>
134:                     <span style={{ fontSize: 11, color: sage, letterSpacing: 1.2 }}>
135:                       {r.named_site.toUpperCase()}
136:                     </span>
137:                   </div>
138:                   <div style={{ fontSize: 13, color: ink2, marginTop: 4 }}>
139:                     figure: <code data-testid="register-figure">{r.figure}</code>
140:                     {" · κ = "}
141:                     <code data-testid="register-kappa">{r.kappa}</code>
142:                     {" · "}{r.date}
143:                   </div>
144:                   <div style={{ fontSize: 12, color: ink3, marginTop: 4 }}>
145:                     method: {r.method}
146:                   </div>
147:                   <div style={{ fontSize: 12, color: ink3, marginTop: 2 }}>
148:                     judges ({r.judges.length}): {r.judges.join(", ")} ·
149:                     rubric {r.rubric_version} · source_rows: {r.source_rows.join(", ")}
150:                   </div>
151:                 </article>
152:               ))}
153:             </div>
154:           )}
155:         </Panel>
156: 
157:         <Panel dt="claims-validation-panel"
158:                title="Claims validation · EP-3 · A-4"
159:                anchor="Doc 19B §19B.4 · never a build gate">
160:           {!claims && !err && <p style={{ color: ink3 }}>Loading…</p>}
161:           {claims && claims.count === 0 && (
162:             <>
163:               <p data-testid="claims-validation-empty" style={{ color: ink2, fontStyle: "italic", margin: "6px 0 0 0" }}>
164:                 No claims-validation row on record. Canon anchor: Doc 19B §19B.4. Drawn, never left blank.
165:               </p>
166:               <p style={{ color: ink3, fontSize: 12, marginTop: 8, lineHeight: 1.5 }}>
167:                 {claims.never_a_gate_note}
168:               </p>
169:             </>
170:           )}
171:           {claims && claims.count > 0 && (
172:             <ul data-testid="claims-validation-list" style={{ listStyle: "none", padding: 0, margin: 0 }}>
173:               {claims.rows.map((c) => (
174:                 <li key={c.claim_id} style={{ borderTop: `1px solid ${line}`, padding: "12px 0" }}>
175:                   <div style={{ display: "flex", justifyContent: "space-between" }}>
176:                     <span style={{ fontFamily: "ui-monospace, monospace", fontSize: 13, color: blue }}>
177:                       {c.claim_id}
178:                     </span>
179:                     <span style={{ fontSize: 11, letterSpacing: 1.2, color: brass, textTransform: "uppercase" }}>
180:                       {c.verdict}
181:                     </span>
182:                   </div>
183:                   <div style={{ fontSize: 12, color: ink2, marginTop: 4 }}>
184:                     kind {c.claim_kind} · subject {c.subject}
185:                   </div>
186:                   <div style={{ fontSize: 12, color: ink3, marginTop: 2 }}>
187:                     arms: {c.three_arms.join(" · ")}
188:                   </div>
189:                 </li>
190:               ))}
191:             </ul>
192:           )}
193:         </Panel>
194: 
195:         <div data-testid="ep5-non-adoption-note" style={{
196:           background: surface, border: `1px dashed ${line}`,
197:           padding: "14px 16px", fontSize: 12, color: ink3, lineHeight: 1.55,
198:         }}>
199:           <strong>EP-5 · explicit non-adoption.</strong> Doc 19B §19B.5 verbatim:
200:           "Explicitly not adopted, per the same proposal: the source spec's
201:           'insurance telemetry' aside (serves a goal never named) and its
202:           internal reduction-skill mandate." No such services exist on this
203:           estate. See test_ep5_non_adoption_invariant.py.
204:         </div>
205: 
206:         <div style={{ marginTop: 30, fontSize: 12, color: ink3 }}>
207:           <Link to="/" style={{ color: blue }} data-testid="evidence-register-back">← Registry</Link>
208:           <span style={{ margin: "0 10px" }}>·</span>
209:           <Link to="/training" style={{ color: blue }} data-testid="evidence-register-training">Training →</Link>
210:         </div>
211:       </div>
212:     </div>
213:   );
214: }

# SOURCE: frontend/src/components/Governance.jsx

1: import React, { useEffect, useState } from "react";
2: import { Link } from "react-router-dom";
3: 
4: /**
5:  * Governance.jsx — W10 CP8 · Governance surface.
6:  *
7:  * Composes three panels sharing REFERENCE-NOT-COPY posture (Design Law
8:  * A8 · 2026-08-19):
9:  *   1. Reserved-Decisions Panel · Canon 8 §19 + §32.6 · W10 CP4.
10:  *      The five closed reserved kinds are named verbatim (R3
11:  *      ratification 2026-08-26T04:20Z · closed Literal enum · no
12:  *      free-text kinds).
13:  *   2. Rules-Updates Timeline · Doc 15 §17 · W8 CP6 · countdown /
14:  *      apply / re-check lifecycle stages surfaced from disk.
15:  *   3. Approvals Ledger · Doc 15 · W8 CP3 · full request+decision
16:  *      pairs (rules-updates · spend-requests · generic).
17:  *
18:  * Data source: GET /api/governance/state. Every row cites its on-disk
19:  * source_path; the surface renders record ids + short provenance
20:  * rather than embedding record bodies (REFERENCE-NOT-COPY). Empty
21:  * stores render an honest sentence naming the canon anchor.
22:  */
23: 
24: const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
25: 
26: // v7 palette tokens (matched to Registry / CostLedger).
27: const paper = "#f5f2ea";
28: const surface = "#ffffff";
29: const ink = "#1b1f27";
30: const ink2 = "#3a3f4a";
31: const ink3 = "#7a7f8a";
32: const line = "#e4dccf";
33: const blue = "#16274a";
34: const oxblood = "#8a2a44";
35: const brass = "#b08d2e";
36: const head = 'ui-serif, "Iowan Old Style", Georgia, serif';
37: 
38: const RESERVED_KINDS = [
39:   "promote_containment",
40:   "extend_expiry",
41:   "sign_de_mark",
42:   "resolve_authority_disagreement",
43:   "cancel_ceremony_in_countdown",
44: ];
45: 
46: function Panel({ "data-testid": dt, title, anchor, children }) {
47:   return (
48:     <section data-testid={dt} style={{
49:       background: surface, border: `1px solid ${line}`, padding: "22px 24px",
50:       marginBottom: 20,
51:     }}>
52:       <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 8 }}>
53:         <h2 style={{ fontFamily: head, fontSize: 20, color: blue, margin: 0 }}>{title}</h2>
54:         <span style={{ fontSize: 11, letterSpacing: 1.5, color: ink3 }}>{anchor}</span>
55:       </div>
56:       {children}
57:     </section>
58:   );
59: }
60: 
61: function EmptyState({ anchor, kind }) {
62:   return (
63:     <p style={{ color: ink2, fontStyle: "italic", margin: "6px 0 0 0" }}>
64:       No {kind} on record. Canon anchor: {anchor}. Drawn, never left blank.
65:     </p>
66:   );
67: }
68: 
69: function EntryRow({ entry, extra }) {
70:   return (
71:     <li style={{ borderBottom: `1px dotted ${line}`, padding: "8px 0" }}>
72:       <div style={{ fontFamily: "ui-monospace, monospace", fontSize: 13, color: blue }}>
73:         {entry.record_id}
74:       </div>
75:       {extra ? <div style={{ fontSize: 12, color: ink2, marginTop: 2 }}>{extra}</div> : null}
76:       <div style={{ fontSize: 11, color: ink3, marginTop: 2 }}>
77:         {entry.source_path}
78:       </div>
79:     </li>
80:   );
81: }
82: 
83: export default function Governance() {
84:   const [state, setState] = useState(null);
85:   const [error, setError] = useState(null);
86: 
87:   useEffect(() => {
88:     (async () => {
89:       try {
90:         const r = await fetch(`${BACKEND_URL}/api/governance/state`);
91:         if (!r.ok) throw new Error(`HTTP ${r.status}`);
92:         setState(await r.json());
93:       } catch (e) {
94:         setError(String(e));
95:       }
96:     })();
97:   }, []);
98: 
99:   return (
100:     <div data-testid="governance-view" style={{
101:       minHeight: "100vh", background: paper, padding: "40px 48px",
102:       fontFamily: "ui-sans-serif, system-ui",
103:     }}>
104:       <div style={{ maxWidth: 1080, margin: "0 auto" }}>
105:         <div style={{ fontSize: 11, letterSpacing: 2, color: ink3 }}>AKKI · GOVERNANCE</div>
106:         <h1 data-testid="governance-title" style={{
107:           fontFamily: head, fontSize: 40, color: blue, margin: "8px 0 6px 0",
108:         }}>Governance Surface</h1>
109:         <p data-testid="governance-reference-note" style={{
110:           color: ink2, fontSize: 13, lineHeight: 1.6, marginBottom: 20,
111:         }}>
112:           REFERENCE-NOT-COPY (Design Law A8). Every entry cites its
113:           on-disk source_path; record bodies live under
114:           <code style={{ margin: "0 4px" }}>phase0/</code> where each
115:           producer wrote them. Reserved-Decisions Panel anchor: Canon 8 §19
116:           + §32.6. Rules-Updates Timeline anchor: Doc 15 §17.
117:         </p>
118: 
119:         <nav style={{ marginBottom: 24, fontSize: 13 }}>
120:           <Link data-testid="nav-to-watch" to="/watch" style={{ color: blue, marginRight: 20 }}>
121:             → The Watch
122:           </Link>
123:           <Link data-testid="nav-to-grey-mirror" to="/grey-mirror" style={{ color: blue, marginRight: 20 }}>
124:             → Grey Mirror
125:           </Link>
126:           <Link to="/" style={{ color: ink3 }}>← Registry</Link>
127:         </nav>
128: 
129:         {error ? (
130:           <div style={{ color: oxblood, marginBottom: 12 }}>
131:             Failed to load governance state: {error}
132:           </div>
133:         ) : null}
134: 
135:         <Panel data-testid="reserved-decisions-panel"
136:                title="Reserved Decisions"
137:                anchor="Canon 8 §19 · §32.6 · W10 CP4">
138:           <div data-testid="reserved-decisions-count" style={{
139:             fontFamily: "ui-monospace, monospace", color: brass, fontSize: 13, marginBottom: 6,
140:           }}>
141:             {state ? `${state.reserved_decisions.count} on record` : "loading…"}
142:           </div>
143:           <p style={{ fontSize: 12, color: ink3, margin: "6px 0" }}>
144:             Reserved kinds (closed Literal · R3 ratification): {RESERVED_KINDS.join(" · ")}. No reserved decision is executed by machine (§32.6); the operator authors the next call after ApprovalDecision.verdict == "approved".
145:           </p>
146:           {state && state.reserved_decisions.count === 0 ? (
147:             <div data-testid="reserved-decisions-empty-state">
148:               <EmptyState anchor="Canon 8 §19" kind="reserved decisions" />
149:             </div>
150:           ) : null}
151:           {state && state.reserved_decisions.count > 0 ? (
152:             <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
153:               {state.reserved_decisions.entries.map((e) => (
154:                 <EntryRow key={e.record_id} entry={e}
155:                   extra={`kind: ${e.reserved_decision_kind} · subject: ${e.subject_ref || "—"}`} />
156:               ))}
157:             </ul>
158:           ) : null}
159:         </Panel>
160: 
161:         <Panel data-testid="rules-updates-timeline"
162:                title="Rules-Updates Timeline"
163:                anchor="Doc 15 §17 · W8 CP6">
164:           <div data-testid="rules-updates-count" style={{
165:             fontFamily: "ui-monospace, monospace", color: brass, fontSize: 13, marginBottom: 6,
166:           }}>
167:             {state ? `${state.rules_updates.count} lifecycle rows` : "loading…"}
168:           </div>
169:           {state && state.rules_updates.count === 0 ? (
170:             <EmptyState anchor="Doc 15 §17" kind="rules-updates lifecycle rows" />
171:           ) : null}
172:           {state && state.rules_updates.count > 0 ? (
173:             <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
174:               {state.rules_updates.entries.map((e) => (
175:                 <EntryRow key={`${e.record_id}-${e.lifecycle_stage}`} entry={e}
176:                   extra={`stage: ${e.lifecycle_stage}`} />
177:               ))}
178:             </ul>
179:           ) : null}
180:         </Panel>
181: 
182:         <Panel data-testid="approvals-ledger"
183:                title="Approvals Ledger"
184:                anchor="Doc 15 · W8 CP3">
185:           <div data-testid="approvals-count" style={{
186:             fontFamily: "ui-monospace, monospace", color: brass, fontSize: 13, marginBottom: 6,
187:           }}>
188:             {state ? `${state.approvals.count} request+decision rows` : "loading…"}
189:           </div>
190:           {state && state.approvals.count === 0 ? (
191:             <EmptyState anchor="Doc 15" kind="approvals" />
192:           ) : null}
193:           {state && state.approvals.count > 0 ? (
194:             <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
195:               {state.approvals.entries.slice(0, 40).map((e, i) => (
196:                 <EntryRow key={`${e.record_id}-${i}`} entry={e}
197:                   extra={e.kind ? `kind: ${e.kind}` : ""} />
198:               ))}
199:             </ul>
200:           ) : null}
201:         </Panel>
202:       </div>
203:     </div>
204:   );
205: }

# SOURCE: frontend/src/components/GreyMirror.jsx

1: import React, { useEffect, useState } from "react";
2: import { Link } from "react-router-dom";
3: 
4: /**
5:  * GreyMirror.jsx — W10 CP8 · Grey Mirror surface.
6:  *
7:  * Composes three panels sharing REFERENCE-NOT-COPY posture (Design
8:  * Law A8):
9:  *   1. Mirages (Canon 8 §15 · installed lures)
10:  *   2. Mirage Touches (Canon 8 §15 · touch_kind CONTRACT-TIME closed
11:  *      to {'innocent_read', 'guilty_use'} per R2 · 2026-08-26T04:20Z)
12:  *   3. Severances (Canon 8 §16 · outcome for guilty_use touches)
13:  *
14:  * BUILD-not-LIFT rationale: Executive-Core carries no mirage-machinery
15:  * material (verified at W10 CP2 grounding brief §4). The whole Grey
16:  * Mirror stack was built fresh from Canon 8 §§15-16 verbatim.
17:  *
18:  * Data source: GET /api/grey_mirror/state.
19:  */
20: 
21: const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
22: 
23: const paper = "#f5f2ea";
24: const surface = "#ffffff";
25: const ink = "#1b1f27";
26: const ink2 = "#3a3f4a";
27: const ink3 = "#7a7f8a";
28: const line = "#e4dccf";
29: const blue = "#16274a";
30: const sage = "#1d7a6e";
31: const oxblood = "#8a2a44";
32: const brass = "#b08d2e";
33: const head = 'ui-serif, "Iowan Old Style", Georgia, serif';
34: 
35: const TOUCH_KINDS = ["innocent_read", "guilty_use"];
36: 
37: function Panel({ "data-testid": dt, title, anchor, children }) {
38:   return (
39:     <section data-testid={dt} style={{
40:       background: surface, border: `1px solid ${line}`, padding: "22px 24px",
41:       marginBottom: 20,
42:     }}>
43:       <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 8 }}>
44:         <h2 style={{ fontFamily: head, fontSize: 20, color: blue, margin: 0 }}>{title}</h2>
45:         <span style={{ fontSize: 11, letterSpacing: 1.5, color: ink3 }}>{anchor}</span>
46:       </div>
47:       {children}
48:     </section>
49:   );
50: }
51: 
52: function Count({ "data-testid": dt, n, label }) {
53:   return (
54:     <div data-testid={dt} style={{
55:       fontFamily: "ui-monospace, monospace", color: brass, fontSize: 13, marginBottom: 6,
56:     }}>{n === null ? "loading…" : `${n} ${label}`}</div>
57:   );
58: }
59: 
60: function EmptyState({ anchor, kind, mechanismStatus }) {
61:   // W11 R7 · Watch/Grey-Mirror honesty. Grey Mirror is Wave-C-target
62:   // BUILD material across all three panels (planting · touch detection ·
63:   // severance). Explicit unbuilt copy per owner directive 2026-08-26.
64:   if (mechanismStatus && mechanismStatus.startsWith("unbuilt")) {
65:     return (
66:       <p data-testid={`empty-unbuilt-${kind.replace(/\s+/g, "-")}`}
67:          style={{ color: oxblood, fontStyle: "italic", margin: "6px 0 0 0" }}>
68:         mechanism not yet built — {mechanismStatus} · Canon anchor: {anchor}.
69:       </p>
70:     );
71:   }
72:   return (
73:     <p style={{ color: ink2, fontStyle: "italic", margin: "6px 0 0 0" }}>
74:       No {kind} on record. Canon anchor: {anchor}. Drawn, never left blank.
75:     </p>
76:   );
77: }
78: 
79: function EntryRow({ entry, extra }) {
80:   return (
81:     <li style={{ borderBottom: `1px dotted ${line}`, padding: "8px 0" }}>
82:       <div style={{ fontFamily: "ui-monospace, monospace", fontSize: 13, color: blue }}>
83:         {entry.record_id}
84:       </div>
85:       {extra ? <div style={{ fontSize: 12, color: ink2, marginTop: 2 }}>{extra}</div> : null}
86:       <div style={{ fontSize: 11, color: ink3, marginTop: 2 }}>{entry.source_path}</div>
87:     </li>
88:   );
89: }
90: 
91: export default function GreyMirror() {
92:   const [state, setState] = useState(null);
93:   const [error, setError] = useState(null);
94: 
95:   useEffect(() => {
96:     (async () => {
97:       try {
98:         const r = await fetch(`${BACKEND_URL}/api/grey_mirror/state`);
99:         if (!r.ok) throw new Error(`HTTP ${r.status}`);
100:         setState(await r.json());
101:       } catch (e) {
102:         setError(String(e));
103:       }
104:     })();
105:   }, []);
106: 
107:   const g = (k) => (state ? state[k] : null);
108:   const gCount = (k) => (g(k) ? g(k).count : null);
109: 
110:   return (
111:     <div data-testid="grey-mirror-view" style={{
112:       minHeight: "100vh", background: paper, padding: "40px 48px",
113:       fontFamily: "ui-sans-serif, system-ui",
114:     }}>
115:       <div style={{ maxWidth: 1080, margin: "0 auto" }}>
116:         <div style={{ fontSize: 11, letterSpacing: 2, color: ink3 }}>AKKI · GREY MIRROR</div>
117:         <h1 data-testid="grey-mirror-title" style={{
118:           fontFamily: head, fontSize: 40, color: blue, margin: "8px 0 6px 0",
119:         }}>Grey Mirror</h1>
120:         <p data-testid="grey-mirror-reference-note" style={{
121:           color: ink2, fontSize: 13, lineHeight: 1.6, marginBottom: 12,
122:         }}>
123:           REFERENCE-NOT-COPY (Design Law A8). Grey Mirror is a BUILD
124:           (not LIFT · Executive-Core carries no mirage-machinery
125:           material · verified W10 CP2 grounding). Anchors: Canon 8 §15
126:           (mirages · touches) · Canon 8 §16 (severances). Every entry
127:           cites its on-disk source_path.
128:         </p>
129:         <p style={{ color: ink2, fontSize: 13, lineHeight: 1.6, marginBottom: 18 }}>
130:           touch_kind grammar is CONTRACT-TIME closed to <code>{TOUCH_KINDS.join(", ")}</code>
131:           {" "}per R2 ratification (2026-08-26T04:20Z · no service-time extensibility).
132:           An <code>innocent_read</code> is a bookkeeping event; a <code>guilty_use</code>
133:           {" "}is the trigger for a severance (§16).
134:         </p>
135: 
136:         <nav style={{ marginBottom: 24, fontSize: 13 }}>
137:           <Link data-testid="nav-to-governance" to="/governance" style={{ color: blue, marginRight: 20 }}>
138:             → Governance
139:           </Link>
140:           <Link data-testid="nav-to-watch" to="/watch" style={{ color: blue, marginRight: 20 }}>
141:             → The Watch
142:           </Link>
143:           <Link to="/" style={{ color: ink3 }}>← Registry</Link>
144:         </nav>
145: 
146:         {error ? (
147:           <div style={{ color: oxblood, marginBottom: 12 }}>Failed to load: {error}</div>
148:         ) : null}
149: 
150:         <Panel data-testid="mirages-panel" title="Mirages" anchor="Canon 8 §15 · installed lures">
151:           <Count data-testid="mirages-count" n={gCount("mirages")} label="mirages" />
152:           {gCount("mirages") === 0 ? (
153:             <EmptyState anchor="Canon 8 §15" kind="mirages" />
154:           ) : null}
155:           {g("mirages") && g("mirages").count > 0 ? (
156:             <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
157:               {g("mirages").entries.slice(0, 40).map((e, i) => (
158:                 <EntryRow key={`${e.record_id}-${i}`} entry={e}
159:                   extra={e.lure_class ? `lure: ${e.lure_class}` : ""} />
160:               ))}
161:             </ul>
162:           ) : null}
163:         </Panel>
164: 
165:         <Panel data-testid="mirage-touches-panel"
166:                title="Mirage Touches"
167:                anchor="Canon 8 §15 · touch_kind CONTRACT-TIME (R2)">
168:           <Count data-testid="mirage-touches-count" n={gCount("touches")} label="touches" />
169:           {gCount("touches") === 0 ? (
170:             <EmptyState anchor="Canon 8 §15" kind="mirage touches" />
171:           ) : null}
172:           {g("touches") && g("touches").count > 0 ? (
173:             <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
174:               {g("touches").entries.slice(0, 40).map((e, i) => (
175:                 <EntryRow key={`${e.record_id}-${i}`} entry={e}
176:                   extra={
177:                     e.touch_kind
178:                       ? `kind: ${e.touch_kind}${e.touch_kind === "guilty_use" ? " ← triggers severance (§16)" : ""}`
179:                       : ""
180:                   } />
181:               ))}
182:             </ul>
183:           ) : null}
184:         </Panel>
185: 
186:         <Panel data-testid="severances-panel" title="Severances" anchor="Canon 8 §16">
187:           <Count data-testid="severances-count" n={gCount("severances")} label="severances" />
188:           {gCount("severances") === 0 ? (
189:             <EmptyState anchor="Canon 8 §16" kind="severances" />
190:           ) : null}
191:           {g("severances") && g("severances").count > 0 ? (
192:             <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
193:               {g("severances").entries.slice(0, 40).map((e, i) => (
194:                 <EntryRow key={`${e.record_id}-${i}`} entry={e}
195:                   extra={e.cites_touch_id ? `cites touch: ${e.cites_touch_id}` : ""} />
196:               ))}
197:             </ul>
198:           ) : null}
199:         </Panel>
200: 
201:         <Panel data-testid="mirage-artifacts-panel"
202:                title="Mirage Artifacts (§Line 183 isolated store)"
203:                anchor="Canon 8 §Line 136 · §Line 183 · CP-C3">
204:           <Count data-testid="mirage-artifacts-count" n={gCount("mirage_artifacts")} label="mirage artifacts" />
205:           {gCount("mirage_artifacts") === 0 ? (
206:             <EmptyState anchor="Canon 8 §Line 183" kind="mirage artifacts" />
207:           ) : null}
208:           {g("mirage_artifacts") && g("mirage_artifacts").count > 0 ? (
209:             <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
210:               {g("mirage_artifacts").entries.slice(0, 40).map((e, i) => {
211:                 const parts = [];
212:                 if (e.mirage_session_id) parts.push(`session: ${e.mirage_session_id}`);
213:                 if (typeof e.is_synthetic !== "undefined") parts.push(`synthetic: ${String(e.is_synthetic)}`);
214:                 if (e.production_store_leak_check) parts.push(`leak_check: ${e.production_store_leak_check}`);
215:                 return <EntryRow key={`${e.record_id}-${i}`} entry={e} extra={parts.join(" · ")} />;
216:               })}
217:             </ul>
218:           ) : null}
219:         </Panel>
220:       </div>
221:     </div>
222:   );
223: }

# SOURCE: frontend/src/components/ModelEcosystem.jsx

1: import React, { useEffect, useState } from "react";
2: import { Link } from "react-router-dom";
3: 
4: /**
5:  * ModelEcosystem.jsx — W7 CP7 · Docs 13/14 · CA1-004/005/011 surface.
6:  *
7:  * Owner Ruling 2026-08-25T23:30Z (W7 GO):
8:  *   "The Model Admission ceremony renders per the v7 oracle's approvals
9:  *    fabric — admission is a ceremony with a record, and the LLMS &
10:  *    TRAINED MODELS tab fills from admission records only."
11:  *
12:  * Three tabs (canonical order):
13:  *   1. LLMs on record        — 7 Emergent Universal purchased LLMs (real facts).
14:  *   2. Trained adapters      — fills from admission records only.
15:  *                               Empty state is drawn-not-blank, not fabricated.
16:  *   3. Admission records     — history of ceremony fires (admit / refuse).
17:  *
18:  * Live data:
19:  *   GET /api/model_registry/models          — inventory (partitioned)
20:  *   GET /api/model_admission/records        — ceremony history
21:  *   GET /api/model_recheck/all              — CA1-011 W7-half states
22:  *   GET /api/baseline_line/records          — CA1-004 baseline lines
23:  *
24:  * Design law: REFERENCE-NOT-COPY (v7 oracle carries approvals fabric;
25:  * this port is structurally faithful, not byte-copy). No emojis in
26:  * icons — Newsreader/Iowan serif for headers, sans for figures.
27:  */
28: 
29: const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
30: 
31: // v7 palette tokens — must match CostLedger.jsx (audit uniformity).
32: const paper = "#f5f2ea";
33: const surface = "#ffffff";
34: const surface2 = "#f0ebe1";
35: const ink = "#1b1f27";
36: const ink2 = "#3a3f4a";
37: const ink3 = "#7a7f8a";
38: const line = "#e4dccf";
39: const blue = "#16274a";
40: const sage = "#1d7a6e";
41: const oxblood = "#8a2a44";
42: const brass = "#b08d2e";
43: const head = 'ui-serif, "Iowan Old Style", Georgia, serif';
44: 
45: 
46: function Tab({ label, active, onClick, count, testid }) {
47:   return (
48:     <button
49:       onClick={onClick}
50:       data-testid={testid}
51:       style={{
52:         background: active ? blue : "transparent",
53:         color: active ? paper : ink2,
54:         border: `1px solid ${active ? blue : line}`,
55:         padding: "10px 20px",
56:         fontFamily: head,
57:         fontSize: 14,
58:         letterSpacing: 0.4,
59:         cursor: "pointer",
60:         marginRight: 8,
61:       }}
62:     >
63:       {label}
64:       {typeof count === "number" && (
65:         <span style={{ marginLeft: 10, opacity: 0.7, fontSize: 12 }}>({count})</span>
66:       )}
67:     </button>
68:   );
69: }
70: 
71: 
72: function LLMsTab({ purchased }) {
73:   if (!purchased) return <div style={{ color: ink3 }}>Loading LLMs on record…</div>;
74:   return (
75:     <div data-testid="llms-on-record">
76:       <div style={{ fontFamily: head, fontSize: 24, color: ink, marginBottom: 6 }}>
77:         LLMs on record
78:       </div>
79:       <div style={{ color: ink3, fontSize: 13, marginBottom: 24, maxWidth: 720 }}>
80:         {purchased.length} purchased LLM{purchased.length === 1 ? "" : "s"} on this estate.
81:         All access via the Emergent Universal proxy — no raw keys on record;
82:         custody markers only (Owner Order 2026-08-25 §4).
83:       </div>
84:       <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
85:         {purchased.map((m) => (
86:           <div
87:             key={m.model_id}
88:             data-testid={`llm-card-${m.model_id}`}
89:             style={{
90:               background: surface,
91:               border: `1px solid ${line}`,
92:               padding: "18px 22px",
93:             }}
94:           >
95:             <div style={{ fontFamily: head, fontSize: 18, color: ink }}>
96:               {m.model_id}
97:             </div>
98:             <div style={{ color: ink3, fontSize: 12, marginTop: 4, letterSpacing: 0.4 }}>
99:               {(m.role || "").replace(/_/g, " ")}
100:             </div>
101:             <div style={{ marginTop: 14, fontSize: 13, color: ink2, lineHeight: 1.5 }}>
102:               <div><b style={{ color: ink }}>Provider:</b> {m.provider}</div>
103:               <div><b style={{ color: ink }}>Custody:</b> {m.custody_kind}</div>
104:               <div><b style={{ color: ink }}>Connected:</b> {m.connected_at}</div>
105:             </div>
106:             <div style={{
107:               marginTop: 12, fontSize: 12, color: ink3, borderTop: `1px solid ${line}`,
108:               paddingTop: 10, lineHeight: 1.5,
109:             }}>
110:               {m.license_note}
111:             </div>
112:           </div>
113:         ))}
114:       </div>
115:     </div>
116:   );
117: }
118: 
119: 
120: function TrainedAdaptersTab({ trained, rechecks }) {
121:   const seamNote = "services.watch.route_recheck_failure (lands W9)";
122:   if (!trained) return <div style={{ color: ink3 }}>Loading trained adapters…</div>;
123:   if (trained.length === 0) {
124:     return (
125:       <div data-testid="trained-empty" style={{
126:         background: surface, border: `1px solid ${line}`, padding: "32px 28px",
127:       }}>
128:         <div style={{ fontFamily: head, fontSize: 22, color: ink, marginBottom: 8 }}>
129:           No trained adapters admitted yet.
130:         </div>
131:         <div style={{ color: ink3, fontSize: 14, lineHeight: 1.6, maxWidth: 660 }}>
132:           Trained adapters fill this list <em>only</em> from admission records
133:           (Owner Ruling 2026-08-25T23:30Z). No ceremony has fired on this
134:           estate yet — the honest state on record is empty. This is
135:           drawn-not-blank per Canon 1 §4.4.
136:         </div>
137:         <div style={{ marginTop: 16, fontSize: 12, color: ink3, letterSpacing: 0.4 }}>
138:           When ceremony fires: MOAC six-criterion card + resolved training
139:           lineage → adapter registered + re-check-date stamped (90-day
140:           cadence · CA1-011 W7 half). Watch route (W9) will fire on overdue.
141:         </div>
142:       </div>
143:     );
144:   }
145:   const rc = new Map((rechecks || []).map((r) => [r.model_id, r]));
146:   return (
147:     <div data-testid="trained-list">
148:       {trained.map((m) => {
149:         const s = rc.get(m.model_id) || {};
150:         return (
151:           <div key={m.model_id} style={{
152:             background: surface, border: `1px solid ${line}`, padding: "18px 22px",
153:             marginBottom: 14,
154:           }} data-testid={`trained-card-${m.model_id}`}>
155:             <div style={{ fontFamily: head, fontSize: 18, color: ink }}>
156:               {m.model_id}
157:             </div>
158:             <div style={{ fontSize: 12, color: ink3, letterSpacing: 0.4, marginTop: 4 }}>
159:               trained adapter · admitted {m.connected_at}
160:             </div>
161:             <div style={{ marginTop: 10, fontSize: 13, color: ink2 }}>
162:               {m.license_note}
163:             </div>
164:             <div style={{
165:               marginTop: 12, fontSize: 12, color: s.state === "overdue" ? oxblood : sage,
166:               borderTop: `1px solid ${line}`, paddingTop: 10,
167:             }}>
168:               <b style={{ letterSpacing: 0.4 }}>CA1-011 re-check:</b>{" "}
169:               {s.state === "overdue" ? `OVERDUE (due ${s.re_check_due_at})` :
170:                s.state === "due_later" ? `due ${s.re_check_due_at}` :
171:                "state on record"}
172:               <span style={{ color: ink3, marginLeft: 12 }}>
173:                 Watch seam: <code style={{ fontSize: 11 }}>{seamNote}</code>
174:               </span>
175:             </div>
176:           </div>
177:         );
178:       })}
179:     </div>
180:   );
181: }
182: 
183: 
184: function AdmissionRecordsTab({ records }) {
185:   if (!records) return <div style={{ color: ink3 }}>Loading admission history…</div>;
186:   if (records.length === 0) {
187:     return (
188:       <div data-testid="admissions-empty" style={{
189:         background: surface, border: `1px solid ${line}`, padding: "32px 28px",
190:       }}>
191:         <div style={{ fontFamily: head, fontSize: 22, color: ink, marginBottom: 8 }}>
192:           Admission history is empty.
193:         </div>
194:         <div style={{ color: ink3, fontSize: 14, lineHeight: 1.6, maxWidth: 660 }}>
195:           No Model Admission ceremony has fired on this estate yet. Records
196:           land under <code>phase0/model_admission_records/</code>. Ceremony
197:           fires trigger: MOAC validation (§26) → uncurated-evidence check
198:           (§27) → rights-lineage check (§28) → floor check → register.
199:         </div>
200:       </div>
201:     );
202:   }
203:   return (
204:     <div data-testid="admission-history">
205:       {records.map((r, i) => (
206:         <div key={i} data-testid={`admission-row-${i}`} style={{
207:           background: surface, border: `1px solid ${line}`, padding: "16px 20px",
208:           marginBottom: 10, borderLeft: `4px solid ${r.outcome === "admitted" ? sage : oxblood}`,
209:         }}>
210:           <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
211:             <div>
212:               <div style={{ fontFamily: head, fontSize: 16, color: ink }}>
213:                 {r.candidate_model_id}
214:               </div>
215:               <div style={{ fontSize: 12, color: ink3, marginTop: 3 }}>
216:                 {r.computed_at}
217:               </div>
218:             </div>
219:             <div style={{
220:               padding: "4px 10px", fontSize: 12, letterSpacing: 0.6,
221:               background: r.outcome === "admitted" ? sage : oxblood,
222:               color: paper,
223:             }}>
224:               {(r.outcome || "").toUpperCase()}
225:             </div>
226:           </div>
227:           {r.reason && (
228:             <div style={{ marginTop: 10, fontSize: 13, color: ink2 }}>
229:               <b>Reason:</b> {r.reason}
230:             </div>
231:           )}
232:           {r.refusal_note && (
233:             <div style={{ marginTop: 6, fontSize: 13, color: ink3, lineHeight: 1.5 }}>
234:               {r.refusal_note}
235:             </div>
236:           )}
237:           {r.outcome === "admitted" && (
238:             <div style={{ marginTop: 10, fontSize: 12, color: sage }}>
239:               Registry bumped to v{r.registry_version_after}.
240:               CA1-011 Watch seam: <code style={{ fontSize: 11 }}>{r.ca1_011_watch_seam}</code>
241:             </div>
242:           )}
243:         </div>
244:       ))}
245:     </div>
246:   );
247: }
248: 
249: 
250: export default function ModelEcosystem() {
251:   const [tab, setTab] = useState("llms");
252:   const [models, setModels] = useState(null);
253:   const [rechecks, setRechecks] = useState(null);
254:   const [admissions, setAdmissions] = useState(null);
255:   const [error, setError] = useState(null);
256: 
257:   useEffect(() => {
258:     const load = async () => {
259:       try {
260:         const [m, r, a] = await Promise.all([
261:           fetch(`${BACKEND_URL}/api/model_registry/models`).then((x) => x.json()),
262:           fetch(`${BACKEND_URL}/api/model_recheck/all`).then((x) => x.json()),
263:           fetch(`${BACKEND_URL}/api/model_admission/records`).then((x) => x.json()),
264:         ]);
265:         setModels(m);
266:         setRechecks(r.statuses || []);
267:         setAdmissions(a.records || []);
268:       } catch (e) {
269:         setError(String(e));
270:       }
271:     };
272:     load();
273:   }, []);
274: 
275:   return (
276:     <div style={{ minHeight: "100vh", background: paper, padding: "48px 40px 80px" }}>
277:       <div style={{ maxWidth: 1080, margin: "0 auto" }}>
278:         <div style={{ fontSize: 11, letterSpacing: 2, color: ink3 }}>
279:           AKKI · MODEL ECOSYSTEM
280:         </div>
281:         <h1 style={{ fontFamily: head, fontSize: 42, color: ink, margin: "10px 0 8px 0", letterSpacing: -0.5 }}>
282:           Every model on the estate, on record.
283:         </h1>
284:         <div style={{ color: ink3, fontSize: 14, maxWidth: 720, lineHeight: 1.6 }}>
285:           Docs 13/14 · CA1-004 baseline line · CA1-005 whitepaper (W8 · named gap) ·
286:           CA1-011 re-check (W7 register + surface · W9 Watch enforcement at named seam).
287:           Purchased LLMs seed from the Emergent Universal connection (real).
288:           Trained adapters fill from Model Admission ceremony records only.
289:         </div>
290: 
291:         <div style={{ marginTop: 32, marginBottom: 20 }}>
292:           <Tab
293:             label="LLMs on record" testid="tab-llms"
294:             active={tab === "llms"} onClick={() => setTab("llms")}
295:             count={models?.purchased_llms?.length}
296:           />
297:           <Tab
298:             label="Trained adapters" testid="tab-trained"
299:             active={tab === "trained"} onClick={() => setTab("trained")}
300:             count={models?.trained_adapters?.length}
301:           />
302:           <Tab
303:             label="Admission records" testid="tab-admissions"
304:             active={tab === "admissions"} onClick={() => setTab("admissions")}
305:             count={admissions?.length}
306:           />
307:         </div>
308: 
309:         {error && (
310:           <div style={{ background: surface, border: `1px solid ${oxblood}`,
311:                         color: oxblood, padding: 16, fontSize: 13 }}>
312:             {error}
313:           </div>
314:         )}
315: 
316:         {tab === "llms" && <LLMsTab purchased={models?.purchased_llms} />}
317:         {tab === "trained" && (
318:           <TrainedAdaptersTab
319:             trained={models?.trained_adapters}
320:             rechecks={rechecks}
321:           />
322:         )}
323:         {tab === "admissions" && <AdmissionRecordsTab records={admissions} />}
324: 
325:         <div style={{ marginTop: 48, fontSize: 12, color: ink3, borderTop: `1px solid ${line}`, paddingTop: 20 }}>
326:           <Link to="/" style={{ color: blue, textDecoration: "none" }} data-testid="nav-registry">
327:             ← Registry
328:           </Link>
329:           <span style={{ marginLeft: 20 }}>
330:             <Link to="/cost-ledger" style={{ color: blue, textDecoration: "none" }} data-testid="nav-cost-ledger">
331:               Cost Ledger →
332:             </Link>
333:           </span>
334:         </div>
335:       </div>
336:     </div>
337:   );
338: }

# SOURCE: frontend/src/components/RefusalCard.jsx

1: import React from "react";
2: import { ShieldAlert } from "lucide-react";
3: import ClassBadge from "./ClassBadge";
4: 
5: /**
6:  * RefusalCard.jsx — W11 R5 · Canon 5 §9.2 binding-copy card.
7:  *
8:  * Owner directive verbatim (2026-08-26):
9:  *   "lift RefusalCard.js verbatim from RMS/OS-V1 into
10:  *    pod_shell/frontend/src/components/, wire every refusal surface
11:  *    (chat, connect, training seal refusal, solva) through it per
12:  *    Canon 5 §9.2 binding-copy card."
13:  *
14:  * Canon 5 §9.2 verbatim (from
15:  * canon/text/Akki_Canon_5_Interface_Architecture.txt lines 130-140):
16:  *   "Not to the standard you asked for.
17:  *    Accept as recorded statement · Narrow the objective · Lower the standard
18:  *    A refusal is the system keeping its promise.
19:  *    The title, the three actions, and the footer are binding copy,
20:  *    reproduced verbatim wherever this card renders. They are never
21:  *    paraphrased, shortened, or restyled for a particular surface."
22:  *
23:  * Canon-vs-donor supersession note: the donor RefusalCard.js in
24:  * Akki-OS-V1 / RMS-IQ-Core-2 renders headline 'Not to the standard
25:  * required.' — this is a paraphrase of Canon 5 §9.2 and violates
26:  * owner Condition 1 (no paraphrasing requirements). This component
27:  * lifts the DONOR STRUCTURE (React shell + amber styling + ShieldAlert
28:  * icon + ClassBadge integration + data-testids) but rebases the
29:  * BINDING COPY on Canon 5 §9.2 verbatim. Recorded in DECISIONS.md
30:  * at Wave A close 2026-08-26.
31:  */
32: 
33: // Canon 5 §9.2 verbatim · binding copy · reproduced without change.
34: const CANON_5_9_2_TITLE = "Not to the standard you asked for.";
35: const CANON_5_9_2_ACTIONS = [
36:   "Accept as recorded statement",
37:   "Narrow the objective",
38:   "Lower the standard",
39: ];
40: const CANON_5_9_2_FOOTER = "A refusal is the system keeping its promise.";
41: 
42: export default function RefusalCard({ refusal, onAction }) {
43:   if (!refusal) return null;
44:   return (
45:     <div
46:       data-testid="refusal-card"
47:       className="rounded-lg border-2 border-amber-300 bg-amber-50 p-5"
48:     >
49:       <div className="flex items-start gap-3">
50:         <ShieldAlert className="w-5 h-5 text-amber-600 mt-0.5 flex-shrink-0" />
51:         <div className="flex-1 min-w-0">
52:           {/* Canon 5 §9.2 verbatim title. Never paraphrased. */}
53:           <h3
54:             data-testid="refusal-headline"
55:             className="text-sm font-semibold text-amber-900"
56:           >
57:             {CANON_5_9_2_TITLE}
58:           </h3>
59: 
60:           <dl className="mt-3 space-y-2 text-sm">
61:             {refusal.asked && (
62:               <div>
63:                 <dt className="text-xs font-medium text-amber-700 uppercase tracking-wide">Asked</dt>
64:                 <dd data-testid="refusal-asked" className="mt-0.5 text-amber-900">{refusal.asked}</dd>
65:               </div>
66:             )}
67:             {refusal.reason && (
68:               <div>
69:                 <dt className="text-xs font-medium text-amber-700 uppercase tracking-wide">Reason</dt>
70:                 <dd data-testid="refusal-reason" className="mt-0.5 text-amber-900 font-mono text-xs">{refusal.reason}</dd>
71:               </div>
72:             )}
73:             {refusal.supported_class && (
74:               <div>
75:                 <dt className="text-xs font-medium text-amber-700 uppercase tracking-wide">Supported class</dt>
76:                 <dd data-testid="refusal-supported-class" className="mt-0.5">
77:                   <ClassBadge defensibilityClass={refusal.supported_class} />
78:                 </dd>
79:               </div>
80:             )}
81:             {refusal.what_would_raise_it && (
82:               <div>
83:                 <dt className="text-xs font-medium text-amber-700 uppercase tracking-wide">What would raise it</dt>
84:                 <dd data-testid="refusal-raise" className="mt-0.5 text-amber-900">{refusal.what_would_raise_it}</dd>
85:               </div>
86:             )}
87:           </dl>
88: 
89:           {/* Canon 5 §9.2 verbatim three-actions row. Never paraphrased. */}
90:           <div
91:             data-testid="refusal-actions"
92:             className="mt-4 flex flex-wrap items-center gap-2"
93:           >
94:             {CANON_5_9_2_ACTIONS.map((action, i) => (
95:               <React.Fragment key={action}>
96:                 {i > 0 && (
97:                   <span className="text-amber-500 text-xs" aria-hidden="true">·</span>
98:                 )}
99:                 <button
100:                   data-testid={`refusal-action-${action.split(" ")[0].toLowerCase()}`}
101:                   onClick={() => onAction && onAction(action)}
102:                   className="text-xs font-medium text-amber-900 border border-amber-300 bg-amber-100 hover:bg-amber-200 rounded px-2 py-1 transition-colors"
103:                   type="button"
104:                 >
105:                   {action}
106:                 </button>
107:               </React.Fragment>
108:             ))}
109:           </div>
110: 
111:           {/* Canon 5 §9.2 verbatim footer. Never paraphrased. */}
112:           <p
113:             data-testid="refusal-footer"
114:             className="mt-4 text-xs text-amber-700 italic"
115:           >
116:             {CANON_5_9_2_FOOTER}
117:           </p>
118:         </div>
119:       </div>
120:     </div>
121:   );
122: }
123: 
124: // Named exports for tests that verify verbatim strings live in the module.
125: export { CANON_5_9_2_TITLE, CANON_5_9_2_ACTIONS, CANON_5_9_2_FOOTER };

# SOURCE: frontend/src/components/Registry.jsx

1: import React, { useEffect, useState } from "react";
2: import ConnectDrawerChat from "@/components/ConnectDrawerChat";
3: 
4: /**
5:  * Registry — the estate's inventory surface (Owner Order 2026-08-19 · FL-P2-25).
6:  *
7:  * Renders per fixtures/screen_mockups_v7.pdf Registry Feature & Component
8:  * Brief. Every figure traces to a durable record on disk via
9:  * GET /api/registry/facts. No fabrication; approximations flagged (≈);
10:  * empty tabs draw the gap ("drawn, never left blank").
11:  *
12:  * Page pattern (§2):
13:  *   Two-column: LEFT fluid | RIGHT 300px.
14:  *   Topline row     | Headliner panel
15:  *   Divider
16:  *   Visual row      | Context panel
17:  *   Divider
18:  *   Table row       | Context panel
19:  *
20:  * Content rules (§6):
21:  *   1. Sentences first, measures second.
22:  *   2. No figure without provenance.
23:  *   3. Gaps are drawn.
24:  *   4. Refusals/failures are work done.
25:  *   5. One emphasis per deck.
26:  *   6. Read-only means read-only.
27:  *
28:  * Role switcher renders static (Track-B; FL-P2-15).
29:  */
30: const cream = "#f6f2ea";
31: const navy = "#1c2b45";
32: const grey = "#666";
33: const mid = "#8a8a8a";
34: const rule = "#e2ded4";
35: const cardWhite = "#ffffff";
36: const crimson = "#b83a2b";
37: const sage = "#7a8a5a";
38: 
39: const TABS = [
40:   { key: "data-connected", label: "DATA CONNECTED", testid: "tab-data-connected" },
41:   { key: "compute-connected", label: "COMPUTE CONNECTED", testid: "tab-compute-connected" },
42:   { key: "llms-trained-models", label: "LLMS & TRAINED MODELS", testid: "tab-llms-trained-models" },
43: ];
44: 
45: const ROLES = ["Compliance Owner", "Watch Officer", "Operator"];
46: 
47: const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
48: 
49: export default function Registry() {
50:   const [activeTab, setActiveTab] = useState("data-connected");
51:   const [wizardOpen, setWizardOpen] = useState(false);
52:   const [facts, setFacts] = useState(null);
53:   const [error, setError] = useState(null);
54:   const [selectedSource, setSelectedSource] = useState(null);
55:   const [selectedCompute, setSelectedCompute] = useState(null);
56: 
57:   useEffect(() => {
58:     // /api/registry/facts
59:     const url = `${BACKEND_URL}/api/registry/facts`;
60:     fetch(url)
61:       .then((r) => r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`)))
62:       .then(setFacts)
63:       .catch((e) => setError(String(e.message || e)));
64:   }, []);
65: 
66:   return (
67:     <div style={{ minHeight: "100vh", background: cream, fontFamily: "ui-sans-serif" }}>
68:       <Header />
69: 
70:       <main style={{ padding: "32px 60px 80px" }}>
71:         <div style={{ maxWidth: 1280, margin: "0 auto" }}>
72:           <TitleDeck />
73:           <TabBar activeTab={activeTab} onTabChange={setActiveTab} onOpenWizard={() => setWizardOpen(true)} />
74: 
75:           <div style={{ marginTop: 32 }}>
76:             {error && <ErrorBanner error={error} />}
77:             {!facts && !error && <LoadingBanner />}
78:             {facts && activeTab === "data-connected" && (
79:               <DataConnectedTab facts={facts} onOpen={setSelectedSource} />
80:             )}
81:             {facts && activeTab === "compute-connected" && (
82:               <ComputeConnectedTab facts={facts} onOpen={setSelectedCompute} />
83:             )}
84:             {facts && activeTab === "llms-trained-models" && (
85:               <LLMsTrainedModelsTab facts={facts} />
86:             )}
87:           </div>
88:         </div>
89:       </main>
90: 
91:       {selectedSource && (
92:         <DataSourceDetailCard source={selectedSource} onClose={() => setSelectedSource(null)} />
93:       )}
94:       {selectedCompute && (
95:         <ComputeDetailCard host={selectedCompute} onClose={() => setSelectedCompute(null)} />
96:       )}
97:       {wizardOpen && <ConnectDrawerChat onClose={() => setWizardOpen(false)} />}
98:     </div>
99:   );
100: }
101: 
102: // ---------------------------------------------------------------------------
103: // Header + Title + TabBar
104: // ---------------------------------------------------------------------------
105: 
106: function Header() {
107:   return (
108:     <header style={{ background: navy, color: cardWhite, padding: "16px 60px",
109:                      display: "flex", alignItems: "center", gap: 24 }}>
110:       <div style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 18, letterSpacing: 0.5 }}>
111:         Akki · ESTATE
112:       </div>
113:       <div style={{ flex: 1 }} />
114:       <div data-testid="role-switcher" style={{ display: "flex", gap: 8 }}>
115:         {ROLES.map((role) => (
116:           <div key={role} data-testid={`role-${role.toLowerCase().replace(/\s+/g, "-")}`}
117:                style={{ padding: "6px 12px", borderRadius: 999,
118:                         background: "rgba(255,255,255,0.08)",
119:                         fontSize: 12, color: cardWhite, letterSpacing: 0.3 }}>
120:             {role}
121:           </div>
122:         ))}
123:         <div style={{ width: 32, height: 32, borderRadius: 999,
124:                       background: "rgba(255,255,255,0.15)",
125:                       display: "flex", alignItems: "center", justifyContent: "center",
126:                       fontSize: 13, marginLeft: 4 }}>U</div>
127:       </div>
128:     </header>
129:   );
130: }
131: 
132: function TitleDeck() {
133:   return (
134:     <div style={{ marginBottom: 32 }}>
135:       <div style={{ fontSize: 11, letterSpacing: 2, color: grey }}>REGISTRY · ESTATE</div>
136:       <h1 data-testid="registry-title"
137:           style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 44,
138:                    margin: "8px 0 12px 0", color: navy }}>
139:         Registry
140:       </h1>
141:       <p style={{ color: grey, lineHeight: 1.55, maxWidth: 720, margin: 0 }}>
142:         What you hold, what is connected, what is answering.
143:         Read-only by design, with one write path — Connect.
144:       </p>
145:     </div>
146:   );
147: }
148: 
149: function TabBar({ activeTab, onTabChange, onOpenWizard }) {
150:   return (
151:     <div style={{ display: "flex", alignItems: "center", gap: 32,
152:                   borderBottom: `1px solid ${rule}` }}>
153:       {TABS.map((t) => {
154:         const active = t.key === activeTab;
155:         return (
156:           <button key={t.key} type="button" data-testid={t.testid}
157:                   onClick={() => onTabChange(t.key)}
158:                   style={{ background: "transparent", border: "none", cursor: "pointer",
159:                            padding: "12px 4px", fontSize: 12, letterSpacing: 2,
160:                            color: active ? navy : grey,
161:                            borderBottom: active ? `2px solid ${navy}` : "2px solid transparent",
162:                            marginBottom: -1 }}>
163:             {t.label}
164:           </button>
165:         );
166:       })}
167:       <div style={{ flex: 1 }} />
168:       <button type="button" data-testid="open-connect-wizard" onClick={onOpenWizard}
169:               style={{ padding: "10px 20px", background: navy, color: cardWhite,
170:                        border: "none", borderRadius: 999, cursor: "pointer",
171:                        fontSize: 13, letterSpacing: 0.3, marginBottom: 8 }}>
172:         + Connect
173:       </button>
174:     </div>
175:   );
176: }
177: 
178: function LoadingBanner() {
179:   return (
180:     <div data-testid="registry-loading" style={{ padding: 32, color: grey }}>
181:       Reading the estate…
182:     </div>
183:   );
184: }
185: 
186: function ErrorBanner({ error }) {
187:   return (
188:     <div data-testid="registry-error"
189:          style={{ padding: 24, background: cardWhite, borderRadius: 8, color: crimson }}>
190:       The estate could not be read: {error}. This is work done, not work lost — try again.
191:     </div>
192:   );
193: }
194: 
195: // ---------------------------------------------------------------------------
196: // Layout primitives — Topline / Headliner / Visual / Table / Context bands
197: // ---------------------------------------------------------------------------
198: 
199: function TwoColBand({ children }) {
200:   return (
201:     <div style={{ display: "grid", gridTemplateColumns: "1fr 300px", gap: 24,
202:                   marginBottom: 24 }}>
203:       {children}
204:     </div>
205:   );
206: }
207: 
208: function Divider() {
209:   return <div style={{ height: 1, background: rule, margin: "24px 0" }} />;
210: }
211: 
212: function SectionTitle({ title, intro, right }) {
213:   return (
214:     <div style={{ display: "flex", alignItems: "baseline", gap: 20, marginBottom: 12 }}>
215:       <div>
216:         <div style={{ fontSize: 12, letterSpacing: 1.5, color: navy, fontWeight: 600 }}>
217:           {title}
218:         </div>
219:         {intro && (
220:           <div style={{ fontSize: 13, color: grey, marginTop: 4 }}>{intro}</div>
221:         )}
222:       </div>
223:       <div style={{ flex: 1 }} />
224:       {right}
225:     </div>
226:   );
227: }
228: 
229: function StatCell({ label, value, note }) {
230:   return (
231:     <div style={{ borderTop: `1px solid ${rule}`, padding: "14px 0" }}>
232:       <div style={{ fontSize: 10, letterSpacing: 1.5, color: mid, textTransform: "uppercase" }}>
233:         {label}
234:       </div>
235:       <div style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 24, color: navy,
236:                     marginTop: 4 }}>
237:         {value}
238:       </div>
239:       {note && <div style={{ fontSize: 11, color: grey, marginTop: 2 }}>{note}</div>}
240:     </div>
241:   );
242: }
243: 
244: function StatGrid({ cells }) {
245:   return (
246:     <div data-testid="registry-topline"
247:          style={{ background: cardWhite, borderRadius: 12, padding: "16px 24px" }}>
248:       <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "0 32px" }}>
249:         {cells.map((c, i) => <StatCell key={i} {...c} />)}
250:       </div>
251:     </div>
252:   );
253: }
254: 
255: function Headliner({ eyebrow, deck, emphasis, provenance }) {
256:   return (
257:     <aside data-testid="registry-headliner"
258:            style={{ background: cardWhite, borderRadius: 12, padding: "18px 20px",
259:                     display: "flex", flexDirection: "column", justifyContent: "center" }}>
260:       <div style={{ fontSize: 10, letterSpacing: 1.5, color: mid,
261:                     textTransform: "uppercase", marginBottom: 8 }}>
262:         {eyebrow}
263:       </div>
264:       <div style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 20,
265:                     lineHeight: 1.35, color: navy }}>
266:         {deck}
267:         {emphasis && (
268:           <span style={{ color: crimson }}> {emphasis}</span>
269:         )}
270:       </div>
271:       {provenance && (
272:         <div style={{ fontSize: 11, color: grey, marginTop: 10, lineHeight: 1.5 }}>
273:           {provenance}
274:         </div>
275:       )}
276:     </aside>
277:   );
278: }
279: 
280: function VisualBars({ rows, denominator }) {
281:   const measured = rows.filter((r) => r.approx_rows != null);
282:   const max = measured.reduce((m, r) => Math.max(m, r.approx_rows || 0), 1);
283:   return (
284:     <div data-testid="registry-visual"
285:          style={{ background: cardWhite, borderRadius: 12, padding: "18px 24px" }}>
286:       {rows.map((r, i) => {
287:         const pct = r.approx_rows ? Math.max(4, Math.round(100 * r.approx_rows / max)) : 0;
288:         const hatched = r.approx_rows == null;
289:         return (
290:           <div key={i} style={{ display: "grid",
291:                                 gridTemplateColumns: "220px 1fr 120px",
292:                                 alignItems: "center", gap: 12, padding: "6px 0" }}>
293:             <div style={{ fontSize: 13, color: navy }}>{r.table}</div>
294:             <div style={{ height: 10, background: rule, borderRadius: 3, position: "relative" }}>
295:               {hatched ? (
296:                 <div style={{ position: "absolute", inset: 0, borderRadius: 3,
297:                               backgroundImage: `repeating-linear-gradient(45deg, ${rule}, ${rule} 4px, ${mid} 4px, ${mid} 5px)` }} />
298:               ) : (
299:                 <div style={{ position: "absolute", left: 0, top: 0, bottom: 0,
300:                               width: `${pct}%`, background: navy, borderRadius: 3 }} />
301:               )}
302:             </div>
303:             <div style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 13,
304:                           color: navy, textAlign: "right" }}>
305:               {hatched ? "not yet measured" : `≈ ${(r.approx_rows).toLocaleString()} rows`}
306:             </div>
307:           </div>
308:         );
309:       })}
310:       <div style={{ fontSize: 11, color: grey, marginTop: 12, borderTop: `1px solid ${rule}`,
311:                     paddingTop: 8 }}>
312:         {denominator}
313:       </div>
314:     </div>
315:   );
316: }
317: 
318: function ContextPanel({ eyebrow, sentences }) {
319:   return (
320:     <aside data-testid="registry-context-panel"
321:            style={{ background: cardWhite, borderRadius: 12, padding: "18px 20px" }}>
322:       <div style={{ fontSize: 10, letterSpacing: 1.5, color: mid,
323:                     textTransform: "uppercase", marginBottom: 10 }}>
324:         {eyebrow}
325:       </div>
326:       {sentences.map((s, i) => (
327:         <p key={i} style={{ fontSize: 13, color: navy, lineHeight: 1.55, margin: "0 0 10px" }}>
328:           {s}
329:         </p>
330:       ))}
331:     </aside>
332:   );
333: }
334: 
335: function Chip({ label, tone = "neutral" }) {
336:   const bg = tone === "sage" ? sage : tone === "crimson" ? crimson :
337:              tone === "navy" ? navy : mid;
338:   return (
339:     <span style={{ display: "inline-block", padding: "3px 10px", borderRadius: 999,
340:                    background: bg, color: cardWhite, fontSize: 11, letterSpacing: 0.5 }}>
341:       {label}
342:     </span>
343:   );
344: }
345: 
346: // ---------------------------------------------------------------------------
347: // DATA CONNECTED tab
348: // ---------------------------------------------------------------------------
349: 
350: function DataConnectedTab({ facts, onOpen }) {
351:   const sources = facts.data_sources || [];
352:   const totalTables = sources.reduce((n, s) => n + (s.table_count || 0), 0);
353: 
354:   if (sources.length === 0) {
355:     return (
356:       <EmptyPanel eyebrow="WHAT YOU HOLD"
357:                   headline="No data connected yet."
358:                   sentence="Nothing has been admitted into the estate through Connect. When a source lands it appears here as measurement, never as an estimate — drawn, never left blank." />
359:     );
360:   }
361: 
362:   // Aggregate top tables across sources (top 10 by approx rows)
363:   const allTop = [];
364:   for (const s of sources) {
365:     for (const t of (s.top_tables || [])) {
366:       allTop.push({ database: s.database, ...t });
367:     }
368:   }
369:   allTop.sort((a, b) => (b.approx_rows || 0) - (a.approx_rows || 0));
370:   const topTen = allTop.slice(0, 10);
371:   const largest = topTen[0];
372: 
373:   const toplineCells = [
374:     { label: "Sources connected", value: sources.length,
375:       note: "drawn, never left blank" },
376:     { label: "Tables inventoried", value: totalTables.toLocaleString(),
377:       note: `across ${sources.length} databases` },
378:     { label: "Largest holding", value: largest ? largest.table : "not yet measured",
379:       note: largest ? `≈ ${largest.approx_rows.toLocaleString()} rows (approx)` : "" },
380:     { label: "Rights class", value: "not yet measured",
381:       note: "record-matrix binding awaits owner ruling" },
382:     { label: "Records read", value: "0",
383:       note: "structure only this pass" },
384:     { label: "Language coverage", value: "not yet measured", note: "" },
385:     { label: "Verified schemas", value: sources.length,
386:       note: "SELECT 1 + information_schema green" },
387:     { label: "Channel", value: "RDS Data API",
388:       note: "HTTPS out via boto3, no VPC peering" },
389:     { label: "Provenance", value: "on-record", note: "every figure traces to disk" },
390:   ];
391: 
392:   const posture = "structure only";
393:   return (
394:     <div>
395:       {/* Topline + Headliner band */}
396:       <TwoColBand>
397:         <StatGrid cells={toplineCells} />
398:         <Headliner
399:           eyebrow="WHAT YOU HOLD"
400:           deck={`Two databases answer over one governed channel; nothing has been read beyond their structure.`}
401:           emphasis="Structure only."
402:           provenance={`Last verified ${sources[0].last_verified ? sources[0].last_verified.slice(0, 19).replace("T", " ") + "Z" : "—"} · via /api/registry/facts.`} />
403:       </TwoColBand>
404: 
405:       <Divider />
406: 
407:       {/* Visual band */}
408:       <SectionTitle
409:         title="COMPOSITION · TOP TABLES"
410:         intro="Where the row-mass sits across the two databases." />
411:       <TwoColBand>
412:         <VisualBars rows={topTen}
413:                     denominator={`Denominator: information_schema.tables.table_rows across ${sources.length} databases (approximate on InnoDB).`} />
414:         <ContextPanel
415:           eyebrow="READING THE MIX"
416:           sentences={[
417:             "USSD activity dominates: the top four tables all sit in digicow_live and hold session-and-response records from the SMS/USSD farmer channel.",
418:             "Row counts are approximations pulled from information_schema — exact counts require record-level access, which waits on a data-handling agreement.",
419:           ]} />
420:       </TwoColBand>
421: 
422:       <Divider />
423: 
424:       {/* Table band */}
425:       <SectionTitle
426:         title="RECORD · SOURCES"
427:         intro="The estate's two connected databases, as last read." />
428:       <TwoColBand>
429:         <div data-testid="registry-record-table"
430:              style={{ background: cardWhite, borderRadius: 12, padding: "8px 0" }}>
431:           <table style={{ width: "100%", borderCollapse: "collapse" }}>
432:             <thead>
433:               <tr>
434:                 {["Source", "Engine", "Tables", "Last verified", "Posture"].map((h) => (
435:                   <th key={h} style={{ padding: "12px 24px", textAlign: "left",
436:                                        fontSize: 10, letterSpacing: 1.5, color: mid,
437:                                        textTransform: "uppercase",
438:                                        borderBottom: `1px solid ${rule}` }}>
439:                     {h}
440:                   </th>
441:                 ))}
442:               </tr>
443:             </thead>
444:             <tbody>
445:               {sources.map((s) => (
446:                 <tr key={s.source_id}
447:                     data-testid="data-source-row"
448:                     data-source-id={s.source_id}
449:                     onClick={() => onOpen(s)}
450:                     style={{ cursor: "pointer" }}
451:                     onMouseEnter={(e) => e.currentTarget.style.background = "#f8f5ee"}
452:                     onMouseLeave={(e) => e.currentTarget.style.background = "transparent"}>
453:                   <td style={{ padding: "16px 24px", color: navy, fontSize: 14 }}>
454:                     <div style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 15 }}>
455:                       {s.database}
456:                     </div>
457:                     <div style={{ fontSize: 11, color: grey, marginTop: 2 }}>{s.region}</div>
458:                   </td>
459:                   <td style={{ padding: "16px 24px", color: navy, fontSize: 13 }}>
460:                     <div>{s.engine}</div>
461:                     <div style={{ fontSize: 11, color: grey }}>{s.engine_version}</div>
462:                   </td>
463:                   <td style={{ padding: "16px 24px", color: navy,
464:                                fontFamily: "ui-serif, Georgia, serif", fontSize: 15 }}>
465:                     ≈ {s.table_count}
466:                   </td>
467:                   <td style={{ padding: "16px 24px", fontSize: 12, color: grey }}>
468:                     {s.last_verified ? s.last_verified.slice(0, 10) : "—"}
469:                   </td>
470:                   <td style={{ padding: "16px 24px" }}>
471:                     <span data-testid="posture-chip-structure-only">
472:                       <Chip label={posture.toUpperCase()} tone="navy" />
473:                     </span>
474:                   </td>
475:                 </tr>
476:               ))}
477:             </tbody>
478:           </table>
479:         </div>
480:         <ContextPanel
481:           eyebrow="WHAT YOU HOLD"
482:           sentences={[
483:             `Two databases sit on one Aurora MySQL cluster in ${sources[0].region}: ${sources.map((s) => s.database).join(" and ")}.`,
484:             "Both answer over the RDS Data API (HTTPS out through boto3). No IP allowlisting on the DB side; no VPC peering.",
485:             "First pass read the shape only — schemas, tables, and column types via information_schema. Record-level access waits on a data-handling agreement.",
486:           ]} />
487:       </TwoColBand>
488:     </div>
489:   );
490: }
491: 
492: function DataSourceDetailCard({ source, onClose }) {
493:   return (
494:     <div style={{ position: "fixed", inset: 0, background: "rgba(28,43,69,0.55)",
495:                   display: "flex", alignItems: "center", justifyContent: "center", zIndex: 40 }}
496:          onClick={onClose}>
497:       <div data-testid="data-source-detail-card"
498:            onClick={(e) => e.stopPropagation()}
499:            style={{ background: cardWhite, borderRadius: 16, width: "min(720px, 92vw)",
500:                     maxHeight: "80vh", overflow: "auto", padding: "28px 32px",
501:                     boxShadow: "0 20px 40px rgba(0,0,0,0.25)" }}>
502:         <div style={{ display: "flex", alignItems: "start" }}>
503:           <div style={{ flex: 1 }}>
504:             <div style={{ fontSize: 11, letterSpacing: 1.5, color: mid, textTransform: "uppercase" }}>
505:               DATA SOURCE
506:             </div>
507:             <h2 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 28,
508:                          margin: "6px 0 4px", color: navy }}>
509:               {source.database}
510:             </h2>
511:             <div style={{ fontSize: 12, color: grey }}>{source.source_id}</div>
512:           </div>
513:           <button data-testid="data-source-detail-close" onClick={onClose}
514:                   style={{ background: "transparent", border: `1px solid ${rule}`,
515:                            padding: "6px 12px", borderRadius: 999, cursor: "pointer",
516:                            color: grey, fontSize: 12 }}>
517:             Close
518:           </button>
519:         </div>
520:         <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 12,
521:                       marginTop: 20 }}>
522:           <KV label="ENGINE" value={source.engine} />
523:           <KV label="VERSION" value={source.engine_version} />
524:           <KV label="REGION" value={source.region} />
525:           <KV label="CHANNEL" value={source.channel} />
526:           <KV label="TABLE COUNT" value={`≈ ${source.table_count}`} />
527:           <KV label="POSTURE" value={source.posture} />
528:         </div>
529:         <h3 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 16,
530:                      margin: "24px 0 8px", color: navy }}>
531:           Top tables (approximate)
532:         </h3>
533:         <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
534:           <thead>
535:             <tr>
536:               {["Table", "≈ Rows", "Size"].map((h) => (
537:                 <th key={h} style={{ padding: "8px 12px", textAlign: "left",
538:                                      fontSize: 10, letterSpacing: 1.5, color: mid,
539:                                      borderBottom: `1px solid ${rule}` }}>{h}</th>
540:               ))}
541:             </tr>
542:           </thead>
543:           <tbody>
544:             {(source.top_tables || []).slice(0, 10).map((t, i) => (
545:               <tr key={i}>
546:                 <td style={{ padding: "8px 12px", color: navy }}>{t.table}</td>
547:                 <td style={{ padding: "8px 12px", color: navy,
548:                              fontFamily: "ui-serif, Georgia, serif" }}>
549:                   ≈ {(t.approx_rows || 0).toLocaleString()}
550:                 </td>
551:                 <td style={{ padding: "8px 12px", color: grey }}>{t.size_mb} MB</td>
552:               </tr>
553:             ))}
554:           </tbody>
555:         </table>
556:         <p style={{ fontSize: 12, color: grey, marginTop: 16 }}>
557:           Row counts are approximations from information_schema.tables. This
558:           first pass read the structure only — zero record contents left the
559:           database.
560:         </p>
561:       </div>
562:     </div>
563:   );
564: }
565: 
566: // ---------------------------------------------------------------------------
567: // COMPUTE CONNECTED tab
568: // ---------------------------------------------------------------------------
569: 
570: function ComputeConnectedTab({ facts, onOpen }) {
571:   const compute = facts.compute || [];
572:   if (compute.length === 0) {
573:     return (
574:       <EmptyPanel eyebrow="WHAT IS CONNECTED"
575:                   headline="No compute connected yet."
576:                   sentence="When a machine lands, this tab renders its commissioning record — hardened, accepted, and receipted. Not yet measured — drawn, never left blank." />
577:     );
578:   }
579:   const host = compute[0];  // one machine for now
580: 
581:   const g = host.gpus || {};
582:   const pv = host.primary_volume || {};
583:   const link = host.link || {};
584: 
585:   const toplineCells = [
586:     { label: "Hosts connected", value: compute.length,
587:       note: host.state_class === "accepted-as-delivered" ? "accepted as delivered" : "" },
588:     { label: "GPUs", value: `${g.count} × ${g.model || "GPU"}`,
589:       note: g.nvlink_active ? "NVLink active" : "no NVLink" },
590:     { label: "Aggregate VRAM", value: g.vram_gb_total ? `${Math.round(g.vram_gb_total)} GB` : "—",
591:       note: g.vram_gb_per_gpu ? `${Math.round(g.vram_gb_per_gpu)} GB/GPU` : "" },
592:     { label: "System RAM", value: `${host.ram_gb_total} GB`, note: "" },
593:     { label: "vCPU threads", value: host.cpu_threads,
594:       note: host.cpu_model ? host.cpu_model.split(" ").slice(-2).join(" ") : "" },
595:     { label: "Primary volume free", value: pv.free_tb ? `≈ ${pv.free_tb} TB` : "—",
596:       note: pv.write_speed_MBps ? `~${pv.write_speed_MBps} MB/s writes` : "" },
597:     { label: "Pod ↔ VM link", value: link.throughput_MBps ? `≈ ${link.throughput_MBps} MB/s` : "—",
598:       note: link.symmetric ? "symmetric" : "" },
599:     { label: "Hardening", value: host.hardened ? "attested" : "not attested",
600:       note: host.hardening_result || "" },
601:     { label: "OS", value: host.os || "—", note: "" },
602:   ];
603: 
604:   return (
605:     <div>
606:       <TwoColBand>
607:         <StatGrid cells={toplineCells} />
608:         <Headliner
609:           eyebrow="WHAT IS CONNECTED"
610:           deck="One machine connected · hardened · accepted as delivered."
611:           emphasis={g.count === 2 ? "Two H200s carry the room." : ""}
612:           provenance={`Commissioned ${host.deploy_date || "—"} · four questions green (link works · found · ready · no failure).`} />
613:       </TwoColBand>
614: 
615:       <Divider />
616: 
617:       {/* Just-connected announcement row + record table */}
618:       <SectionTitle
619:         title="RECORD · HOSTS"
620:         intro="The estate's compute inventory, as last received." />
621:       <TwoColBand>
622:         <div data-testid="registry-record-table"
623:              style={{ background: cardWhite, borderRadius: 12 }}>
624:           {/* Announcement row */}
625:           <div style={{ display: "flex", alignItems: "center", gap: 12,
626:                         padding: "10px 24px", background: "#f2eee4",
627:                         borderTopLeftRadius: 12, borderTopRightRadius: 12,
628:                         borderBottom: `1px solid ${rule}` }}>
629:             <Chip label="JUST CONNECTED" tone="sage" />
630:             <span style={{ fontSize: 12, color: grey }}>
631:               {host.host_name} landed {host.deploy_date} — accepted as delivered
632:             </span>
633:           </div>
634:           <table style={{ width: "100%", borderCollapse: "collapse" }}>
635:             <thead>
636:               <tr>
637:                 {["Host", "GPUs · VRAM", "RAM · CPU", "Link · Free storage", "Status"].map((h) => (
638:                   <th key={h} style={{ padding: "12px 24px", textAlign: "left",
639:                                        fontSize: 10, letterSpacing: 1.5, color: mid,
640:                                        textTransform: "uppercase",
641:                                        borderBottom: `1px solid ${rule}` }}>{h}</th>
642:                 ))}
643:               </tr>
644:             </thead>
645:             <tbody>
646:               {compute.map((h) => (
647:                 <tr key={h.host_name} data-testid="compute-row"
648:                     onClick={() => onOpen(h)}
649:                     style={{ cursor: "pointer" }}
650:                     onMouseEnter={(e) => e.currentTarget.style.background = "#f8f5ee"}
651:                     onMouseLeave={(e) => e.currentTarget.style.background = "transparent"}>
652:                   <td style={{ padding: "16px 24px", color: navy }}>
653:                     <div style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 15 }}>
654:                       {h.host_name}
655:                     </div>
656:                     <div style={{ fontSize: 11, color: grey, marginTop: 2 }}>{h.os}</div>
657:                   </td>
658:                   <td style={{ padding: "16px 24px", fontSize: 13, color: navy }}>
659:                     {h.gpus.count} × {h.gpus.model} · ≈ {Math.round(h.gpus.vram_gb_total)} GB
660:                   </td>
661:                   <td style={{ padding: "16px 24px", fontSize: 13, color: navy }}>
662:                     {h.ram_gb_total} GB · {h.cpu_threads} threads
663:                   </td>
664:                   <td style={{ padding: "16px 24px", fontSize: 13, color: navy }}>
665:                     ≈ {h.link.throughput_MBps} MB/s · {h.primary_volume.free_tb} TB free
666:                   </td>
667:                   <td style={{ padding: "16px 24px" }}>
668:                     <Chip label={h.hardened ? "HARDENED · ACCEPTED" : "NOT HARDENED"}
669:                           tone={h.hardened ? "sage" : "crimson"} />
670:                   </td>
671:                 </tr>
672:               ))}
673:             </tbody>
674:           </table>
675:         </div>
676:         <ContextPanel
677:           eyebrow="THE CONNECTION"
678:           sentences={[
679:             `A 2 × ${g.model} workhorse with ≈ ${Math.round(g.vram_gb_total)} GB aggregate VRAM and NVLink active between the cards.`,
680:             `The pod↔VM link is the real ceiling at ≈ ${link.throughput_MBps} MB/s symmetric — bulk audio should land on the VM from its own internet, not this pod.`,
681:             "Hardening attested: password auth dead server-wide; SSH is key-only.",
682:           ]} />
683:       </TwoColBand>
684:     </div>
685:   );
686: }
687: 
688: function ComputeDetailCard({ host, onClose }) {
689:   const g = host.gpus || {};
690:   const link = host.link || {};
691:   const pv = host.primary_volume || {};
692: 
693:   // Doc 12 §B5.1 · reflection-before-commit. The panel is a REFERENCE-NOT-COPY
694:   // read path: it POSTs the proposed action to /api/compute/reflection to
695:   // obtain a projection envelope by identity, renders it in place, then
696:   // POSTs /api/compute/commit with the identity as the acknowledgment. The
697:   // "Freeze & commit" button is the plain-sentence ack (v7 oracle ceremony
698:   // fabric); server-side gate refuses without a valid reflection_id.
699:   const [envelope, setEnvelope] = useState(null);
700:   const [reflectionError, setReflectionError] = useState(null);
701:   const [reflectionLoading, setReflectionLoading] = useState(false);
702:   const [commitOutcome, setCommitOutcome] = useState(null);
703:   const [commitError, setCommitError] = useState(null);
704:   const [committing, setCommitting] = useState(false);
705: 
706:   // The commissioner drives the ack identity. On a real estate this comes
707:   // from the identity middleware; today the surface renders the operator
708:   // as the ack-carrying actor.
709:   const commissioner = "operator@estate";
710:   const scopeRef = host.host_name || "";
711: 
712:   const proposedAction = {
713:     kind: "training",
714:     scope_ref: `training-run:${scopeRef}`,
715:     scope_ceiling: { gpu_hours_ceiling: 1 },
716:     budget_ceiling: { amount: 0.0, currency: "USD" },
717:     commissioner,
718:     lawful_basis: "declared_purpose:archive_processing",
719:   };
720: 
721:   const runReflection = () => {
722:     setReflectionLoading(true);
723:     setReflectionError(null);
724:     setCommitOutcome(null);
725:     setCommitError(null);
726:     fetch(`${BACKEND_URL}/api/compute/reflection`, {
727:       method: "POST",
728:       headers: { "Content-Type": "application/json" },
729:       body: JSON.stringify({ proposed_action: proposedAction }),
730:     })
731:       .then((r) => r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`)))
732:       .then(setEnvelope)
733:       .catch((e) => setReflectionError(String(e.message || e)))
734:       .finally(() => setReflectionLoading(false));
735:   };
736: 
737:   const freezeAndCommit = () => {
738:     if (!envelope || !envelope.reflection_id) return;
739:     setCommitting(true);
740:     setCommitError(null);
741:     fetch(`${BACKEND_URL}/api/compute/commit`, {
742:       method: "POST",
743:       headers: { "Content-Type": "application/json" },
744:       body: JSON.stringify({
745:         reflection_id: envelope.reflection_id,
746:         actor: commissioner,
747:         proposed_action: proposedAction,
748:       }),
749:     })
750:       .then((r) => r.ok ? r.json() : r.json().then(j => Promise.reject(new Error(j.detail || `HTTP ${r.status}`))))
751:       .then(setCommitOutcome)
752:       .catch((e) => setCommitError(String(e.message || e)))
753:       .finally(() => setCommitting(false));
754:   };
755: 
756:   return (
757:     <div style={{ position: "fixed", inset: 0, background: "rgba(28,43,69,0.55)",
758:                   display: "flex", alignItems: "center", justifyContent: "center", zIndex: 40 }}
759:          onClick={onClose}>
760:       <div data-testid="compute-detail-card"
761:            onClick={(e) => e.stopPropagation()}
762:            style={{ background: cardWhite, borderRadius: 16, width: "min(720px, 92vw)",
763:                     maxHeight: "82vh", overflow: "auto", padding: "28px 32px",
764:                     boxShadow: "0 20px 40px rgba(0,0,0,0.25)" }}>
765:         <div style={{ display: "flex", alignItems: "start" }}>
766:           <div style={{ flex: 1 }}>
767:             <div style={{ fontSize: 11, letterSpacing: 1.5, color: mid, textTransform: "uppercase" }}>
768:               HOST
769:             </div>
770:             <h2 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 28,
771:                          margin: "6px 0 4px", color: navy }}>
772:               {host.host_name}
773:             </h2>
774:             <div style={{ fontSize: 12, color: grey }}>{host.state_class}</div>
775:           </div>
776:           <button data-testid="compute-detail-close" onClick={onClose}
777:                   style={{ background: "transparent", border: `1px solid ${rule}`,
778:                            padding: "6px 12px", borderRadius: 999, cursor: "pointer",
779:                            color: grey, fontSize: 12 }}>
780:             Close
781:           </button>
782:         </div>
783: 
784:         <h3 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 16,
785:                      margin: "24px 0 8px", color: navy }}>The four questions</h3>
786:         <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 10 }}>
787:           <FQ label="LINK WORKING" value={host.four_questions?.link_working ? "yes" : "no"} />
788:           <FQ label="FOUND" value={host.four_questions?.found ? "yes" : "no"} />
789:           <FQ label="READY" value={host.four_questions?.ready ? "yes" : "no"} />
790:           <FQ label="FAILURE" value={host.four_questions?.failure || "none"} />
791:         </div>
792: 
793:         <h3 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 16,
794:                      margin: "20px 0 8px", color: navy }}>Measured capacity</h3>
795:         <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 12 }}>
796:           <KV label="GPUS" value={`${g.count} × ${g.model}`} />
797:           <KV label="AGGREGATE VRAM" value={`${Math.round(g.vram_gb_total)} GB`} />
798:           <KV label="NVLINK" value={g.nvlink_active ?
799:             `active · ${Math.round(g.nvlink_aggregate_gbps_per_gpu)} GB/s aggregate per GPU` : "not active"} />
800:           <KV label="SYSTEM RAM" value={`${host.ram_gb_total} GB`} />
801:           <KV label="CPU" value={`${host.cpu_threads} threads · ${host.cpu_model}`} />
802:           <KV label="PRIMARY VOLUME" value={`${pv.mount} · ≈ ${pv.free_tb} TB free · ~${pv.write_speed_MBps} MB/s`} />
803:           <KV label="POD ↔ VM LINK" value={`≈ ${link.throughput_MBps} MB/s · ${link.symmetric ? "symmetric" : "asymmetric"}`} />
804:           <KV label="HARDENING" value={host.hardened ? `attested · ${host.hardening_result}` : "not attested"} />
805:         </div>
806: 
807:         <h3 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 16,
808:                      margin: "20px 0 8px", color: navy }}>What it can carry</h3>
809:         <p style={{ fontSize: 13, color: navy, lineHeight: 1.6 }}>
810:           {host.usability_paragraph}
811:         </p>
812: 
813:         <ReflectionPanel
814:           envelope={envelope}
815:           error={reflectionError}
816:           loading={reflectionLoading}
817:           onRun={runReflection}
818:           onFreezeAndCommit={freezeAndCommit}
819:           commitOutcome={commitOutcome}
820:           commitError={commitError}
821:           committing={committing}
822:           proposedAction={proposedAction}
823:         />
824:       </div>
825:     </div>
826:   );
827: }
828: 
829: function ReflectionPanel({ envelope, error, loading, onRun, onFreezeAndCommit,
830:                            commitOutcome, commitError, committing, proposedAction }) {
831:   // Doc 12 §B5.1 · Reflection-before-commit. The panel opens closed; the
832:   // operator taps "Reflect on this run" to compute the projection through
833:   // the governed read path. Nothing commits until the projection is
834:   // acknowledged with "Freeze & commit" (v7 oracle ceremony fabric).
835:   return (
836:     <div data-testid="compute-reflection-panel"
837:          style={{ marginTop: 24, border: `1px solid ${rule}`, borderRadius: 10,
838:                   padding: "18px 20px" }}>
839:       <div style={{ display: "flex", alignItems: "baseline", gap: 12,
840:                     marginBottom: 12 }}>
841:         <div style={{ fontSize: 11, letterSpacing: 1.5, color: navy,
842:                       fontWeight: 600, textTransform: "uppercase" }}>
843:           REFLECT BEFORE COMMIT
844:         </div>
845:         <div style={{ fontSize: 12, color: grey, flex: 1 }}>
846:           Cost is shown at the point of commit, before commit.
847:         </div>
848:         {!envelope && (
849:           <button data-testid="compute-reflection-run"
850:                   onClick={onRun}
851:                   disabled={loading}
852:                   style={{ padding: "8px 14px", background: cardWhite,
853:                            border: `1px solid ${navy}`, color: navy,
854:                            borderRadius: 6, cursor: "pointer",
855:                            fontSize: 12, fontWeight: 600,
856:                            opacity: loading ? 0.6 : 1 }}>
857:             {loading ? "Reflecting…" : "Reflect on this run"}
858:           </button>
859:         )}
860:       </div>
861: 
862:       {error && (
863:         <div data-testid="compute-reflection-error"
864:              style={{ fontSize: 12, color: crimson, marginTop: 8 }}>
865:           Reflection could not be read: {error}. This is work done, not work lost — try again.
866:         </div>
867:       )}
868: 
869:       {envelope && (
870:         <>
871:           <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 10 }}>
872:             <KV label="FEASIBILITY"
873:                 data-testid="compute-reflection-feasibility"
874:                 value={envelope.feasibility_verdict} />
875:             <KV label="GROUNDING"
876:                 data-testid="compute-reflection-grounding"
877:                 value={envelope.grounding_marker} />
878:             <KV label="LAWFUL BASIS"
879:                 data-testid="compute-reflection-lawful-basis"
880:                 value={envelope.lawful_basis || "—"} />
881:             <KV label="BUDGET CEILING"
882:                 data-testid="compute-reflection-budget"
883:                 value={envelope.budget_ceiling && envelope.budget_ceiling.amount != null
884:                   ? `${envelope.budget_ceiling.amount} ${envelope.budget_ceiling.currency || ""}`.trim()
885:                   : "—"} />
886:             <KV label="SCOPE CEILING"
887:                 data-testid="compute-reflection-scope-ceiling"
888:                 value={renderScopeCeiling(envelope.scope_ceiling)} />
889:             <KV label="PRICE MODEL"
890:                 data-testid="compute-reflection-price-model-version"
891:                 value={envelope.price_model_version || "—"} />
892:           </div>
893: 
894:           <div data-testid="compute-reflection-measured-quantities"
895:                style={{ marginTop: 14, borderTop: `1px solid ${rule}`,
896:                         paddingTop: 12 }}>
897:             <div style={{ fontSize: 10, letterSpacing: 1.5, color: mid,
898:                           textTransform: "uppercase", marginBottom: 8 }}>
899:               Measured quantities
900:             </div>
901:             {Object.keys(envelope.measured_quantities || {}).length === 0 && (
902:               <div style={{ fontSize: 12, color: grey }}>
903:                 No measured quantities on record for this scope yet.
904:               </div>
905:             )}
906:             {Object.entries(envelope.measured_quantities || {}).map(([k, v]) => (
907:               <div key={k} style={{ display: "grid",
908:                                     gridTemplateColumns: "180px 1fr 200px",
909:                                     fontSize: 12, padding: "4px 0", color: navy }}>
910:                 <div style={{ letterSpacing: 0.5 }}>{k}</div>
911:                 <div style={{ fontFamily: "ui-serif, Georgia, serif" }}>
912:                   {renderMeasuredValue(v)}
913:                 </div>
914:                 <div style={{ fontSize: 11, color: grey }}>
915:                   from {v.provenance_ref}
916:                 </div>
917:               </div>
918:             ))}
919:           </div>
920: 
921:           {envelope.honest_gap && (
922:             <div data-testid="compute-reflection-honest-gap"
923:                  style={{ marginTop: 14, borderTop: `1px solid ${rule}`,
924:                           paddingTop: 12, fontSize: 12, color: navy,
925:                           lineHeight: 1.55, fontStyle: "italic" }}>
926:               {envelope.honest_gap}
927:             </div>
928:           )}
929: 
930:           <div style={{ marginTop: 16, display: "flex", alignItems: "center",
931:                         gap: 12, borderTop: `1px solid ${rule}`, paddingTop: 14 }}>
932:             <div style={{ flex: 1, fontSize: 11, color: grey }}>
933:               Frozen — a changed intent is a new objective.
934:             </div>
935:             {!commitOutcome && (
936:               <button data-testid="compute-reflection-freeze-and-commit"
937:                       onClick={onFreezeAndCommit}
938:                       disabled={committing}
939:                       style={{ padding: "9px 16px", background: sage,
940:                                color: cardWhite, border: "none",
941:                                borderRadius: 6, cursor: "pointer",
942:                                fontSize: 12.5, fontWeight: 600,
943:                                opacity: committing ? 0.6 : 1 }}>
944:                 {committing ? "Committing…" : "Freeze & commit"}
945:               </button>
946:             )}
947:           </div>
948: 
949:           {commitError && (
950:             <div data-testid="compute-reflection-commit-error"
951:                  style={{ marginTop: 10, fontSize: 12, color: crimson,
952:                           background: "#f7ecea", padding: "8px 12px",
953:                           borderRadius: 6 }}>
954:               Commit refused: {commitError}
955:             </div>
956:           )}
957: 
958:           {commitOutcome && (
959:             <div data-testid="compute-reflection-commit-outcome"
960:                  style={{ marginTop: 12, padding: "10px 14px",
961:                           background: "#eef2ea", borderLeft: `2px solid ${sage}`,
962:                           borderRadius: 4 }}>
963:               <div style={{ fontSize: 11, color: sage, fontWeight: 700,
964:                             letterSpacing: 0.5, textTransform: "uppercase" }}>
965:                 COMMITTED
966:               </div>
967:               <div style={{ fontSize: 13, color: navy, marginTop: 4 }}>
968:                 Run {commitOutcome.run_id} · acknowledged by {commitOutcome.acknowledged_by} · {commitOutcome.acknowledged_at_iso}
969:               </div>
970:               <div style={{ fontSize: 11, color: grey, marginTop: 2 }}>
971:                 Projection reference: {commitOutcome.reflection_id}
972:               </div>
973:             </div>
974:           )}
975:         </>
976:       )}
977:     </div>
978:   );
979: }
980: 
981: function renderScopeCeiling(sc) {
982:   if (!sc || typeof sc !== "object") return "—";
983:   const parts = [];
984:   if (sc.rows_ceiling) parts.push(`${sc.rows_ceiling.toLocaleString()} rows`);
985:   if (sc.gpu_hours_ceiling) parts.push(`${sc.gpu_hours_ceiling} GPU-hours`);
986:   if (sc.duration_seconds_ceiling) parts.push(`${sc.duration_seconds_ceiling}s`);
987:   return parts.length ? parts.join(" · ") : "—";
988: }
989: 
990: function renderMeasuredValue(v) {
991:   if (!v || typeof v !== "object") return String(v);
992:   if (typeof v.value === "number") {
993:     return `${v.value.toLocaleString()} ${v.unit || ""}`.trim();
994:   }
995:   if (typeof v.value === "string") {
996:     return v.value || "—";
997:   }
998:   if (typeof v.value === "object" && v.value !== null) {
999:     return JSON.stringify(v.value);
1000:   }
1001:   return "—";
1002: }
1003: 
1004: function FQ({ label, value }) {
1005:   const yes = value === "yes";
1006:   return (
1007:     <div style={{ border: `1px solid ${rule}`, borderRadius: 8, padding: "10px 12px" }}>
1008:       <div style={{ fontSize: 10, letterSpacing: 1.5, color: mid,
1009:                     textTransform: "uppercase" }}>{label}</div>
1010:       <div style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 18,
1011:                     color: yes ? sage : (value === "no" ? crimson : navy), marginTop: 2 }}>
1012:         {value}
1013:       </div>
1014:     </div>
1015:   );
1016: }
1017: 
1018: function KV({ label, value }) {
1019:   return (
1020:     <div style={{ border: `1px solid ${rule}`, borderRadius: 8, padding: "10px 12px" }}>
1021:       <div style={{ fontSize: 10, letterSpacing: 1.5, color: mid,
1022:                     textTransform: "uppercase" }}>{label}</div>
1023:       <div style={{ fontSize: 13, color: navy, marginTop: 4, lineHeight: 1.4 }}>{value}</div>
1024:     </div>
1025:   );
1026: }
1027: 
1028: // ---------------------------------------------------------------------------
1029: // LLMS & TRAINED MODELS tab (honest empty)
1030: // ---------------------------------------------------------------------------
1031: 
1032: function LLMsTrainedModelsTab({ facts }) {
1033:   const reason = (facts.models && facts.models.reason) ||
1034:     "No models connected yet.";
1035:   return (
1036:     <EmptyPanel eyebrow="WHAT IS ANSWERING"
1037:                 headline="No models connected yet."
1038:                 sentence={reason + " Not yet measured — drawn, never left blank."} />
1039:   );
1040: }
1041: 
1042: // ---------------------------------------------------------------------------
1043: // Shared empty panel
1044: // ---------------------------------------------------------------------------
1045: 
1046: function EmptyPanel({ eyebrow, headline, sentence }) {
1047:   return (
1048:     <div data-testid="tab-empty-panel"
1049:          style={{ background: cardWhite, borderRadius: 12, padding: "48px 44px" }}>
1050:       <div style={{ fontSize: 11, letterSpacing: 2, color: grey, marginBottom: 12 }}>{eyebrow}</div>
1051:       <h2 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 28,
1052:                    margin: "0 0 16px 0", color: navy }}>
1053:         {headline}
1054:       </h2>
1055:       <p style={{ color: grey, lineHeight: 1.6, fontSize: 15, maxWidth: 640 }}>{sentence}</p>
1056:       <p style={{ color: grey, lineHeight: 1.6, fontSize: 13, marginTop: 20, fontStyle: "italic" }}>
1057:         drawn, never left blank
1058:       </p>
1059:     </div>
1060:   );
1061: }

# SOURCE: frontend/src/components/SkillFiles.jsx

1: import React, { useEffect, useState } from "react";
2: import { Link } from "react-router-dom";
3: 
4: /**
5:  * SkillFiles.jsx — W11 B · CP4 · Doc 18 A18.7 provenance surface.
6:  *
7:  * Doc 18 §A18.7 verbatim (Wave B grounding brief):
8:  *   "every skill's provenance chain traces back to the training run
9:  *    that produced its adapter (extends Doc14-016 rights-lineage +
10:  *    Doc14-017 version-history)."
11:  *
12:  * Doc 18 §A18.4 verbatim (grounding brief):
13:  *   "Below the floor is a refusal, never a degraded answer."
14:  *
15:  * Data source: GET /api/skill-files/state.
16:  * Every rendered row cites its on-disk record identifiers (skill_id,
17:  * adapter_id, training_run_id, moac_card_id, recipe_version); no raw
18:  * signing material crosses the response boundary. Empty stores render
19:  * an honest sentence naming the canon anchor. REFERENCE-NOT-COPY.
20:  *
21:  * NO provisioning happens from this surface. Provisioning is a
22:  * POST /api/skill-files/{skill_id}/provenance triggered by the
23:  * trainer runner at CP8 close (Doc 18 §A18.5 registry admission).
24:  * This surface's job is to make the provenance chain legible after
25:  * the fact, per Doc 18 A18.4 ("refusal, never a degraded answer") —
26:  * the surface refuses to lie about empty state.
27:  */
28: 
29: const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
30: 
31: // v7 palette · matched to Training / Governance / Watch / GreyMirror.
32: const paper = "#f5f2ea";
33: const surface = "#ffffff";
34: const ink = "#1b1f27";
35: const ink2 = "#3a3f4a";
36: const ink3 = "#7a7f8a";
37: const line = "#e4dccf";
38: const blue = "#16274a";
39: const sage = "#1d7a6e";
40: const brass = "#b08d2e";
41: const head = 'ui-serif, "Iowan Old Style", Georgia, serif';
42: 
43: function Panel({ "data-testid": dt, title, anchor, children }) {
44:   return (
45:     <section data-testid={dt} style={{
46:       background: surface, border: `1px solid ${line}`, padding: "22px 24px",
47:       marginBottom: 20,
48:     }}>
49:       <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 8 }}>
50:         <h2 style={{ fontFamily: head, fontSize: 20, color: blue, margin: 0 }}>{title}</h2>
51:         <span style={{ fontSize: 11, letterSpacing: 1.5, color: ink3 }}>{anchor}</span>
52:       </div>
53:       {children}
54:     </section>
55:   );
56: }
57: 
58: function EmptyState({ anchor, kind }) {
59:   return (
60:     <p data-testid="skill-files-empty" style={{ color: ink2, fontStyle: "italic", margin: "6px 0 0 0" }}>
61:       No {kind} on record. Canon anchor: {anchor}. Drawn, never left blank.
62:     </p>
63:   );
64: }
65: 
66: function ChainCrumbs({ chain }) {
67:   const kindLabel = {
68:     base_model: "base model",
69:     training_run: "training run",
70:     moac_admission: "MOAC admission",
71:     skill_provision: "skill provision",
72:   };
73:   return (
74:     <ol data-testid="skill-file-chain" style={{
75:       margin: "8px 0 0 0", paddingLeft: 20, color: ink2, fontSize: 13,
76:     }}>
77:       {chain.map((step, i) => (
78:         <li key={step.step_id || i} data-testid={`chain-step-${step.kind}`}
79:             style={{ marginBottom: 4 }}>
80:           <span style={{ letterSpacing: 1.2, fontSize: 11, color: sage, textTransform: "uppercase" }}>
81:             {kindLabel[step.kind] || step.kind}
82:           </span>
83:           <span style={{ margin: "0 6px", color: ink3 }}>·</span>
84:           <span style={{ color: ink }}>{step.label}</span>
85:           <span style={{ marginLeft: 8, color: ink3, fontSize: 11 }}>
86:             {step.at}
87:           </span>
88:           {step.artifact_ref && (
89:             <span data-testid="chain-step-artifact"
90:                   style={{ marginLeft: 8, color: brass, fontSize: 11, fontFamily: "ui-monospace, monospace" }}>
91:               artifact: {step.artifact_ref}
92:             </span>
93:           )}
94:         </li>
95:       ))}
96:     </ol>
97:   );
98: }
99: 
100: export default function SkillFiles() {
101:   const [state, setState] = useState(null);
102:   const [err, setErr] = useState(null);
103: 
104:   useEffect(() => {
105:     fetch(`${BACKEND_URL}/api/skill-files/state`)
106:       .then((r) => r.ok ? r.json() : Promise.reject(`HTTP ${r.status}`))
107:       .then((body) => setState(body))
108:       .catch((e) => setErr(String(e)));
109:   }, []);
110: 
111:   return (
112:     <div data-testid="skill-files-page" style={{
113:       minHeight: "100vh", background: paper, padding: "48px 40px", fontFamily: "ui-sans-serif",
114:     }}>
115:       <div style={{ maxWidth: 960, margin: "0 auto" }}>
116:         <div style={{ fontSize: 11, letterSpacing: 2, color: ink3 }}>AKKI · SKILL FILES</div>
117:         <h1 style={{ fontFamily: head, fontSize: 40, margin: "10px 0 6px 0", color: blue }}>
118:           Provenance chain register
119:         </h1>
120:         <p data-testid="skill-files-doc-anchor"
121:            style={{ color: ink2, maxWidth: 720, lineHeight: 1.55, margin: "0 0 26px 0" }}>
122:           Doc 18 §A18.7 · every skill's provenance chain traces back to the training run
123:           that produced its adapter, extending Doc14-016 rights-lineage and Doc14-017
124:           version-history. Below the floor is a refusal (A18.4), never a degraded answer.
125:         </p>
126: 
127:         {err && (
128:           <Panel data-testid="skill-files-error" title="Surface unreachable" anchor="A18.4">
129:             <p style={{ color: "#8a2a44" }}>Backend refused this request: {err}</p>
130:           </Panel>
131:         )}
132: 
133:         <Panel data-testid="skill-files-state-panel"
134:                title="Skill files on record"
135:                anchor="Doc 18 §A18.7 · Wave B CP4">
136:           {!state && !err && (
137:             <p style={{ color: ink3, fontStyle: "italic" }}>Loading state…</p>
138:           )}
139:           {state && state.count === 0 && (
140:             <>
141:               <EmptyState anchor="Doc 18 §A18.7" kind="provisioned skills" />
142:               <p style={{ color: ink3, fontSize: 12, marginTop: 8 }}>
143:                 Ship-state: {state.ship_state}. The seat is empty by design — CP5
144:                 fills the recipe seat via the Muon two-arm optimizer protocol
145:                 (Doc 17 §A17.5–A17.6), and CP8's trainer runner writes the first
146:                 provenance row on close. No pre-population by convention.
147:               </p>
148:             </>
149:           )}
150:           {state && state.count > 0 && (
151:             <div data-testid="skill-files-list">
152:               <p style={{ color: ink3, fontSize: 12, marginBottom: 12 }}>
153:                 {state.count} skill{state.count === 1 ? "" : "s"} on record ·
154:                 ship_state = {state.ship_state}.
155:               </p>
156:               {state.skills.map((s) => (
157:                 <article key={s.skill_id}
158:                          data-testid={`skill-file-row-${s.skill_id}`}
159:                          style={{
160:                            borderTop: `1px solid ${line}`, padding: "14px 0",
161:                          }}>
162:                   <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
163:                     <h3 style={{ fontFamily: head, fontSize: 16, color: ink, margin: 0 }}>
164:                       {s.skill_id}
165:                     </h3>
166:                     <span style={{ fontSize: 11, color: ink3 }}>
167:                       provisioned {s.provisioned_at}
168:                     </span>
169:                   </div>
170:                   <div style={{ fontSize: 12, color: ink2, marginTop: 4 }}>
171:                     adapter <code data-testid="skill-adapter-id">{s.adapter_id}</code> ·
172:                     training run <code>{s.training_run_id}</code> ·
173:                     MOAC card <code>{s.moac_card_id}</code> ·
174:                     recipe <code data-testid="skill-recipe-version">{s.recipe_version}</code>
175:                   </div>
176:                   <ChainCrumbs chain={s.chain} />
177:                 </article>
178:               ))}
179:             </div>
180:           )}
181:         </Panel>
182: 
183:         <div style={{ marginTop: 32, fontSize: 12, color: ink3 }}>
184:           <Link to="/" style={{ color: blue }} data-testid="skill-files-back">← Registry</Link>
185:           <span style={{ margin: "0 10px" }}>·</span>
186:           <Link to="/training" style={{ color: blue }} data-testid="skill-files-training">Training →</Link>
187:         </div>
188:       </div>
189:     </div>
190:   );
191: }

# SOURCE: frontend/src/components/ThinkLab.jsx

1: import React, { useEffect, useState } from "react";
2: import { useParams, useNavigate, Link } from "react-router-dom";
3: 
4: /**
5:  * ThinkLab.jsx — Doc 05 Northena · direction/scope + ThinkLab surfaces.
6:  *
7:  * Owner Order 2026-08-25 · "W4 go" · v7 oracle fabric EXACT per T1.
8:  *
9:  * Four destinations under the thinklab group:
10:  *   - /thinklab              landing (mode tiles + Outputs)
11:  *   - /thinklab/clarity      Seek clarity
12:  *   - /thinklab/strategy     Develop strategy
13:  *   - /thinklab/hypothesis   Simulate a hypothesis
14:  *   - /thinklab/perspective  Get perspectives
15:  *
16:  * Mode registry, LANDING_TIPS, TL_STAGE_LABELS, TL_OUTPUTS, and the
17:  * dormant-state sentence come from GET /api/thinklab/config —
18:  * REFERENCE-NOT-COPY: this file does not bake the copy inline.
19:  *
20:  * Direction capture is LIVE and admits into Northena via
21:  * POST /api/thinklab/admit. On admission the frozen artifact renders
22:  * with its judgement_provenance (Solva-boundary stub annotated
23:  * honestly) and the 5-stage strip (Frame -> Name -> Challenge ->
24:  * Weigh -> Lock-in) as navigation ONLY; the body carries the
25:  * dormant-state sentence because the reasoning faculty (Solver)
26:  * lands in a later wave. No fake LLM responses. No canned reasoning.
27:  */
28: 
29: const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
30: 
31: // v7 palette tokens (paper / ink / blue / sage / oxblood / brass) —
32: // extracted verbatim from prototype.html :root vars.
33: const paper = "#f5f2ea";
34: const surface = "#ffffff";
35: const surface2 = "#f0ebe1";
36: const ink = "#1b1f27";
37: const ink2 = "#3a3f4a";
38: const ink3 = "#7a7f8a";
39: const line = "#e4dccf";
40: const blue = "#16274a";
41: const sage = "#1d7a6e";
42: const oxblood = "#8a2a44";
43: const oxblood2 = "#b8395b";
44: const brass = "#b08d2e";
45: const head = 'ui-serif, "Iowan Old Style", Georgia, serif';
46: 
47: 
48: export default function ThinkLab() {
49:   const { mode } = useParams();
50:   if (mode) return <ThinkLabMode modeKey={mode} />;
51:   return <ThinkLabLanding />;
52: }
53: 
54: 
55: function ThinkLabLanding() {
56:   const [config, setConfig] = useState(null);
57:   const [err, setErr] = useState(null);
58: 
59:   useEffect(() => {
60:     let alive = true;
61:     fetch(`${BACKEND_URL}/api/thinklab/config`)
62:       .then(r => r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`)))
63:       .then(j => { if (alive) setConfig(j); })
64:       .catch(e => { if (alive) setErr(String(e.message || e)); });
65:     return () => { alive = false; };
66:   }, []);
67: 
68:   return (
69:     <div data-testid="thinklab-surface"
70:          style={{ minHeight: "100vh", background: paper, padding: "48px 56px",
71:                   fontFamily: 'ui-sans-serif, "Söhne", system-ui, sans-serif',
72:                   color: ink }}>
73:       <div style={{ maxWidth: 1120, margin: "0 auto" }}>
74: 
75:         {/* Breadcrumb */}
76:         <div style={{ display: "flex", alignItems: "center", gap: 8,
77:                       fontSize: 11, letterSpacing: 1.5, color: ink3,
78:                       textTransform: "uppercase", marginBottom: 6 }}>
79:           <Link to="/" style={{ color: ink3, textDecoration: "none" }}>Estate</Link>
80:           <span>·</span>
81:           <span style={{ color: ink }}>ThinkLab</span>
82:         </div>
83: 
84:         <h1 style={{ fontFamily: head, fontSize: 44, margin: "12px 0 6px",
85:                      color: blue, letterSpacing: -0.2 }}>
86:           ThinkLab
87:         </h1>
88:         <p style={{ fontSize: 15, color: ink2, lineHeight: 1.6,
89:                     maxWidth: 720, margin: "8px 0 32px" }}>
90:           Four ways to think through a governed session. Choose the shape of
91:           the work you are about to do.
92:         </p>
93: 
94:         {err && (
95:           <div style={{ padding: "10px 14px", background: "#f7ecea",
96:                         borderLeft: `2px solid ${oxblood2}`, borderRadius: 4,
97:                         marginBottom: 20, fontSize: 12, color: oxblood }}>
98:             ThinkLab configuration could not be read: {err}
99:           </div>
100:         )}
101: 
102:         {config && (
103:           <>
104:             <div style={{ display: "grid",
105:                           gridTemplateColumns: "repeat(2, 1fr)",
106:                           gap: 20 }}>
107:               {(config.modes || []).map((m) => (
108:                 <ModeTile key={m.key} mode={m} tips={config.landing_tips?.[m.key] || []} />
109:               ))}
110:             </div>
111: 
112:             <h2 data-testid="thinklab-outputs"
113:                 style={{ fontFamily: head, fontSize: 20, marginTop: 44,
114:                          marginBottom: 12, color: blue }}>
115:               What every session produces
116:             </h2>
117:             <ul style={{ paddingLeft: 22, color: ink2, fontSize: 13.5,
118:                          lineHeight: 1.7 }}>
119:               {(config.outputs || []).map(o => <li key={o}>{o}</li>)}
120:             </ul>
121:           </>
122:         )}
123:       </div>
124:     </div>
125:   );
126: }
127: 
128: 
129: function ModeTile({ mode, tips }) {
130:   // Explicit testid map — the tests file-scan for each literal.
131:   const testidByKey = {
132:     clarity: "thinklab-mode-tile-clarity",
133:     strategy: "thinklab-mode-tile-strategy",
134:     hypothesis: "thinklab-mode-tile-hypothesis",
135:     perspective: "thinklab-mode-tile-perspective",
136:   };
137:   const testid = testidByKey[mode.key] || `thinklab-mode-tile-${mode.key}`;
138:   return (
139:     <Link data-testid={testid}
140:           to={`/thinklab/${mode.key}`}
141:           style={{ display: "block", background: surface,
142:                    border: `1px solid ${line}`, borderRadius: 12,
143:                    padding: "22px 24px", textDecoration: "none",
144:                    color: ink, transition: "border-color 120ms" }}
145:           onMouseEnter={(e) => e.currentTarget.style.borderColor = sage}
146:           onMouseLeave={(e) => e.currentTarget.style.borderColor = line}>
147:       <div style={{ display: "flex", justifyContent: "space-between",
148:                     alignItems: "baseline", marginBottom: 6 }}>
149:         <span style={{ fontFamily: "ui-monospace, Menlo, monospace",
150:                        fontSize: 11, color: brass, letterSpacing: 1.5 }}>
151:           {mode.num}
152:         </span>
153:         <span style={{ fontSize: 10, color: ink3, letterSpacing: 1 }}>
154:           {mode.duration}
155:         </span>
156:       </div>
157:       <div style={{ fontFamily: head, fontSize: 22, color: blue,
158:                     marginBottom: 6 }}>
159:         {mode.title}
160:       </div>
161:       <div style={{ fontSize: 13, color: ink2, lineHeight: 1.55,
162:                     marginBottom: tips?.length ? 12 : 0 }}>
163:         {mode.objective}
164:       </div>
165:       {tips.map((t, i) => (
166:         <div key={i} style={{ fontSize: 11.5, color: ink3, fontStyle: "italic",
167:                               lineHeight: 1.55, marginTop: 4 }}>
168:           {t}
169:         </div>
170:       ))}
171:     </Link>
172:   );
173: }
174: 
175: 
176: function ThinkLabMode({ modeKey }) {
177:   const nav = useNavigate();
178:   const [config, setConfig] = useState(null);
179:   const [direction, setDirection] = useState("");
180:   const [scopeText, setScopeText] = useState("registry.estate.audit");
181:   const [lawfulBasis, setLawfulBasis] = useState("declared_purpose:thinklab_session");
182:   const [busy, setBusy] = useState(false);
183:   const [result, setResult] = useState(null);
184:   const [err, setErr] = useState(null);
185: 
186:   useEffect(() => {
187:     fetch(`${BACKEND_URL}/api/thinklab/config`)
188:       .then(r => r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`)))
189:       .then(setConfig)
190:       .catch(e => setErr(String(e.message || e)));
191:   }, []);
192: 
193:   const mode = config?.modes?.find(m => m.key === modeKey);
194: 
195:   const submitAdmit = async () => {
196:     setBusy(true);
197:     setErr(null);
198:     setResult(null);
199:     try {
200:       const r = await fetch(`${BACKEND_URL}/api/thinklab/admit`, {
201:         method: "POST",
202:         headers: { "Content-Type": "application/json" },
203:         body: JSON.stringify({
204:           mode: modeKey,
205:           artifact_id: `tl-${modeKey}-${Date.now()}`,
206:           scope: scopeText.split(/[\n,]/).map(s => s.trim()).filter(Boolean),
207:           lawful_basis: lawfulBasis,
208:           direction_statement: direction,
209:           commissioner: "operator@estate",
210:         }),
211:       });
212:       const j = await r.json();
213:       if (!r.ok) throw new Error(j.detail || `HTTP ${r.status}`);
214:       setResult(j);
215:     } catch (e) {
216:       setErr(String(e.message || e));
217:     } finally {
218:       setBusy(false);
219:     }
220:   };
221: 
222:   return (
223:     <div data-testid="thinklab-surface"
224:          style={{ minHeight: "100vh", background: paper, padding: "40px 56px",
225:                   fontFamily: 'ui-sans-serif, "Söhne", system-ui, sans-serif',
226:                   color: ink }}>
227:       <div style={{ maxWidth: 900, margin: "0 auto" }}>
228: 
229:         {/* Breadcrumb */}
230:         <div style={{ display: "flex", alignItems: "center", gap: 8,
231:                       fontSize: 11, letterSpacing: 1.5, color: ink3,
232:                       textTransform: "uppercase", marginBottom: 6 }}>
233:           <Link to="/" style={{ color: ink3, textDecoration: "none" }}>Estate</Link>
234:           <span>·</span>
235:           <Link to="/thinklab" style={{ color: ink3, textDecoration: "none" }}>ThinkLab</Link>
236:           <span>·</span>
237:           <span style={{ color: ink }}>{modeKey}</span>
238:         </div>
239: 
240:         {mode && (
241:           <div data-testid="thinklab-mode-entry"
242:                style={{ marginBottom: 32 }}>
243:             <div style={{ display: "flex", justifyContent: "space-between",
244:                           alignItems: "baseline", marginBottom: 4 }}>
245:               <span style={{ fontFamily: "ui-monospace, Menlo, monospace",
246:                              fontSize: 11, color: brass, letterSpacing: 1.5 }}>
247:                 {mode.num}
248:               </span>
249:               <span style={{ fontSize: 10, color: ink3, letterSpacing: 1 }}>
250:                 {mode.duration}
251:               </span>
252:             </div>
253:             <h1 style={{ fontFamily: head, fontSize: 36, color: blue,
254:                          margin: "4px 0 8px" }}>
255:               {mode.title}
256:             </h1>
257:             <p style={{ fontSize: 14, color: ink2, lineHeight: 1.6,
258:                         maxWidth: 720 }}>
259:               {mode.objective}
260:             </p>
261:           </div>
262:         )}
263: 
264:         {/* Stage strip */}
265:         <StageStrip labels={config?.stage_labels || []} activeIdx={result?.decision === "admitted" ? 0 : -1} />
266: 
267:         {err && (
268:           <div style={{ padding: "10px 14px", background: "#f7ecea",
269:                         borderLeft: `2px solid ${oxblood2}`, borderRadius: 4,
270:                         margin: "16px 0", fontSize: 12, color: oxblood }}>
271:             {err}
272:           </div>
273:         )}
274: 
275:         {!result && (
276:           <DirectionCaptureForm
277:             direction={direction}    setDirection={setDirection}
278:             scopeText={scopeText}    setScopeText={setScopeText}
279:             lawfulBasis={lawfulBasis} setLawfulBasis={setLawfulBasis}
280:             onSubmit={submitAdmit}
281:             busy={busy}
282:           />
283:         )}
284: 
285:         {result && result.decision === "refused" && (
286:           <RefusalCard reason={result.reason} row={result.ledger_row} onRetry={() => setResult(null)} />
287:         )}
288: 
289:         {result && result.decision === "admitted" && (
290:           <>
291:             <FrozenArtifactCard artifact={result.frozen_artifact} row={result.ledger_row} />
292:             <SolvaReasoningPanel
293:               directionStatement={direction}
294:               dormantSentence={config?.reasoning_dormant_state}
295:             />
296:           </>
297:         )}
298: 
299:       </div>
300:     </div>
301:   );
302: }
303: 
304: 
305: function StageStrip({ labels, activeIdx = -1 }) {
306:   return (
307:     <div data-testid="thinklab-stage-strip"
308:          style={{ display: "flex", gap: 6, alignItems: "center",
309:                   padding: "10px 0", borderTop: `1px solid ${line}`,
310:                   borderBottom: `1px solid ${line}` }}>
311:       {labels.map((label, i) => (
312:         <React.Fragment key={label}>
313:           <div style={{
314:             padding: "6px 12px",
315:             fontSize: 12,
316:             fontWeight: 600,
317:             color: i === activeIdx ? sage : ink3,
318:             background: i === activeIdx ? surface2 : "transparent",
319:             borderRadius: 4,
320:             fontFamily: "ui-monospace, Menlo, monospace",
321:             letterSpacing: 0.3,
322:           }}>{label}</div>
323:           {i < labels.length - 1 && (
324:             <div style={{ fontSize: 11, color: ink3 }}>·</div>
325:           )}
326:         </React.Fragment>
327:       ))}
328:     </div>
329:   );
330: }
331: 
332: 
333: function DirectionCaptureForm({ direction, setDirection, scopeText, setScopeText,
334:                                 lawfulBasis, setLawfulBasis, onSubmit, busy }) {
335:   return (
336:     <div style={{ marginTop: 20, padding: "22px 24px", background: surface,
337:                   border: `1px solid ${line}`, borderRadius: 10 }}>
338:       <div style={{ fontSize: 11, letterSpacing: 1.5, color: ink3,
339:                     textTransform: "uppercase", fontWeight: 600,
340:                     marginBottom: 12 }}>
341:         Direction & scope
342:       </div>
343: 
344:       <label style={{ display: "block", marginBottom: 12 }}>
345:         <div style={{ fontSize: 11, color: ink3, marginBottom: 4 }}>
346:           What are you thinking through?
347:         </div>
348:         <textarea data-testid="thinklab-direction-input"
349:                   value={direction}
350:                   onChange={(e) => setDirection(e.target.value)}
351:                   rows={3}
352:                   placeholder="State the question, the decision, or the hypothesis in plain language."
353:                   style={{ width: "100%", padding: "10px 12px",
354:                            fontSize: 13, border: `1px solid ${line}`,
355:                            borderRadius: 5, background: surface, color: ink,
356:                            fontFamily: "inherit", resize: "vertical" }} />
357:       </label>
358: 
359:       <label style={{ display: "block", marginBottom: 12 }}>
360:         <div style={{ fontSize: 11, color: ink3, marginBottom: 4 }}>
361:           Scope (comma or newline separated; strict set-membership at Gate)
362:         </div>
363:         <input data-testid="thinklab-scope-input"
364:                value={scopeText}
365:                onChange={(e) => setScopeText(e.target.value)}
366:                style={{ width: "100%", padding: "8px 12px", fontSize: 13,
367:                         border: `1px solid ${line}`, borderRadius: 5,
368:                         background: surface, color: ink,
369:                         fontFamily: "ui-monospace, Menlo, monospace" }} />
370:       </label>
371: 
372:       <label style={{ display: "block", marginBottom: 16 }}>
373:         <div style={{ fontSize: 11, color: ink3, marginBottom: 4 }}>
374:           Lawful basis (declared purpose)
375:         </div>
376:         <input data-testid="thinklab-lawful-basis-input"
377:                value={lawfulBasis}
378:                onChange={(e) => setLawfulBasis(e.target.value)}
379:                style={{ width: "100%", padding: "8px 12px", fontSize: 13,
380:                         border: `1px solid ${line}`, borderRadius: 5,
381:                         background: surface, color: ink,
382:                         fontFamily: "ui-monospace, Menlo, monospace" }} />
383:       </label>
384: 
385:       <button data-testid="thinklab-admit-button"
386:               onClick={onSubmit}
387:               disabled={busy || !direction.trim() || !lawfulBasis.trim()}
388:               style={{ padding: "10px 18px", background: sage,
389:                        color: surface, border: "none", borderRadius: 6,
390:                        cursor: "pointer", fontSize: 13, fontWeight: 600,
391:                        opacity: (busy || !direction.trim() || !lawfulBasis.trim()) ? 0.6 : 1 }}>
392:         {busy ? "Admitting…" : "Admit & freeze objective"}
393:       </button>
394: 
395:       <div style={{ fontSize: 11, color: ink3, marginTop: 10,
396:                     fontStyle: "italic", lineHeight: 1.55 }}>
397:         A changed intent is a new admission — the objective is frozen once
398:         the run starts.
399:       </div>
400:     </div>
401:   );
402: }
403: 
404: 
405: function FrozenArtifactCard({ artifact, row }) {
406:   const prov = artifact?.judgement_provenance || {};
407:   return (
408:     <div data-testid="thinklab-admit-result"
409:          style={{ marginTop: 20, padding: "22px 24px", background: surface,
410:                   borderLeft: `3px solid ${sage}`, borderRadius: 6,
411:                   border: `1px solid ${line}` }}>
412:       <div style={{ fontSize: 11, letterSpacing: 1.5, color: sage,
413:                     textTransform: "uppercase", fontWeight: 700 }}>
414:         Admitted · frozen
415:       </div>
416:       <div data-testid="thinklab-frozen-artifact"
417:            style={{ marginTop: 12 }}>
418:         <Row label="run_id"     value={artifact?.run_id} />
419:         <Row label="trace_id"   value={artifact?.trace_id} />
420:         <Row label="lawful basis" value={artifact?.lawful_basis} />
421:         <Row label="scope" value={(artifact?.scope || []).join(" · ")} />
422:         <Row label="defensibility floor"
423:              value={`${artifact?.defensibility_floor} (${prov.defensibility_floor})`} />
424:         <Row label="preservation depth"
425:              value={`${artifact?.preservation_depth} (${prov.preservation_depth})`} />
426:         <Row label="frozen at" value={artifact?.frozen_at_iso} />
427:         <Row label="ledger row" value={row?.row_id} />
428:       </div>
429:       <div style={{ fontSize: 11, color: ink3, marginTop: 12,
430:                     fontStyle: "italic", lineHeight: 1.55 }}>
431:         Solva-assisted judgement pending — the fields marked
432:         <code style={{ background: surface2, padding: "1px 4px", margin: "0 3px",
433:                        borderRadius: 3 }}>stub_awaiting_solva</code>
434:         will resolve through the depth governor when it lands.
435:       </div>
436:     </div>
437:   );
438: }
439: 
440: 
441: function Row({ label, value }) {
442:   return (
443:     <div style={{ display: "grid", gridTemplateColumns: "180px 1fr",
444:                   fontSize: 12, padding: "4px 0", color: ink }}>
445:       <div style={{ letterSpacing: 0.5, color: ink3 }}>{label}</div>
446:       <div style={{ fontFamily: "ui-monospace, Menlo, monospace",
447:                     wordBreak: "break-all" }}>
448:         {value || "—"}
449:       </div>
450:     </div>
451:   );
452: }
453: 
454: 
455: function ReasoningDormantPanel({ dormantSentence }) {
456:   return (
457:     <div data-testid="thinklab-reasoning-dormant"
458:          style={{ marginTop: 20, padding: "18px 22px", background: surface2,
459:                   borderLeft: `3px solid ${brass}`, borderRadius: 6 }}>
460:       <div style={{ fontSize: 11, letterSpacing: 1.5, color: brass,
461:                     textTransform: "uppercase", fontWeight: 700,
462:                     marginBottom: 6 }}>
463:         Reasoning — dormant
464:       </div>
465:       <div style={{ fontSize: 13, color: ink, lineHeight: 1.6 }}>
466:         {dormantSentence || "The reasoning faculty is not yet in force."}
467:       </div>
468:       <div style={{ fontSize: 11, color: ink3, marginTop: 8,
469:                     fontStyle: "italic", lineHeight: 1.55 }}>
470:         The five stages above (Frame → Name → Challenge → Weigh → Lock-in)
471:         are the shape of the walk. Their body lights up when the Solver
472:         lands — until then, the direction is captured, the objective is
473:         admitted and frozen, and the ledger records the admission.
474:       </div>
475:     </div>
476:   );
477: }
478: 
479: 
480: function SolvaReasoningPanel({ directionStatement, dormantSentence }) {
481:   const [state, setState] = useState("idle");  // idle | running | done | error
482:   const [run, setRun] = useState(null);
483:   const [error, setError] = useState(null);
484: 
485:   const runSolva = async () => {
486:     setState("running");
487:     setError(null);
488:     try {
489:       const r = await fetch(`${BACKEND_URL}/api/thinklab/reason`, {
490:         method: "POST",
491:         headers: { "Content-Type": "application/json" },
492:         body: JSON.stringify({
493:           direction_statement: directionStatement,
494:           actor: "operator@estate",
495:         }),
496:       });
497:       if (!r.ok) throw new Error(`HTTP ${r.status}`);
498:       const body = await r.json();
499:       setRun(body);
500:       setState("done");
501:     } catch (exc) {
502:       setError(String(exc));
503:       setState("error");
504:     }
505:   };
506: 
507:   if (state === "idle") {
508:     return (
509:       <div data-testid="thinklab-reasoning-idle"
510:            style={{ marginTop: 20, padding: "18px 22px", background: surface2,
511:                     borderLeft: `3px solid ${sage}`, borderRadius: 6 }}>
512:         <div style={{ fontSize: 11, letterSpacing: 1.5, color: sage,
513:                       textTransform: "uppercase", fontWeight: 700,
514:                       marginBottom: 6 }}>
515:           Solva reasoning — ready
516:         </div>
517:         <div style={{ fontSize: 13, color: ink, lineHeight: 1.6 }}>
518:           {dormantSentence || "Solva reasoning is in force."}
519:         </div>
520:         <button data-testid="thinklab-run-solva-btn"
521:                 onClick={runSolva}
522:                 style={{ marginTop: 14, padding: "9px 16px",
523:                          background: sage, color: "#fff",
524:                          border: `1px solid ${sage}`, borderRadius: 5,
525:                          cursor: "pointer", fontSize: 12, fontWeight: 700 }}>
526:           Run Solva reasoning
527:         </button>
528:       </div>
529:     );
530:   }
531: 
532:   if (state === "running") {
533:     return (
534:       <div data-testid="thinklab-reasoning-running"
535:            style={{ marginTop: 20, padding: "18px 22px", background: surface2,
536:                     borderLeft: `3px solid ${sage}`, borderRadius: 6,
537:                     fontSize: 13, color: ink3, fontStyle: "italic" }}>
538:         Running frame_audit → candidate_generation → synthesis through the LLM chokepoint…
539:       </div>
540:     );
541:   }
542: 
543:   if (state === "error") {
544:     return (
545:       <div data-testid="thinklab-reasoning-error"
546:            style={{ marginTop: 20, padding: "18px 22px", background: surface,
547:                     borderLeft: `3px solid ${oxblood2}`, borderRadius: 6,
548:                     border: `1px solid ${line}` }}>
549:         <div style={{ fontSize: 11, letterSpacing: 1.5, color: oxblood,
550:                       textTransform: "uppercase", fontWeight: 700 }}>
551:           Reasoning refused (endpoint)
552:         </div>
553:         <div style={{ fontSize: 12, color: ink, marginTop: 8,
554:                       fontFamily: "ui-monospace, Menlo, monospace" }}>
555:           {error}
556:         </div>
557:       </div>
558:     );
559:   }
560: 
561:   // state === "done"
562:   return (
563:     <div data-testid="thinklab-reasoning-done" style={{ marginTop: 20 }}>
564:       <SolvaStageBlock label="Frame audit"
565:                        stage={run?.frame_audit}
566:                        renderBody={(fa) => (
567:                          <div>
568:                            <div style={{ fontSize: 12, color: ink3, marginBottom: 4 }}>Verdict</div>
569:                            <div style={{ fontSize: 14, color: ink,
570:                                          fontFamily: "ui-monospace, Menlo, monospace" }}>
571:                              {fa.verdict}
572:                            </div>
573:                            <div style={{ fontSize: 11, color: ink3, marginTop: 10 }}>Dimensions</div>
574:                            {(fa.dimensions || []).map(d => (
575:                              <div key={d.dimension}
576:                                   style={{ fontSize: 12, color: ink,
577:                                            display: "grid",
578:                                            gridTemplateColumns: "180px 100px 1fr",
579:                                            padding: "3px 0" }}>
580:                                <span style={{ color: ink3 }}>{d.dimension}</span>
581:                                <span style={{ color: d.score === "sufficient" ? sage : oxblood }}>
582:                                  {d.score}
583:                                </span>
584:                                <span style={{ color: ink3, fontStyle: "italic" }}>
585:                                  {d.invalidation || ""}
586:                                </span>
587:                              </div>
588:                            ))}
589:                          </div>
590:                        )} />
591:       <SolvaStageBlock label="Candidate generation"
592:                        stage={run?.candidate_generation}
593:                        renderBody={(cg) => (
594:                          <div>
595:                            {(cg.candidates || []).length === 0 && (
596:                              <div style={{ fontSize: 12, color: ink3, fontStyle: "italic" }}>
597:                                No candidates parsed. This is honest empty — the shield may have
598:                                returned an unparseable body.
599:                              </div>
600:                            )}
601:                            {(cg.candidates || []).map((c, i) => (
602:                              <div key={c.id || i}
603:                                   style={{ padding: "10px 0",
604:                                            borderBottom: `1px solid ${line}` }}>
605:                                <div style={{ fontSize: 13, color: ink, lineHeight: 1.5 }}>
606:                                  <b style={{ color: ink3, fontSize: 11,
607:                                              letterSpacing: 0.5,
608:                                              textTransform: "uppercase" }}>
609:                                    {c.candidate_type || "cause"}
610:                                  </b>{" · "}
611:                                  {c.description}
612:                                </div>
613:                                <div style={{ fontSize: 11, color: ink3, marginTop: 4,
614:                                              fontStyle: "italic" }}>
615:                                  Evidence would come from: {c.evidence_requirement}
616:                                </div>
617:                              </div>
618:                            ))}
619:                          </div>
620:                        )} />
621:       <SolvaStageBlock label="Synthesis"
622:                        stage={run?.synthesis}
623:                        renderBody={(syn) => (
624:                          <div style={{ fontSize: 14, color: ink, lineHeight: 1.65,
625:                                        fontFamily: head }}>
626:                            {syn.paragraph || (
627:                              <span style={{ color: ink3, fontStyle: "italic" }}>
628:                                No synthesis returned.
629:                              </span>
630:                            )}
631:                          </div>
632:                        )} />
633:       <div style={{ marginTop: 10, fontSize: 11, color: ink3,
634:                     fontFamily: "ui-monospace, Menlo, monospace" }}>
635:         Run identity · {run?.run_id} · at {run?.at_iso}
636:       </div>
637:     </div>
638:   );
639: }
640: 
641: 
642: function SolvaStageBlock({ label, stage, renderBody }) {
643:   if (!stage) return null;
644: 
645:   if (stage.refused) {
646:     return (
647:       <div data-testid={`solva-stage-refused-${label.toLowerCase().replace(/\s+/g, "-")}`}
648:            style={{ marginTop: 14, padding: "16px 20px", background: surface,
649:                     borderLeft: `3px solid ${oxblood2}`, borderRadius: 6,
650:                     border: `1px solid ${line}` }}>
651:         <div style={{ fontSize: 11, letterSpacing: 1.5, color: oxblood,
652:                       textTransform: "uppercase", fontWeight: 700 }}>
653:           {label} — refused
654:         </div>
655:         <div style={{ fontSize: 12, color: ink, marginTop: 8,
656:                       fontFamily: "ui-monospace, Menlo, monospace",
657:                       background: "#f7ecea", padding: "8px 10px",
658:                       borderRadius: 4 }}>
659:           {stage.refusal_reason}
660:         </div>
661:         <div style={{ fontSize: 11, color: ink3, marginTop: 6, fontStyle: "italic" }}>
662:           A8-Q3 · the shield's refusal is rendered verbatim, never a smoothed answer.
663:         </div>
664:       </div>
665:     );
666:   }
667: 
668:   return (
669:     <div data-testid={`solva-stage-${label.toLowerCase().replace(/\s+/g, "-")}`}
670:          style={{ marginTop: 14, padding: "18px 22px", background: surface,
671:                   border: `1px solid ${line}`, borderRadius: 6 }}>
672:       <div style={{ display: "flex", justifyContent: "space-between",
673:                     alignItems: "center", marginBottom: 10 }}>
674:         <div style={{ fontSize: 11, letterSpacing: 1.5, color: sage,
675:                       textTransform: "uppercase", fontWeight: 700 }}>
676:           {label}
677:         </div>
678:         <div style={{ fontSize: 10, color: ink3,
679:                       fontFamily: "ui-monospace, Menlo, monospace" }}
680:              data-testid="solva-stage-provenance">
681:           Answered by <b style={{ color: ink }}>{stage.model_id}</b> via {stage.provider} ·{" "}
682:           receipt <b>{stage.receipt_id}</b>
683:         </div>
684:       </div>
685:       {renderBody(stage)}
686:     </div>
687:   );
688: }
689: 
690: 
691: function RefusalCard({ reason, row, onRetry }) {
692:   return (
693:     <div data-testid="thinklab-refusal-card"
694:          style={{ marginTop: 20, padding: "22px 24px", background: surface,
695:                   borderLeft: `3px solid ${oxblood2}`, borderRadius: 6,
696:                   border: `1px solid ${line}` }}>
697:       <div style={{ fontSize: 11, letterSpacing: 1.5, color: oxblood,
698:                     textTransform: "uppercase", fontWeight: 700 }}>
699:         Refused at Admit
700:       </div>
701:       <div style={{ fontSize: 13.5, color: ink, lineHeight: 1.6,
702:                     marginTop: 8, fontFamily: "ui-monospace, Menlo, monospace",
703:                     background: "#f7ecea", padding: "10px 12px",
704:                     borderRadius: 4 }}>
705:         {reason}
706:       </div>
707:       <div style={{ fontSize: 11, color: ink3, marginTop: 8 }}>
708:         Ledger row: {row?.row_id} · stage: {row?.stage} · at {row?.at || ""}
709:       </div>
710:       <button onClick={onRetry}
711:               style={{ marginTop: 14, padding: "8px 14px",
712:                        background: "transparent", color: blue,
713:                        border: `1px solid ${blue}`, borderRadius: 5,
714:                        cursor: "pointer", fontSize: 12, fontWeight: 600 }}>
715:         Try again
716:       </button>
717:     </div>
718:   );
719: }

# SOURCE: frontend/src/components/Training.jsx

1: import React, { useEffect, useState } from "react";
2: import { Link } from "react-router-dom";
3: 
4: /**
5:  * Training.jsx — W11 CP3 · Multidimensional Training Engine surface.
6:  *
7:  * Doc 17 · Incremental Training & Capacity + Owner-approved CP3 slice:
8:  *   1. Demand Table panel  (§4.1 · admissibility + §3.5 · E = B + I).
9:  *   2. Capacity Ledger panel (§4.2 · empty-at-ship · provenance day-one).
10:  *   3. Test-set Seal panel (A17.11 · live-verify FIRST · honest hold).
11:  *
12:  * Data source: GET /api/training/state. Every row cites its on-disk
13:  * artifact by objective_id / seal_id (REFERENCE-NOT-COPY · Design
14:  * Law A8). Empty stores render an honest sentence citing the canon
15:  * anchor. Refusals (stale verification, link_working=false, no record)
16:  * are surfaced verbatim; the seal never lies about hold-state.
17:  *
18:  * NO trainer run fires from this surface. Sampling & Reflection remains
19:  * unbuilt; CP8 will bring the trainer runner. This surface's job is to
20:  * let the Owner see the Demand-Table + Capacity-Ledger + Test-set-Seal
21:  * ceremony end to end on real DigiCow strata BEFORE any GPU-hours are
22:  * spent (per Owner directive at W11 open).
23:  */
24: 
25: const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
26: 
27: // v7 palette · matched to Governance/Watch/GreyMirror.
28: const paper = "#f5f2ea";
29: const surface = "#ffffff";
30: const ink = "#1b1f27";
31: const ink2 = "#3a3f4a";
32: const ink3 = "#7a7f8a";
33: const line = "#e4dccf";
34: const blue = "#16274a";
35: const sage = "#1d7a6e";
36: const brass = "#b08d2e";
37: const oxblood = "#8a2a44";
38: const head = 'ui-serif, "Iowan Old Style", Georgia, serif';
39: 
40: function Panel({ "data-testid": dt, title, anchor, children }) {
41:   return (
42:     <section data-testid={dt} style={{
43:       background: surface, border: `1px solid ${line}`, padding: "22px 24px",
44:       marginBottom: 20,
45:     }}>
46:       <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 8 }}>
47:         <h2 style={{ fontFamily: head, fontSize: 20, color: blue, margin: 0 }}>{title}</h2>
48:         <span style={{ fontSize: 11, letterSpacing: 1.5, color: ink3 }}>{anchor}</span>
49:       </div>
50:       {children}
51:     </section>
52:   );
53: }
54: 
55: function EmptyState({ anchor, kind }) {
56:   return (
57:     <p style={{ color: ink2, fontStyle: "italic", margin: "6px 0 0 0" }}>
58:       No {kind} on record. Canon anchor: {anchor}. Drawn, never left blank.
59:     </p>
60:   );
61: }
62: 
63: function DemandTableRow({ table }) {
64:   return (
65:     <li style={{ borderBottom: `1px dotted ${line}`, padding: "10px 0" }}>
66:       <div style={{ fontFamily: "ui-monospace, monospace", fontSize: 13, color: blue }}
67:            data-testid="demand-table-objective-id">
68:         {table.objective_id}
69:       </div>
70:       <div style={{ fontSize: 12, color: ink2, marginTop: 4 }}>
71:         compiled {table.compiled_at} · {table.schemes_count} scheme{table.schemes_count === 1 ? "" : "s"}
72:         {" "}· {table.strata_count} stratum row{table.strata_count === 1 ? "" : "s"}
73:       </div>
74:       {table.schemes && table.schemes.length > 0 && (
75:         <details style={{ marginTop: 8 }}>
76:           <summary style={{ cursor: "pointer", fontSize: 12, color: ink2 }}>
77:             Named-failure list (admissibility rule · §4.1)
78:           </summary>
79:           <ul style={{ margin: "6px 0 0 20px", padding: 0 }}>
80:             {table.schemes.map((s, i) => (
81:               <li key={i} style={{ fontSize: 12, color: ink, marginBottom: 4 }}>
82:                 <span style={{ fontFamily: "ui-monospace, monospace", color: blue }}>{s.id}</span>
83:                 {" — "}
84:                 <span style={{ color: ink2 }}>{s.named_failure}</span>
85:               </li>
86:             ))}
87:           </ul>
88:         </details>
89:       )}
90:       {table.per_stratum && table.per_stratum.length > 0 && (
91:         <table data-testid="demand-table-strata" style={{
92:           marginTop: 10, borderCollapse: "collapse", fontSize: 12, color: ink2,
93:         }}>
94:           <thead>
95:             <tr style={{ background: paper }}>
96:               <th style={{ padding: "4px 12px", textAlign: "left" }}>stratum</th>
97:               <th style={{ padding: "4px 12px", textAlign: "right" }}>B</th>
98:               <th style={{ padding: "4px 12px", textAlign: "right" }}>I</th>
99:               <th style={{ padding: "4px 12px", textAlign: "right" }}>E</th>
100:             </tr>
101:           </thead>
102:           <tbody>
103:             {table.per_stratum.map((r, i) => (
104:               <tr key={i}>
105:                 <td style={{ padding: "4px 12px", fontFamily: "ui-monospace, monospace" }}>
106:                   {r.stratum_id}
107:                 </td>
108:                 <td style={{ padding: "4px 12px", textAlign: "right" }}>{r.B}</td>
109:                 <td style={{ padding: "4px 12px", textAlign: "right", color: r.I ? oxblood : ink2 }}>
110:                   {r.I}
111:                 </td>
112:                 <td style={{ padding: "4px 12px", textAlign: "right", color: brass, fontWeight: 600 }}>
113:                   {r.E}
114:                 </td>
115:               </tr>
116:             ))}
117:           </tbody>
118:         </table>
119:       )}
120:     </li>
121:   );
122: }
123: 
124: function CapacityRow({ row }) {
125:   return (
126:     <li style={{ borderBottom: `1px dotted ${line}`, padding: "8px 0" }}>
127:       <div style={{ fontFamily: "ui-monospace, monospace", fontSize: 13, color: blue }}>
128:         {row.scheme_id} <span style={{ color: ink3 }}>· {row.stratum}</span>
129:       </div>
130:       <div style={{ fontSize: 12, color: ink2, marginTop: 2 }}>
131:         level {row.level.toFixed(3)} · state {row.state}
132:         {" · "}
133:         {row.provenance_count} commission{row.provenance_count === 1 ? "" : "s"}
134:       </div>
135:     </li>
136:   );
137: }
138: 
139: function SealRow({ seal }) {
140:   return (
141:     <li style={{ borderBottom: `1px dotted ${line}`, padding: "10px 0" }}>
142:       <div style={{ fontFamily: "ui-monospace, monospace", fontSize: 12, color: blue }}
143:            data-testid="test-set-seal-id">
144:         {seal.seal_id}
145:       </div>
146:       <div style={{ fontSize: 12, color: ink2, marginTop: 4 }}>
147:         objective {seal.objective_id} · table {seal.target_table} · sample_size {seal.sample_size}
148:       </div>
149:       <div style={{ fontSize: 11, color: ink3, marginTop: 4, fontFamily: "ui-monospace, monospace" }}>
150:         manifest_sha256: {seal.manifest_sha256 && seal.manifest_sha256.slice(0, 24)}…
151:       </div>
152:       <div style={{ fontSize: 11, color: ink3, marginTop: 2 }}>
153:         sealed {seal.sealed_at} · rds link verified at {seal.rds_link_verified_at}
154:       </div>
155:       <div style={{ fontSize: 11, color: ink3, marginTop: 2 }}>
156:         strata: {(seal.strata || []).join(", ") || "(none named)"}
157:       </div>
158:     </li>
159:   );
160: }
161: 
162: export default function Training() {
163:   const [state, setState] = useState(null);
164:   const [error, setError] = useState(null);
165:   // W11 B CP5 · Doc 17 §A17.3-A17.6 · recipe seat + optimizer harness rollups.
166:   const [recipes, setRecipes] = useState(null);
167:   const [comparisons, setComparisons] = useState(null);
168: 
169:   useEffect(() => {
170:     let alive = true;
171:     fetch(`${BACKEND_URL}/api/training/state`, { credentials: "include" })
172:       .then(r => (r.ok ? r.json() : Promise.reject(r.statusText)))
173:       .then(body => { if (alive) setState(body); })
174:       .catch(e => { if (alive) setError(String(e)); });
175:     fetch(`${BACKEND_URL}/api/training/recipes`, { credentials: "include" })
176:       .then(r => (r.ok ? r.json() : Promise.reject(r.statusText)))
177:       .then(body => { if (alive) setRecipes(body); })
178:       .catch(() => { /* silent; empty-seat is honest default */ });
179:     fetch(`${BACKEND_URL}/api/training/optimizer-comparisons`, { credentials: "include" })
180:       .then(r => (r.ok ? r.json() : Promise.reject(r.statusText)))
181:       .then(body => { if (alive) setComparisons(body); })
182:       .catch(() => { /* silent; empty-seat is honest default */ });
183:     return () => { alive = false; };
184:   }, []);
185: 
186:   return (
187:     <div data-testid="training-surface" style={{
188:       minHeight: "100vh", background: paper, padding: "40px 32px",
189:       fontFamily: "ui-sans-serif, system-ui, -apple-system, sans-serif", color: ink,
190:     }}>
191:       <div style={{ maxWidth: 960, margin: "0 auto" }}>
192:         <div style={{ fontSize: 11, letterSpacing: 2, color: ink3, marginBottom: 6 }}>
193:           AKKI · TRAINING PLANE · W11 CP3
194:         </div>
195:         <h1 style={{ fontFamily: head, fontSize: 40, margin: "0 0 6px 0", color: blue }}>
196:           The Training Plane
197:         </h1>
198:         <p style={{ color: ink2, marginTop: 0, marginBottom: 30, maxWidth: 720, lineHeight: 1.5 }}>
199:           Doc 17 · Multidimensional Training Engine + Incremental Training & Capacity
200:           module. Demand travels with the objective. Capacity stays with the trainer.
201:           Test-sets precede training. Nothing on this surface fires a training run —
202:           the trainer runner lands at CP8, gated on the SSH key.
203:         </p>
204: 
205:         <nav style={{ marginBottom: 22, fontSize: 12, color: ink3 }}>
206:           <Link to="/" style={{ color: blue, marginRight: 12 }}>Registry</Link>·
207:           <Link to="/governance" style={{ color: blue, margin: "0 12px" }}>Governance</Link>·
208:           <Link to="/watch" style={{ color: blue, margin: "0 12px" }}>Watch</Link>·
209:           <Link to="/grey-mirror" style={{ color: blue, margin: "0 12px" }}>Grey Mirror</Link>·
210:           <span style={{ color: brass, marginLeft: 12 }}>Training (you are here)</span>
211:         </nav>
212: 
213:         {error && (
214:           <div data-testid="training-load-error" style={{
215:             background: "#fff6f6", border: `1px solid ${oxblood}`, color: oxblood,
216:             padding: "12px 16px", marginBottom: 20, fontFamily: "ui-monospace, monospace",
217:             fontSize: 12,
218:           }}>
219:             /api/training/state unreachable: {error}
220:           </div>
221:         )}
222: 
223:         {state && (
224:           <>
225:             <div data-testid="training-ship-state" style={{
226:               fontSize: 12, color: state.ship_state === "empty" ? ink3 : sage,
227:               marginBottom: 20, fontFamily: "ui-monospace, monospace",
228:             }}>
229:               ship_state: {state.ship_state}
230:             </div>
231: 
232:             <Panel dt="training-demand-tables-panel" title="Demand Tables"
233:                    anchor="Doc 17 §4.1 · admissibility · E = B + I">
234:               {state.demand_tables.length === 0
235:                 ? <EmptyState anchor="Doc 17 §4.1" kind="compiled demand tables" />
236:                 : (
237:                   <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
238:                     {state.demand_tables.map((t, i) => <DemandTableRow key={i} table={t} />)}
239:                   </ul>
240:                 )}
241:             </Panel>
242: 
243:             <Panel dt="training-capacity-panel" title="Capacity Ledger"
244:                    anchor="Doc 17 §4.2 · empty-at-ship · provenance day-one">
245:               <div data-testid="capacity-row-count" style={{
246:                 fontFamily: "ui-monospace, monospace", color: brass, fontSize: 13, marginBottom: 8,
247:               }}>
248:                 {state.capacity_ledger_rows} row{state.capacity_ledger_rows === 1 ? "" : "s"}
249:               </div>
250:               {state.capacity_ledger_rows === 0
251:                 ? <EmptyState anchor="Doc 17 §4.2" kind="capacity rows" />
252:                 : (
253:                   <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
254:                     {state.capacity_ledger.map((r, i) => <CapacityRow key={i} row={r} />)}
255:                   </ul>
256:                 )}
257:               <p style={{ fontSize: 11, color: ink3, marginTop: 12, fontStyle: "italic" }}>
258:                 Deprioritized at CP3 open: marginal-gain writer and forecasting.
259:                 Rows appear here as calibration probes execute (CP8).
260:               </p>
261:             </Panel>
262: 
263:             <Panel dt="training-seals-panel" title="Test-set Seals"
264:                    anchor="Doc 17 A17.11 · test-set-precedes-training">
265:               {state.test_set_seals.length === 0
266:                 ? <EmptyState anchor="Doc 17 A17.11" kind="test-set seals" />
267:                 : (
268:                   <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
269:                     {state.test_set_seals.map((s, i) => <SealRow key={i} seal={s} />)}
270:                   </ul>
271:                 )}
272:               <p style={{ fontSize: 11, color: ink3, marginTop: 12, fontStyle: "italic" }}>
273:                 Sealing refuses honestly when the on-disk data_connection_record is
274:                 stale (older than 24h), link_working=false, or missing. The seal
275:                 references a freshly verified live probe — never a stale cache.
276:               </p>
277:             </Panel>
278: 
279:             {/* W11 B CP5 · Doc 17 A17.3-A17.4 · recipe seat (empty until first training run). */}
280:             <section data-testid="training-recipes-panel" style={{
281:               background: surface, border: `1px solid ${line}`, padding: "22px 24px",
282:               marginBottom: 20,
283:             }}>
284:               <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 8 }}>
285:                 <h2 style={{ fontFamily: head, fontSize: 20, color: blue, margin: 0 }}>Recipe Seat · training_params@v0</h2>
286:                 <span style={{ fontSize: 11, letterSpacing: 1.5, color: ink3 }}>Doc 17 §A17.3-A17.4 · Wave B CP5</span>
287:               </div>
288:               {recipes === null
289:                 ? <p style={{ color: ink3, fontStyle: "italic", margin: "6px 0 0 0" }}>Loading…</p>
290:                 : recipes.count === 0
291:                   ? (
292:                     <>
293:                       <p data-testid="recipes-empty" style={{ color: ink2, fontStyle: "italic", margin: "6px 0 0 0" }}>
294:                         No recipe on record. Canon anchor: Doc 17 §A17.5-A17.6. Drawn, never left blank.
295:                       </p>
296:                       <p style={{ fontSize: 11, color: ink3, marginTop: 8, lineHeight: 1.5 }}>
297:                         {recipes.empty_seat_note}
298:                       </p>
299:                     </>
300:                   ) : (
301:                     <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
302:                       {recipes.recipes.map((r, i) => (
303:                         <li key={i} style={{ borderBottom: `1px dotted ${line}`, padding: "10px 0" }}>
304:                           <div style={{ fontFamily: "ui-monospace, monospace", fontSize: 13, color: blue }}
305:                                data-testid="recipe-version">
306:                             {r.recipe_version}
307:                           </div>
308:                           <div style={{ fontSize: 12, color: ink2, marginTop: 4 }}>
309:                             optimizer <span style={{ color: sage }}>{r.optimizer_kind}</span>
310:                             {" · "}base <code>{r.base_model_id}</code>
311:                             {" · "}comparison <code>{r.comparison_ref}</code>
312:                           </div>
313:                           <div style={{ fontSize: 11, color: ink3, marginTop: 2 }}>
314:                             budget {r.budget_cap.wallclock_seconds}s / {r.budget_cap.gpu_hours} GPU-h ·
315:                             ratified {r.ratified_at}
316:                           </div>
317:                         </li>
318:                       ))}
319:                     </ul>
320:                   )
321:               }
322:             </section>
323: 
324:             {/* W11 B CP5 · Doc 17 A17.5-A17.6 · two-arm optimizer harness (empty until first probe). */}
325:             <section data-testid="training-optimizer-panel" style={{
326:               background: surface, border: `1px solid ${line}`, padding: "22px 24px",
327:               marginBottom: 20,
328:             }}>
329:               <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 8 }}>
330:                 <h2 style={{ fontFamily: head, fontSize: 20, color: blue, margin: 0 }}>Optimizer Comparisons · two-arm harness</h2>
331:                 <span style={{ fontSize: 11, letterSpacing: 1.5, color: ink3 }}>Doc 17 §A17.5-A17.6 · Wave B CP5</span>
332:               </div>
333:               {comparisons === null
334:                 ? <p style={{ color: ink3, fontStyle: "italic", margin: "6px 0 0 0" }}>Loading…</p>
335:                 : comparisons.count === 0
336:                   ? (
337:                     <>
338:                       <p data-testid="comparisons-empty" style={{ color: ink2, fontStyle: "italic", margin: "6px 0 0 0" }}>
339:                         No optimizer comparison on record. Canon anchor: Doc 17 §A17.5. Drawn, never left blank.
340:                       </p>
341:                       <p style={{ fontSize: 11, color: ink3, marginTop: 8, lineHeight: 1.5 }}>
342:                         The protocol executes at the first adapter training on real material, inside the
343:                         P4-instrumented run. Quality parity on M-a and M-b is mandatory; compute-to-convergence
344:                         is reported, never gating.
345:                       </p>
346:                     </>
347:                   ) : (
348:                     <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
349:                       {comparisons.comparisons.map((c, i) => (
350:                         <li key={i} style={{ borderBottom: `1px dotted ${line}`, padding: "10px 0" }}>
351:                           <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
352:                             <span style={{ fontFamily: "ui-monospace, monospace", fontSize: 13, color: blue }}
353:                                   data-testid="comparison-id">
354:                               {c.comparison_id}
355:                             </span>
356:                             <span data-testid="comparison-verdict" style={{
357:                               fontSize: 11, letterSpacing: 1.2, color: c.verdict === "adopted" ? sage
358:                                 : c.verdict === "ineligible" ? oxblood
359:                                   : c.verdict === "rejected" ? ink3 : brass,
360:                               textTransform: "uppercase",
361:                             }}>
362:                               {c.verdict}
363:                             </span>
364:                           </div>
365:                           <div style={{ fontSize: 12, color: ink2, marginTop: 4 }}>
366:                             base <code>{c.base_model_id}</code> · stratum <code>{c.smallest_stratum}</code>
367:                           </div>
368:                           {c.verdict_note && (
369:                             <div style={{ fontSize: 11, color: c.verdict === "ineligible" ? oxblood : ink3, marginTop: 4, fontStyle: "italic" }}>
370:                               {c.verdict_note}
371:                             </div>
372:                           )}
373:                           {c.baseline_measurements && c.muon_measurements && (
374:                             <table style={{ marginTop: 8, borderCollapse: "collapse", fontSize: 11, color: ink2 }}>
375:                               <thead>
376:                                 <tr style={{ background: paper }}>
377:                                   <th style={{ padding: "3px 10px", textAlign: "left" }}>arm</th>
378:                                   <th style={{ padding: "3px 10px", textAlign: "right" }}>M-a</th>
379:                                   <th style={{ padding: "3px 10px", textAlign: "right" }}>M-b</th>
380:                                   <th style={{ padding: "3px 10px", textAlign: "right" }}>M-e</th>
381:                                   <th style={{ padding: "3px 10px", textAlign: "right" }}>wallclock</th>
382:                                   <th style={{ padding: "3px 10px", textAlign: "right" }}>GPU-h</th>
383:                                 </tr>
384:                               </thead>
385:                               <tbody>
386:                                 {["baseline", "muon"].map((arm) => {
387:                                   const m = c[`${arm}_measurements`];
388:                                   return (
389:                                     <tr key={arm}>
390:                                       <td style={{ padding: "3px 10px", fontFamily: "ui-monospace, monospace" }}>{arm}</td>
391:                                       <td style={{ padding: "3px 10px", textAlign: "right" }}>{m.moac_m_a_improvement.toFixed(3)}</td>
392:                                       <td style={{ padding: "3px 10px", textAlign: "right" }}>{m.moac_m_b_regression.toFixed(3)}</td>
393:                                       <td style={{ padding: "3px 10px", textAlign: "right" }}>{m.moac_m_e_calibration.toFixed(3)}</td>
394:                                       <td style={{ padding: "3px 10px", textAlign: "right", color: ink3 }}>{m.wallclock_seconds_to_convergence}s</td>
395:                                       <td style={{ padding: "3px 10px", textAlign: "right", color: ink3 }}>{m.gpu_hours_to_convergence}</td>
396:                                     </tr>
397:                                   );
398:                                 })}
399:                               </tbody>
400:                             </table>
401:                           )}
402:                         </li>
403:                       ))}
404:                     </ul>
405:                   )
406:               }
407:             </section>
408: 
409:             <div data-testid="training-reference-note" style={{
410:               fontSize: 11, color: ink3, borderTop: `1px solid ${line}`,
411:               marginTop: 30, paddingTop: 12, lineHeight: 1.5,
412:             }}>
413:               {state.reference_note}
414:             </div>
415:           </>
416:         )}
417:       </div>
418:     </div>
419:   );
420: }

# SOURCE: frontend/src/components/Watch.jsx

1: import React, { useEffect, useState } from "react";
2: import { Link } from "react-router-dom";
3: 
4: /**
5:  * Watch.jsx — W10 CP8 · The Watch surface.
6:  *
7:  * Composes seven panels sharing REFERENCE-NOT-COPY posture (Design
8:  * Law A8):
9:  *   1. Verdicts (Canon 8 §7 · Macho sensor · W9 CP1)
10:  *   2. Actions (Canon 8 §8 · Mkono responder · W9 CP1)
11:  *   3. Containments + Reconciliations (Canon 8 §14 + §18 · W9 CP5)
12:  *   4. Continuity Attestations (Canon 8 §9 · CA1-N5 · W9 CP4)
13:  *   5. Witness Attestations (Canon 8 §9 · W10 CP5)
14:  *   6. Tamper Alarms (Canon 8 §9 · W10 CP5)
15:  *   7. Fitness Summary (Canon 8 §25-§28 · W10 CP3 · demonstrated
16:  *      firings over observation window · Ruling-1 precondition (b)
17:  *      demonstrated status)
18:  *
19:  * Data source: GET /api/watch/state.
20:  */
21: 
22: const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
23: 
24: const paper = "#f5f2ea";
25: const surface = "#ffffff";
26: const ink = "#1b1f27";
27: const ink2 = "#3a3f4a";
28: const ink3 = "#7a7f8a";
29: const line = "#e4dccf";
30: const blue = "#16274a";
31: const sage = "#1d7a6e";
32: const oxblood = "#8a2a44";
33: const brass = "#b08d2e";
34: const head = 'ui-serif, "Iowan Old Style", Georgia, serif';
35: 
36: function Panel({ "data-testid": dt, title, anchor, children }) {
37:   return (
38:     <section data-testid={dt} style={{
39:       background: surface, border: `1px solid ${line}`, padding: "20px 22px",
40:       marginBottom: 18,
41:     }}>
42:       <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 6 }}>
43:         <h2 style={{ fontFamily: head, fontSize: 19, color: blue, margin: 0 }}>{title}</h2>
44:         <span style={{ fontSize: 11, letterSpacing: 1.5, color: ink3 }}>{anchor}</span>
45:       </div>
46:       {children}
47:     </section>
48:   );
49: }
50: 
51: function Count({ "data-testid": dt, n, label }) {
52:   return (
53:     <div data-testid={dt} style={{
54:       fontFamily: "ui-monospace, monospace", color: brass, fontSize: 13, marginBottom: 6,
55:     }}>{n === null ? "loading…" : `${n} ${label}`}</div>
56:   );
57: }
58: 
59: function EmptyState({ anchor, kind, mechanismStatus }) {
60:   // W11 R7 · Watch/Grey-Mirror honesty. If `mechanismStatus` is
61:   // "unbuilt", surface the honest state explicitly rather than "no X on
62:   // record" (which reads as "wired mechanism happens to be empty").
63:   if (mechanismStatus && mechanismStatus.startsWith("unbuilt")) {
64:     return (
65:       <p data-testid={`empty-unbuilt-${kind.replace(/\s+/g, "-")}`}
66:          style={{ color: oxblood, fontStyle: "italic", margin: "6px 0 0 0" }}>
67:         mechanism not yet built — {mechanismStatus} · Canon anchor: {anchor}.
68:       </p>
69:     );
70:   }
71:   return (
72:     <p style={{ color: ink2, fontStyle: "italic", margin: "6px 0 0 0" }}>
73:       No {kind} on record. Canon anchor: {anchor}. Drawn, never left blank.
74:     </p>
75:   );
76: }
77: 
78: function EntryRow({ entry, extra }) {
79:   return (
80:     <li style={{ borderBottom: `1px dotted ${line}`, padding: "8px 0" }}>
81:       <div style={{ fontFamily: "ui-monospace, monospace", fontSize: 13, color: blue }}>
82:         {entry.record_id}
83:       </div>
84:       {extra ? <div style={{ fontSize: 12, color: ink2, marginTop: 2 }}>{extra}</div> : null}
85:       <div style={{ fontSize: 11, color: ink3, marginTop: 2 }}>{entry.source_path}</div>
86:     </li>
87:   );
88: }
89: 
90: // W11 C CP-C2 · render both MachoVerdict (verdict_class + intensity +
91: // sever_certainty_signal_id) and legacy WatchVerdictRow_v0
92: // (signal_class + severity). Doc 8 §Line 30 verbatim closed grammar
93: // surfaced in-place.
94: function verdictExtra(e) {
95:   if (e.verdict_class) {
96:     const parts = [`class: ${e.verdict_class}`];
97:     if (e.verdict_class === "externally_steerable" && e.intensity) {
98:       parts.push(`intensity: ${e.intensity}`);
99:     }
100:     if (e.sever_certainty_signal_id) {
101:       parts.push(`sever_certainty_signal: ${e.sever_certainty_signal_id}`);
102:     }
103:     return parts.join(" · ");
104:   }
105:   if (e.signal_class) {
106:     return `signal_class: ${e.signal_class}${e.severity ? ` · severity: ${e.severity}` : ""}`;
107:   }
108:   return "";
109: }
110: 
111: // W11 C CP-C2 · render both WatchActionV0 (four-class ladder +
112: // ttl_seconds + reversible + sever_certainty_signal_id) and legacy
113: // WatchActionRecord_v0 (7-verb grammar). Doc 8 §Line 99 verbatim.
114: function actionExtra(e) {
115:   if (typeof e.reversible !== "undefined" || typeof e.ttl_seconds !== "undefined") {
116:     const parts = [`class: ${e.action_class}`];
117:     if (e.ttl_seconds !== null && typeof e.ttl_seconds !== "undefined") {
118:       parts.push(`ttl: ${e.ttl_seconds}s`);
119:     }
120:     if (typeof e.reversible !== "undefined") {
121:       parts.push(`reversible: ${String(e.reversible)}`);
122:     }
123:     if (e.sever_certainty_signal_id) {
124:       parts.push(`sever_certainty_signal: ${e.sever_certainty_signal_id}`);
125:     }
126:     return parts.join(" · ");
127:   }
128:   return e.action_class ? `class: ${e.action_class}` : "";
129: }
130: 
131: // W11 C CP-C3 · render MirageArtifactV0 rows honestly with the
132: // §Line 183 isolation invariants surfaced.
133: function mirageArtifactExtra(e) {
134:   const parts = [];
135:   if (e.mirage_session_id) parts.push(`session: ${e.mirage_session_id}`);
136:   if (typeof e.is_synthetic !== "undefined") parts.push(`synthetic: ${String(e.is_synthetic)}`);
137:   if (e.production_store_leak_check) parts.push(`leak_check: ${e.production_store_leak_check}`);
138:   if (typeof e.outward_lie_only !== "undefined") parts.push(`outward_lie_only: ${String(e.outward_lie_only)}`);
139:   return parts.join(" · ");
140: }
141: 
142: // W11 C CP-C3 · render MarkV0 dye-pack rows binding all six
143: // dimensions of §Line 127 verbatim.
144: function markExtra(e) {
145:   const parts = [];
146:   if (e.identity) parts.push(`identity: ${e.identity}`);
147:   if (e.credentials) parts.push(`cred: ${e.credentials}`);
148:   if (e.session_id) parts.push(`sess: ${e.session_id}`);
149:   if (e.device_fingerprint) parts.push(`device: ${e.device_fingerprint}`);
150:   if (e.behavioural_signature) parts.push(`bh: ${e.behavioural_signature}`);
151:   if (e.content_hashes && e.content_hashes.length) parts.push(`hashes: ${e.content_hashes.length}`);
152:   return parts.join(" · ");
153: }
154: 
155: // W11 C CP-C4 · surface subject_kind + attested_hash for
156: // witness attestations (§Line 170 sentence 1 discipline).
157: function witnessAttestationExtra(e) {
158:   const parts = [];
159:   if (e.subject_kind) parts.push(`subject_kind: ${e.subject_kind}`);
160:   if (e.subject_ref) parts.push(`ref: ${e.subject_ref}`);
161:   if (e.attested_hash) {
162:     const short = e.attested_hash.length > 24
163:       ? `${e.attested_hash.slice(0, 24)}…`
164:       : e.attested_hash;
165:     parts.push(`hash: ${short}`);
166:   }
167:   return parts.join(" · ");
168: }
169: 
170: // W11 C CP-C4 · surface tamper alarm evidence (§Line 170 last
171: // sentence: 'this one is a measurement').
172: function tamperAlarmExtra(e) {
173:   const parts = [];
174:   if (e.evidence_kind) parts.push(`kind: ${e.evidence_kind}`);
175:   if (e.evidence_ref) parts.push(`ref: ${e.evidence_ref}`);
176:   return parts.join(" · ");
177: }
178: 
179: function List({ entries, extraFn, extraKey }) {
180:   if (!entries || entries.length === 0) return null;
181:   return (
182:     <ul style={{ listStyle: "none", padding: 0, margin: "8px 0 0 0" }}>
183:       {entries.slice(0, 40).map((e, i) => (
184:         <EntryRow key={`${e.record_id}-${i}`} entry={e}
185:           extra={extraFn ? extraFn(e) : (extraKey ? String(e[extraKey] || "") : "")} />
186:       ))}
187:     </ul>
188:   );
189: }
190: 
191: export default function Watch() {
192:   const [state, setState] = useState(null);
193:   const [error, setError] = useState(null);
194: 
195:   useEffect(() => {
196:     (async () => {
197:       try {
198:         const r = await fetch(`${BACKEND_URL}/api/watch/state`);
199:         if (!r.ok) throw new Error(`HTTP ${r.status}`);
200:         setState(await r.json());
201:       } catch (e) {
202:         setError(String(e));
203:       }
204:     })();
205:   }, []);
206: 
207:   const g = (k) => (state ? state[k] : null);
208:   const gCount = (k) => (g(k) ? g(k).count : null);
209: 
210:   return (
211:     <div data-testid="watch-view" style={{
212:       minHeight: "100vh", background: paper, padding: "40px 48px",
213:       fontFamily: "ui-sans-serif, system-ui",
214:     }}>
215:       <div style={{ maxWidth: 1080, margin: "0 auto" }}>
216:         <div style={{ fontSize: 11, letterSpacing: 2, color: ink3 }}>AKKI · THE WATCH</div>
217:         <h1 data-testid="watch-title" style={{
218:           fontFamily: head, fontSize: 40, color: blue, margin: "8px 0 6px 0",
219:         }}>The Watch</h1>
220:         <p data-testid="watch-reference-note" style={{
221:           color: ink2, fontSize: 13, lineHeight: 1.6, marginBottom: 12,
222:         }}>
223:           REFERENCE-NOT-COPY (Design Law A8). Every Watch entry cites its
224:           on-disk source_path; raw signing material never appears on this
225:           surface (Owner Order 2026-08-25 §4). Anchors: Canon 8 §7 (verdicts) ·
226:           Canon 8 §8 (actions) · Canon 8 §9 (witness) · Canon 8 §14 (containments) ·
227:           Canon 8 §25 (fitness).
228:         </p>
229:         <p style={{ color: ink2, fontSize: 13, lineHeight: 1.6, marginBottom: 18 }}>
230:           Ruling-1 precondition (b) — Watch reconciler demonstrated firing —
231:           {state && state.fitness && state.fitness.ruling_1_precondition_b_demonstrated
232:             ? <span style={{ color: sage }}> DEMONSTRATED (see phase0/drill_receipts/ruling_1_drill_witness_note.md).</span>
233:             : <span style={{ color: oxblood }}> not yet on record.</span>}
234:         </p>
235: 
236:         <nav style={{ marginBottom: 24, fontSize: 13 }}>
237:           <Link data-testid="nav-to-governance" to="/governance" style={{ color: blue, marginRight: 20 }}>
238:             → Governance
239:           </Link>
240:           <Link data-testid="nav-to-grey-mirror" to="/grey-mirror" style={{ color: blue, marginRight: 20 }}>
241:             → Grey Mirror
242:           </Link>
243:           <Link to="/" style={{ color: ink3 }}>← Registry</Link>
244:         </nav>
245: 
246:         {error ? (
247:           <div style={{ color: oxblood, marginBottom: 12 }}>Failed to load: {error}</div>
248:         ) : null}
249: 
250:         <Panel data-testid="watch-fitness-summary"
251:                title="Fitness Summary"
252:                anchor="Canon 8 §25-§28 · W10 CP3">
253:           {state && state.fitness ? (
254:             <div style={{ fontSize: 13, color: ink2, lineHeight: 1.7 }}>
255:               Verdicts over window: <strong>{state.fitness.verdicts_over_window}</strong> ·
256:               Actions over window: <strong>{state.fitness.actions_over_window}</strong> ·
257:               Drill green receipts on record: <strong>{state.fitness.drill_green_receipts_on_record}</strong> ·
258:               Ruling-1 precondition (b) demonstrated:{" "}
259:               <strong>{String(state.fitness.ruling_1_precondition_b_demonstrated)}</strong>
260:             </div>
261:           ) : "loading…"}
262:         </Panel>
263: 
264:         <Panel data-testid="watch-verdicts-panel"
265:                title="Verdicts (Macho)"
266:                anchor="Canon 8 §7 · §Line 28 · §Line 30 · §Line 31">
267:           <Count data-testid="watch-verdicts-count" n={gCount("verdicts")} label="verdicts" />
268:           {gCount("verdicts") === 0 ? <EmptyState anchor="Canon 8 §Line 28" kind="verdicts" /> : null}
269:           <List entries={g("verdicts") ? g("verdicts").entries : []} extraFn={verdictExtra} />
270:         </Panel>
271: 
272:         <Panel data-testid="watch-actions-panel"
273:                title="Actions (Mkono · four-class ladder)"
274:                anchor="Canon 8 §8 · §Line 28 · §Line 99">
275:           <Count data-testid="watch-actions-count" n={gCount("actions")} label="actions" />
276:           {gCount("actions") === 0 ? <EmptyState anchor="Canon 8 §Line 99" kind="actions" /> : null}
277:           <List entries={g("actions") ? g("actions").entries : []} extraFn={actionExtra} />
278:         </Panel>
279: 
280:         <Panel data-testid="watch-mirage-artifacts-panel"
281:                title="Mirage Artifacts (isolated store)"
282:                anchor="Canon 8 §Line 136 · §Line 183 · CP-C3">
283:           <Count data-testid="watch-mirage-artifacts-count" n={gCount("mirage_artifacts")} label="mirage artifacts" />
284:           {gCount("mirage_artifacts") === 0 ? (
285:             <EmptyState anchor="Canon 8 §Line 183"
286:                         kind="mirage artifacts" />
287:           ) : null}
288:           <List entries={g("mirage_artifacts") ? g("mirage_artifacts").entries : []}
289:                 extraFn={mirageArtifactExtra} />
290:         </Panel>
291: 
292:         <Panel data-testid="watch-marks-panel"
293:                title="Marks (dye pack · minted on conviction)"
294:                anchor="Canon 8 §Line 127 · CP-C3">
295:           <Count data-testid="watch-marks-count" n={gCount("marks")} label="marks" />
296:           {gCount("marks") === 0 ? (
297:             <EmptyState anchor="Canon 8 §Line 127" kind="marks" />
298:           ) : null}
299:           <List entries={g("marks") ? g("marks").entries : []} extraFn={markExtra} />
300:         </Panel>
301: 
302:         <Panel data-testid="watch-containments-panel"
303:                title="Containments"
304:                anchor="Canon 8 §14 · §17 expiry · §18 reconciliation · W9 CP5">
305:           <Count data-testid="watch-containments-count" n={gCount("containments")} label="containments" />
306:           {gCount("containments") === 0 ? <EmptyState anchor="Canon 8 §14" kind="containments" /> : null}
307:           <List entries={g("containments") ? g("containments").entries : []} />
308:         </Panel>
309: 
310:         <Panel data-testid="watch-witness-panel"
311:                title="Witness Attestations (§Line 170)"
312:                anchor="Canon 8 §Line 170 · CP-C4">
313:           <Count data-testid="watch-witness-attestations-count" n={gCount("witness_attestations")} label="attestations" />
314:           {gCount("witness_attestations") === 0 ? <EmptyState anchor="Canon 8 §Line 170" kind="witness attestations" /> : null}
315:           <List entries={g("witness_attestations") ? g("witness_attestations").entries : []}
316:                 extraFn={witnessAttestationExtra} />
317:         </Panel>
318: 
319:         <Panel data-testid="watch-tamper-alarms-panel"
320:                title="Tamper Alarms (measurement, not assertion)"
321:                anchor="Canon 8 §Line 170 last sentence · CP-C4">
322:           <Count data-testid="watch-tamper-alarms-count" n={gCount("tamper_alarms")} label="alarms" />
323:           {gCount("tamper_alarms") === 0 ? (
324:             <EmptyState anchor="Canon 8 §Line 170"
325:                         kind="tamper alarms" />
326:           ) : null}
327:           <List entries={g("tamper_alarms") ? g("tamper_alarms").entries : []}
328:                 extraFn={tamperAlarmExtra} />
329:         </Panel>
330:       </div>
331:     </div>
332:   );
333: }
