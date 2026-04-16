import { teamMembers } from '../data/siteContent'

function AboutPage() {
  return (
    <div className="page-content">
      <section className="page-hero page-hero-compact">
        <p className="eyebrow">About MealMatch</p>
        <h1>MealMatch turns location-aware food recovery into a clear platform story.</h1>
        <p className="hero-text">
          The project focuses on reducing food waste while improving access to
          meals and groceries for shelters, food banks, and people in need.
        </p>
      </section>

      <section className="content-section card-grid card-grid-two">
        <article className="surface-card">
          <p className="eyebrow">The Mission</p>
          <h2>Connect surplus food with real community need.</h2>
          <p>
            MealMatch exists to make food donation feel organized, trustworthy,
            and modern. Instead of leaving logistics scattered across calls and
            messages, the platform presents a shared system for matching food
            supply with local demand.
          </p>
        </article>

        <article className="surface-card">
          <p className="eyebrow">The Problem</p>
          <h2>Usable food is wasted while communities still face shortages.</h2>
          <p>
            Restaurants, grocery stores, and event organizers often have extra
            food, but the process of finding the right recipient nearby can be
            slow or unclear. MealMatch reduces that gap with a cleaner workflow.
          </p>
        </article>
      </section>

      <section className="content-section split-section">
        <div className="section-heading section-heading-tight">
          <p className="eyebrow">Mapping System</p>
          <h2>Location-based matching is a core feature, not an add-on.</h2>
          <p>
            MealMatch uses a mapping-focused concept to connect donors and
            recipients based on proximity, availability, and support capacity.
            This helps identify the best nearby option, reduce delays, and make
            the platform more actionable in real community settings.
          </p>
        </div>

        <div className="surface-card info-highlight info-highlight-tall">
          <strong>Why mapping matters</strong>
          <p>
            When food support is time-sensitive, location is one of the most
            important data points. A mapping system turns the platform into a
            practical decision tool instead of just a donation form.
          </p>
        </div>
      </section>

      <section className="content-section">
        <div className="section-heading">
          <p className="eyebrow">Future Goals</p>
          <h2>Where the MealMatch concept can grow next</h2>
        </div>

        <div className="card-grid card-grid-three">
          <article className="surface-card">
            <h3>Interactive live map</h3>
            <p>Replace the placeholder with real geolocation, routes, and partner markers.</p>
          </article>
          <article className="surface-card">
            <h3>Verified partner network</h3>
            <p>Support onboarding for shelters, food banks, and community organizations.</p>
          </article>
          <article className="surface-card">
            <h3>Impact analytics</h3>
            <p>Track rescued meals, donor activity, and response time across the network.</p>
          </article>
        </div>
      </section>

      <section className="content-section">
        <div className="section-heading">
          <p className="eyebrow">Team</p>
          <h2>The people behind the MealMatch demo</h2>
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
    </div>
  )
}

export default AboutPage
