"""Extract directly referenced original documents; inventory supplemental clauses."""
from pathlib import Path
import hashlib,json,re
from docx import Document
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.table import Table

ROOT=Path('/app'); HERE=Path(__file__).resolve().parent
OUT=HERE/'source_text';OUT.mkdir(exist_ok=True)
inventory=json.loads((HERE/'SOURCE_INVENTORY.json').read_text())
paths=set()
for item in inventory:
    docs=[ROOT/r['path'] for r in item['candidates'] if r['path'].endswith('.docx')]
    paths.update(docs)
paths.update((ROOT/'assessment_workspace/canon/text').glob('Akki_Canon_[1-9]_*.txt'))
aliases={
 '17_20.md':ROOT/'assessment_workspace/canon/w11_batch2_v3/AKKI_Canon_Documents_17_20_v3.docx',
 'wpw.md':ROOT/'assessment_workspace/canon/fixtures/whitepaper_wizard_spec_v1/spec.docx',
}
paths.update(p for p in aliases.values() if p.exists())
paths.add(ROOT/'assessment_workspace/fixtures/files_9_extracted/16_Cross_Cutting_Orchestration.docx')
sources=[]; supplements=[]; seen={}
for path in sorted(paths):
    if not path.exists():continue
    h=hashlib.sha256(path.read_bytes()).hexdigest()
    if h in seen:
        seen[h]['duplicate_byte_paths'].append(str(path.relative_to(ROOT)));continue
    name=f'{path.stem}_{h[:8]}.txt';blocks=[]
    if path.suffix=='.docx':
        d=Document(path)
        for i,c in enumerate(d.element.body.iterchildren(),1):
            if c.tag==qn('w:p'):
                text=Paragraph(c,d).text.strip()
                if text:blocks.append({'anchor':f'B{i}','text':text})
            elif c.tag==qn('w:tbl'):
                for j,row in enumerate(Table(c,d).rows,1):blocks.append({'anchor':f'B{i}R{j}','text':' | '.join(cell.text for cell in row.cells)})
    else:
        blocks=[{'anchor':f'L{i}','text':line.strip()} for i,line in enumerate(path.read_text(errors='replace').splitlines(),1) if line.strip()]
    (OUT/name).write_text('\n\n'.join(f"[{b['anchor']}] {b['text']}" for b in blocks)+'\n')
    row={'source':str(path.relative_to(ROOT)),'sha256':h,'extraction':str((OUT/name).relative_to(ROOT)),'blocks':len(blocks),'duplicate_byte_paths':[]}
    seen[h]=row;sources.append(row)
    for b in blocks:
        text=b['text']
        # An inventory candidate is not automatically an additional adopted rule.
        labelled=re.match(r'^(?:\d+\s+)?(?:R[-‑–]\d+|LIM[-‑–]\d+)\b',text)
        normative=re.search(r'\b(?:MUST|MUST NOT|SHALL|SHALL NOT|never|No .*may|does not claim)\b',text)
        if labelled or normative:
            kind='RULING' if re.match(r'^R[-‑–]\d+',text) else 'LIMITATION' if re.match(r'^LIM[-‑–]\d+',text) else 'NORMATIVE_SOURCE_BLOCK'
            supplements.append({'supplement_id':f'SUP-{len(supplements)+1:04d}','source':row['source'],'source_sha256':h,'anchor':b['anchor'],'kind':kind,'text':text,'scope_note':'Candidate source obligation/limit. May overlap a primary registry row; does not enlarge adopted rule count without mapping.','assessment':'PENDING_SEMANTIC_MAPPING'})
(HERE/'SOURCE_CORPUS.json').write_text(json.dumps(sources,indent=2)+'\n')
(HERE/'SOURCE_ALIASES.json').write_text(json.dumps({k:{'original':str(v.relative_to(ROOT)),'relationship':'corresponding original DOCX; original markdown line numbers NOT inherited'} for k,v in aliases.items()},indent=2)+'\n')
(HERE/'SUPPLEMENTAL_INVENTORY.json').write_text(json.dumps(supplements,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'unique_source_bodies':len(sources),'supplement_candidates':len(supplements),'labelled_rulings':sum(x['kind']=='RULING' for x in supplements),'labelled_limits':sum(x['kind']=='LIMITATION' for x in supplements)},indent=2))