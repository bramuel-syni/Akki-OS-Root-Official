import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

export const LegacyFeatureRedirect = ({ to }) => {
  const { search, hash } = useLocation();
  return <Navigate to={{ pathname: to, search, hash }} replace />;
};