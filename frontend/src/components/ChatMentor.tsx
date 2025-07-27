'use client';

import React, { useState } from 'react';
import axios from 'axios';

interface ChatMentorProps {
  className?: string;
}

interface ApiResponse {
  response?: string;
  message?: string;
  error?: string;
}

const ChatMentor: React.FC<ChatMentorProps> = ({ className = '' }) => {
  const [input, setInput] = useState<string>('');
  const [response, setResponse] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim()) {
      setError('Por favor, digite uma mensagem');
      return;
    }

    setLoading(true);
    setError('');
    setResponse('');

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

      const result = await axios.post<ApiResponse>(
        `${apiUrl}/mentor/sales/prepare-meeting`,
        {
          client_name: input.trim()
        },
        {
          headers: {
            'Content-Type': 'application/json',
          },
          timeout: 30000, // 30 segundos
        }
      );

      if (result.data.response) {
        setResponse(result.data.response);
      } else if (result.data.message) {
        setResponse(result.data.message);
      } else {
        setResponse('Resposta recebida com sucesso!');
      }

      setInput(''); // Limpa o input após sucesso

    } catch (err: any) {
      console.error('Erro na requisição:', err);

      if (err.response?.status === 401) {
        setError('Erro de autenticação. Verifique suas credenciais.');
      } else if (err.response?.status === 500) {
        setError('Erro interno do servidor. Tente novamente mais tarde.');
      } else if (err.code === 'ECONNREFUSED') {
        setError('Não foi possível conectar com a API. Verifique se o servidor está rodando.');
      } else if (err.code === 'ECONNABORTED') {
        setError('Timeout na requisição. Tente novamente.');
      } else {
        setError(err.response?.data?.detail || err.message || 'Erro desconhecido');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`chat-mentor ${className}`}>
      <div className="chat-container">
        <h2 className="chat-title">🤖 Mentor de Vendas IA</h2>
        <p className="chat-subtitle">
          Digite o nome do cliente para obter insights de vendas personalizados
        </p>

        <form onSubmit={handleSubmit} className="chat-form">
          <div className="input-group">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ex: João Silva - Empresa XYZ"
              className="chat-input"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="chat-button"
            >
              {loading ? '⏳ Processando...' : '📤 Enviar'}
            </button>
          </div>
        </form>

        {error && (
          <div className="error-message">
            <span className="error-icon">❌</span>
            <span>{error}</span>
          </div>
        )}

        {response && (
          <div className="response-container">
            <h3 className="response-title">💡 Insights do Mentor:</h3>
            <div className="response-content">
              {response.split('\n').map((line, index) => (
                <p key={index}>{line}</p>
              ))}
            </div>
          </div>
        )}
      </div>

      <style jsx>{`
        .chat-mentor {
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        .chat-container {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          border-radius: 16px;
          padding: 32px;
          box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
          color: white;
        }

        .chat-title {
          font-size: 2rem;
          font-weight: bold;
          text-align: center;
          margin-bottom: 8px;
          text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }

        .chat-subtitle {
          text-align: center;
          opacity: 0.9;
          margin-bottom: 32px;
          font-size: 1.1rem;
        }

        .chat-form {
          margin-bottom: 24px;
        }

        .input-group {
          display: flex;
          gap: 12px;
          flex-wrap: wrap;
        }

        .chat-input {
          flex: 1;
          min-width: 250px;
          padding: 16px 20px;
          border: none;
          border-radius: 12px;
          font-size: 1rem;
          background: rgba(255, 255, 255, 0.95);
          color: #333;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
          transition: all 0.3s ease;
        }

        .chat-input:focus {
          outline: none;
          background: white;
          box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
          transform: translateY(-2px);
        }

        .chat-input:disabled {
          opacity: 0.7;
          cursor: not-allowed;
        }

        .chat-button {
          padding: 16px 24px;
          border: none;
          border-radius: 12px;
          background: linear-gradient(135deg, #ff6b6b, #ee5a24);
          color: white;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
          box-shadow: 0 4px 12px rgba(238, 90, 36, 0.3);
          white-space: nowrap;
        }

        .chat-button:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 6px 20px rgba(238, 90, 36, 0.4);
        }

        .chat-button:disabled {
          opacity: 0.7;
          cursor: not-allowed;
          transform: none;
        }

        .error-message {
          background: rgba(255, 107, 107, 0.2);
          border: 1px solid rgba(255, 107, 107, 0.5);
          border-radius: 12px;
          padding: 16px;
          margin-bottom: 20px;
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .error-icon {
          font-size: 1.2rem;
        }

        .response-container {
          background: rgba(255, 255, 255, 0.1);
          border-radius: 12px;
          padding: 24px;
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .response-title {
          font-size: 1.3rem;
          font-weight: 600;
          margin-bottom: 16px;
          color: #ffd700;
        }

        .response-content {
          line-height: 1.6;
          font-size: 1rem;
        }

        .response-content p {
          margin-bottom: 12px;
        }

        .response-content p:last-child {
          margin-bottom: 0;
        }

        @media (max-width: 768px) {
          .chat-mentor {
            padding: 16px;
          }

          .chat-container {
            padding: 24px;
          }

          .input-group {
            flex-direction: column;
          }

          .chat-input {
            min-width: auto;
          }

          .chat-title {
            font-size: 1.5rem;
          }
        }
      `}</style>
    </div>
  );
};

export default ChatMentor;
