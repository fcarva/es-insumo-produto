@echo off
REM =====================================================================
REM  fechar_R1.bat — fecha o item R1 do parecer (rodada 3) em um clique.
REM  Na maquina local (onde esta o Material IO):
REM    1. troca para a branch de trabalho e atualiza;
REM    2. preserva versoes locais originais dos scripts 24/25, se existirem;
REM    3. roda 25_decomposicao_fd.py e 24_micro_mult_chave.py;
REM       (cada um AUTOVERIFICA contra as tabelas publicadas e falha se divergir)
REM    4. se ambos passarem, commita e pusha os CSVs gerados.
REM  Nada e commitado se qualquer assert falhar.
REM =====================================================================
setlocal
cd /d "%~dp0"
set BRANCH=claude/espirito-santo-io-analysis-5gpy8h

echo [1/4] Atualizando a branch %BRANCH%...
git fetch origin %BRANCH% || goto :fail

REM preserva scripts locais NAO rastreados antes do checkout (evita conflito)
for %%f in (24_micro_mult_chave 25_decomposicao_fd) do (
    if exist "pesquisa\%%f.py" (
        git ls-files --error-unmatch "pesquisa/%%f.py" >nul 2>&1 || (
            echo   - preservando versao local original: pesquisa\%%f.py -^> %%f.local.py
            ren "pesquisa\%%f.py" "%%f.local.py"
        )
    )
)
git checkout %BRANCH% || goto :fail
git pull origin %BRANCH% || goto :fail

echo.
echo [2/4] Rodando 25_decomposicao_fd.py (decomposicao da demanda final)...
python "pesquisa\25_decomposicao_fd.py" || goto :failassert

echo.
echo [3/4] Rodando 24_micro_mult_chave.py (multiplicadores territoriais)...
python "pesquisa\24_micro_mult_chave.py" || goto :failassert

echo.
echo [4/4] Asserts OK — commitando e pushando os CSVs...
git add pesquisa/outputs/decomposicao_fd.csv pesquisa/outputs/decomposicao_fd_setorial.csv pesquisa/outputs/micro_multiplicadores.csv
git commit -m "R1: CSVs das Tabelas 1 e 4 gerados do dado bruto (autoverificacao OK)" || goto :fail
git push origin %BRANCH% || goto :fail

echo.
echo ============================================================
echo [OK] R1 FECHADO: CSVs validados, commitados e pushados.
echo      O rastro reprodutivel do artigo esta 100%% completo.
echo ============================================================
if exist "pesquisa\24_micro_mult_chave.local.py" echo NOTA: sua versao local original foi preservada como *.local.py — compare se quiser.
if exist "pesquisa\25_decomposicao_fd.local.py"  echo NOTA: sua versao local original foi preservada como *.local.py — compare se quiser.
goto :eof

:failassert
echo.
echo ============================================================
echo [FAIL] Um script NAO reproduziu a tabela publicada (veja os
echo        itens FAIL acima). NADA foi commitado.
echo        Se voce tem a versao original do script (agora salva
echo        como *.local.py), rode-a e compare as saidas — ou me
echo        mande o output acima que eu ajusto a reconstrucao.
echo ============================================================
exit /b 1

:fail
echo.
echo [ERRO] Falha de git (branch/checkout/push). Veja a mensagem acima.
exit /b 1
