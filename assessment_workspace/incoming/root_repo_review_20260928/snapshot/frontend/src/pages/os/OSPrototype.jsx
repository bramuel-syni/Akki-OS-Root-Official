/**
 * OSPrototype.jsx — thin wrapper re-exporting PortalIframe from App.js.
 *
 * R-91 CP-APP-JS-UNIFY: the V8 substitution engine and PortalIframe
 * component now live physically in App.js (required by 63 sealed backend
 * invariants that pin text-substrings against App.js file bytes).
 * This file exists only as a re-export for the pod_shell mirror
 * (9 pages files inventory) and any legacy import references.
 */
import { PortalIframe } from "@/App";

export default PortalIframe;
