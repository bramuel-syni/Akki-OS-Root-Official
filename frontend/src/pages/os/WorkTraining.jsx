import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, RefreshCw } from 'lucide-react';
import { CensusAccess } from '@/components/census/CensusAccess';
import { usePrototypeSession } from '@/components/prototype/usePrototypeSession';
import { useTrainingLab } from '@/components/training/useTrainingLab';
import { BaselineCard } from '@/components/training/BaselineCard';
import { CorpusCard, ReferenceCard } from '@/components/training/CorpusCard';
import { LanguagesCard } from '@/components/training/LanguagesCard';
import '@/components/census/census.css';
import '@/components/estate/estate.css';
import '@/components/media/media.css';
import '@/components/training/training.css';

export default function WorkTraining() {
  const session = usePrototypeSession(); const identity = session.data?.principal_id;
  const canOperate = session.data?.roles?.some(r => ['operator', 'master_admin'].includes(r)); const isRms = session.data?.tenant_id === 'RMS';
  const lab = useTrainingLab(identity);
  return <main className="estate training-lab" data-testid="work-training-surface">
    <Link className="media-back" to="/os" data-testid="work-training-back"><ArrowLeft size={14} />WorkStudio</Link>
    <header className="estate-header media-header"><div><div className="estate-crumb" data-testid="work-training-breadcrumb">WORKSTUDIO · {session.data?.tenant_id || 'Training lab'}</div><h1 className="estate-title" data-testid="work-training-title">Training lab</h1></div>
      {identity && <div className="estate-actions"><Link className="estate-btn" to="/os/work/media" data-testid="work-training-media">Media library</Link><button className="estate-btn" onClick={lab.reload} data-testid="work-training-refresh"><RefreshCw size={15} />Refresh</button></div>}
    </header>
    {!identity ? <CensusAccess error={session.error} loading={session.loading} retry={session.reload} /> : <div className="media-body lab-body">
      <p className="lab-intro" data-testid="work-training-intro">Baselines, measurements and plans. Nothing on this page starts training; every training request stays held until you approve it.</p>
      {lab.error && <p role="alert" className="estate-alert" data-testid="work-training-error">{lab.error}</p>}
      <BaselineCard lab={lab} canOperate={canOperate} />
      <div className="lab-pair"><ReferenceCard canOperate={canOperate} /><CorpusCard lab={lab} canOperate={canOperate} isRms={isRms} /></div>
      <LanguagesCard lab={lab} canOperate={canOperate} isRms={isRms} />
      <footer className="media-footer"><span data-testid="work-training-private-status">Private · {session.data.tenant_id}</span><p data-testid="work-training-authority">Training is never started from this page. Approval, recipe and compute cap remain yours.</p></footer>
    </div>}
  </main>;
}
