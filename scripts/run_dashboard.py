#!/usr/bin/env python3
# run_dashboard.py
import subprocess
import sys
from pathlib import Path

def run_dashboard():
    """Executa o dashboard Streamlit."""
    dashboard_path = Path(__file__).parent / "dashboard.py"
    
    try:
        print("🚀 Iniciando Aurora Project Dashboard...")
        print("📊 Acesse: http://localhost:8501")
        print("⏹️  Para parar: Ctrl+C")
        print("-" * 50)
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(dashboard_path),
            "--server.port=8501",
            "--server.address=localhost"
        ])
        
    except KeyboardInterrupt:
        print("\n✅ Dashboard encerrado.")
    except Exception as e:
        print(f"❌ Erro ao executar dashboard: {e}")

if __name__ == "__main__":
    run_dashboard()