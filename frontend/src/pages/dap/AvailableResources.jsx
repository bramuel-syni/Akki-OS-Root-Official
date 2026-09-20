import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchComputeEstate, fetchModels, fetchFullRecord, fetchSkillFilesState } from "@/lib/apiClient";
import LoadingState from "@/components/shared/LoadingState";
import TransportError from "@/components/shared/TransportError";
import HonestEmpty from "@/components/shared/HonestEmpty";

/**
 * Available Resources — DAP §4.4
 * 4 sub-views: Compute, Base Models, Trained Models, Skills
 * All wired to real endpoints.
 */

function ComputeView() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchComputeEstate()
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingState message="Reading the compute estate…" />;
  if (error) return <TransportError error={error} />;
  if (!data || !data.hosts || data.hosts.length === 0) {
    return <HonestEmpty message="No compute resources are attached to the estate. This list will populate as hosts are connected." />;
  }

  return (
    <div data-testid="available-compute">
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="rounded-lg border p-4" style={{ borderColor: "var(--line)", background: "white" }}>
          <p className="text-xs font-medium mb-1" style={{ color: "var(--ink3)" }}>Hosts attached</p>
          <p data-testid="compute-host-count" className="text-2xl font-semibold" style={{ color: "var(--ink)" }}>{data.rollup?.host_count || data.hosts.length}</p>
        </div>
        <div className="rounded-lg border p-4" style={{ borderColor: "var(--line)", background: "white" }}>
          <p className="text-xs font-medium mb-1" style={{ color: "var(--ink3)" }}>GPUs total</p>
          <p data-testid="compute-gpu-count" className="text-2xl font-semibold" style={{ color: "var(--ink)" }}>{data.rollup?.gpu_count_total ?? "not measured"}</p>
        </div>
        <div className="rounded-lg border p-4" style={{ borderColor: "var(--line)", background: "white" }}>
          <p className="text-xs font-medium mb-1" style={{ color: "var(--ink3)" }}>GPU memory</p>
          <p data-testid="compute-gpu-memory" className="text-2xl font-semibold" style={{ color: "var(--ink)" }}>{data.rollup?.gpu_memory_gb_total ? `${Math.round(data.rollup.gpu_memory_gb_total)} GiB` : "not measured"}</p>
        </div>
      </div>
      <h3 className="text-sm font-medium mb-3" style={{ color: "var(--ink)" }}>Hosts</h3>
      <div className="space-y-2">
        {data.hosts.map((host, i) => (
          <div
            key={i}
            data-testid={`compute-host-${i}`}
            className="flex items-center justify-between rounded-lg border p-4"
            style={{ borderColor: "var(--line)", background: "white" }}
          >
            <div>
              <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>{host.name}</p>
              <p className="text-xs" style={{ color: "var(--ink3)" }}>
                {host.gpu_model?.replace(/^NVIDIA\s+/i, "")} · {host.gpu_count} GPU{host.gpu_count > 1 ? "s" : ""} · {Math.round(host.gpu_memory_gb_per_gpu)} GiB each
              </p>
            </div>
            <span
              className="text-xs px-2 py-0.5 rounded-full"
              style={{ color: "var(--sage)", background: "rgba(29,122,110,.12)" }}
            >
              {host.readiness}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

function BaseModelsView() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchModels()
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingState message="Reading the model registry…" />;
  if (error) return <TransportError error={error} />;

  const models = data?.purchased_llms || [];
  const open = data?.open_weight_bases || [];
  const all = [...models, ...open];

  if (all.length === 0) {
    return <HonestEmpty message="No models are registered. This list will populate as models are connected and admitted." />;
  }

  return (
    <div data-testid="available-base-models">
      <p className="text-sm mb-4" style={{ color: "var(--ink2)" }}>{data?.total ?? all.length} models registered</p>
      <div className="space-y-2">
        {all.map((m, i) => (
          <div
            key={i}
            data-testid={`model-row-${i}`}
            className="flex items-center justify-between rounded-lg border p-4"
            style={{ borderColor: "var(--line)", background: "white" }}
          >
            <div>
              <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>{m.model_id}</p>
              <p className="text-xs" style={{ color: "var(--ink3)" }}>
                {m.provider} · {m.role || m.custody_kind || "model"}
              </p>
            </div>
            <span className="text-xs" style={{ color: "var(--ink3)" }}>
              {m.connected_at ? new Date(m.connected_at).toLocaleDateString() : ""}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

function TrainedModelsView() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFullRecord()
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingState message="Reading the model record…" />;
  if (error) return <TransportError error={error} />;

  const models = data?.models || [];
  if (models.length === 0) {
    return <HonestEmpty message="No trained models on record. This list will populate as training runs complete." />;
  }

  return (
    <div data-testid="available-trained-models">
      <p className="text-sm mb-4" style={{ color: "var(--ink2)" }}>{models.length} trained models on record</p>
      <div className="space-y-2">
        {models.map((m, i) => (
          <div
            key={i}
            data-testid={`trained-model-${i}`}
            className="flex items-center justify-between rounded-lg border p-4"
            style={{ borderColor: "var(--line)", background: "white" }}
          >
            <div>
              <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>{m.run_name || m.run_id}</p>
              <p className="text-xs" style={{ color: "var(--ink3)" }}>
                {m.version} · {m.state}
              </p>
            </div>
            {m.state_evidence && (
              <span
                className="text-[10px] px-2 py-0.5 rounded font-mono"
                style={{ color: "var(--ink3)", background: "var(--surface)" }}
              >
                {m.state_evidence.split("/").pop()}
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function SkillsView() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSkillFilesState()
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingState message="Reading the skill files…" />;
  if (error) return <TransportError error={error} />;

  const skills = data?.skills || [];
  if (skills.length === 0) {
    return (
      <HonestEmpty message="No skill files have been built yet. This list will populate as skills are developed against the estate." />
    );
  }

  return (
    <div data-testid="available-skills">
      <p className="text-sm mb-4" style={{ color: "var(--ink2)" }}>{skills.length} skills available</p>
      <div className="space-y-2">
        {skills.map((s, i) => (
          <div key={i} data-testid={`skill-row-${i}`} className="rounded-lg border p-4" style={{ borderColor: "var(--line)", background: "white" }}>
            <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>{s.skill_id || s.name || `Skill ${i + 1}`}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

const VIEW_MAP = {
  compute: { title: "Compute", Component: ComputeView },
  "base-models": { title: "Base Models", Component: BaseModelsView },
  "trained-models": { title: "Trained Models", Component: TrainedModelsView },
  skills: { title: "Skills", Component: SkillsView },
};

export default function AvailableResources() {
  const { tab } = useParams();
  const current = VIEW_MAP[tab] || VIEW_MAP["compute"];
  const Component = current.Component;

  return (
    <div data-testid="available-resources" className="max-w-5xl mx-auto px-8 py-10">
      <h1
        data-testid="available-resources-title"
        className="text-xl font-semibold mb-1"
        style={{ color: "var(--ink)", fontFamily: "var(--head, Iowan Old Style, Georgia, serif)" }}
      >
        Available Resources
      </h1>
      <p className="text-sm mb-6" style={{ color: "var(--ink3)" }}>
        {current.title}
      </p>
      <Component />
    </div>
  );
}
