import { useEffect, useState } from "react";
import { client } from "./api/client";
import type { components } from "./api/schema";

type HealthResponse = components["schemas"]["HealthResponse"];

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    client.GET("/health").then(({ data, error: fetchError }) => {
      if (fetchError) {
        setError(JSON.stringify(fetchError));
      } else if (data) {
        setHealth(data);
      }
    });
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow p-8 max-w-sm w-full">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">Writer's Workshop</h1>
        {error && <p className="text-red-600 text-sm">Error: {error}</p>}
        {health ? (
          <div>
            <p className="text-green-600 font-medium">{health.status}</p>
            <p className="text-gray-600 text-sm mt-1">{health.message}</p>
          </div>
        ) : !error ? (
          <p className="text-gray-400 text-sm">Connecting to backend…</p>
        ) : null}
      </div>
    </div>
  );
}

export default App;
