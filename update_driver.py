# update_driver.py
import undetected_chromedriver as uc
import time

print("INFO: Iniciando a verificação e atualização do chromedriver...")

try:
    # Instanciar o Chrome com use_subprocess=False é importante para
    # garantir que o patch seja aplicado corretamente no processo principal.
    driver = uc.Chrome(use_subprocess=False)

    print(
        "INFO: WebDriver inicializado com sucesso. Navegando para uma página de teste..."
    )
    driver.get("https://www.google.com")

    print(f"INFO: Título da página: {driver.title}")
    print("INFO: Pausando por 5 segundos para garantir que tudo está estável...")
    time.sleep(5)

    driver.quit()

    print(
        "✅ SUCESSO: O chromedriver está instalado, atualizado e funcionando corretamente."
    )

except Exception as e:
    print("❌ ERRO: Ocorreu uma falha durante a atualização ou teste do driver.")
    print(f"   -> Detalhes do erro: {e}")
