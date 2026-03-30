# Fuinha Network Monitor v3.0

## Como Rodar o Projeto
1. Instale as dependências:
   ```bash
   pip install psutil customtkinter pystray Pillow
   ```
2. Inicie o Fuinha:
   ```bash
   python main.py
   ```

## Como Gerar os Instaladores

### Windows
1. Instale o PyInstaller: `pip install pyinstaller`
2. Gere o executável:
   ```bash
   cd build_tools
   pyinstaller fuinha.spec
   ```
3. O resultado estará na pasta `dist/Fuinha`.
4. Use o Inno Setup para compilar o arquivo `fuinha.iss` e gerar o `Setup.exe`.

### Linux (.deb)
1. Gere o executável usando o PyInstaller (mesmo comando acima).
2. Prepare a estrutura debian:
   ```bash
   mkdir -p fuinha-pkg/DEBIAN
   mkdir -p fuinha-pkg/usr/bin
   mkdir -p fuinha-pkg/usr/share/fuinha
   ```
3. Copie os arquivos de `dist/Fuinha` para `fuinha-pkg/usr/share/fuinha`.
4. Crie um script em `/usr/bin/fuinha` que aponte para o executável.
5. Copie `build_tools/debian/control` para `fuinha-pkg/DEBIAN/control`.
6. Compile o pacote:
   ```bash
   dpkg-deb --build fuinha-pkg
   ```

---
*Fuinha - Traduzindo sua rede.*
