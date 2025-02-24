import axios from 'axios';
import { useEffect, useState } from 'react';
import './App.css'; // ملف CSS خارجي

function App() {
  const [data, setData] = useState(null);
  const [isStreaming, setIsStreaming] = useState(false);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/')
      .then(response => setData(response.data))
      .catch(error => console.error('Error:', error));
  }, []);

  // دالة بدء البث
  const startStreaming = () => {
    setIsStreaming(true);
  };

  // دالة إيقاف البث
  const stopStreaming = () => {
    setIsStreaming(false);
  };

  return (
    <div className="App">
      {/* الهيدر */}
      <header className="header">
        <h1>🎥 Object Recognition App</h1>
      </header>

      {/* المحتوى الرئيسي */}
      <main className="main-content">
        <section className="data-section">
          <h2>📊 Server data</h2>
          {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : <p>جاري التحميل...</p>}
        </section>

        <section className="stream-section">
          <h2>📡 Broadcast analysis</h2>

          {isStreaming ? (
            <img
              src="http://127.0.0.1:5000/video_feed"
              alt="Camera Stream"
              className="video-feed"
            />
          ) : (
            <div className="placeholder">Broadcast is down🚫</div>
          )}

          {/* أزرار التحكم */}
          <div className="button-group">
            {!isStreaming ? (
              <button className="start-btn" onClick={startStreaming}>▶️ Broadcast started</button>
            ) : (
              <button className="stop-btn" onClick={stopStreaming}>⏹️stop broadcasting</button>
            )}
          </div>
        </section>
      </main>

      {/* الفوتر */}
      <footer className="footer">
        <p>© 2024 Object Recognition App | Made with Abdullah_Salah</p>
      </footer>
    </div>
  );
}

export default App;