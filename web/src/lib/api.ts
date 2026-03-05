const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8080/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
    cache: "no-store",
  });

  if (!res.ok) {
    let msg = `Request failed: ${res.status}`;
    try {
      const data = await res.json();
      msg = data?.error?.message || msg;
    } catch {}
    throw new Error(msg);
  }

  return res.json();
}

export function fetchWaitlist(tenantId: string, token: string) {
  return request<{ items: any[] }>(`/tenants/${tenantId}/waitlist`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export function fetchAnalyticsSummary(tenantId: string, token: string) {
  const from = new Date(Date.now() - 1000 * 60 * 60 * 24 * 7).toISOString().slice(0, 10);
  const to = new Date().toISOString().slice(0, 10);
  return request<{ metrics: any }>(`/tenants/${tenantId}/analytics/summary?from=${from}&to=${to}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export function markPartyReady(tenantId: string, partyId: string, token: string) {
  return request(`/tenants/${tenantId}/parties/${partyId}/ready`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify({ send_sms: true }),
  });
}
