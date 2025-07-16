from fastapi import APIRouter, Depends, HTTPException, status
from src.aurora_platform.services.agent_profiling_service import AgentProfilingService

router = APIRouter(
    prefix="/profiling",
    tags=["Agent Profiling"]
)

def get_profiling_service():
    return AgentProfilingService()

@router.post("/run", status_code=status.HTTP_202_ACCEPTED)
async def run_profiling_suite(
    profiling_service: AgentProfilingService = Depends(get_profiling_service)
):
    """
    Dispara a execução completa da suíte de benchmarks de IA.
    Esta é uma operação que pode levar tempo.
    """
    try:
        results = profiling_service.run_benchmarks()
        summary = {
            "message": "Suíte de benchmarking executada com sucesso.",
            "total_tests_run": len(results),
            "results_log_file": "profiling_results.json"
        }
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao executar a suíte de benchmarks: {e}"
        )
