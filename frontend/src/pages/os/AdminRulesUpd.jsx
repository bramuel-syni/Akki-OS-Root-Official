import React from 'react';
import { useNavigate } from 'react-router-dom';
import { OwnerWorkspace } from '@/components/prototype/OwnerWorkspace';
import { usePrototypeSession } from '@/components/prototype/usePrototypeSession';

export default function AdminRulesUpd() {
  const session = usePrototypeSession(), navigate = useNavigate();
  const model = { isApprovalsGroup: true, approvalsTitle: 'Rules Updates', approvalsOneliner: '',
    approvalsTilesView: [['Spend Requests', '/os/admin/spendreq'], ['Rules Updates', '/os/admin/rulesupd'], ['Model Approval', '/os/admin/modeladmission']].map(([label, path]) => ({ key: path, label, border: label === 'Rules Updates' ? 'var(--blue)' : 'var(--line)', bg: label === 'Rules Updates' ? 'var(--blue)' : '#fff', color: label === 'Rules Updates' ? '#fff' : 'var(--ink2)', onClick: () => navigate(path) })) };
  return <OwnerWorkspace session={session} title="Rules Updates" group="Approvals" section="approvals" model={model} returnTo="/os?nav=admin" enhance={{ 4298: { hidden: true } }} slots={{ 4306: <div data-testid="admin-rulesupd-honest-gap"><h2 style={{ font: '400 20px var(--head)', marginBottom: 12 }} data-testid="admin-rulesupd-honest-gap-label">Rule review is not available here yet</h2><p style={{ fontSize: 13, lineHeight: 1.6, color: 'var(--ink3)' }} data-testid="admin-rulesupd-honest-gap-body">Changes cannot be submitted or approved on this page. Contact your rule owner to arrange a review.</p></div> }} />;
}