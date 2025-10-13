/*
NYC Metropolis Taxi Analytics — Frontend Starter (React + Tailwind)

This single-file starter exports a React component as the default export (App).
It includes:
- Layout inspired by WRI.org: header, left filters, main map + charts, right methodology panel
- KPI cards, filter controls, map placeholder (Leaflet), charts placeholder (Recharts)
- State management with React hooks and example fetch to backend API endpoints
- Accessibility considerations and responsive layout (mobile collapse)

--- Installation notes (copy into your project root) ---

1) package.json (example)
{
  "name": "nyc-metropolis-taxi-analytics-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "leaflet": "^1.9.4",
    "react-leaflet": "^4.2.1",
    "recharts": "^2.5.0",
    "date-fns": "^2.30.0",
    "axios": "^1.4.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test --env=jsdom",
    "eject": "react-scripts eject"
  }
}

2) Tailwind setup (optional but recommended)
- Install Tailwind, add config, and include in src/index.css.
- For quick start without Tailwind, you can use plain CSS.

3) Files:
- src/App.jsx  -> paste this file's content (the default export)
- src/index.js -> classic React entry
- src/index.css -> include Tailwind base/components/utilities or custom CSS

4) To run:
- npm install
- npm start

--- Notes ---
- This starter focuses on frontend UI structure and sample interactions.
- Map uses react-leaflet; you'll need to add Leaflet CSS in index.html or index.css.
- Replace API endpoints (API_BASE) with your backend (e.g., http://localhost:8000/api)

*/

import React, { useEffect, useMemo, useState } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar, CartesianGrid, Legend } from "recharts";
import axios from "axios";
import { format, parseISO } from "date-fns";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000/api";

/* ---------------------- Utility components ---------------------- */

function Header() {
  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h1 className="text-2xl font-semibold text-slate-800">NYC Metropolis Taxi Analytics</h1>
          <span className="text-sm text-slate-500">Research-focused mobility insights • Inspired by WRI</span>
        </div>
        <nav className="flex items-center gap-4">
          <a href="#" className="text-sm text-sky-600 hover:underline">Methodology</a>
          <a href="#" className="text-sm text-sky-600 hover:underline">Data</a>
          <a href="#" className="text-sm text-sky-600 hover:underline">Docs</a>
        </nav>
      </div>
    </header>
  );
}

function KPI({label, value, sub}){
  return (
    <div className="bg-white p-4 rounded-lg shadow-sm">
      <div className="text-sm text-slate-500">{label}</div>
      <div className="text-2xl font-bold text-slate-800">{value}</div>
      {sub && <div className="text-xs text-slate-400 mt-1">{sub}</div>}
    </div>
  )
}

function Sidebar({filters, setFilters, onApply}){
  return (
    <aside className="w-80 bg-slate-50 p-4 border-r border-slate-200 h-[calc(100vh-72px)] overflow-auto">
      <h2 className="text-lg font-semibold mb-2">Explorer</h2>

      <label className="block text-sm text-slate-600 mt-3">Date range</label>
      <div className="flex gap-2">
        <input aria-label="start date" type="date" className="mt-1 p-2 w-1/2 border rounded" value={filters.startDate} onChange={e=>setFilters(f=>({...f,startDate:e.target.value}))} />
        <input aria-label="end date" type="date" className="mt-1 p-2 w-1/2 border rounded" value={filters.endDate} onChange={e=>setFilters(f=>({...f,endDate:e.target.value}))} />
      </div>

      <label className="block text-sm text-slate-600 mt-4">Time of day</label>
      <div className="flex gap-2 items-center">
        <input aria-label="start hour" type="number" min={0} max={23} value={filters.startHour} onChange={e=>setFilters(f=>({...f,startHour:Math.max(0,Math.min(23,Number(e.target.value)||0))}))} className="p-2 w-1/2 border rounded" />
        <input aria-label="end hour" type="number" min={0} max={23} value={filters.endHour} onChange={e=>setFilters(f=>({...f,endHour:Math.max(0,Math.min(23,Number(e.target.value)||23))}))} className="p-2 w-1/2 border rounded" />
      </div>

      <label className="block text-sm text-slate-600 mt-4">Passenger count</label>
      <select aria-label="passenger count" value={filters.passengerCount} onChange={e=>setFilters(f=>({...f,passengerCount:e.target.value}))} className="w-full p-2 border rounded mt-1">
        <option value="">Any</option>
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4+</option>
      </select>

      <label className="block text-sm text-slate-600 mt-4">Distance (miles)</label>
      <div className="flex gap-2">
        <input aria-label="min distance" type="number" min={0} step="0.1" value={filters.minDistance} onChange={e=>setFilters(f=>({...f,minDistance:e.target.value}))} className="p-2 w-1/2 border rounded" />
        <input aria-label="max distance" type="number" min={0} step="0.1" value={filters.maxDistance} onChange={e=>setFilters(f=>({...f,maxDistance:e.target.value}))} className="p-2 w-1/2 border rounded" />
      </div>

      <label className="block text-sm text-slate-600 mt-4">Payment type</label>
      <select aria-label="payment type" value={filters.paymentType} onChange={e=>setFilters(f=>({...f,paymentType:e.target.value}))} className="w-full p-2 border rounded mt-1">
        <option value="">Any</option>
        <option value="1">Credit card</option>
        <option value="2">Cash</option>
        <option value="3">No charge</option>
        <option value="4">Dispute</option>
        <option value="5">Unknown</option>
      </select>

      <div className="mt-6 flex gap-2">
        <button onClick={onApply} className="flex-1 bg-sky-600 text-white p-2 rounded">Apply filters</button>
        <button onClick={()=>window.location.reload()} className="p-2 border rounded">Reset</button>
      </div>

      <div className="mt-6 text-xs text-slate-500">
        <strong>Tip:</strong> Use the date range and time filters together to create targeted narratives for peak vs off-peak behavior. Export options live in the top-right actions.
      </div>
    </aside>
  );
}

/* ---------------------- Map & Charts ---------------------- */

function MapView({trips}){
  // Center roughly NYC
  const position = [40.7128, -74.0060];
  return (
    <div className="h-96 md:h-full rounded-lg overflow-hidden border">
      <MapContainer center={position} zoom={11} scrollWheelZoom={true} style={{height: '100%', width: '100%'}}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {trips.slice(0,200).map((t, i)=> (
          <CircleMarker key={i} center={[t.pickup_lat, t.pickup_lng]} radius={4} weight={0.6}>
            <Popup>
              <div className="text-sm">
                <div><strong>Pickup:</strong> {t.pickup_zone || `${t.pickup_lat.toFixed(4)}, ${t.pickup_lng.toFixed(4)}`}</div>
                <div><strong>Dropoff:</strong> {t.dropoff_zone || `${t.dropoff_lat.toFixed(4)}, ${t.dropoff_lng.toFixed(4)}`}</div>
                <div><strong>Fare:</strong> ${t.fare_amount}</div>
                <div><strong>Duration:</strong> {Math.round(t.trip_duration_sec/60)} min</div>
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  )
}

function TimeSeriesChart({data}){
  return (
    <div className="bg-white p-4 rounded shadow-sm h-64">
      <h3 className="text-sm font-medium mb-2">Trips per hour</h3>
      {data.length>0 ? (
        <ResponsiveContainer width="100%" height="85%">
          <LineChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="hour" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="count" stroke="#1e3a8a" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      ) : (
        <div className="text-sm text-slate-500">No data yet. Apply filters to load a timeseries.</div>
      )}
    </div>
  )
}

function FareHistogram({data}){
  return (
    <div className="bg-white p-4 rounded shadow-sm h-64">
      <h3 className="text-sm font-medium mb-2">Fare distribution</h3>
      {data.length>0 ? (
        <ResponsiveContainer width="100%" height="85%">
          <BarChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="bin" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" />
          </BarChart>
        </ResponsiveContainer>
      ) : (
        <div className="text-sm text-slate-500">No data yet. Apply filters to load histogram.</div>
      )}
    </div>
  )
}

/* ---------------------- Main App ---------------------- */

export default function App(){
  const [filters, setFilters] = useState({
    startDate: '',
    endDate: '',
    startHour: 0,
    endHour: 23,
    passengerCount: '',
    minDistance: '',
    maxDistance: '',
    paymentType: ''
  });

  const [kpis, setKpis] = useState({totalTrips: '-', avgFare: '-', dateRange: '-' });
  const [trips, setTrips] = useState([]);
  const [timeseries, setTimeseries] = useState([]);
  const [histogram, setHistogram] = useState([]);
  const [loading, setLoading] = useState(false);

  const appliedFilters = useMemo(()=>({
    ...filters
  }), [filters]);

  async function fetchOverview(params){
    setLoading(true);
    try{
      // Example API calls - replace endpoints with your backend
      const q = new URLSearchParams(params).toString();
      const [tripsRes, summaryRes, timesRes, histRes] = await Promise.all([
        axios.get(`${API_BASE}/trips?limit=500&${q}`),
        axios.get(`${API_BASE}/summary/daily?${q}`),
        axios.post(`${API_BASE}/query/aggregate`, { ...params, group_by:['pickup_hour'], metrics:['count'] }),
        axios.get(`${API_BASE}/histogram/fare?${q}`)
      ].map(p=>p.catch(e=>({error:e}))));

      if(!tripsRes.error){
        setTrips(tripsRes.data.data || tripsRes.data || []);
      }
      if(!summaryRes.error){
        const meta = summaryRes.data?.meta || {};
        setKpis({ totalTrips: meta.total_trips || (Array.isArray(tripsRes.data?.data) ? tripsRes.data.data.length : '-'), avgFare: meta.avg_fare || '-', dateRange: `${params.startDate||'--'} — ${params.endDate||'--'}` })
      }
      if(!timesRes.error){
        // Transform timeseries to chart-friendly
        const tdata = (timesRes.data?.data || []).map(r=>({ hour: r.pickup_hour, count: r.count }));
        setTimeseries(tdata);
      }
      if(!histRes.error){
        setHistogram(histRes.data?.data || []);
      }

    }catch(err){
      console.error(err);
    }finally{
      setLoading(false);
    }
  }

  useEffect(()=>{
    // initial load: fetch recent day sample data
    const today = new Date();
    const d1 = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    const d0 = new Date(d1); d0.setDate(d1.getDate()-1);
    const sd = format(d0, 'yyyy-MM-dd');
    const ed = format(d1, 'yyyy-MM-dd');
    setFilters(f=>({...f, startDate: sd, endDate: ed}));
    fetchOverview({start_datetime: sd+'T00:00:00', end_datetime: ed+'T23:59:59'});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[]);

  function handleApply(){
    const params = {
      start_datetime: filters.startDate ? `${filters.startDate}T00:00:00` : undefined,
      end_datetime: filters.endDate ? `${filters.endDate}T23:59:59` : undefined,
      min_distance: filters.minDistance || undefined,
      max_distance: filters.maxDistance || undefined,
      passenger_count: filters.passengerCount || undefined,
      payment_type: filters.paymentType || undefined
    };
    fetchOverview(params);
  }

  return (
    <div className="min-h-screen bg-slate-100 text-slate-800">
      <Header />
      <div className="max-w-7xl mx-auto px-4 py-6 grid grid-cols-1 md:grid-cols-12 gap-6">
        <div className="md:col-span-3">
          <Sidebar filters={filters} setFilters={setFilters} onApply={handleApply} />
        </div>

        <main className="md:col-span-6 space-y-4">
          <section className="grid grid-cols-3 gap-4">
            <KPI label="Total trips" value={kpis.totalTrips} sub={`Range: ${kpis.dateRange}`} />
            <KPI label="Average fare" value={kpis.avgFare !== '-' ? `$${kpis.avgFare}` : '-'} sub={"Avg fare (USD)"} />
            <KPI label="Loaded sample" value={trips.length} sub={loading ? 'Loading…' : 'Sample size loaded'} />
          </section>

          <section className="bg-transparent rounded">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
              <div className="lg:col-span-2">
                <div className="bg-white p-4 rounded shadow-sm h-[520px] flex flex-col gap-4">
                  <div className="flex items-center justify-between">
                    <h2 className="text-lg font-semibold">Map Explorer</h2>
                    <div className="flex items-center gap-2">
                      <button className="text-sm px-3 py-1 border rounded">Download CSV</button>
                      <button className="text-sm px-3 py-1 border rounded">Share</button>
                    </div>
                  </div>
                  <MapView trips={trips} />
                </div>
              </div>

              <div className="lg:col-span-1 space-y-4">
                <TimeSeriesChart data={timeseries} />
                <FareHistogram data={histogram} />
              </div>
            </div>
          </section>

          <section>
            <div className="bg-white p-4 rounded shadow-sm">
              <h3 className="text-lg font-semibold mb-2">Key findings</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-3 border rounded">
                  <h4 className="font-medium">Peak evening demand concentration</h4>
                  <p className="text-sm text-slate-600">Evening trips concentrate in Midtown Manhattan and major transit hubs. Consider implications for evening transit supplement or demand-responsive services.</p>
                </div>
                <div className="p-3 border rounded">
                  <h4 className="font-medium">Fare inequality across boroughs</h4>
                  <p className="text-sm text-slate-600">Median fares vary substantially between outer boroughs and Manhattan; policy implications for equitable access to taxi services.</p>
                </div>
              </div>
            </div>
          </section>

        </main>

        <aside className="md:col-span-3">
          <div className="sticky top-24 space-y-4">
            <div className="bg-white p-4 rounded shadow-sm">
              <h3 className="font-semibold">Methodology & Data</h3>
              <p className="text-sm text-slate-600 mt-2">This demo loads a small sample via the API. The full ETL and data provenance are available in the repository's <a className="text-sky-600 underline" href="#">Methodology</a> page.</p>
              <ul className="text-sm text-slate-500 mt-3 space-y-1">
                <li>• ETL version: <strong>v0.1</strong></li>
                <li>• Rows flagged: <strong>~2.4%</strong></li>
                <li>• Spatial indexing: PostGIS</li>
              </ul>
              <div className="mt-3">
                <button className="w-full py-2 bg-sky-600 text-white rounded">Open Repro Notebook</button>
              </div>
            </div>

            <div className="bg-white p-4 rounded shadow-sm">
              <h3 className="font-semibold">Report Builder</h3>
              <p className="text-sm text-slate-600 mt-2">Pin visualizations and narrative cards to build a short PDF report for sharing with stakeholders.</p>
              <div className="mt-3 grid grid-cols-2 gap-2">
                <button className="py-2 px-3 border rounded text-sm">Pin</button>
                <button className="py-2 px-3 border rounded text-sm">Export PDF</button>
              </div>
            </div>

            <div className="bg-white p-4 rounded shadow-sm">
              <h3 className="font-semibold">Data sources</h3>
              <p className="text-sm text-slate-600 mt-2">NYC TLC Trip Records (sample). Additional socio-demographic datasets can be linked in the ETL for equity analysis.</p>
            </div>
          </div>
        </aside>
      </div>

      <footer className="bg-white border-t mt-6">
        <div className="max-w-7xl mx-auto px-4 py-6 text-sm text-slate-500">© NYC Metropolis Taxi Analytics • Research demo — include citation and methodology when publishing findings.</div>
      </footer>
    </div>
  )
}

/* End of App.jsx */
