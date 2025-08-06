// test-api.js - Script para testar a conexão com a API
const axios = require('axios');

async function testAPI() {
  console.log('🧪 Testando conexão com Aurora-Core API...\n');

  const API_URL = 'http://localhost:8000';

  try {
    // Teste 1: Health check
    console.log('1️⃣ Testando health check...');
    const healthResponse = await axios.get(`${API_URL}/`);
    console.log('✅ Health check OK:', healthResponse.data.message);

    // Teste 2: Endpoint do mentor (sem autenticação)
    console.log('\n2️⃣ Testando endpoint do mentor...');
    try {
      const mentorResponse = await axios.post(
        `${API_URL}/mentor/sales/prepare-meeting`,
        { client_name: 'Teste Cliente' },
        { headers: { 'Content-Type': 'application/json' } }
      );
      console.log('✅ Mentor endpoint OK:', mentorResponse.data);
    } catch (mentorError) {
      if (mentorError.response?.status === 401) {
        console.log('🔐 Mentor endpoint requer autenticação (401)');

        // Teste 3: Login para obter token
        console.log('\n3️⃣ Testando login...');
        try {
          const loginResponse = await axios.post(
            `${API_URL}/auth/token`,
            new URLSearchParams({
              username: 'admin',
              password: 'secret'
            }),
            { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
          );

          const token = loginResponse.data.access_token;
          console.log('✅ Login OK, token obtido');

          // Teste 4: Mentor com autenticação
          console.log('\n4️⃣ Testando mentor com autenticação...');
          const authenticatedResponse = await axios.post(
            `${API_URL}/mentor/sales/prepare-meeting`,
            { client_name: 'Teste Cliente Autenticado' },
            {
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
              }
            }
          );
          console.log('✅ Mentor com auth OK:', authenticatedResponse.data);

        } catch (loginError) {
          console.log('❌ Erro no login:', loginError.response?.data || loginError.message);
        }
      } else {
        console.log('❌ Erro no mentor:', mentorError.response?.data || mentorError.message);
      }
    }

  } catch (error) {
    if (error.code === 'ECONNREFUSED') {
      console.log('❌ Não foi possível conectar com a API.');
      console.log('💡 Certifique-se de que o Aurora-Core está rodando:');
      console.log('   poetry run uvicorn src.aurora_platform.main:app --reload --port 8000');
    } else {
      console.log('❌ Erro inesperado:', error.message);
    }
  }
}

testAPI();
