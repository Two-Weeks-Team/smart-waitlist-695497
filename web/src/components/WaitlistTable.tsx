type Props = {
  rows: any[];
  loading: boolean;
  actionBusyId: string | null;
  onMarkReady: (partyId: string) => void;
};

export function WaitlistTable({ rows, loading, actionBusyId, onMarkReady }: Props) {
  if (loading) return <p>Loading waitlist...</p>;
  if (!rows.length) return <p>No active parties.</p>;

  return (
    <table>
      <thead>
        <tr>
          <th>Pos</th>
          <th>Name</th>
          <th>Party</th>
          <th>Quoted</th>
          <th>No-show AI</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((r) => {
          const risk = r.noshow_prob_current ?? 0;
          const cls = risk >= 0.6 ? "badge-high" : risk >= 0.3 ? "badge-medium" : "badge-low";
          return (
            <tr key={r.id}>
              <td>{r.position}</td>
              <td>{r.name || "Guest"}</td>
              <td>{r.party_size}</td>
              <td>~{r.quoted_wait_minutes ?? "--"} min</td>
              <td>
                <span className={`badge ${cls}`}>{Math.round(risk * 100)}%</span>
              </td>
              <td>
                <button disabled={actionBusyId === r.id} onClick={() => onMarkReady(r.id)}>
                  {actionBusyId === r.id ? "Sending..." : "Ready + SMS"}
                </button>
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
