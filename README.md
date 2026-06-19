# Trabalho RoKiSim - Cinematica Direta

Modelagem de cinematica direta do robo ABB IRB6640 320 130 com garra IRB1600_Pince, desenvolvida para a disciplina Robotica I.

O programa calcula a posicao do frame 6 e a posicao final da ponta da garra, chamada ponto H, a partir dos seis angulos das juntas do robo.

## Arquivos do projeto

- `irb6640_320_130_COM_GARRA_FINAL_COMENTADO.py`: programa principal comentado.
- `requirements.txt`: dependencias Python do projeto.
- `.gitignore`: arquivos e pastas que nao devem ser enviados ao GitHub, como `.venv/` e caches do Python.

## Requisitos

- Python 3.10 ou superior.
- `pip`, normalmente instalado junto com o Python.
- Git, caso voce queira versionar e enviar o projeto para o GitHub.

Dependencia Python usada pelo programa:

```txt
numpy
```

## Como preparar o ambiente

Recomenda-se usar uma virtual environment (`venv`) para instalar as dependencias apenas dentro deste projeto.

### Windows PowerShell

Entre na pasta do projeto:

```powershell
cd "C:\caminho\para\Trabalho-RoKiSim-Cinematica-Direta-Robotica-1-Debora-Sales-Costa"
```

Crie a env:

```powershell
python -m venv .venv
```

Ative a env:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
python -m pip install -r requirements.txt
```

Se o PowerShell bloquear a ativacao da env, rode o Python diretamente pela env:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Windows CMD

```cmd
cd C:\caminho\para\Trabalho-RoKiSim-Cinematica-Direta-Robotica-1-Debora-Sales-Costa
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

### macOS e Linux

```bash
cd /caminho/para/Trabalho-RoKiSim-Cinematica-Direta-Robotica-1-Debora-Sales-Costa
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Como rodar o programa

Com a env ativa, execute:

```bash
python irb6640_320_130_COM_GARRA_FINAL_COMENTADO.py
```

No Windows, se preferir rodar direto pela env sem ativar:

```powershell
.\.venv\Scripts\python.exe .\irb6640_320_130_COM_GARRA_FINAL_COMENTADO.py
```

O programa vai pedir os seis angulos das juntas em graus:

```txt
M1 M2 M3 M4 M5 M6 =
```

Exemplo de entrada:

```txt
0 0 0 0 0 0
```

Para sair do programa:

```txt
sair
```

## Como desativar a env

Em qualquer sistema, use:

```bash
deactivate
```

## Como subir para o GitHub

Confira o estado do repositorio:

```bash
git status
```

Adicione os arquivos:

```bash
git add .
```

Crie um commit:

```bash
git commit -m "Adicionar programa de cinematica direta"
```

Envie para o GitHub:

```bash
git push origin main
```

Se o Git pedir login, entre com a conta do GitHub que tem permissao no repositorio.

## Configuracao de nome e e-mail dos commits

Para conferir qual nome e e-mail o Git esta usando:

```bash
git config user.name
git config user.email
```

Para configurar apenas neste repositorio:

```bash
git config user.name "Seu Nome"
git config user.email "seu-email-do-github@email.com"
```

Para configurar globalmente na maquina:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu-email-do-github@email.com"
```

## Observacao

A pasta `.venv/` nao deve ser enviada ao GitHub. Quem baixar o projeto deve recriar a env localmente usando `python -m venv .venv` e instalar as dependencias com `pip install -r requirements.txt`.
