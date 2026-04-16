import { NavLink, Outlet } from 'react-router-dom'

const navItems = [
  { label: 'Home', to: '/' },
  { label: 'About', to: '/about' },
  { label: 'Donate', to: '/donate' },
  { label: 'Find Food', to: '/find-food' },
  { label: 'Contact', to: '/contact' },
]

function SiteLayout() {
  return (
    <div className="app-shell">
      <div className="ambient ambient-left" aria-hidden="true" />
      <div className="ambient ambient-right" aria-hidden="true" />

      <div className="page-frame">
        <header className="site-header">
          <NavLink className="brand" to="/">
            <span className="brand-mark" aria-hidden="true">
              MM
            </span>
            <span>
              <span className="brand-name">MealMatch</span>
              <span className="brand-tag">Food donation platform</span>
            </span>
          </NavLink>

          <nav className="site-nav" aria-label="Primary">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  isActive ? 'nav-link nav-link-active' : 'nav-link'
                }
                end={item.to === '/'}
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </header>

        <main className="page-main">
          <Outlet />
        </main>

        <footer className="site-footer">
          <div className="footer-block">
            <strong>MealMatch</strong>
            <p>
              A premium class-demo concept for location-based food recovery,
              donation matching, and community support.
            </p>
          </div>

          <div className="footer-block">
            <span className="footer-heading">Explore</span>
            <div className="footer-links">
              {navItems.map((item) => (
                <NavLink key={item.to} to={item.to} end={item.to === '/'}>
                  {item.label}
                </NavLink>
              ))}
            </div>
          </div>

          <div className="footer-block">
            <span className="footer-heading">Contact</span>
            <p>hello@mealmatch.org</p>
            <p>(555) 010-2026</p>
            <p>Serving restaurants, grocers, and community partners.</p>
          </div>
        </footer>
      </div>
    </div>
  )
}

export default SiteLayout
