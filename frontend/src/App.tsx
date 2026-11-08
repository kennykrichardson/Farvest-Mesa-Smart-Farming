import { useCallback, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'
import {
  Activity, AlertTriangle, CloudRain, Droplets, Pause, Play, RotateCcw,
  Sprout, Sun, TrendingUp, Tractor, Waves, Zap
} from 'lucide-react'
import {
  Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis
} from 'recharts'
import type { Snapshot } from './types'

const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
const stageColor: Record<string,string> = {SEED:'#9a8065',SPROUT:'#276b42',YOUNG:'#8ecb65',MATURE:'#4da66a',READY:'#e8c65d',DEAD:'#77564a'}
const fmt = (n:number) => new Intl.NumberFormat('en-US').format(Math.round(n))
function App() {
  const [data,setData] = useState<Snapshot|null>(null)
  const [busy,setBusy] = useState(false)
  const [days,setDays] = useState(5)
  const [selected,setSelected] = useState<number|null>(null)
  const [layer,setLayer] = useState<'stage'|'water'|'health'>('stage')
  const [error,setError] = useState('')
  const load = useCallback(async () => {
    try { const r=await fetch(`${API}/api/snapshot`); if(!r.ok) throw new Error('API unavailable'); setData(await r.json()); setError('') }
    catch { setError('Simulation API is offline. Start the Python API server to connect the field.') }
  },[])
  useEffect(()=>{load(); const id=window.setInterval(load,2500); return ()=>window.clearInterval(id)},[load])
  const act = async (path:string,body?:unknown) => {
    setBusy(true); try { const r=await fetch(`${API}${path}`,{method:'POST',headers:{'Content-Type':'application/json'},body:body?JSON.stringify(body):undefined}); if(!r.ok) throw new Error(await r.text()); setData(await r.json()); setError('') } catch(e){setError(e instanceof Error?e.message:'Action failed')} finally{setBusy(false)}
  }
  const trend = useMemo(()=>data?.history.map(point=>({...point,day:`D${point.day}`})) ?? [],[data])
  const chosen = data?.crops.find(c=>c.id===selected)
  if(!data) return <div className="loading"><div className="brand-mark"><Sprout/></div><span>Connecting to Farvest simulation…</span>{error&&<p>{error}</p>}</div>
  const m=data.metrics
  return <div className="app-shell">
    <main className="main" style={{marginLeft:0,width:"100%",maxWidth:"100%",minWidth:0}}>
      <header className="topbar"><div className="breadcrumb"><b>Farvest</b><span>/</span> Farm overview</div><div className="top-actions"><div className="live-pill"><i/> LIVE SIMULATION</div></div></header>
      {error&&<div className="error-banner"><AlertTriangle size={16}/>{error}</div>}
      <div className="content">
        <section className="page-heading"><div><div className="eyebrow">FARM OPERATIONS / OVERVIEW</div><h1>Good morning, operator.</h1><p>Your farm is looking {m.health>=75?'healthy':m.health>=45?'stable':'under pressure'}. Here’s the latest field intelligence.</p></div><div className="heading-right"><div className="day-box"><span>SIMULATION DAY</span><b>{String(data.meta.day).padStart(3,'0')} <small>/ 365</small></b></div><button className="secondary-btn" onClick={()=>act('/api/simulation/reset',{seed:data.meta.seed})} disabled={busy}><RotateCcw size={15}/> Reset</button></div></section>
        <section className="weather-strip"><div className="weather-main">{data.weather.name==='Rainy'?<CloudRain/>:<Sun/>}<div><small>FIELD CONDITIONS</small><b>{data.weather.name} · {data.weather.temperature}°C</b></div></div><div className="weather-divider"/><div className="weather-stat"><span>Field health</span><b>{m.health.toFixed(0)}%</b></div><div className="weather-stat"><span>Avg. soil water</span><b>{m.water.toFixed(0)}%</b></div><div className="weather-stat"><span>Crop growth</span><b>{m.growth.toFixed(0)}%</b></div><div className="weather-note"><span className="weather-dot"/>{data.weather.rainy?'Rainfall replenishing the field':'Environmental systems nominal'}</div></section>
        <section className="metric-grid">
          <Metric icon={<Sprout/>} label="Living crops" value={`${m.living_crops}`} detail={`of ${m.total_crops} planted`} tone="green" />
          <Metric icon={<Waves/>} label="Farm health score" value={`${m.farm_score.toFixed(0)}`} detail="Composite field index" tone="mint"/>
          <Metric icon={<Droplets/>} label="Water applied" value={fmt(m.water_used)} detail={`${m.irrigations} irrigation events`} tone="blue"/>
          <Metric icon={<Tractor/>} label="Harvest yield" value={fmt(m.harvests)} detail={`${m.ready_crops} currently ready`} tone="gold"/>
        </section>
        <section className="primary-grid">
          <div className="panel field-panel">
            <div className="panel-head"><div><div className="eyebrow">SPATIAL OPERATIONS</div><h2>Field monitor</h2><p>Live crop distribution and autonomous worker positions</p></div><div className="field-actions"><select value={layer} onChange={e=>setLayer(e.target.value as any)}><option value="stage">Crop stage</option><option value="water">Water stress</option><option value="health">Crop health</option></select><span className="map-size">{data.meta.width} × {data.meta.height} GRID</span></div></div>
            <div className="field-canvas"><div className="field-grid" style={{gridTemplateColumns:`repeat(${data.meta.width}, minmax(0,1fr))`}}>
              {Array.from({length:data.meta.width*data.meta.height},(_,i)=>{const x=i%data.meta.width,y=Math.floor(i/data.meta.width);const crop=data.crops.find(c=>c.x===x&&c.y===y);const farmer=data.farmers.find(f=>f.x===x&&f.y===y);let color='#26392c';if(crop){if(layer==='stage')color=stageColor[crop.stage]||'#4c7652';if(layer==='water')color=crop.water<30?'#d77b55':crop.water<60?'#d6bd69':'#6da9b4';if(layer==='health')color=crop.health<30?'#d77b55':crop.health<65?'#d6bd69':'#70b783'}return <button key={i} title={crop?`Crop #${crop.id} · ${crop.stage} · water ${crop.water}%`:farmer?`Farmer #${farmer.id}`:`Plot ${x}, ${y}`} onClick={()=>crop&&setSelected(crop.id)} className={`plot ${crop?'planted':''} ${selected===crop?.id?'selected':''}`} style={{background:color}}>{farmer&&<span className="farmer-pin">✦</span>}{crop&&selected===crop.id&&<span className="plot-ring"/>}</button>})}
            </div><div className="map-compass">N<br/>↑</div><div className="map-coordinates">FIELD A · SECTOR 01</div></div>
            <div className="map-legend"><span><i style={{background:'#276b42'}}/>Sprout</span><span><i style={{background:'#8ecb65'}}/>Growing</span><span><i style={{background:'#4da66a'}}/>Mature</span><span><i style={{background:'#e8c65d'}}/>Harvest-ready</span><span><i className="star">✦</i>Farmer</span><span className="legend-right">{m.stressed_crops} plots need attention</span></div>
          </div>
          <div className="panel control-panel"><div className="panel-head"><div><div className="eyebrow">ENGINE CONTROL</div><h2>Simulation controls</h2><p>Manage the farm timeline</p></div><span className={`status-tag ${data.meta.running?'running':'paused'}`}>{data.meta.running?'RUNNING':'PAUSED'}</span></div>
            <div className="control-day"><span>DAY COUNTER</span><b>{String(data.meta.day).padStart(3,'0')}</b><small>One step represents one simulated day</small></div>
            <div className="batch-control"><div><label>Batch duration</label><b>{days} days</b></div><input type="range" min="1" max="25" value={days} onChange={e=>setDays(Number(e.target.value))}/><div className="range-labels"><span>1 day</span><span>25 days</span></div></div>
            <button className="primary-action" disabled={busy} onClick={()=>act('/api/simulation/step')}><Play size={16} fill="currentColor"/> Advance one day</button>
            <button className="batch-action" disabled={busy} onClick={()=>act('/api/simulation/batch',{days})}><Zap size={16}/> Run {days}-day batch</button>
            <button className="pause-action" disabled={busy} onClick={()=>act(data.meta.running?'/api/simulation/pause':'/api/simulation/resume')}>{data.meta.running?<Pause size={16}/>:<Play size={16}/>} {data.meta.running?'Pause simulation':'Resume simulation'}</button>
            <div className="control-foot"><span><i/> API responsive</span><span>Seed {data.meta.seed}</span></div>
          </div>
        </section>
        <section className="lower-grid">
          <div className="panel chart-panel"><div className="panel-head"><div><div className="eyebrow">CROP PERFORMANCE</div><h2>Field development</h2><p>Recorded daily simulation metrics</p></div><span className="chart-badge"><TrendingUp size={14}/> Growth</span></div><div className="chart-wrap"><ResponsiveContainer width="100%" height="100%"><AreaChart data={trend}><defs><linearGradient id="growthFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#8fbd78" stopOpacity={.27}/><stop offset="100%" stopColor="#8fbd78" stopOpacity={0}/></linearGradient></defs><CartesianGrid stroke="#26372c" vertical={false}/><XAxis dataKey="day" tick={{fill:'#718277',fontSize:10}} axisLine={false} tickLine={false}/><YAxis tick={{fill:'#718277',fontSize:10}} axisLine={false} tickLine={false} width={28}/><Tooltip contentStyle={{background:'#17221b',border:'1px solid #35483a',borderRadius:9,color:'#eaf1eb'}}/><Area type="monotone" dataKey="growth" stroke="#a7cf8e" strokeWidth={2.2} fill="url(#growthFill)"/></AreaChart></ResponsiveContainer></div></div>
          <div className="panel distribution-panel"><div className="panel-head"><div><div className="eyebrow">FIELD COMPOSITION</div><h2>Crop distribution</h2><p>Current growth stages</p></div></div><div className="distribution-list">{Object.entries(stageColor).filter(([k])=>k!=='DEAD').map(([stage,color])=>{const count=data.crops.filter(c=>c.stage===stage).length;return <div className="distribution-row" key={stage}><span><i style={{background:color}}/>{stage.toLowerCase()}</span><b>{count}</b><div className="dist-track"><i style={{width:`${m.total_crops?count/m.total_crops*100:0}%`,background:color}}/></div></div>})}</div><div className="distribution-foot"><span>Crop survival</span><b>{m.total_crops?Math.round(m.living_crops/m.total_crops*100):0}%</b></div></div>
        </section>
        <section className="bottom-grid">
          <div className="panel agents-panel"><div className="panel-head"><div><div className="eyebrow">AUTONOMOUS SYSTEMS</div><h2>Field workforce</h2><p>Agent task status and energy reserves</p></div><span className="map-size">{data.farmers.length} ACTIVE AGENTS</span></div>{data.farmers.map(f=><div className="agent-row" key={f.id}><div className="agent-icon"><Tractor size={17}/></div><div className="agent-info"><b>Farmer #{f.id}</b><small>{f.task}</small></div><div className="agent-position">({f.x}, {f.y})</div><div className="energy"><div><span>ENERGY</span><b>{f.energy}%</b></div><i><em style={{width:`${f.energy}%`}}/></i></div></div>)}</div>
          <div className="panel activity-panel"><div className="panel-head"><div><div className="eyebrow">SYSTEM LOG</div><h2>Recent activity</h2><p>Latest events from the simulation</p></div><Activity size={17} className="muted-icon"/></div><div className="activity-list">{data.events.slice(0,5).map((e,i)=><div className="activity-item" key={`${e.tick}-${i}`}><i className="activity-marker"/><div><b>{e.title}</b><p>{e.message}</p><small>DAY {e.tick}</small></div></div>)}</div></div>
        </section>
        <footer><span>FARVEST <b>2.0</b> · AGRICULTURAL INTELLIGENCE</span><span>MESA SIMULATION CORE · PYTHON API</span></footer>
      </div>
    </main>
    {chosen&&<div className="drawer-backdrop" onClick={()=>setSelected(null)}><aside className="crop-drawer" onClick={e=>e.stopPropagation()}><button className="drawer-close" onClick={()=>setSelected(null)}>×</button><div className="eyebrow">PLOT INSPECTOR</div><h2>Crop #{chosen.id}</h2><span className="crop-stage" style={{color:stageColor[chosen.stage]}}>{chosen.stage}</span><div className="drawer-stats">{[['Growth',chosen.growth],['Health',chosen.health],['Water',chosen.water]].map(([label,val],index)=><div key={index}><span>{label}</span><b>{val}%</b><i><em style={{width:`${val}%`}}/></i></div>)}</div><p className="drawer-note">Plot coordinates: ({chosen.x}, {chosen.y}) · Age: {chosen.age} days</p>{chosen.ready&&<div className="ready-note">This crop is ready for harvest.</div>}</aside></div>}
  </div>
}
function Metric({icon,label,value,detail,tone}:{icon:ReactNode;label:string;value:string;detail:string;tone:string}){return <div className="metric-card"><div className={`metric-icon ${tone}`}>{icon}</div><div className="metric-label">{label}</div><div className="metric-value">{value}</div><div className="metric-detail">{detail}</div></div>}
export default App
