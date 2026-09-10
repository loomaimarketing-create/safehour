import { useEffect, useMemo, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

const CITIES = {
  Chicago: [41.8781, -87.6298],
  "New York City": [40.7128, -74.006],
  "Los Angeles": [34.0522, -118.2437],
};

function App() {
  const [city, setCity] = useState("Chicago");
  const [hour, setHour] = useState(21);
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const center = CITIES[city];

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setLoading(true);
      setError("");

      try {
        const endpoint =
          city === "Chicago"
            ? "/chicago/incidents?limit=500"
            : city === "New York City"
              ? "/nyc/incidents?limit=500"
              : "/la/incidents?limit=500";

        const response = await fetch(`${API}${endpoint}`);
        if (!response.ok) throw new Error(`API ${response.status}`);
        const data = await response.json();

        if (!cancelled) setIncidents(data.incidents || []);
      } catch (err) {
        if (!cancelled) {
          setError(
            "Не удалось получить данные API. Запусти backend на http://localhost:8000."
          );
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [city]);

  useEffect(() => {
    const map = L.map("map", {
      zoomControl: false,
      attributionControl: true,
    }).setView(center, city === "Chicago" ? 11 : 11);

    L.control.zoom({ position: "bottomright" }).addTo(map);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors',
    }).addTo(map);

    incidents.forEach((incident) => {
      if (incident.latitude == null || incident.longitude == null) return;

      const date = incident.occurred_at
        ? new Date(incident.occurred_at)
        : null;

      // MVP: show incidents from the loaded period. Time filtering is
      // intentionally not presented as predictive crime probability.
      const marker = L.circleMarker(
        [incident.latitude, incident.longitude],
        {
          radius: 4,
          weight: 1,
          fillOpacity: 0.45,
        }
      );

      marker.bindPopup(
        `<strong>${escapeHtml(incident.category)}</strong><br/>` +
          `${date ? date.toLocaleString() : "Unknown time"}`
      );
      marker.addTo(map);
    });

    return () => map.remove();
  }, [center, city, incidents]);

  const visibleCount = useMemo(() => incidents.length, [incidents]);

  return (
    <main className="app">
      <header>
        <div>
          <div className="eyebrow">SAFEHOUR</div>
          <h1>Understand the city before the city surprises you.</h1>
          <p>
            Public-data safety intelligence built around time, place and
            optional personalization.
          </p>
        </div>

        <div className="controls">
          <label>
            City
            <select value={city} onChange={(e) => setCity(e.target.value)}>
              {Object.keys(CITIES).map((name) => (
                <option key={name}>{name}</option>
              ))}
            </select>
          </label>

          <label>
            Hour
            <input
              type="range"
              min="0"
              max="23"
              value={hour}
              onChange={(e) => setHour(Number(e.target.value))}
            />
            <span>{String(hour).padStart(2, "0")}:00</span>
          </label>
        </div>
      </header>

      <section className="map-shell">
        <div id="map" />
        <aside className="panel">
          <div className="panel-title">Safety overview</div>
          <div className="big">{loading ? "…" : visibleCount}</div>
          <div className="muted">loaded official-data records</div>

          <div className="info">
            <strong>{city}</strong>
            <span>Historical activity view</span>
          </div>

          <div className="note">
            Historical incident data helps describe patterns. It does not
            predict an individual crime or guarantee that an area is safe.
          </div>

          {error && <div className="error">{error}</div>}
        </aside>
      </section>
    </main>
  );
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

export default App;
