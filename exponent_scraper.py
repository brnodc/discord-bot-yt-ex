from playwright.sync_api import sync_playwright
import time

def get_implied_apy(url: str) -> float | None:
    """
    Navega até a URL fornecida, localiza o elemento que contém o Implied APY
    e retorna o valor como um float.
    """
    implied_apy_value = None
    with sync_playwright() as p:
        browser = None
        try:
            browser = p.chromium.launch(headless=True) # headless=False para depuração visual
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=60000) # Espera a rede ficar ociosa
            
            # Espera um pouco mais para garantir que o conteúdo dinâmico seja carregado
            # Isso pode precisar de ajuste dependendo da velocidade de carregamento da página
            time.sleep(5) 

            # O seletor CSS é baseado na informação fornecida pelo usuário
            # <p class="body-md leading-[1] sm:body-lg sm:leading-[11px]">18.28%</p>
            # As classes do Tailwind podem ser um pouco instáveis se a estrutura do site mudar.
            # Uma abordagem mais robusta seria procurar por um texto próximo ou um ID, se disponível.
            # Por enquanto, usaremos o seletor de classe fornecido.
            selector = "p.body-md.leading-\[1\].sm\:body-lg.sm\:leading-\[11px\]"
            
            # Tenta localizar o elemento. Pode haver múltiplos elementos com essa classe.
            # Precisamos encontrar o correto. O usuário indicou que este é o elemento.
            element = page.query_selector(selector)

            if element:
                raw_text = element.inner_text()
                print(f"Texto extraído bruto: {raw_text}")
                # Remove o símbolo de porcentagem e converte para float
                cleaned_text = raw_text.replace("%", "").strip()
                implied_apy_value = float(cleaned_text)
            else:
                print(f"Elemento com seletor '{selector}' não encontrado.")
                # Salva o HTML da página para depuração se o elemento não for encontrado
                page_content = page.content()
                with open("/home/ubuntu/page_content_debug.html", "w", encoding="utf-8") as f:
                    f.write(page_content)
                print("Conteúdo da página salvo em /home/ubuntu/page_content_debug.html para depuração.")

        except Exception as e:
            print(f"Ocorreu um erro ao tentar buscar o Implied APY: {e}")
            if browser:
                 page_content = page.content()
                 with open("/home/ubuntu/page_content_error.html", "w", encoding="utf-8") as f:
                    f.write(page_content)
                 print("Conteúdo da página (erro) salvo em /home/ubuntu/page_content_error.html para depuração.")
        finally:
            if browser:
                browser.close()
    return implied_apy_value

if __name__ == "__main__":
    target_url = "https://www.exponent.finance/farm/fragsol-10Jul25"
    apy = get_implied_apy(target_url)
    if apy is not None:
        print(f"O Implied APY é: {apy}%")
    else:
        print("Não foi possível obter o Implied APY.")

