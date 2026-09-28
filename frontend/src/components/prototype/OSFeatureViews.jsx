import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, ArrowRight, Eye, Users, Target, LayoutGrid, LockKeyhole } from 'lucide-react';
import { watchSections } from './osHierarchy';

const support = {
  team: { title: 'My Team', icon: Users, status: 'Team records unavailable', text: 'No admitted team roster is connected to this workspace.' },
  goals: { title: 'Company Goals', icon: Target, status: 'Company goals unavailable', text: 'No admitted goals or performance measures are connected to this workspace.' },
  board: { title: 'Board', icon: LayoutGrid, status: 'Board records unavailable', text: 'No admitted board packs, minutes or responses are connected to this workspace.' },
};

export const WorkSupportView = ({ section }) => {
  const view = support[section];
  if (!view) return null;
  const Icon = view.icon;
  return <section className="os-feature-content" data-testid={`my-work-${section}-view`} aria-labelledby={`my-work-${section}-title`}>
    <Icon size={22} strokeWidth={1.5} aria-hidden="true" />
    <h1 id={`my-work-${section}-title`} data-testid={`my-work-${section}-title`}>{view.title}</h1>
    <div className="os-feature-unavailable" role="status" data-testid={`my-work-${section}-unavailable`}>
      <h2>{view.status}</h2><p>{view.text}</p>
    </div>
  </section>;
};

export const GreyMirrorWorkspace = ({ section }) => {
  const overview = section === 'overview';
  const selected = watchSections.find(s => s.key === section) || watchSections[0];
  return <section className="os-feature-content os-mirror-workspace" data-testid="grey-mirror-workspace">
    <header className="os-feature-header">
      <Link className="os-feature-back" data-testid="grey-mirror-back" to={overview ? '/os?nav=admin&app=greymirror' : '/os/admin/greymirror'}><ArrowLeft size={14} aria-hidden="true" />Back</Link>
      <div data-testid="grey-mirror-parent-title">Grey Mirror</div><span>Manage Estate</span>
    </header>
    {overview ? <>
      <h1 data-testid="grey-mirror-title">Grey Mirror</h1>
      <Link className="os-feature-entry" data-testid="grey-mirror-watch-open" to={watchSections[0].path}>
        <Eye size={21} strokeWidth={1.5} aria-hidden="true" /><span>The Watch</span><ArrowRight size={16} aria-hidden="true" />
      </Link>
    </> : <>
      <nav aria-label="Grey Mirror hierarchy" className="os-feature-breadcrumb" data-testid="watch-breadcrumb">
        <Link to="/os/admin/greymirror" data-testid="watch-grey-mirror-link">Grey Mirror</Link><span aria-hidden="true">/</span><span>The Watch</span>
      </nav>
      <h1 data-testid="watch-title">The Watch</h1>
      <nav className="os-feature-tabs" aria-label="The Watch views" data-testid="watch-navigation">
        {watchSections.map(view => <Link key={view.key} to={view.path} aria-current={selected.key === view.key ? 'page' : undefined}
          data-testid={`watch-${view.key}-link`}>{view.label}</Link>)}
      </nav>
      <section aria-labelledby="watch-subview-title" data-testid={`watch-${selected.key}-view`}>
        <h2 id="watch-subview-title" data-testid="watch-subview-title">{selected.label}</h2>
        <div className="os-feature-unavailable" role="status" data-testid="watch-evidence-unavailable">
          <LockKeyhole size={19} aria-hidden="true" /><h2>Watch evidence unavailable</h2>
          <p>No current, tenant-admitted Watch record is connected. Monitoring, notices and decisions are not verified here.</p>
        </div>
      </section>
    </>}
  </section>;
};