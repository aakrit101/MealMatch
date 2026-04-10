import { Link } from 'react-router-dom'
import MapShowcase from '../components/MapShowcase'
import {
  features,
  impactStats,
  steps,
  teamMembers,
  testimonials,
} from '../data/siteContent'

function HomePage() {
  return (
    <div className="page-content">
      <section className="hero-section">
        <div className="hero-copy">
          <p className="eyebrow">Luxury design. Practical impact.</p>
          <h1>Elevating food recovery into a smarter community network.</h1>
          <p className="hero-text">
            MealMatch is a polished platform concept that helps restaurants,
            grocery stores, and donors route surplus food to nearby shelters,
            food banks, and people in need with speed, clarity, and trust.
          </p>

          <div className="hero-actions">
            <Link className="button button-primary" to="/donate">
              Donate Food
            </Link>
            <Link className="button button-secondary" to="/find-food">
              Explore Food Support
            </Link>
          </div>

          <div className="hero-stats">
            {impactStats.map((stat) => (
              <div key={stat.label}>
                <strong>{stat.value}</strong>
                <span>{stat.label}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="hero-panel">
          <div className="panel-card panel-card-primary">
            <p className="panel-label">Operational Snapshot</p>
            <strong>Location-based matching built for real-world handoffs</strong>
            <span>
              A premium interface for donors, partner organizations, and
              community support teams.
            </span>
          </div>

          <div className="panel-grid">
            <div className="panel-card">
              <p className="panel-label">Donors</p>
              <strong>Restaurants, grocers, events</strong>
            </div>
            <div className="panel-card">
              <p className="panel-label">Recipients</p>
              <strong>Shelters, banks, outreach partners</strong>
            </div>
          </div>
        </div>
      </section>

      <section className="content-section">
        <div className="section-heading">
          <p className="eyebrow">Platform Highlights</p>
          <h2>Clean startup-style presentation with a meaningful civic use case</h2>
        </div>

        <div className="card-grid card-grid-three">
          {features.map((feature) => (
            <article className="surface-card feature-card" key={feature.title}>
              <div className="feature-icon" aria-hidden="true" />
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="content-section split-section">
        <div className="section-heading section-heading-tight">
          <p className="eyebrow">Mission</p>
          <h2>Good food should circulate with dignity instead of being wasted.</h2>
          <p>
            MealMatch reframes food donation as a coordinated, location-aware
            service. The platform is built to reduce waste, simplify outreach,
            and strengthen the network between donors and the organizations that
            serve people every day.
          </p>
        </div>

        <div className="stacked-cards">
          <div className="surface-card">
            <strong>Reliable logistics</strong>
            <p>Pickup windows, address details, and contacts stay visible.</p>
          </div>
          <div className="surface-card">
            <strong>Better local coordination</strong>
            <p>Nearby matches help food move quickly while it is still useful.</p>
          </div>
          <div className="surface-card">
            <strong>Presentation-ready impact</strong>
            <p>Elegant summaries make the concept easy to explain in class.</p>
          </div>
        </div>
      </section>

      <section className="content-section">
        <div className="section-heading">
          <p className="eyebrow">How It Works</p>
          <h2>Three steps from surplus inventory to direct community support</h2>
        </div>

        <div className="card-grid card-grid-three">
          {steps.map((step) => (
            <article className="surface-card step-card" key={step.number}>
              <span className="step-number">{step.number}</span>
              <h3>{step.title}</h3>
              <p>{step.description}</p>
            </article>
          ))}
        </div>
      </section>

      <MapShowcase />

      <section className="content-section">
        <div className="section-heading">
          <p className="eyebrow">Impact</p>
          <h2>Designed to feel credible, measurable, and community-centered</h2>
        </div>

        <div className="card-grid card-grid-two">
          {testimonials.map((testimonial) => (
            <article className="surface-card quote-card" key={testimonial.name}>
              <p className="quote-mark">“</p>
              <p>{testimonial.quote}</p>
              <strong>{testimonial.name}</strong>
            </article>
          ))}
        </div>
      </section>

      <section className="content-section">
        <div className="section-heading">
          <p className="eyebrow">Team</p>
          <h2>Built by a team combining product design, outreach, and systems thinking</h2>
        </div>

        <div className="card-grid card-grid-three">
          {teamMembers.map((member) => (
            <article className="surface-card team-card" key={member.name}>
              <div className="team-badge">{member.name.slice(0, 1)}</div>
              <h3>{member.name}</h3>
              <p className="team-role">{member.role}</p>
              <p>{member.bio}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="cta-banner">
        <div>
          <p className="eyebrow">Ready To Present</p>
          <h2>A polished multi-page demo for MealMatch.</h2>
          <p>
            Explore the donation workflow, the mapping concept, and the
            community impact story across the full site.
          </p>
        </div>

        <div className="hero-actions">
          <Link className="button button-primary" to="/donate">
            Open Donate Page
          </Link>
          <Link className="button button-secondary" to="/contact">
            Contact The Team
          </Link>
        </div>
      </section>
    </div>
  )
}

export default HomePage
