import { useEffect, useState } from 'react';
import { useCensusWorkspace } from '@/components/census/useCensusWorkspace';
import { fetchMe, login } from '@/lib/apiClient';

export function usePrototypeSession() {
  const census = useCensusWorkspace();
  const principalId = census.data?.principal_id;
  const [user, setUser] = useState(null);
  useEffect(() => {
    let active = true;
    if (!principalId) { setUser(null); return undefined; }
    fetchMe().then(response => { if (active) setUser(response.user || response.identity || response); }).catch(() => { if (active) setUser(null); });
    return () => { active = false; };
  }, [principalId]);
  const name = user?.name || user?.email || (census.data ? 'Admitted operator' : 'Not signed in');
  return { ...census, user: census.data ? { ...user, name, roles: census.data.roles } : null,
    login: async (email, password) => { await login(email, password); window.dispatchEvent(new Event('akki-session-changed')); },
    logout: () => { sessionStorage.removeItem('akki_access_token'); sessionStorage.removeItem('akki_refresh_token'); window.dispatchEvent(new Event('akki-session-changed')); },
  };
}