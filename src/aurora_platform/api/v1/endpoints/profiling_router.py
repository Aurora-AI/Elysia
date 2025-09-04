from fastapi import APIRouter, status

# TODO: Reativar/substituir na integração do Crawler.
# from aurora_platform.services.agent_profiling_service import AgentProfilingService

router = APIRouter(prefix="/profiling", tags=["Agent Profiling"])


def get_profiling_service():
    # TODO: Reativar/substituir na integração do Crawler.
    # return AgentProfilingService()
    pass


@router.post("/run", status_code=status.HTTP_202_ACCEPTED)
async def run_profiling_suite():
    """
    Dispara a execução completa da suíte de benchmarks de IA.
    Esta é uma operação que pode levar tempo.
    """
    return {
        "message": "Endpoint desativado temporariamente para integração do Crawler."
    }
    # TODO: Reativar/substituir na integração do Crawler.
    # try:
    #     results = profiling_service.run_benchmarks()
    #     summary = {
    #         "message": "Suíte de benchmarking executada com sucesso.",
    #         "total_tests_run": len(results),
    #         "results_log_file": "profiling_results.json",
    #     }
    #     return summary
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f"Ocorreu um erro ao executar a suíte de benchmarks: {e}",
    #     )
    pass
