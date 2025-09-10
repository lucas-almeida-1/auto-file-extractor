import os
import zipfile
import rarfile
import py7zr
import tarfile
import time
import shutil
from dotenv import load_dotenv

# --- CONFIGURAÇÃO ---
# Lista de todas as extensões suportadas pelo extrator.
SUPPORTED_EXTENSIONS = (
    '.zip', '.rar', '.7z',
    '.tar', '.gz', '.bz2', '.xz',
    '.tgz', '.tbz2', '.txz'
)

def check_dependencies():
    """Verifica se as dependências para extrair .rar estão presentes."""
    if not shutil.which("unrar") and not os.path.exists("UnRAR.exe"):
        print("="*60)
        print("!!! ATENÇÃO: DEPENDÊNCIA PARA .RAR NÃO ENCONTRADA !!!")
        print("Para extrair arquivos .rar, o programa 'UnRAR' precisa estar visível.")
        print("Solução: Baixe o 'UnRAR.exe' de 'rarlab.com/rar_add.htm' e")
        print("COLOQUE O ARQUIVO 'UnRAR.exe' NA MESMA PASTA DESTE SCRIPT.")
        print("="*60)
        input("Pressione Enter para continuar (a extração de .rar irá falhar)...")
        return False
    return True

def attempt_extraction(full_archive_path, target_path):
    """
    Tenta extrair um único arquivo compactado, lidando com diferentes formatos.
    Retorna True se bem-sucedido, False caso contrário.
    """
    try:
        # Define o nome da pasta de destino com base no nome do arquivo (sem extensão)
        folder_name = os.path.basename(full_archive_path)
        folder_name = os.path.splitext(folder_name)[0]
        if folder_name.lower().endswith('.tar'):
            folder_name = os.path.splitext(folder_name)[0]

        extraction_folder = os.path.join(target_path, folder_name)
        os.makedirs(extraction_folder, exist_ok=True)

        archive_filename = os.path.basename(full_archive_path)

        # --- Lógica de Extração ---
        if archive_filename.lower().endswith('.zip'):
            with zipfile.ZipFile(full_archive_path, 'r') as archive:
                files_to_extract = [m for m in archive.infolist() if not m.is_dir()]
                print(f"    - {len(files_to_extract)} arquivos detectados para extração.")
                archive.extractall(path=extraction_folder, members=files_to_extract)
        
        elif archive_filename.lower().endswith('.rar'):
            with rarfile.RarFile(full_archive_path, 'r') as archive:
                files_to_extract = [m for m in archive.infolist() if not m.isdir()]
                print(f"    - {len(files_to_extract)} arquivos detectados para extração.")
                archive.extractall(path=extraction_folder, members=files_to_extract)

        elif archive_filename.lower().endswith('.7z'):
            with py7zr.SevenZipFile(full_archive_path, mode='r') as archive:
                print(f"    - {len(archive.getnames())} arquivos detectados para extração.")
                archive.extractall(path=extraction_folder)
        
        elif any(archive_filename.lower().endswith(ext) for ext in ['.tar', '.gz', '.bz2', '.xz', '.tgz', '.tbz2', '.txz']):
            with tarfile.open(full_archive_path, mode='r:*') as archive:
                files_to_extract = [m for m in archive.getmembers() if m.isfile()]
                print(f"    - {len(files_to_extract)} arquivos detectados para extração.")
                archive.extractall(path=extraction_folder, members=files_to_extract)
        
        else:
            print(f"    [ERRO] Formato não suportado para '{archive_filename}'.")
            return False

        print(f"      - Extração concluída para a pasta '{folder_name}'.")
        return True

    except Exception as e:
        print(f"\n    [ERRO] Falha ao extrair '{os.path.basename(full_archive_path)}': {e}\n")
        return False

def main():
    """Função principal do script."""
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()
    check_dependencies()
    
    # --- DEFINIÇÃO DOS CAMINHOS ---
    # Tenta ler o caminho do arquivo .env. Se não encontrar, usa o diretório do script como padrão.
    source_path = os.getenv("SOURCE_PATH", default=os.getcwd())
    
    # Tenta ler o caminho de destino. Se não encontrar, cria a pasta "uncompressed" dentro do source_path.
    default_target = os.path.join(source_path, "uncompressed")
    target_path = os.getenv("TARGET_PATH", default=default_target)
    
    print("="*50)
    print("Iniciando o Extrator Universal...")
    print(f"Pasta de origem: {source_path}")
    print(f"Pasta de destino: {target_path}")
    print("="*50)

    # Garante que a pasta de destino exista
    os.makedirs(target_path, exist_ok=True)

    try:
        all_files = os.listdir(source_path)
        archives_to_process = [f for f in all_files if f.lower().endswith(SUPPORTED_EXTENSIONS)]
    except FileNotFoundError:
        print(f"[ERRO] O diretório de origem '{source_path}' não foi encontrado.")
        return

    if not archives_to_process:
        print(f"[AVISO] Nenhum arquivo com as extensões {SUPPORTED_EXTENSIONS} foi encontrado.")
        return

    total_archives = len(archives_to_process)
    archive_padding = len(str(total_archives))
    print(f"Total de {total_archives} arquivos compactados encontrados.\n")

    failed_archives = []

    for index, archive_filename in enumerate(archives_to_process, start=1):
        full_archive_path = os.path.join(source_path, archive_filename)
        archive_counter = str(index).zfill(archive_padding)
        
        print(f"--> Processando: {archive_filename} ({archive_counter}/{total_archives})")
        
        success = attempt_extraction(full_archive_path, target_path)
        if not success:
            failed_archives.append(full_archive_path)
        
        print("-" * 20)

    if failed_archives:
        print("\n" + "="*50)
        print("Processo de extração inicial concluído.")
        print("Os seguintes arquivos apresentaram erro:")
        for failed in failed_archives:
            print(f" - {os.path.basename(failed)}")
        print("="*50, "\n")
        
        retrying_archives = list(failed_archives)
        
        for failed_path in retrying_archives:
            filename = os.path.basename(failed_path)
            while True:
                choice = input(f"O que fazer com '{filename}'? [R]etentar extração ou [I]gnorar? ").upper()
                if choice in ['R', 'I']:
                    break
                print("Opção inválida. Digite 'R' ou 'I'.")
            
            if choice == 'R':
                print(f"--> Tentando novamente: {filename}")
                if attempt_extraction(failed_path, target_path):
                    print(f"    - Sucesso! '{filename}' foi extraído.")
                    failed_archives.remove(failed_path)
                else:
                    print(f"    - A extração de '{filename}' falhou novamente.")
            else:
                print(f"    - '{filename}' foi ignorado.")
            print("-" * 20)

    print("\n" + "="*50)
    print("RELATÓRIO FINAL")
    print("="*50)

    if not failed_archives:
        print("✅ Sucesso! Todos os arquivos foram extraídos corretamente.")
    else:
        print("⚠️ Processo finalizado com pendências.")
        print("Os seguintes arquivos não puderam ser extraídos:")
        for failed_path in failed_archives:
            print(f" - {os.path.basename(failed_path)}")

    print("="*50)


if __name__ == "__main__":
    main()