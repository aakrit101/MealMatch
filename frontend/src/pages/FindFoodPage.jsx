import MapShowcase from '../components/MapShowcase'
import { listings } from '../data/siteContent'

function FindFoodPage() {
  return (
    <div className="page-content">
      <section className="page-hero page-hero-compact">
        <p className="eyebrow">Find Food</p>
        <h1>Browse nearby support options and future map-based match results.</h1>
        <p className="hero-text">
          This page is designed to integrate directly with the MealMatch mapping
          system, making it easy to discover food support partners and pickup
          opportunities by location.
        </p>
      </section>

      <section className="content-section">
        <div className="surface-card filter-bar">
          <label>
            Location
            <input type="text" placeholder="Enter city or neighborhood" />
          </label>
          <label>
            Food Type
            <select defaultValue="">
              <option value="" disabled>
                Any food type
              </option>
              <option>Prepared meals</option>
              <option>Produce</option>
              <option>Pantry goods</option>
              <option>Support partner</option>
            </select>
          </label>
          <label>
            Availability
            <select defaultValue="">
              <option value="" disabled>
                Any availability
              </option>
              <option>Available now</option>
              <option>Today</option>
              <option>Tomorrow</option>
            </select>
          </label>
          <button className="button button-primary" type="button">
            Search
          </button>
        </div>
      </section>

      <MapShowcase
        compact
        title="Future-ready map experience for location-based food access"
        description="The Find Food page is structured to support a real interactive map later. For now, this premium placeholder presents how MealMatch will connect nearby donors, shelters, food banks, and support partners through location-aware matching."
      />

      <section className="content-section">
        <div className="section-heading">
          <p className="eyebrow">Sample Listings</p>
          <h2>Example pickup locations and community support partners</h2>
        </div>

        <div className="card-grid card-grid-three">
          {listings.map((listing) => (
            <article className="surface-card listing-card" key={listing.name}>
              <div className="listing-meta">
                <span className="listing-type">{listing.type}</span>
                <span>{listing.location}</span>
              </div>
              <h3>{listing.name}</h3>
              <p>{listing.details}</p>
              <div className="listing-footer">
                <strong>{listing.availability}</strong>
                <button className="button button-secondary" type="button">
                  View Details
                </button>
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  )
}

export default FindFoodPage
