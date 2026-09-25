import React from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';

export function PrototypeNotice({ message, onClose }) {
  return <Dialog open={Boolean(message)} onOpenChange={open => !open && onClose()}><DialogContent data-testid="prototype-notice-dialog" className="prototype-notice">
    <DialogHeader><DialogTitle data-testid="prototype-notice-title">{message?.title}</DialogTitle><DialogDescription data-testid="prototype-notice-body">{message?.body}</DialogDescription></DialogHeader>
    <button data-testid="prototype-notice-close" className="prototype-control" onClick={onClose}>Close</button>
  </DialogContent></Dialog>;
}

export function PrototypeAccount({ open, session, navigate, close }) {
  if (!open) return null;
  return <div className="prototype-account" data-testid="prototype-account-menu" role="dialog" aria-label="Your account">
    <strong data-testid="prototype-account-name">{session.user?.name || 'Not signed in'}</strong>
    <span data-testid="prototype-account-tenant">{session.data?.tenant_id || 'No admitted tenant'}</span>
    <button data-testid="prototype-account-os" onClick={() => { close(); navigate('/os'); }}>Akki OS</button>
    <button data-testid="prototype-account-dap" onClick={() => { close(); navigate('/dap'); }}>Data Access Portal</button>
    {session.user && <button data-testid="prototype-account-signout" onClick={() => { close(); session.logout(); }}>Sign out</button>}
    <button data-testid="prototype-account-close" onClick={close}>Close</button>
  </div>;
}