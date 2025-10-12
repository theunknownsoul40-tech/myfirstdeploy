import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Header.css';

const Header = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <header className="header">
      <div className="header-container">
        <Link to="/" className="header-logo">
          <img src="/images/logo.png" alt="AI Mentor" className="header-logo-image" style={{ width: 78, height: 78, objectFit: 'contain' }} />
        </Link>
        
        <nav className="header-nav">
          <ul className="header-nav-list">
            <li className="header-nav-item">
              <Link to="/" className={`header-nav-link ${isActive('/') ? 'active' : ''}`}>Home</Link>
            </li>
            <li className="header-nav-item">
              <Link to="/gallery" className={`header-nav-link ${isActive('/gallery') ? 'active' : ''}`}>Gallery</Link>
            </li>
            <li className="header-nav-item">
              <Link to="/design" className={`header-nav-link ${isActive('/design') ? 'active' : ''}`}>Design</Link>
            </li>
            {/* <li className="header-nav-item">
              <Link to="/pricing" className="header-nav-link">Pricing</Link>
            </li> */}
          </ul>
        </nav>

        <div className="header-actions">
          <button className="search-button" aria-label="Search">
            <img src="/images/search icon png.png" alt="Search" style={{width: '20px', height: '20px', filter: 'brightness(0) invert(1)'}} />
          </button>
          <button className="login-button">
            <img src="/images/lock-icon.png.png" alt="Login" style={{width: '16px', height: '16px', filter: 'brightness(0) invert(1)'}} />
            Login
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;