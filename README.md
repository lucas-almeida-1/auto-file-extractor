# ⚙️ Extrator Universal de Arquivos

Um script em Python projetado para automatizar a extração de múltiplos arquivos compactados, com suporte para `.zip`, `.rar`, `.7z` e a família de arquivos `.tar` (`.tar.gz`, etc.). Ele fornece feedback detalhado no terminal e um sistema interativo para lidar com arquivos corrompidos ou com erro na descompressão.

Este projeto foi uma necessidade pessoal minha e aproveitei para testar [Poetry](https://python-poetry.org/) como gerenciador de dependências. Caso queira sugerir uma nova adição ao projeto, fique à vontade para fazer um pull request. Se o script te ajudou, dá uma estrelinha para ele!

## ✨ Principais Funcionalidades

* **Suporte Universal:** Extrai os formatos mais populares, incluindo `.zip`, `.rar`, `.7z`, `.tar`, `.tar.gz`, `.tgz`, `.tar.bz2`, `.tbz2`, `.tar.xz`, e `.txz`.
* **Extração em Massa:** Processa automaticamente todos os arquivos compactados na pasta do projeto.
* **Progresso Detalhado:** Acompanhe em tempo real o status da extração de cada arquivo.
* **Tratamento de Erros Interativo:** Permite tentar novamente ou ignorar arquivos que falharem na extração.
* **Relatório Final:** Apresenta um resumo claro dos sucessos e falhas ao final do processo.

## 📁 Estrutura de Arquivos

Para que o script funcione da forma prevista, verifique se a pasta contém os seguintes arquivos:

```
PASTA_DO_PROJETO/
├── .env                # Opcional, permite declarar o caminho da pasta dos arquivos compactados e onde devem ser extraídos
├── .env.example        # Opcional, exemplo de como preencher o arquivo .env
├── .gitignore          # Opcional, impede que certas informações sejam postadas no repositório
├── main.py             # O código principal do script extrator
├── poetry.lock         # Garante que as mesmas versões de dependências sejam usadas
├── pyproject.toml      # Arquivo de configuração do Poetry (gerencia as dependências)
├── README.md           # Opcional, você está aqui!
└── UnRAR.exe           # Opcional, mas NECESSÁRIO para extrair arquivos .rar
```

⚠️ **Importante:** Se você **não** usar o arquivo `.env` para definir um caminho de origem, coloque todos os arquivos compactados que deseja extrair **dentro desta mesma pasta** antes de rodar o script.

## 🛠️ Configuração de Pastas (Opcional)

Por padrão, o script busca os arquivos compactados na mesma pasta em que ele está e extrai o conteúdo para uma subpasta chamada `uncompressed`.

Para usar pastas específicas:
1.  **Renomeie** o arquivo `.env.example` para `.env`.
2.  **Abra o arquivo `.env`** com um editor de texto.
3.  **Descomente** (remova o `#`) e edite as variáveis `SOURCE_PATH` e `TARGET_PATH` com os caminhos desejados.

## 🚀 Instalação

Garanta que seu sistema atenda aos seguintes requisitos:

1.  **Python 3.8+**
2.  **Poetry**
3.  **Para `.rar` (Opcional):** O executável `UnRAR.exe` deve estar na pasta do projeto.

Com os pré-requisitos atendidos, siga os passos no terminal:

1.  **Clone ou baixe os arquivos** do projeto.
2.  **Adicione a dependência para ler arquivos `.env`:**
    ```bash
    poetry add python-dotenv
    ```
3.  **Instale todas as dependências:** Este comando cria o ambiente virtual e instala tudo o que o projeto precisa.
    ```bash
    poetry install
    ```

## ▶️ Como Usar

Com tudo configurado, a execução é simples:

1.  Configure seu arquivo `.env` (opcional) ou coloque seus arquivos compactados na pasta raiz.
2.  Execute o script com o seguinte comando no terminal:
    ```bash
    poetry run python main.py
    ```
3.  O script iniciará a extração. Acompanhe o progresso e, caso algum arquivo apresente erro, você será questionado ao final sobre o que fazer (`R` para tentar novamente, `I` para ignorar). Os arquivos extraídos serão salvos na pasta de destino configurada (por padrão, uma subpasta chamada `uncompressed` ou a especificada no seu arquivo `.env`). Uma nova tentativa de extração sempre usará este mesmo destino.