import React, { useState } from 'react';
import './Gallery.css';

const Gallery = () => {
  const [activeCategory, setActiveCategory] = useState('Art Direction');

  const categories = ['Art Direction', 'Illustration', 'Design', 'Creative'];

  const galleryImages = [
    {
      id: 1,
      category: 'Art Direction',
      title: 'Majestic Fox Portrait',
      description: 'AI-generated stylized fox with vibrant colors',
      image: '/images/1.png'
    },
    {
      id: 2,
      category: 'Art Direction',
      title: 'Vintage Boots Still Life',
      description: 'Artistic rendering of vintage boots with flowers',
      image: '/images/2.png'
    },
    {
      id: 3,
      category: 'Illustration',
      title: 'Cosmic Astronaut',
      description: 'Surreal space exploration artwork',
      image: '/images/3.png'
    },
    {
      id: 4,
      category: 'Design',
      title: 'Geometric Spheres',
      description: 'Abstract geometric composition',
      image: '/images/4.png'
    },
    {
      id: 5,
      category: 'Creative',
      title: 'Brain Galaxy',
      description: 'Conceptual brain in cosmic setting',
      image: '/images/5.png'
    },
    {
      id: 6,
      category: 'Illustration',
      title: 'Twin Cats Portrait',
      description: 'Minimalist cat illustration',
      image: '/images/6.png'
    },
    {
      id: 7,
      category: 'Design',
      title: 'Isometric Room',
      description: '3D isometric interior design',
      image: '/images/7.jpg'
    },
    {
      id: 8,
      category: 'Creative',
      title: 'Mystical Forest',
      description: 'Atmospheric forest scene',
      image: '/images/8.jpg'
    },
    {
      id: 9,
      category: 'Art Direction',
      title: 'Digital Art Creation',
      description: 'Modern digital artwork',
      image: '/images/9.jpg'
    },
    {
      id: 10,
      category: 'Creative',
      title: 'Fantasy Landscape',
      description: 'Imaginative landscape design',
      image: '/images/10.jpg'
    },
    {
      id: 11,
      category: 'Illustration',
      title: 'Character Design',
      description: 'Creative character illustration',
      image: '/images/11.png'
    },
    {
      id: 12,
      category: 'Design',
      title: 'Abstract Composition',
      description: 'Modern abstract design',
      image: '/images/12.jpg'
    }
  ];

  const filteredImages = galleryImages.filter(
    image => image.category === activeCategory
  );

  return (
    <div className="gallery-container">
      <div className="gallery-header">
        <h1 className="gallery-title">AI-Powered Design</h1>
        <p className="gallery-description">Explore our collection of AI-generated artwork and designs</p>
      </div>

      <nav className="category-nav">
        {categories.map((category) => (
          <button
            key={category}
            className={`category-button ${activeCategory === category ? 'active' : ''}`}
            onClick={() => setActiveCategory(category)}
          >
            {category}
          </button>
        ))}
      </nav>

      <div className="gallery-grid">
        {filteredImages.map((image) => (
          <div key={image.id} className="gallery-item">
            <div className="gallery-image-container">
              <img src={image.image} alt={image.title} className="gallery-image" />
              <div className="gallery-overlay">
                <div className="overlay-content">
                  <h3>{image.title}</h3>
                  <p>{image.description}</p>
                </div>
              </div>
            </div>
            <div className="gallery-content">
              <h3>{image.title}</h3>
              <p>{image.description}</p>
              <span className="category-badge">{image.category}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Gallery;