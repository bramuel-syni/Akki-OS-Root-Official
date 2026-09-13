READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# canon_trust_domain_description_v1_requirements.md

**Source.** `canon/drops/20260909/raw/files_14.zip` → `Trust_Domain_Description_v1.docx` sha256 `0d9fc546c9…` · 12,729 B. Extracted text `canon/drops/20260909/extracted/text/Trust_Domain_Description_v1.txt`.
**Spec id.** `trust_domains_v1`. Draft for owner ratification · closes **Doc 0 G-12**.
**R-5 resolution (verbatim, Table 0 R1).** *"Dedicated infrastructure per tenant. Grounded directly in Akki_Appliance_Assembly_Spec_RevA, already ratified … per-unit serials in the signed test record. The deployment model was already decided; this document is the first to state it as the answer to R-5."*

---

## §A · The Three Domains (§2 verbatim)

- **TD-1** — The Platform Domain: *"the appliance's own governed core: the six engines, the Watch, the Ledger, the Rules Service, running inside the sealed unit. Bounded by the appliance's own physical and network perimeter (Akki_Appliance_Assembly_Spec_RevA CR-1: dual-port ESTATE/WAN separation; B-5: front panel exposes only PORT-A, PORT-B, power, status — nothing else)."*
- **TD-2** — The Tenant's Estate Domain: *"the customer's own data and systems, reached only through PORT-A (ESTATE), never through the appliance's WAN-facing side. This domain is, by the appliance's physical design, not shared with any other tenant — there is no code path for it to be, since there is no other tenant's data on the same unit."*
- **TD-3** — The External-Party Domain: *"any AI lab, research institution, or buyer reaching the estate through DAP, over PORT-B (WAN). This is the domain DAP-5 already governs: no shared identifier resolution, store, or credential with the estate's own domain. Multiple external parties may share this domain's outer boundary (the appliance's WAN port) while remaining mutually isolated within it."*

## §B · Managed Interfaces (§3 · Table 1 verbatim)

| Boundary | Managed interface |
|---|---|
| Platform ↔ Tenant's Estate | PORT-A (ESTATE), colour-keyed. Governed by SyniSense's chokepoint (SFP-4, Custody Floor). |
| Platform ↔ External Party | PORT-B (WAN), colour-keyed. Governed by full DAP surface — admission (DAP-1, DAP-12), crossing profiles (DAP §4), release budget (SFP-6). |
| Platform ↔ Watch's own domain | Verdict interface (A2). Not a network port; software seam with same separation discipline. |
| **Tenant's Estate ↔ External Party** | **None, directly.** *"This is the boundary the whole architecture exists to prevent — an external party never has a path to the estate that does not pass through the Platform Domain's own governance."* |

verbatim §3 tail: *"The fourth row is the one worth stating explicitly rather than leaving implicit … a direct path would be exactly the side door Promise #26's single-crossing doctrine forbids."*

## §C · Multi-Estate Tenants (§4 verbatim)

*"Where one customer operates more than one estate — RMS's own case, given DigiCow and the broadcast archive are already distinct estates on record — each estate is its own instance of the Tenant's Estate Domain, on its own appliance or its own logical partition of one … TD-2 is stated per estate, not per customer."*

## §D · Standing (§5 verbatim)

*"This description supersedes DAP-5 as the general statement of trust domains; DAP-5 remains correct and is now read as this document's instance for the External-Party Domain specifically, not a separate rule."*

## §E · Milestone binding

- **M2** — TD-1..TD-3 fold into W-DOC0-ATTR3-TRIAD (governed triad, principal/asset/operation catalogs) and W-DOC0-ATTR12 fan-in.
- **M1** — DAP-5 unchanged; TD-3 lands as the composition-anchor for W-DAP-STACK 2B (trust-domain separation).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
