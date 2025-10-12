import React from 'react';
import './Design.css';

const Design = () => {
  const designTools = [
    {
      id: 1,
      title: 'Smart Cat Reader',
      description: 'AI-powered reading companion with glasses',
      category: 'Education',
      image: '/images/1.png'
    },
    {
      id: 2,
      title: 'Futuristic Vehicle',
      description: 'Next-gen transportation design',
      category: 'Transportation',
      image: '/images/7.jpg'
    },
    {
      id: 3,
      title: 'Neural Network Brain',
      description: 'Cognitive AI visualization tool',
      category: 'Science',
      image: '/images/5.png'
    }
    // {
    //   id: 4,
    //   title: 'Custom Motorcycle',
    //   description: 'Personalized vehicle generator',
    //   category: 'Automotive',
    //   image: '/images/10.jpg'
    // }
  ];

  return (
    <div className="design-container">
      <div className="design-header">
        <h2 style={{ color: 'white', fontSize: '1.25rem', marginBottom: '1rem' }}>What We do?</h2>
        <h1 className="design-title">
          Unleash the Potential of AI Development<br />
          Tools Crafted with <span className="gradient-text">Brilliance</span>, Style, Quality,<br />
          and Creativity
        </h1>
        <p className="design-description">
          Discover our cutting-edge AI tools designed to transform your creative workflow.
        </p>
      </div>

      <div className="tools-grid">
        {designTools.map((tool) => (
          <div key={tool.id} className="tool-card">
            <div className="tool-icon">
              🎨
            </div>
            <img src={tool.image} alt={tool.title} style={{ width: '100%', height: '200px', objectFit: 'cover', borderRadius: '12px', marginBottom: '1rem' }} />
            <div style={{ backgroundColor: 'rgba(139, 92, 246, 0.2)', color: '#8B5CF6', padding: '0.25rem 0.75rem', borderRadius: '15px', fontSize: '0.75rem', fontWeight: '600', display: 'inline-block', marginBottom: '1rem' }}>
              {tool.category}
            </div>
            <h3 className="tool-title">{tool.title}</h3>
            <p className="tool-description">{tool.description}</p>
            <ul className="tool-features">
              <li>AI-powered generation</li>
              <li>High-quality output</li>
              <li>Easy to use interface</li>
            </ul>
          </div>
        ))}
      </div>

      {/* Floating particles */}
      <div className="floating-particle particle-1"></div>
      <div className="floating-particle particle-2"></div>
      <div className="floating-particle particle-3"></div>
      <div className="floating-particle particle-4"></div>
    </div>
  );
};

export default Design;