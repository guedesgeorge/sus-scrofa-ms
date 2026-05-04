"""
===========================================================================
MAPA DE CALOR — Ocorrência de Javali (Sus scrofa) no Mato Grosso do Sul
===========================================================================

Projeto de pesquisa: Espantamento e registro de ataques de javali
em lavouras do estado do MS.

COMO RODAR:
-----------
1. Crie um ambiente Conda:
   conda create -n javali python=3.11 -y
   conda activate javali

2. Instale as dependências:
   pip install geopandas matplotlib mapclassify pandas shapely geobr

3. Execute no VS Code ou terminal:
   python javali_mapa_calor_ms.py

Fontes dos dados:
- IBAMA / SIMAF (Sistema de Informação de Manejo de Fauna)
- Embrapa Pantanal (Circular Técnica 124, 2022)
- UFMS — Mapeamento de Javalis em MS (Wagner Fischer, 2019)
- FAMASUL — Relatórios de danos em lavouras
- Plano Nacional de Prevenção, Controle e Monitoramento do Javali
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from shapely.geometry import Point
import numpy as np
import os
import sys

# ============================================================
# CONFIGURAÇÕES
# ============================================================
SALVAR_PNG = True          # Salvar figuras como PNG
SALVAR_CSV = True          # Salvar tabela CSV com os dados
MOSTRAR_GRAFICOS = True    # Exibir gráficos na tela (plt.show)
USAR_GEOBR = True         # Tentar baixar malha municipal via geobr
DPI_SAIDA = 200            # Resolução das imagens salvas
PASTA_SAIDA = "saida_javali"

# ============================================================
# DADOS: Municípios do MS com ocorrência de javali
# ============================================================
# Níveis de severidade:
#   5 = Prioridade extremamente alta (Plano Javali IBAMA)
#   4 = Prioridade alta / muitos relatos e abates
#   3 = Ocorrência frequente confirmada
#   2 = Ocorrência confirmada
#   1 = Relatos esporádicos

MUNICIPIOS_JAVALI = [
    # ---- PRIORIDADE EXTREMAMENTE ALTA (nível 5) ----
    {"municipio": "Rio Brilhante",      "lat": -21.8025, "lon": -54.5461, "nivel": 5,
     "obs": "Epicentro - maior nº de ataques, >1000 animais, R$1.5M prejuízo milho"},
    {"municipio": "Douradina",          "lat": -22.0411, "lon": -54.6156, "nivel": 5,
     "obs": "Prioridade extremamente alta IBAMA"},
    {"municipio": "Fátima do Sul",      "lat": -22.3789, "lon": -54.5131, "nivel": 5,
     "obs": "Prioridade extremamente alta IBAMA"},
    {"municipio": "Laguna Carapã",      "lat": -22.5444, "lon": -55.1483, "nivel": 5,
     "obs": "Prioridade extremamente alta IBAMA, múltiplos aspectos"},

    # ---- PRIORIDADE ALTA (nível 4) ----
    {"municipio": "Dourados",           "lat": -22.2211, "lon": -54.8056, "nivel": 4,
     "obs": "Maior nº de abates registrados no SIMAF"},
    {"municipio": "Maracaju",           "lat": -21.6142, "lon": -55.1681, "nivel": 4,
     "obs": "Grande área agrícola afetada"},
    {"municipio": "Nova Alvorada do Sul","lat": -21.4658, "lon": -54.3828, "nivel": 4,
     "obs": "Ocorrência frequente confirmada"},
    {"municipio": "Itaporã",            "lat": -22.0797, "lon": -54.7886, "nivel": 4,
     "obs": "Região agrícola fortemente afetada"},
    {"municipio": "Caarapó",            "lat": -22.6364, "lon": -54.8206, "nivel": 4,
     "obs": "Ocorrência frequente"},
    {"municipio": "Ponta Porã",         "lat": -22.5358, "lon": -55.7256, "nivel": 4,
     "obs": "Fronteira - rota original de entrada dos javalis"},

    # ---- OCORRÊNCIA FREQUENTE (nível 3) ----
    {"municipio": "Bela Vista",         "lat": -22.1069, "lon": -56.5214, "nivel": 3,
     "obs": "Região Sul - cruzamento javaporcos"},
    {"municipio": "Aral Moreira",       "lat": -22.9367, "lon": -55.6383, "nivel": 3,
     "obs": "Fronteira com Paraguai"},
    {"municipio": "Amambai",            "lat": -23.1050, "lon": -55.2256, "nivel": 3,
     "obs": "Ocorrência confirmada"},
    {"municipio": "Antônio João",       "lat": -22.1914, "lon": -55.9531, "nivel": 3,
     "obs": "Fronteira - rota de entrada"},
    {"municipio": "Naviraí",            "lat": -23.0631, "lon": -54.1908, "nivel": 3,
     "obs": "Ocorrência confirmada"},
    {"municipio": "Ivinhema",           "lat": -22.3089, "lon": -53.8167, "nivel": 3,
     "obs": "Ocorrência confirmada"},
    {"municipio": "Bonito",             "lat": -21.1267, "lon": -56.4836, "nivel": 3,
     "obs": "Área turística afetada"},
    {"municipio": "Coronel Sapucaia",   "lat": -23.2722, "lon": -55.5264, "nivel": 3,
     "obs": "Fronteira"},
    {"municipio": "Jardim",             "lat": -21.4797, "lon": -56.1383, "nivel": 3,
     "obs": "Ocorrência confirmada"},
    {"municipio": "Porto Murtinho",     "lat": -21.6989, "lon": -57.8828, "nivel": 3,
     "obs": "Prioridade alta - aspecto ambiental"},
    {"municipio": "Rochedo",            "lat": -19.9519, "lon": -54.8906, "nivel": 3,
     "obs": "Prioridade alta - aspecto ambiental"},
    {"municipio": "Sidrolândia",        "lat": -20.9306, "lon": -54.9611, "nivel": 3,
     "obs": "Grande área agrícola"},

    # ---- OCORRÊNCIA CONFIRMADA (nível 2) ----
    {"municipio": "Angélica",           "lat": -22.1531, "lon": -53.7711, "nivel": 2,
     "obs": "Ocorrência confirmada"},
    {"municipio": "Anaurilândia",       "lat": -22.1856, "lon": -52.7189, "nivel": 2,
     "obs": "Ocorrência confirmada"},
    {"municipio": "Aquidauana",         "lat": -20.4714, "lon": -55.7867, "nivel": 2,
     "obs": "Ocorrência confirmada"},
    {"municipio": "Bataiporã",          "lat": -22.2944, "lon": -53.2706, "nivel": 2,
     "obs": "Ocorrência confirmada"},
    {"municipio": "Bodoquena",          "lat": -20.5381, "lon": -56.7147, "nivel": 2,
     "obs": "Ocorrência confirmada"},
    {"municipio": "Caracol",            "lat": -22.0111, "lon": -57.0272, "nivel": 2,
     "obs": "Ocorrência confirmada"},
    {"municipio": "Corumbá",            "lat": -19.0092, "lon": -57.6514, "nivel": 2,
     "obs": "Pantanal - porco monteiro"},
    {"municipio": "Coxim",              "lat": -18.5069, "lon": -54.7600, "nivel": 2,
     "obs": "Ocorrência confirmada"},
    {"municipio": "Deodápolis",         "lat": -22.2767, "lon": -54.1681, "nivel": 2,
     "obs": "Ocorrência confirmada"},
    {"municipio": "Glória de Dourados", "lat": -22.4133, "lon": -54.2328, "nivel": 2,
     "obs": "Ocorrência confirmada"},
    {"municipio": "Guia Lopes da Laguna","lat": -21.4583, "lon": -56.1117, "nivel": 2,
     "obs": "Ocorrência confirmada"},
    {"municipio": "Itaquiraí",          "lat": -23.4767, "lon": -54.1875, "nivel": 2,
     "obs": "Ocorrência confirmada"},
    {"municipio": "Jateí",              "lat": -22.4803, "lon": -54.3078, "nivel": 2,
     "obs": "Ocorrência confirmada"},
    {"municipio": "Juti",               "lat": -22.8600, "lon": -54.6064, "nivel": 2,
     "obs": "Ocorrência confirmada"},
    {"municipio": "Miranda",            "lat": -20.2406, "lon": -56.3778, "nivel": 2,
     "obs": "Ocorrência confirmada"},
    {"municipio": "Nova Andradina",     "lat": -22.2328, "lon": -53.3433, "nivel": 2,
     "obs": "Ocorrência confirmada"},

    # ---- RELATOS ESPORÁDICOS (nível 1) ----
    {"municipio": "Campo Grande",       "lat": -20.4697, "lon": -54.6201, "nivel": 1,
     "obs": "Relatos periurbanos"},
    {"municipio": "Três Lagoas",        "lat": -20.7511, "lon": -51.6783, "nivel": 1,
     "obs": "Relatos esporádicos"},
    {"municipio": "Mundo Novo",         "lat": -23.9356, "lon": -54.2808, "nivel": 1,
     "obs": "Relatos esporádicos"},
    {"municipio": "Eldorado",           "lat": -23.7867, "lon": -54.2836, "nivel": 1,
     "obs": "Relatos esporádicos"},
]

# ============================================================
# PALETA DE CORES E LABELS
# ============================================================
CORES = {
    5: "#d7191c",   # vermelho escuro
    4: "#fdae61",   # laranja
    3: "#fee08b",   # amarelo
    2: "#abdda4",   # verde claro
    1: "#2b83ba",   # azul
}

LABELS = {
    5: "Extremamente Alta",
    4: "Alta",
    3: "Frequente",
    2: "Confirmada",
    1: "Esporádica",
}


def criar_pasta_saida():
    """Cria pasta de saída se não existir."""
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    print(f"📁 Pasta de saída: {os.path.abspath(PASTA_SAIDA)}")


def carregar_dados():
    """Converte os dados em DataFrame e GeoDataFrame."""
    df = pd.DataFrame(MUNICIPIOS_JAVALI)
    geometry = [Point(row["lon"], row["lat"]) for _, row in df.iterrows()]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    print(f"✅ {len(gdf)} municípios carregados")
    return df, gdf


def carregar_malha_ms():
    """
    Tenta baixar a malha municipal do MS via geobr.
    Se falhar, retorna None (o mapa funcionará sem contorno).
    """
    if not USAR_GEOBR:
        return None

    try:
        import geobr
        print("⏳ Baixando malha municipal do MS via geobr...")
        ms = geobr.read_municipality(code_muni=50, year=2020)
        print(f"✅ Malha municipal carregada: {len(ms)} municípios")
        return ms
    except Exception as e:
        print(f"⚠️  Não foi possível baixar a malha via geobr: {e}")
        print("   O mapa será gerado sem os contornos municipais.")
        print("   Para instalar: pip install geobr")
        return None


def imprimir_resumo(df):
    """Imprime resumo no terminal."""
    print("\n" + "=" * 65)
    print("  RESUMO — Ocorrência de Javali (Sus scrofa) em MS")
    print("=" * 65)

    for nivel in [5, 4, 3, 2, 1]:
        subset = df[df["nivel"] == nivel]
        muns = ", ".join(subset["municipio"].tolist())
        print(f"\n  🔴 {LABELS[nivel]} (nível {nivel}) — {len(subset)} municípios:")
        print(f"     {muns}")

    print(f"\n  📊 Total: {len(df)} municípios mapeados")
    print("=" * 65)


def gerar_mapa_calor(gdf, malha_ms=None):
    """
    Gera o mapa de calor com zonas de buffer coloridas
    por nível de severidade.
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 16))
    fig.patch.set_facecolor("#f5f5f0")
    ax.set_facecolor("#eae8e0")

    # --- Contorno do estado (se disponível) ---
    if malha_ms is not None:
        malha_ms.plot(
            ax=ax,
            facecolor="#f0ede5",
            edgecolor="#cccccc",
            linewidth=0.4,
            zorder=1
        )

    # --- Projeção métrica para buffers ---
    gdf_proj = gdf.to_crs("EPSG:31982")  # UTM zona 22S

    # --- Zonas de calor (buffers) ---
    for nivel in [1, 2, 3, 4, 5]:
        subset = gdf_proj[gdf_proj["nivel"] == nivel]
        if len(subset) == 0:
            continue
        buffer_km = 15 + (nivel * 8)  # raio em km
        buffered = subset.copy()
        buffered["geometry"] = buffered.geometry.buffer(buffer_km * 1000)
        buffered_wgs = buffered.to_crs("EPSG:4326")
        buffered_wgs.plot(
            ax=ax,
            color=CORES[nivel],
            alpha=0.30,
            edgecolor="none",
            zorder=2
        )

    # --- Pontos ---
    for nivel in [1, 2, 3, 4, 5]:
        subset = gdf[gdf["nivel"] == nivel]
        subset.plot(
            ax=ax,
            color=CORES[nivel],
            markersize=50 + (nivel * 40),
            edgecolor="black",
            linewidth=0.5,
            alpha=0.9,
            label=f"{LABELS[nivel]} ({len(subset)} mun.)",
            zorder=5
        )

    # --- Rótulos dos municípios com nível >= 3 ---
    for _, row in gdf.iterrows():
        if row["nivel"] >= 3:
            fontsize = 6 + row["nivel"]
            fontweight = "bold" if row["nivel"] >= 4 else "normal"
            ax.annotate(
                row["municipio"],
                xy=(row["lon"], row["lat"]),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=fontsize,
                fontweight=fontweight,
                color="#333333",
                bbox=dict(
                    boxstyle="round,pad=0.2",
                    facecolor="white",
                    alpha=0.75,
                    edgecolor="#999999"
                ),
                zorder=10
            )

    # --- Limites do mapa (MS) ---
    ax.set_xlim(-58.2, -51.2)
    ax.set_ylim(-24.3, -17.8)

    # --- Estilo ---
    ax.grid(True, linestyle="--", alpha=0.25, color="#999999")
    ax.set_xlabel("Longitude", fontsize=12)
    ax.set_ylabel("Latitude", fontsize=12)
    ax.set_title(
        "Mapa de Calor — Ocorrência de Javali (Sus scrofa)\n"
        "Mato Grosso do Sul",
        fontsize=16, fontweight="bold", pad=20
    )

    # --- Legenda ---
    ax.legend(
        title="Nível de Ocorrência",
        loc="upper left",
        fontsize=10,
        title_fontsize=12,
        framealpha=0.9,
        edgecolor="gray"
    )

    # --- Nota de fonte ---
    ax.text(
        0.5, -0.04,
        "Fontes: IBAMA/SIMAF · Embrapa Pantanal · UFMS · FAMASUL · Reportagens regionais\n"
        "Projeto de Pesquisa — Monitoramento de Javali em Lavouras do MS",
        transform=ax.transAxes,
        fontsize=8, ha="center", style="italic", color="gray"
    )

    plt.tight_layout()

    if SALVAR_PNG:
        caminho = os.path.join(PASTA_SAIDA, "mapa_calor_javali_ms.png")
        plt.savefig(caminho, dpi=DPI_SAIDA, bbox_inches="tight")
        print(f"💾 Mapa salvo: {caminho}")

    return fig


def gerar_grafico_barras(df):
    """Gera gráfico de barras horizontal por nível de severidade."""
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor("#f5f5f0")
    ax.set_facecolor("#fafaf5")

    df_sorted = df.sort_values("nivel", ascending=True)
    bar_colors = [CORES[n] for n in df_sorted["nivel"]]

    bars = ax.barh(
        df_sorted["municipio"],
        df_sorted["nivel"],
        color=bar_colors,
        edgecolor="#666666",
        linewidth=0.4
    )

    ax.set_xlabel("Nível de Ocorrência", fontsize=12)
    ax.set_xlim(0, 6)
    ax.set_title(
        "Municípios do MS com Ocorrência de Javali\n"
        "(Classificados por Nível de Severidade)",
        fontsize=14, fontweight="bold"
    )

    for bar, nivel in zip(bars, df_sorted["nivel"]):
        ax.text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            LABELS[nivel],
            va="center", fontsize=7, color="#555555"
        )

    plt.tight_layout()

    if SALVAR_PNG:
        caminho = os.path.join(PASTA_SAIDA, "grafico_municipios_javali_ms.png")
        plt.savefig(caminho, dpi=DPI_SAIDA, bbox_inches="tight")
        print(f"💾 Gráfico salvo: {caminho}")

    return fig


def gerar_mapa_concentracao(gdf, malha_ms=None):
    """
    Gera mapa de concentração com interpolação tipo KDE
    (Kernel Density Estimation) para efeito visual de calor contínuo.
    """
    from scipy.ndimage import gaussian_filter

    fig, ax = plt.subplots(1, 1, figsize=(14, 16))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")

    # Contorno do estado
    if malha_ms is not None:
        malha_ms.plot(
            ax=ax,
            facecolor="#1a1a3e",
            edgecolor="#334466",
            linewidth=0.3,
            zorder=1
        )

    # Criar grid para KDE
    x_min, x_max = -58.2, -51.2
    y_min, y_max = -24.3, -17.8
    grid_res = 500

    x_grid = np.linspace(x_min, x_max, grid_res)
    y_grid = np.linspace(y_min, y_max, grid_res)
    X, Y = np.meshgrid(x_grid, y_grid)
    Z = np.zeros_like(X)

    # Acumular "calor" por ponto (ponderado pelo nível)
    for _, row in gdf.iterrows():
        dist = np.sqrt((X - row["lon"])**2 + (Y - row["lat"])**2)
        sigma = 0.3 + (row["nivel"] * 0.15)
        Z += row["nivel"] * np.exp(-dist**2 / (2 * sigma**2))

    # Suavizar
    Z = gaussian_filter(Z, sigma=8)

    # Plotar como imshow
    from matplotlib.colors import LinearSegmentedColormap
    cmap_custom = LinearSegmentedColormap.from_list(
        "javali_heat",
        ["#16213e", "#1b4332", "#2d6a4f", "#95d5b2",
         "#fee08b", "#fdae61", "#f46d43", "#d73027", "#a50026"],
        N=256
    )

    im = ax.imshow(
        Z,
        extent=[x_min, x_max, y_min, y_max],
        origin="lower",
        cmap=cmap_custom,
        alpha=0.85,
        aspect="auto",
        zorder=2
    )

    # Pontos
    for _, row in gdf.iterrows():
        ax.plot(
            row["lon"], row["lat"],
            "o",
            color="white",
            markersize=3 + row["nivel"],
            markeredgecolor="white",
            markeredgewidth=0.3,
            alpha=0.8,
            zorder=5
        )
        if row["nivel"] >= 4:
            ax.annotate(
                row["municipio"],
                xy=(row["lon"], row["lat"]),
                xytext=(6, 6),
                textcoords="offset points",
                fontsize=8,
                fontweight="bold",
                color="white",
                bbox=dict(
                    boxstyle="round,pad=0.2",
                    facecolor="#00000066",
                    edgecolor="none"
                ),
                zorder=10
            )

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("Longitude", fontsize=11, color="#cccccc")
    ax.set_ylabel("Latitude", fontsize=11, color="#cccccc")
    ax.tick_params(colors="#999999")
    ax.set_title(
        "Densidade de Ocorrência de Javali — Mato Grosso do Sul\n"
        "(Kernel Density Estimation - KDE)",
        fontsize=15, fontweight="bold", color="white", pad=20
    )

    cbar = plt.colorbar(im, ax=ax, shrink=0.6, pad=0.02)
    cbar.set_label("Intensidade de ocorrência", fontsize=10, color="#cccccc")
    cbar.ax.tick_params(colors="#999999")

    ax.text(
        0.5, -0.04,
        "Fontes: IBAMA/SIMAF · Embrapa Pantanal · UFMS · FAMASUL\n"
        "Projeto de Pesquisa — Monitoramento de Javali em Lavouras do MS",
        transform=ax.transAxes,
        fontsize=8, ha="center", style="italic", color="#888888"
    )

    plt.tight_layout()

    if SALVAR_PNG:
        caminho = os.path.join(PASTA_SAIDA, "mapa_kde_javali_ms.png")
        plt.savefig(caminho, dpi=DPI_SAIDA, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
        print(f"💾 Mapa KDE salvo: {caminho}")

    return fig


def salvar_csv(df):
    """Salva tabela CSV ordenada por severidade."""
    df_export = df.sort_values("nivel", ascending=False)
    df_export = df_export.rename(columns={
        "municipio": "Município",
        "lat": "Latitude",
        "lon": "Longitude",
        "nivel": "Nível de Ocorrência",
        "obs": "Observação"
    })
    caminho = os.path.join(PASTA_SAIDA, "municipios_javali_ms.csv")
    df_export.to_csv(caminho, index=False, encoding="utf-8-sig")
    print(f"💾 CSV salvo: {caminho}")


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================
def main():
    print("\n🐗 ANÁLISE DE OCORRÊNCIA DE JAVALI — MATO GROSSO DO SUL")
    print("=" * 60)

    criar_pasta_saida()
    df, gdf = carregar_dados()
    malha_ms = carregar_malha_ms()
    imprimir_resumo(df)

    print("\n⏳ Gerando visualizações...")

    # Mapa de calor com buffers
    gerar_mapa_calor(gdf, malha_ms)

    # Gráfico de barras
    gerar_grafico_barras(df)

    # Mapa KDE (densidade contínua)
    try:
        gerar_mapa_concentracao(gdf, malha_ms)
    except ImportError:
        print("⚠️  scipy não instalado — pulando mapa KDE")
        print("   Para instalar: pip install scipy")

    # CSV
    if SALVAR_CSV:
        salvar_csv(df)

    print(f"\n✅ Tudo pronto! Arquivos em: {os.path.abspath(PASTA_SAIDA)}/")

    if MOSTRAR_GRAFICOS:
        print("\n📊 Exibindo gráficos... (feche as janelas para encerrar)")
        plt.show()


if __name__ == "__main__":
    main()
