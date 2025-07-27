import React from 'react';
import ChatMentor from '../components/ChatMentor';

const HomePage: React.FC = () => {
  return (
    <div className="homepage">
      <header className="header">
        <h1 className="main-title">🚀 Aurora Platform</h1>
        <p className="main-subtitle">
          Plataforma de IA para Vendas e Atendimento Inteligente
        </p>
      </header>

      <main className="main-content">
        <ChatMentor />
      </main>

      <footer className="footer">
        <p>&copy; 2025 Aurora Platform - Powered by AI</p>
      </footer>

      <style jsx>{`
        .homepage {
          min-height: 100vh;
          background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
          display: flex;
          flex-direction: column;
        }

        .header {
          text-align: center;
          padding: 60px 20px 40px;
          color: white;
        }

        .main-title {
          font-size: 3.5rem;
          font-weight: bold;
          margin-bottom: 16px;
          text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
          background: linear-gradient(45deg, #ffd700, #ffed4e);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .main-subtitle {
          font-size: 1.3rem;
          opacity: 0.9;
          max-width: 600px;
          margin: 0 auto;
          line-height: 1.5;
        }

        .main-content {
          flex: 1;
          padding: 20px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .footer {
          text-align: center;
          padding: 30px 20px;
          color: rgba(255, 255, 255, 0.7);
          border-top: 1px solid rgba(255, 255, 255, 0.1);
        }

        @media (max-width: 768px) {
          .main-title {
            font-size: 2.5rem;
          }

          .main-subtitle {
            font-size: 1.1rem;
          }

          .header {
            padding: 40px 20px 30px;
          }
        }
      `}</style>
    </div>
  );
};

export default HomePage;
