import React from 'react';
import source from './generated/nexus-fragments.json';
import { OwnerMarkup } from './OwnerMarkup';

const templates = Object.fromEntries(Object.entries(source.fragments).map(([key, node]) => [key, { nodes: [node] }]));

export const NexusFragment = ({ name, ...props }) => <OwnerMarkup template={templates[name]} surface={`nexus-${name}`} fragment {...props} />;
export const nexusSourceHash = source.source_sha256;