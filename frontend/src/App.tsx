import { useEffect, useState } from "react";
import { client } from "./api/client";
import type { components } from "./api/schema";

type InvestigationList = components["schemas"]["InvestigationList"];

function App() {
  const [list, setList] = useState<InvestigationList | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    client.GET("/investigations").then(({ data, error: fetchError }) => {
      if (fetchError) {
        setError(JSON.stringify(fetchError));
      } else if (data) {
        setList(data);
      }
    });
  }, []);

return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow p-8 max-w-sm w-full">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">Writer's Workshop</h1>
        {error ? (
          <p className="text-red-600 text-sm">Error: {error}</p>
        ) : !list ? (
          <p className="text-gray-400 text-sm">Loading…</p>
        ) : list.investigations.length === 0 ? (
          <p className="text-gray-400 text-sm">No investigations yet.</p>
        ) : (
          <ul className="space-y-1">
            {list.investigations.map((inv) => (
              <li key={inv.id} className="text-gray-800">
                {inv.title} — {new Date(inv.created_at).toLocaleDateString()}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;
