import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate, useParams } from 'react-router-dom';
import { BookOpen, Users, Landmark, Shield, Globe, Cpu, Info, ChevronLeft, Search } from 'lucide-react';
import researchData from './data/research-data.json';
import ReactMarkdown from 'react-markdown';

const Sidebar = ({ searchQuery, setSearchQuery }) => {
  const categories = [
    { id: 'summary', name: 'Overview', path: '/', icon: <Info size={20} /> },
    { id: 'cases', name: 'Cases', path: '/cases', icon: <BookOpen size={20} /> },
    { id: 'people', name: 'People', path: '/people', icon: <Users size={20} /> },
    { id: 'organizations', name: 'Organizations', path: '/organizations', icon: <Landmark size={20} /> },
    { id: 'technologies', name: 'Technologies', path: '/technologies', icon: <Cpu size={20} /> },
    { id: 'places', name: 'Places', path: '/places', icon: <Globe size={20} /> },
    { id: 'programs', name: 'Programs', path: '/programs', icon: <Shield size={20} /> },
  ];

  return (
    <div className="sidebar" style={{ width: '280px', borderRight: '1					1px solid var(--border-color)', padding: '2rem 1rem', minHeight: '100vh' }}>
      <div style={{ marginBottom: '2rem', fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--accent-color)', letterSpacing: '2px' }}>
        PHENOMENON
      </div>
      <nav>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {categories.map((cat) => (
            <li key={cat.id} style={{ marginBottom: '0.5rem' }}>
              <Link 
                to={cat.path} 
                style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  padding: '0.75rem 1rem',
                  textDecoration: 'none',
                  color: 'var(--text-primary)',
                  borderRadius: '4px',
                  transition: 'all 0.2s'
                }}
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'var(--card-bg)'}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
              >
                <span style={{ marginRight: '0.75rem' }}>{cat.icon}</span>
                {cat.name}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
};

const CategoryView = ({ categoryId, searchQuery }) => {
  const items = researchData.categories[categoryId] || [];
  const filteredItems = items.filter(item => 
    item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.content.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (categoryId === 'summary') {
    return (
      <div className="markdown-content">
        <h1 style={{ marginBottom: '1.5rem' }}>Phenomenon Overview</h1>
        <ReactMarkdown>{researchData.summary}</ReactMarkdown>
      </div>
    );
  }

  return (
    <div>
      <h1 style={{ marginBottom: '2rem', textTransform: 'capitalize' }}>{categoryId}</h1>
      <div className="grid">
        {filteredItems.length > 0 ? (
          filteredItems.map((item) => (
            <Link key={item.id} to={`/item/${encodeURIComponent(item.id)}`} style={{ textDecoration: 'none' }}>
              <div className="card">
                <h3 style={{ marginTop: 0, color: 'var(--accent-color)' }}>{item.title}</h3>
                <p style={{ 
                  fontSize: '0.9rem', 
                  color: 'var(--text-secondary)',
                  display: '-webkit-box',
                  WebkitLineClamp: 3,
                  WebkitBoxOrient: 'vertical',
                  overflow: 'hidden',
                  margin: 0
                }}>
                  {item.content.substring(0, 150)}...
                </p>
              </div>
            </Link>
          ))
        ) : (
          <p style={{ color: 'var(--text-secondary)' }}>No results found in {categoryId}.</p>
        )}
      </div>
    </div>
  );
};

const ItemView = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const decodedId = decodeURIComponent(id);
  
  let item = null;
  for (const cat in researchData.categories) {
    const found = researchData.categories[cat].find(i => i.id === decodedId);
    if (found) {
      item = found;
      break;
    }
  }

  if (!item) return <div className="card">Item not found.</div>;

  return (
    <div className="markdown-content">
      <button onClick={() => navigate(-1)} style={{ marginBottom: '2rem', cursor: 'pointer', background: 'none', border: 'none', color: 'var(--accent-color)', fontSize: '1rem', display: 'flex', alignItems: 'center', padding: 0 }}>
        <ChevronLeft size={20} />
        Back
      </button>
      <h1 style={{ marginBottom: '1.5rem' }}>{item.title}</h1>
      <ReactMarkdown>{item.content}</ReactMarkdown>
    </div>
  );
};

const App = () => {
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <Router>
      <div style={{ display: 'flex', minHeight: '100vh', backgroundColor: 'var(--bg-color)' }}>
        <Sidebar searchQuery={searchQuery} setSearchQuery={setSearchQuery} />
        <main style={{ flex: 1 }}>
          <div className="container">
            <div style={{ marginBottom: '2rem', position: 'relative' }}>
              <div style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-secondary)' }}>
                <Search size={20} />
              </div>
              <input
                type="text"
                className="search-bar"
                placeholder="Search the phenomenon archives..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                style={{ paddingLeft: '2.5rem' }}
              />
            </div>
            <Routes>
              <Route path="/" element={<CategoryView categoryId="summary" searchQuery={searchQuery} />} />
              <Route path="/summary" element={<CategoryView categoryId="summary" searchQuery={searchQuery} />} />
              <Route path="/cases" element={<CategoryView categoryId="cases" searchQuery={searchQuery} />} />
              <Route path="/people" element={<CategoryView categoryId="people" searchQuery={searchQuery} />} />
              <Route path="/organizations" element={<CategoryView categoryId="organizations" searchQuery={searchQuery} />} />
              <Route path="/technologies" element={<CategoryView categoryId="technologies" searchQuery={searchQuery} />} />
              <Route path="/places" element={<CategoryView categoryId="places" searchQuery={searchQuery} />} />
              <Route path="/programs" element={<CategoryView categoryId="programs" searchQuery={searchQuery} />} />
              <Route path="/item/:id" element={<ItemView />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
};

export default App;
