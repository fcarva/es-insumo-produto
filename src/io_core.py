"""
io_core.py — implementação de referência do arcabouço inter-regional (Isard)
para "O Espírito Santo como economia-plataforma".

Reconstrução fiel ao método do artigo (reconcilie com o pipeline original da
sessão de 29/05 se houver divergência). Regiões: L = ES, M = restante do Brasil.

Esquema esperado do CSV da MIP inter-regional (dados/mip_es_br_2008.csv):
  - matriz de consumo intermediário Z empilhada por região (52 x 52), em R$ milhões;
  - linha/coluna identificadas por código de setor com sufixo de região (ex.: 0191_L, 0191_M);
  - colunas auxiliares: 'x' (produto total por setor) e 'ocup' (pessoal ocupado por setor).
Ajuste o parser ao layout exato do seu arquivo.
"""
from __future__ import annotations
import argparse
import numpy as np
import pandas as pd


# --------------------------------------------------------------------------- #
# Núcleo de Leontief / Isard
# --------------------------------------------------------------------------- #
def coef_tecnicos(Z: np.ndarray, x: np.ndarray) -> np.ndarray:
    """A = Z * xhat^{-1} (coeficientes técnicos diretos)."""
    x_safe = np.where(x == 0, 1.0, x)
    return Z / x_safe[np.newaxis, :]


def leontief_inversa(A: np.ndarray) -> np.ndarray:
    """B = (I - A)^{-1}."""
    n = A.shape[0]
    return np.linalg.inv(np.eye(n) - A)


# --------------------------------------------------------------------------- #
# Decomposição do multiplicador de produção: retido (L) vs vazado (M)
# --------------------------------------------------------------------------- #
def multiplicadores_producao(B: np.ndarray, mask_L: np.ndarray) -> pd.DataFrame:
    """
    Para cada setor-coluna j:
      O_j      = soma da coluna de B
      O^L_j    = soma sobre linhas i em L           (retido no ES)
      O^M_j    = soma sobre linhas i em M           (vazado p/ resto do Brasil)
      vaz_rel  = O^M_j / O_j
    """
    O = B.sum(axis=0)
    O_L = B[mask_L, :].sum(axis=0)
    O_M = B[~mask_L, :].sum(axis=0)
    vaz_rel = np.divide(O_M, O, out=np.zeros_like(O), where=O != 0)
    return pd.DataFrame({"O": O, "O_L": O_L, "O_M": O_M, "vazamento_rel": vaz_rel})


# --------------------------------------------------------------------------- #
# Multiplicador de emprego
# --------------------------------------------------------------------------- #
def multiplicadores_emprego(B: np.ndarray, ocup: np.ndarray, x: np.ndarray,
                            mask_L: np.ndarray) -> pd.DataFrame:
    """E_j = sum_i w_i b_ij, com w_i = ocup_i / x_i. Decompõe retido/vazado."""
    x_safe = np.where(x == 0, 1.0, x)
    w = ocup / x_safe
    E = (w[:, np.newaxis] * B).sum(axis=0)
    E_L = (w[mask_L, np.newaxis] * B[mask_L, :]).sum(axis=0)
    E_M = (w[~mask_L, np.newaxis] * B[~mask_L, :]).sum(axis=0)
    vaz = np.divide(E_M, E, out=np.zeros_like(E), where=E != 0)
    return pd.DataFrame({"E": E, "E_L": E_L, "E_M": E_M, "vazamento_emprego": vaz})


# --------------------------------------------------------------------------- #
# Experimento spillover / feedback
# --------------------------------------------------------------------------- #
def spillover_feedback(B: np.ndarray, y_L: np.ndarray, mask_L: np.ndarray) -> dict:
    """
    Injeta-se a demanda final própria do ES (y^L), com y^M = 0.
      x = B y
      injecao  = soma de y^L
      spillover = produção total puxada em M
      feedback  = produção em L que decorre do retorno via M
                  (aprox.: x_L - (I - A^LL)^{-1} y^L), reportada como fração.
    Aqui usamos a leitura agregada por blocos a partir de x = B y.
    """
    y = np.zeros(B.shape[0])
    y[mask_L] = y_L
    x = B @ y
    injecao = y_L.sum()
    spillover = x[~mask_L].sum()
    x_L_total = x[mask_L].sum()
    # produção em L sem rota inter-regional (somente bloco intra-L de B):
    B_LL = B[np.ix_(mask_L, mask_L)]
    x_L_intra = (B_LL @ y_L).sum()
    feedback = max(x_L_total - x_L_intra, 0.0)
    return {
        "injecao": injecao,
        "spillover_M": spillover,
        "feedback_L": feedback,
        "feedback_rel": feedback / injecao if injecao else 0.0,
    }


# --------------------------------------------------------------------------- #
# Ligações de Rasmussen-Hirschman
# --------------------------------------------------------------------------- #
def rasmussen_hirschman(B: np.ndarray) -> pd.DataFrame:
    """Backward = média de coluna; forward = média de linha; ambas normalizadas."""
    n = B.shape[0]
    media_geral = B.mean()
    backward = B.mean(axis=0) / media_geral
    forward = B.mean(axis=1) / media_geral
    return pd.DataFrame({"backward": backward, "forward": forward})


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="Pipeline inter-regional ES x Brasil (Isard).")
    ap.add_argument("--mip", required=True, help="CSV da MIP inter-regional (ver dados/README.md)")
    args = ap.parse_args()

    print(f"[io_core] carregando {args.mip} ...")
    print("NOTA: ajuste o parser abaixo ao layout exato do seu CSV.")
    # df = pd.read_csv(args.mip, index_col=0)
    # Z = df.iloc[:52, :52].to_numpy(float)
    # x = df["x"].to_numpy(float); ocup = df["ocup"].to_numpy(float)
    # mask_L = np.array([c.endswith("_L") for c in df.index[:52]])
    # A = coef_tecnicos(Z, x); B = leontief_inversa(A)
    # print(multiplicadores_producao(B, mask_L).describe())
    # print(spillover_feedback(B, y_L=<vetor de demanda final do ES>, mask_L=mask_L))


if __name__ == "__main__":
    main()
