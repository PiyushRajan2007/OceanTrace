import { useState } from 'react'
import './App.css'
import { demoMode, incident, vessels, trafficStages } from './demoData.js'

function Icon({ children }) {
  return <span className="icon" aria-hidden="true">{children}</span>
}

function App() {
  const [activeNav, setActiveNav] = useState('Overview')
  const [playing, setPlaying] = useState(false)
  const [selectedVessel, setSelectedVessel] = useState(0)
  const [layers, setLayers] = useState({ sar: true, slick: true, vessels: true, currents: true })
  const [trafficMode, setTrafficMode] = useState('filtered')
  const [trafficStage, setTrafficStage] = useState(5)
  const [alertVisible, setAlertVisible] = useState(true)
  const [detailsOpen, setDetailsOpen] = useState(false)

  const toggleLayer = (layer) => setLayers((current) => ({ ...current, [layer]: !current[layer] }))

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand"><div className="brand-mark"><span /></div><div><strong>OCEAN<span>TRACE</span></strong><small>MARITIME INTELLIGENCE</small></div></div>
        <nav>{['Overview', 'Incidents', 'Vessels', 'Data layers'].map((item) => <button key={item} className={activeNav === item ? 'active' : ''} onClick={() => setActiveNav(item)}>{item}</button>)}</nav>
        <div className="top-actions"><span className="live"><i /> LIVE SYSTEM</span><button className="avatar">AR</button></div>
      </header>

      <main>
        <section className="intro"><div><p className="eyebrow">OPERATIONS / NORTH INDIAN OCEAN</p><h1>Spill intelligence <em>at a glance.</em></h1></div><div className="scene-meta"><span className="status-dot" /> <div><b>{incident.scene}</b><small>Processed 08:42 UTC &nbsp; / &nbsp; Confidence {incident.slick.confidence}% &nbsp; / &nbsp; {demoMode ? 'DEMO MODE' : 'LIVE'}</small></div><button className="ghost-button" onClick={() => window.location.href = '/report'}><Icon>↗</Icon> Export report</button></div></section>

        <section className="stats"><div className="stat"><span>ACTIVE INCIDENTS</span><strong>04</strong><small className="up">+1 <i>since yesterday</i></small></div><div className="stat"><span>DETECTED SLICK AREA</span><strong>{incident.slick.area.replace(' km²', '')} <small>km²</small></strong><small className="up">+3.2% <i>last 6 hours</i></small></div><div className="stat"><span>VESSELS IN ENVELOPE</span><strong>17</strong><small><i>3 high priority</i></small></div><div className="stat"><span>MODEL CONFIDENCE</span><strong>{incident.slick.confidence}<small>%</small></strong><small className="up">+0.8% <i>vs. last run</i></small></div></section>

        <section className="traffic-control panel"><div><span className="section-kicker">TRAFFIC FILTERING</span><strong>{trafficMode === 'filtered' ? 'Operational traffic' : 'Normal traffic'}</strong><small>{trafficMode === 'filtered' ? 'Showing attribution candidates' : 'Showing all observed AIS traffic'}</small></div><div className="traffic-stages">{trafficStages.map((stage, index) => <button key={stage.label} className={trafficStage === index ? 'selected' : ''} onClick={() => setTrafficStage(index)}><span>{stage.label}</span><b>{stage.count}</b></button>)}</div><div className="traffic-mode"><button className={trafficMode === 'normal' ? 'selected' : ''} onClick={() => setTrafficMode('normal')}>Normal Traffic</button><button className={trafficMode === 'filtered' ? 'selected' : ''} onClick={() => setTrafficMode('filtered')}>Operational</button></div></section>

        <section className="workspace-grid">
          <div className="map-panel panel"><div className="panel-heading"><div><span className="section-kicker">01 / DETECTION &amp; TRACKING</span><h2>Incident map</h2></div><div className="map-actions"><button className="icon-button">−</button><button className="icon-button">+</button><button className="icon-button">⌖</button></div></div>
            <div className={`map-canvas ${trafficMode === 'normal' ? 'normal-traffic' : ''}`}>{layers.sar && <div className="sar-overlay" />}<div className="map-label label-india">INDIA</div><div className="map-label label-sri">SRI LANKA</div><div className="map-label label-sea">ARABIAN SEA</div>{layers.slick && <><div className="slick slick-one" /><div className="slick slick-two" /></>}<div className="track track-one" /><div className="track track-two" />{layers.vessels && <><div className="vessel v-one">◆</div><div className="vessel v-two">◆</div><div className="vessel v-three">◆</div></>}{layers.currents && <><div className="current c-one">›››››</div><div className="current c-two">›››››</div></>}<div className="map-tooltip"><span className="pulse" /><div><b>{incident.id}</b><small>Oil slick detected · {incident.slick.area}</small></div><strong>WARNING</strong></div><div className="coordinates">{incident.coordinates}</div><div className="north">N<br /><span>↑</span></div></div>
            <div className="map-footer"><div className="layer-toggles"><label><input type="checkbox" checked={layers.sar} onChange={() => toggleLayer('sar')} /><span className="swatch sar" /> SAR imagery</label><label><input type="checkbox" checked={layers.slick} onChange={() => toggleLayer('slick')} /><span className="swatch slick-swatch" /> Slick overlay</label><label><input type="checkbox" checked={layers.vessels} onChange={() => toggleLayer('vessels')} /><span className="swatch vessel-swatch" /> Vessels</label><label><input type="checkbox" checked={layers.currents} onChange={() => toggleLayer('currents')} /><span className="swatch current-swatch" /> Currents</label></div><span className="map-source">© OpenSeaMap &nbsp; / &nbsp; Sentinel-1 GRD</span></div>
          </div>

          <aside className="side-column"><div className="panel signal-panel"><div className="panel-heading"><div><span className="section-kicker">02 / PRIORITY QUEUE</span><h2>Suspect vessels <span className="count">03</span></h2></div><button className="more">•••</button></div><div className="vessel-list">{vessels.map((vessel, index) => <button className={`vessel-row ${selectedVessel === index ? 'selected' : ''}`} key={vessel.mmsi} onClick={() => setSelectedVessel(index)}><span className={`rank ${vessel.color}`}>0{index + 1}</span><div className="vessel-info"><b>{vessel.name}</b><small>MMSI {vessel.mmsi} &nbsp;·&nbsp; {vessel.flag}</small><span className={`vessel-note ${vessel.color}`}>{vessel.reasons[0]}</span></div><span className={`score ${vessel.color}`}>{vessel.score}<small>/100</small></span></button>)}</div><button className="full-list" onClick={() => setDetailsOpen(true)}>View attribution details <span>→</span></button></div>{alertVisible && <div className="panel alert-panel"><span className="alert-icon">!</span><div><b>Dark vessel detected</b><p>Unidentified hull in SAR scene. AIS match pending.</p><small>2 minutes ago</small></div><button className="close-alert" onClick={() => setAlertVisible(false)}>×</button></div>}</aside>
        </section>

        <section className="incident-details panel"><div className="details-heading"><div><span className="section-kicker">INCIDENT CHARACTERIZATION</span><h2>{incident.id} <small>· {incident.impact.severity.toUpperCase()}</small></h2></div><button className="details-toggle" onClick={() => setDetailsOpen(!detailsOpen)}>{detailsOpen ? 'Collapse' : 'Open forensic details'} ↗</button></div><div className="detail-metrics"><div><small>SLICK AGE</small><b>{incident.slick.age}</b></div><div><small>PERIMETER / L × W</small><b>{incident.slick.perimeter} / {incident.slick.length} × {incident.slick.width}</b></div><div><small>ASPECT RATIO</small><b>{incident.slick.aspect}</b></div><div><small>EST. VOLUME</small><b>{incident.slick.volume}</b></div><div><small>GEOMETRY</small><b>{incident.slick.geometry}</b></div></div>{detailsOpen && <div className="attribution-detail"><div><b>Explainable attribution · {vessels[selectedVessel].name}</b><p>Overall score {vessels[selectedVessel].score}/100. Weighted formula: 30% proximity + 25% trajectory + 25% behavior + 20% AIS gap.</p><div className="breakdown">{Object.entries(vessels[selectedVessel].breakdown).map(([key, value]) => <span key={key}><i style={{ width: `${value}%` }} /><b>{key} <em>{value}</em></b></span>)}</div></div><ul>{vessels[selectedVessel].reasons.map((reason) => <li key={reason}>{reason}</li>)}</ul></div>}</section>

        <section className="timeline panel"><div className="timeline-head"><div><span className="section-kicker">03 / DRIFT SIMULATION</span><h2>Hindcast &amp; forecast</h2></div><div className="timeline-meta"><span className="legend"><i className="hindcast" /> Hindcast</span><span className="legend"><i className="forecast" /> Forecast</span><b>UTC</b></div></div><div className="timeline-body"><button className="play" onClick={() => setPlaying(!playing)}>{playing ? 'Ⅱ' : '▶'}</button><div className="scrubber"><div className="scrub-line"><span className="scrub-progress" style={{ width: playing ? '68%' : '44%' }} /><i className="scrub-knob" style={{ left: playing ? '68%' : '44%' }} /></div><div className="dates"><span>22 AUG<br /><b>00:00</b></span><span>23 AUG<br /><b>00:00</b></span><span className="now">24 AUG<br /><b>08:42</b></span><span>25 AUG<br /><b>00:00</b></span><span>26 AUG<br /><b>00:00</b></span></div></div><button className="speed">1× <span>⌄</span></button></div></section>
      </main><footer><span>OCEANTRACE OPS v1.8.2</span><span>ALL SYSTEMS NOMINAL <i /></span><span>LAST SYNC 08:44:12 UTC</span></footer>
    </div>
  )
}

export default App
