"""
io_core.py — implementação de referência do arcabouço inter-regional (Isard)
para "O Espírito Santo como economia-plataforma".

Espelha o pipeline canônico `pesquisa/01_es_br_base.py` (convenção Miller-Blair V3):
mesmas fórmulas de multiplicador, spillover/feedback (inversa particionada) e
ligações de Rasmussen-Hirschman (para frente pela inversa de Ghosh). Em caso de
divergência, `01_es_br_base.py` sobre o dado real é a referência.
Regiões: L = ES, M = restante do Brasil.

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
def spillover_feedback(A: np.ndarray, mask_L: np.ndarray, y_L: np.ndarray) -> dict:
    """
    Decomposição spillover/feedback de Isard–Miller-Blair (convenção V3), idêntica a
    `pesquisa/01_es_br_base.py`. Injeta-se a demanda final do ES por produtos do ES
    (y^L, com y^M = 0) e medem-se:
      x^L_closed = (I − A^LL)^{-1} y^L                              (economia do ES "fechada")
      x^L_full   = [I − A^LL − A^LM (I − A^MM)^{-1} A^ML]^{-1} y^L  (com o loop de feedback;
                   inversa particionada — Miller & Blair, 2009, cap. 3)
      spillover  = soma de (I − A^MM)^{-1} A^ML x^L_full            (produção induzida no RB)
      feedback   = soma(x^L_full) − soma(x^L_closed)               (retorno ao ES via M)

    NOTA: o feedback NÃO pode ser lido de x = B y restrito a L — como y^M = 0,
    (B y)[L] ≡ B_LL y_L já contém o loop, anulando a diferença. É preciso a inversa
    particionada acima (este é o bug que a versão antiga deste módulo continha).
    """
    L = np.where(mask_L)[0]
    M = np.where(~mask_L)[0]
    A_LL = A[np.ix_(L, L)]; A_LM = A[np.ix_(L, M)]
    A_ML = A[np.ix_(M, L)]; A_MM = A[np.ix_(M, M)]
    inv_MM   = np.linalg.inv(np.eye(M.size) - A_MM)
    inv_LL   = np.linalg.inv(np.eye(L.size) - A_LL)                          # ES fechado
    inv_feed = np.linalg.inv(np.eye(L.size) - A_LL - A_LM @ inv_MM @ A_ML)   # com feedback
    xL_closed = inv_LL @ y_L
    xL_full   = inv_feed @ y_L
    xM_spill  = inv_MM @ A_ML @ xL_full
    injecao   = float(y_L.sum())
    spillover = float(xM_spill.sum())
    feedback  = float(xL_full.sum() - xL_closed.sum())
    return {
        "injecao": injecao,
        "spillover_M": spillover,
        "feedback_L": feedback,
        "feedback_rel": feedback / injecao if injecao else 0.0,
        "spillover_rel": spillover / injecao if injecao else 0.0,
    }


# --------------------------------------------------------------------------- #
# Ligações de Rasmussen-Hirschman
# --------------------------------------------------------------------------- #
def ghosh_inversa(Z: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Inversa de Ghosh G = (I − Â)^{-1}, com Â = x̂^{-1} Z (coef. de alocação, normalizados por linha)."""
    x_safe = np.where(x == 0, 1.0, x)
    Ahat = Z / x_safe[:, np.newaxis]
    n = Z.shape[0]
    return np.linalg.inv(np.eye(n) - Ahat)


def rasmussen_hirschman(B: np.ndarray, G: np.ndarray) -> pd.DataFrame:
    """
    Índices de ligação de Rasmussen–Hirschman (normalizados pela média geral):
      para trás  (backward) pela inversa de Leontief B  — lado da demanda;
      para frente (forward)  pela inversa de Ghosh G     — lado da oferta.
    Miller & Blair (2009): a ligação para frente usa a inversa de Ghosh, não a soma
    de linha da inversa de Leontief (corrige o viés da versão antiga deste módulo).
    Idêntico a `pesquisa/01_es_br_base.py`.
    """
    n = B.shape[0]
    backward = B.sum(axis=0) / n / B.mean()
    forward  = G.sum(axis=1) / n / G.mean()
    return pd.DataFrame({"backward": backward, "forward": forward})


def carrega_mip(path: str):
    """Le um CSV no layout dados/mip_es_br_*.csv: coluna 'setor' (codigo+sufixo _L/_M)
    como indice, colunas de mesmo nome formando a matriz Z empilhada quadrada,
    mais colunas auxiliares 'x' e 'ocup'. Dimensao e generica (qualquer n por regiao)."""
    df = pd.read_csv(path, index_col=0)
    codigos = df.index.tolist()
    Z = df[codigos].to_numpy(float)
    x = df["x"].to_numpy(float)
    ocup = df["ocup"].to_numpy(float)
    mask_L = np.array([str(c).endswith("_L") for c in codigos])
    return codigos, Z, x, ocup, mask_L


def main():
    ap = argparse.ArgumentParser(description="Pipeline inter-regional ES x Brasil (Isard).")
    ap.add_argument("--mip", required=True, help="CSV da MIP inter-regional (ver dados/README.md)")
    args = ap.parse_args()

    print(f"[io_core] carregando {args.mip} ...")
    codigos, Z, x, ocup, mask_L = carrega_mip(args.mip)
    print(f"[io_core] {len(codigos)} setores ({mask_L.sum()} ES / {(~mask_L).sum()} resto do Brasil)")

    A = coef_tecnicos(Z, x)
    B = leontief_inversa(A)
    G = ghosh_inversa(Z, x)
    print(f"[io_core] soma de A por coluna: min={A.sum(0).min():.3f} max={A.sum(0).max():.3f} (deve ser <1)")
    print(f"[io_core] B>=0? {bool((B >= -1e-9).all())}")

    print("\n[multiplicadores de producao — retido (ES) vs vazado (resto do Brasil)]")
    mp = multiplicadores_producao(B, mask_L)
    print(mp[mask_L].describe())

    print("\n[multiplicadores de emprego — vazamento]")
    me = multiplicadores_emprego(B, ocup, x, mask_L)
    print(me[mask_L].describe())

    print("\n[ligacoes de Rasmussen-Hirschman — para frente pela inversa de Ghosh]")
    rh = rasmussen_hirschman(B, G)
    print(rh[mask_L].describe())


if __name__ == "__main__":
    main()
