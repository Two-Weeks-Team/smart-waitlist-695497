"use client";

import { useEffect, useState } from "react";
import { fetchAnalyticsSummary, fetchWaitlist, markPartyReady } from "@/lib/api";
import { WaitlistTable } from "@/components/WaitlistTable";
import { AnalyticsCards } from "@/components/AnalyticsCards";
import { AiOpsPanel } from "@/components/AiOpsPanel";

const TENANT_ID = process.env.NEXT_PUBLIC_DEMO_TENANT_ID || "demo-tenant-id";
const STAFF_TOKEN = process.env.NEXT_PUBLIC_STAFF_TOKEN || "demo-staff-token";

export default function Page() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [waitlist, setWaitlist] = useState<any[]>([]);
  const [analytics, setAnalytics] = useState<any | null>(null);
  const [actionBusyId, setActionBusyId] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const [w, a] = await Promise.all([
        fetchWaitlist(TENANT_ID, STAFF_TOKEN),
        fetchAnalyticsSummary(TENANT_ID, STAFF_TOKEN),
      ]);
      setWaitlist(w.items || []);
      setAnalytics(a.metrics || null);
    } catch (e: any) {
      setError(e.message || "Failed to load dashboard.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const handleReady = async (partyId: string) => {
    setActionBusyId(partyId);
    try {
      await markPartyReady(TENANT_ID, partyId, STAFF_TOKEN);
      await load();
    } catch (e: any) {
      setError(e.message || "Failed to mark party ready.");
    } finally {
      setActionBusyId(null);
    }
  };

  return (
    <main className="container">
      <header className="header">
        <h1>Smart Waitlist</h1>
        <p>Host Dashboard · Live queue + AI-driven decisions</p>
      </header>

      {error && <div className="error">{error}</div>}

      <AnalyticsCards metrics={analytics} loading={loading} />

      <AiOpsPanel waitlist={waitlist} />

      <section className="panel">
        <div className="panel-head">
          <h2>Active Waitlist</h2>
          <button onClick={load} disabled={loading}>
            Refresh
          </button>
        </div>
        <WaitlistTable
          rows={waitlist}
          loading={loading}
          actionBusyId={actionBusyId}
          onMarkReady={handleReady}
        />
      </section>
    </main>
  );
}
