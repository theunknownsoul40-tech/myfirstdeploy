import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/common/Button';
import './Home.css';

const Home = () => {
  const navigate = useNavigate();
  return (
    <div className="home-container">
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            The <span className="gradient-text">Future</span><br />
            in AI Graphic<br />
            Generator
          </h1>
          <p className="hero-subtitle">
            Create stunning AI-generated graphics with our advanced machine learning technology.
          </p>
          <Button 
            variant="primary" 
            size="xl" 
            onClick={() => navigate('/gallery')}
          >
            Get Started
          </Button>
        </div>
        
        <div className="hero-image-container">
          <img 
            src="/images/background.png" 
            alt="AI Woman Character" 
            className="hero-image"
          />
        </div>
      </section>
      
      {/* Floating orbs */}
      <div className="floating-orb orb-1"></div>
      <div className="floating-orb orb-2"></div>
      <div className="floating-orb orb-3"></div>
    </div>
  );
};

export default Home;