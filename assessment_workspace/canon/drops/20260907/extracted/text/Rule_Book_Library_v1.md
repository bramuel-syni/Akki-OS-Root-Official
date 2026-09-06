## sheet: `Index` · rows=10 · max_col=7

| Rule Book Library — v1 Index |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| Each rule book is atomic (one regulatory domain). Profiles bundle rule books per business type — see Profiles sheet. Status: FULL = every rule written, cited, and checked against source text. SKELETON = sources named, sections and expected rule count set, rules not yet written. |  |  |  |  |  |  |
| Book ID | Rule book | Source standards / regulations | Free to verify? | Sections | Expected rules | v1 status |
| RB-PDP | Personal Data Protection | Kenya Data Protection Act 2019 (primary) · Data Protection (General) Regulations 2021 · GDPR (EU) 2016/679 as international reference · POPIA (ZA) and NDPA 2023 (NG) noted as regional variants | Yes — all | Lawful basis & consent · Data-subject rights · Sensitive-category data · Cross-border transfer · Retention & erasure · Breach notification (72h) · Automated decisions (s.35 / Art.22) · DPO & accountability | 18–22 | FULL — next |
| RB-AIG | AI-System Governance | EU AI Act 2024/1689 (Arts. 9–15 high-risk obligations, Art. 14 oversight) · ISO/IEC 42001:2023 (paywalled) · NIST AI RMF 1.0 · ISO/IEC TR 5469:2024 (paywalled) | EU AI Act, NIST: yes · ISO: paywalled | Risk classification · Data & training governance · Human oversight (5 capabilities) · Transparency & record-keeping · Accuracy, robustness, cybersecurity · Post-market monitoring · Determinism boundary (platform-native) | 16–20 | FULL — next |
| RB-FIN | Financial Data Access | PCI DSS v4.0 (card data) · CBK Prudential Guidelines & Banking Act (Kenya) · BCBS 239 (risk-data aggregation) · EU DORA 2022/2554 (operational resilience) · IRA guidelines (insurance variant) | PCI DSS, BCBS 239, DORA, CBK: yes | Cardholder data handling · Access control & least privilege · Data aggregation & lineage · Operational resilience & incident reporting · Third-party / ICT risk · Retention · Insurance variant (IRA) | 18–24 | SKELETON |
| RB-HLT | Health Data | Kenya Health Act 2017 · DPA 2019 s.44 (health data as sensitive category) · Digital Health Act 2023 (Kenya) · HIPAA (US) as international reference | Kenya Acts, HIPAA: yes | Patient consent & confidentiality · De-identification standard · Access by role · Research use of clinical data · Retention · Breach & disclosure | 14–18 | SKELETON |
| RB-MED | Media & Archive Rights | Copyright Act (Kenya, Cap 130) · Kenya Information and Communications Act & CA regulations · KFCB classification guidelines · Contributor / talent consent · Licensing for content acquisition | Yes — Kenya Law | Archive rights & ownership · Contributor consent & likeness · Licensing & acquisition terms · Training-use permission (rights-declared corpus, Doc 17 A17.15) · Broadcast regulatory · Retention & takedown | 14–18 | SKELETON — first industry book after base |
| RB-RES | Research & Academic Data | NACOSTI research licensing (Kenya) · Institutional ethics review · DPA 2019 research exemptions & conditions · FAIR data principles · Funder data-management requirements | Mostly yes | Ethics approval & consent · Anonymisation for research · Data-management plans · Open-data vs restricted · Secondary use · Retention | 12–16 | SKELETON |
| Skeletons noted in Profiles but not yet indexed as books: agricultural data (agri-tech), telecoms regulator (Communications Authority), public-sector records. Each is a v2 candidate; none blocks a v1 profile because all three fall back to the base bundle. |  |  |  |  |  |  |

## sheet: `Profiles` · rows=13 · max_col=8

| Business-Type Profiles — which rule books the Rules Service recommends at onboarding (RBM-15, RBM-16) |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| Business type | RB-PDP | RB-AIG | RB-FIN | RB-HLT | RB-MED | RB-RES | Industry-specific note |
| Healthcare — hospital / clinic | ● | ● |  | ● |  |  | Health Act + DPA s.44 govern; HIPAA reference only. |
| Media — broadcaster | ● | ● |  |  | ● |  | Archive rights and contributor consent are the binding layer; RMS is the live deployment. |
| Media — content acquisition / production | ● | ● |  |  | ● |  | RB-MED with licensing emphasis; acquisition terms bind training-use permission. |
| Financial services — bank | ● | ● | ● |  |  |  | CBK prudential guidelines; PCI DSS where card data is held. |
| Financial services — insurer | ● | ● | ● |  |  |  | RB-FIN insurance variant — IRA guidelines replace CBK. |
| Agriculture / agri-tech | ● | ● |  |  |  |  | Base bundle; agricultural-data book is a v2 skeleton (DigiCow is the live estate). |
| University / research institution | ● | ● |  |  |  | ● | NACOSTI licensing and ethics review are binding. |
| Telecommunications | ● | ● |  |  |  |  | Base bundle; CA-regulator book is a v2 skeleton. |
| Government / public sector | ● | ● |  |  |  |  | Base bundle; public-records book is a v2 skeleton. |
| Other / not listed | ● | ● |  |  |  |  | Base bundle + recorded finding (RBM-16). |
| RB-PDP and RB-AIG appear in every profile — the base bundle. That is why they are built in full first. |  |  |  |  |  |  |  |

## sheet: `RB-PDP` · rows=12 · max_col=8

| RB-PDP — Personal Data Protection |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| Sources: Kenya DPA 2019 · DP (General) Regulations 2021 · GDPR as reference · POPIA / NDPA noted |  |  |  |  |  |  |  |
| Status: FULL build next — rules to be written against the Act's text, each with section citation. |  |  |  |  |  |  |  |
| Rule ID | Section | Statement (plain language) | Enforced by (Akki component) | Enforcement class | Assessment procedure | Source clause | Status |
|  | Lawful basis & consent | — to be written — |  |  |  |  |  |
|  | Data-subject rights | — to be written — |  |  |  |  |  |
|  | Sensitive-category data | — to be written — |  |  |  |  |  |
|  | Cross-border transfer | — to be written — |  |  |  |  |  |
|  | Retention & erasure | — to be written — |  |  |  |  |  |
|  | Breach notification | — to be written — |  |  |  |  |  |
|  | Automated decisions | — to be written — |  |  |  |  |  |
|  | DPO & accountability | — to be written — |  |  |  |  |  |

## sheet: `RB-AIG` · rows=11 · max_col=8

| RB-AIG — AI-System Governance |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| Sources: EU AI Act 2024/1689 · ISO/IEC 42001 (paywalled) · NIST AI RMF 1.0 · ISO/IEC TR 5469 (paywalled) |  |  |  |  |  |  |  |
| Status: FULL build next — EU AI Act and NIST clauses verified against published text; ISO cited by clause number. |  |  |  |  |  |  |  |
| Rule ID | Section | Statement (plain language) | Enforced by (Akki component) | Enforcement class | Assessment procedure | Source clause | Status |
|  | Risk classification | — to be written — |  |  |  |  |  |
|  | Data & training governance | — to be written — |  |  |  |  |  |
|  | Human oversight | — to be written — |  |  |  |  |  |
|  | Transparency & record-keeping | — to be written — |  |  |  |  |  |
|  | Accuracy, robustness, cybersecurity | — to be written — |  |  |  |  |  |
|  | Post-market monitoring | — to be written — |  |  |  |  |  |
|  | Determinism boundary | — to be written — |  |  |  |  |  |

## sheet: `RB-FIN` · rows=11 · max_col=8

| RB-FIN — Financial Data Access |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| Sources: PCI DSS v4.0 · CBK Prudential Guidelines · BCBS 239 · EU DORA · IRA guidelines |  |  |  |  |  |  |  |
| Status: SKELETON — sections set; rules not yet written. |  |  |  |  |  |  |  |
| Rule ID | Section | Statement (plain language) | Enforced by (Akki component) | Enforcement class | Assessment procedure | Source clause | Status |
|  | Cardholder data handling | — to be written — |  |  |  |  |  |
|  | Access control & least privilege | — to be written — |  |  |  |  |  |
|  | Data aggregation & lineage | — to be written — |  |  |  |  |  |
|  | Operational resilience & incident reporting | — to be written — |  |  |  |  |  |
|  | Third-party / ICT risk | — to be written — |  |  |  |  |  |
|  | Retention | — to be written — |  |  |  |  |  |
|  | Insurance variant (IRA) | — to be written — |  |  |  |  |  |

## sheet: `RB-HLT` · rows=10 · max_col=8

| RB-HLT — Health Data |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| Sources: Kenya Health Act 2017 · DPA 2019 s.44 · Digital Health Act 2023 · HIPAA reference |  |  |  |  |  |  |  |
| Status: SKELETON. |  |  |  |  |  |  |  |
| Rule ID | Section | Statement (plain language) | Enforced by (Akki component) | Enforcement class | Assessment procedure | Source clause | Status |
|  | Patient consent & confidentiality | — to be written — |  |  |  |  |  |
|  | De-identification standard | — to be written — |  |  |  |  |  |
|  | Access by role | — to be written — |  |  |  |  |  |
|  | Research use of clinical data | — to be written — |  |  |  |  |  |
|  | Retention | — to be written — |  |  |  |  |  |
|  | Breach & disclosure | — to be written — |  |  |  |  |  |

## sheet: `RB-MED` · rows=10 · max_col=8

| RB-MED — Media & Archive Rights |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| Sources: Copyright Act Cap 130 · KICA & CA regulations · KFCB · contributor consent · acquisition licensing |  |  |  |  |  |  |  |
| Status: SKELETON — first industry book after the base pair (RMS live deployment). |  |  |  |  |  |  |  |
| Rule ID | Section | Statement (plain language) | Enforced by (Akki component) | Enforcement class | Assessment procedure | Source clause | Status |
|  | Archive rights & ownership | — to be written — |  |  |  |  |  |
|  | Contributor consent & likeness | — to be written — |  |  |  |  |  |
|  | Licensing & acquisition terms | — to be written — |  |  |  |  |  |
|  | Training-use permission | — to be written — |  |  |  |  |  |
|  | Broadcast regulatory | — to be written — |  |  |  |  |  |
|  | Retention & takedown | — to be written — |  |  |  |  |  |

## sheet: `RB-RES` · rows=10 · max_col=8

| RB-RES — Research & Academic Data |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| Sources: NACOSTI · institutional ethics review · DPA 2019 research conditions · FAIR · funder DMP requirements |  |  |  |  |  |  |  |
| Status: SKELETON. |  |  |  |  |  |  |  |
| Rule ID | Section | Statement (plain language) | Enforced by (Akki component) | Enforcement class | Assessment procedure | Source clause | Status |
|  | Ethics approval & consent | — to be written — |  |  |  |  |  |
|  | Anonymisation for research | — to be written — |  |  |  |  |  |
|  | Data-management plans | — to be written — |  |  |  |  |  |
|  | Open-data vs restricted | — to be written — |  |  |  |  |  |
|  | Secondary use | — to be written — |  |  |  |  |  |
|  | Retention | — to be written — |  |  |  |  |  |
