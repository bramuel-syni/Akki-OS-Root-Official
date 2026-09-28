import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { OwnerMarkup } from './OwnerMarkup';
import { NexusFragment } from './NexusFragment';
import oldSource from './generated/os.json';

const nodes = function* (list) { for(const n of list){if(typeof n==='object'){yield n;yield* nodes(n.children||[]);}} };
test('source header actions are composed at the real old-header parent, including the bell',()=>{
  const header=[...nodes(oldSource.nodes)].find(n=>n.line===31&&n.tag==='div');
  const model={rolePerson:'TEST operator',roleDept:'TEST scope',roleInitials:'TO',topBellToggle:()=>{},topBellOpen:true,
    topBellTitle:'Work notices',topBellHasCount:true,topBellCount:'1',topBellMarkAll:()=>{},topBellItems:[{key:'TEST',headline:'TEST-held work',kind:'Work held',source:'Work record',hasReason:true,reason:'Admission missing',time:'now',link:'View record',onOpen:()=>{}}]};
  const markup=renderToStaticMarkup(<OwnerMarkup template={{nodes:[header]}} surface="os" model={model} slots={{36:<NexusFragment name="headerActions" model={model} onUnbound={()=>{}}/>}} onUnbound={()=>{}}/>);
  expect(markup).toContain('data-proto-line="nexus-38"');expect(markup).toContain('TEST-held work');expect(markup).toContain('View record');
  expect(markup).not.toContain('data-proto-line="38"');
});