import axios from "axios";
import { useEffect, useState } from "react";
import "./App.css"; // ملف CSS خارجي

function App() {
  const [data, setData] = useState(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamUrl, setStreamUrl] = useState("");

  // جلب بيانات السيرفر عند تحميل الصفحة
  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/")
      .then((response) => setData(response.data))
      .catch((error) => console.error("Error fetching server data:", error));
  }, []);

  // 🎥 دالة بدء البث
  const startStreaming = () => {
    setIsStreaming(true);
    setStreamUrl("http://127.0.0.1:5000/video_feed?${new Date().getTime()}"); // تحديث الرابط لمنع التخزين المؤقت
  };

  // ⏹️ دالة إيقاف البث
  const stopStreaming = () => {
    setIsStreaming(false);
    setStreamUrl(""); // إفراغ الرابط لإخفاء الفيديو
  };

  return (
    <div className="App">
      {/* ✅ الهيدر */}
      <header className="header">
        <h1>🎥 Object Recognition App</h1>
      </header>

      {/* ✅ المحتوى الرئيسي */}
      <main className="main-content">
        <section className="data-section">
          <h2>📊 Server Data</h2>
          {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : <p>جاري التحميل...</p>}
        </section>

        <section className="stream-section">
          <h2>📡 Broadcast Analysis</h2>

          {isStreaming ? (
            <img src={streamUrl} alt="Camera Stream" className="video-feed" />
          ) : (
            <div className="placeholder">🚫 Broadcast is down</div>
          )}

          {/* ✅ أزرار التحكم */}
          <div className="button-group">
            {!isStreaming ? (
              <button className="start-btn" onClick={startStreaming}>
                ▶️ Start Broadcast
              </button>
            ) : (
              <button className="stop-btn" onClick={stopStreaming}>
                ⏹️ Stop Broadcast
              </button>
            )}
          </div>
        </section>
      </main>

      {/* ✅ الفوتر */}
      <footer className="footer">
        <p>© 2024 Object Recognition App | Made with Abdullah_Salah</p>
      </footer>
    </div>
  );
}

export default App;