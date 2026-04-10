function DonatePage() {
  return (
    <div className="page-content">
      <section className="page-hero page-hero-compact">
        <p className="eyebrow">Donate Food</p>
        <h1>Share surplus food through a cleaner, more coordinated workflow.</h1>
        <p className="hero-text">
          This form represents how MealMatch can streamline donor intake for
          restaurants, grocery stores, and community organizations.
        </p>
      </section>

      <section className="content-section form-layout">
        <form className="surface-card form-card">
          <div className="form-header">
            <h2>Donate Food Form</h2>
            <p>Submit donation details so nearby partners can be matched quickly.</p>
          </div>

          <div className="form-grid">
            <label>
              Donor Name
              <input type="text" placeholder="Jane Smith" />
            </label>
            <label>
              Organization / Business Name
              <input type="text" placeholder="Green Table Bistro" />
            </label>
            <label>
              Food Type
              <select defaultValue="">
                <option value="" disabled>
                  Select food type
                </option>
                <option>Prepared meals</option>
                <option>Produce</option>
                <option>Bakery items</option>
                <option>Pantry goods</option>
              </select>
            </label>
            <label>
              Quantity
              <input type="text" placeholder="40 boxed meals" />
            </label>
            <label className="field-full">
              Pickup Address
              <input type="text" placeholder="123 Market Street, City, State" />
            </label>
            <label>
              Contact Info
              <input type="text" placeholder="email or phone number" />
            </label>
            <label>
              Preferred Pickup Time
              <input type="text" placeholder="Today, 6:00 PM" />
            </label>
            <label className="field-full">
              Notes
              <textarea
                rows="5"
                placeholder="Allergy notes, packaging details, refrigeration needs, or access instructions"
              />
            </label>
          </div>

          <button className="button button-primary" type="submit">
            Submit Donation
          </button>
        </form>

        <aside className="surface-card info-panel">
          <p className="eyebrow">How Donations Work</p>
          <h2>Designed for speed, clarity, and local coordination.</h2>
          <div className="info-list">
            <div>
              <strong>1. Share the details</strong>
              <p>Provide food type, quantity, location, and timing.</p>
            </div>
            <div>
              <strong>2. Match nearby partners</strong>
              <p>MealMatch uses location-based logic to identify the best local fit.</p>
            </div>
            <div>
              <strong>3. Coordinate pickup</strong>
              <p>Recipients and volunteers can align on quick, low-friction handoff.</p>
            </div>
          </div>

          <div className="info-highlight">
            <strong>Why this matters</strong>
            <p>
              A polished intake experience makes donor participation easier and
              helps reduce food waste at the point of surplus.
            </p>
          </div>
        </aside>
      </section>
    </div>
  )
}

export default DonatePage
