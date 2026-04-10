function MapShowcase({
  title = 'MealMatch Mapping System',
  description = 'MealMatch uses location-based matching to connect donors with nearby shelters, food banks, and people in need. This placeholder is structured to be replaced with a live interactive map later.',
  compact = false,
}) {
  return (
    <section className={compact ? 'map-showcase map-showcase-compact' : 'map-showcase'}>
      <div className="map-copy">
        <p className="eyebrow">Core Platform Feature</p>
        <h2>{title}</h2>
        <p>{description}</p>
      </div>

      <div className="map-card" aria-label="Map interface placeholder">
        <div className="map-toolbar">
          <span className="map-pill">Live Radius Matching</span>
          <span className="map-pill map-pill-muted">Future interactive map</span>
        </div>

        <div className="map-grid">
          <div className="map-node map-node-donor">
            <strong>Donor Hub</strong>
            <span>Restaurants and grocers posting surplus food</span>
          </div>
          <div className="map-node map-node-route">
            <strong>Routing Layer</strong>
            <span>Location data aligns pickup windows and distance</span>
          </div>
          <div className="map-node map-node-recipient">
            <strong>Recipient Network</strong>
            <span>Shelters, banks, and support partners nearby</span>
          </div>
        </div>

        <div className="map-overlay">
          <div className="map-pin map-pin-one" />
          <div className="map-pin map-pin-two" />
          <div className="map-pin map-pin-three" />
          <div className="map-route" />
        </div>
      </div>
    </section>
  )
}

export default MapShowcase
