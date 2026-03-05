type Props = {
  metrics: any;
  loading: boolean;
};

export function AnalyticsCards({ metrics, loading }: Props) {
  return (
    <section className="grid">
      <div className="card">
        <div className="muted">Parties Seated (7d)</div>
        <div className="value">{loading ? "--" : metrics?.parties_seated ?? 0}</div>
      </div>
      <div className="card">
        <div className="muted">Avg Wait</div>
        <div className="value">{loading ? "--" : `${Math.round(metrics?.avg_wait_minutes ?? 0)}m`}</div>
      </div>
      <div className="card">
        <div className="muted">No-show Rate</div>
        <div className="value">
          {loading
            ? "--"
            : `${Math.round(((metrics?.parties_noshow ?? 0) / Math.max(metrics?.parties_created ?? 1, 1)) * 100)}%`}
        </div>
      </div>
      <div className="card">
        <div className="muted">Peak Hour</div>
        <div className="value">{loading ? "--" : metrics?.peak_hour_local ?? "--:--"}</div>
      </div>
    </section>
  );
}
