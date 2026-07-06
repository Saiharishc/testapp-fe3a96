import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [echoedMessage, setEchoedMessage] = useState('');

  const handleTestClick = async () => {
    try {
      const response = await fetch('/api/test');
      const data = await response.json();
      alert(data.message);
    } catch (error) {
      console.error('Error fetching /api/test:', error);
      alert('Error reaching backend.');
    }
  };

  const handleEchoMessageChange = (event) => {
    setMessage(event.target.value);
  };

  const handleEchoSubmit = async (event) => {
    event.preventDefault();
    if (!message) return;
    try {
      const response = await fetch(`/api/test/${message}`);
      const data = await response.json();
      setEchoedMessage(data.echo);
    } catch (error) {
      console.error(`Error fetching /api/test/${message}:`, error);
      alert('Error reaching backend.');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to TestApp</h1>
        <button onClick={handleTestClick}>Test Backend</button>
        <form onSubmit={handleEchoSubmit} style={{ marginTop: '20px' }}>
          <input
            type="text"
            value={message}
            onChange={handleEchoMessageChange}
            placeholder="Enter a message to echo"
          />
          <button type="submit">Echo Message</button>
        </form>
        {echoedMessage && (
          <p style={{ marginTop: '20px' }}>
            Backend echoed: <strong>{echoedMessage}</strong>
          </p>
        )}
      </header>
    </div>
  );
}

export default App;
