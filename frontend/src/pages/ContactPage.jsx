function ContactPage() {
  return (
    <div className="page-content">
      <section className="page-hero page-hero-compact">
        <p className="eyebrow">Contact</p>
        <h1>Reach the MealMatch team for feedback, collaboration, or demo questions.</h1>
        <p className="hero-text">
          This page presents a clean support layout with contact details and a
          simple inquiry form suitable for a class demo.
        </p>
      </section>

      <section className="content-section form-layout">
        <div className="surface-card info-panel">
          <p className="eyebrow">Support Info</p>
          <h2>Contact details</h2>
          <div className="info-list">
            <div>
              <strong>Email</strong>
              <p>hello@mealmatch.org</p>
            </div>
            <div>
              <strong>Phone</strong>
              <p>(555) 010-2026</p>
            </div>
            <div>
              <strong>Office Hours</strong>
              <p>Monday to Friday, 9:00 AM to 5:00 PM</p>
            </div>
          </div>

          <div className="info-highlight">
            <strong>Demo note</strong>
            <p>
              In a full production version, this page could connect to support
              routing, volunteer requests, or partner outreach workflows.
            </p>
          </div>
        </div>

        <form className="surface-card form-card">
          <div className="form-header">
            <h2>Contact Form</h2>
            <p>Send a message to the MealMatch team.</p>
          </div>

          <div className="form-grid">
            <label>
              Full Name
              <input type="text" placeholder="Your name" />
            </label>
            <label>
              Email Address
              <input type="email" placeholder="your@email.com" />
            </label>
            <label>
              Subject
              <input type="text" placeholder="Question about the demo" />
            </label>
            <label>
              Organization
              <input type="text" placeholder="School, nonprofit, or business" />
            </label>
            <label className="field-full">
              Message
              <textarea
                rows="6"
                placeholder="Write your message here"
              />
            </label>
          </div>

          <button className="button button-primary" type="submit">
            Send Message
          </button>
        </form>
      </section>
    </div>
  )
}

export default ContactPage
