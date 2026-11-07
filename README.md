<div align="center">

# 🐗 JavaliMS — Mapeamento da Ocorrência de Javali no Mato Grosso do Sul

### Análise geoespacial da presença do javali (*Sus scrofa*) nos municípios do MS a partir de dados oficiais

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![GeoPandas](https://img.shields.io/badge/GeoPandas-mapas-139C5A?style=for-the-badge)](https://geopandas.org)
[![Folium](https://img.shields.io/badge/Folium-mapa_interativo-77B829?style=for-the-badge)](https://python-visualization.github.io/folium/)

<br>

**Laboratório Inovisão — Universidade Católica Dom Bosco (UCDB)**

*Campo Grande, MS — Brasil*

</div>

---

## 📋 Sobre o Projeto

O **JavaliMS** mapeia a ocorrência do javali (*Sus scrofa*) nos municípios de Mato Grosso do Sul com base em dados oficiais, para apoiar o enfrentamento de um dos maiores problemas do agronegócio sul-mato-grossense: a invasão da espécie em lavouras de soja, milho e cana-de-açúcar.

O javali é considerado uma das **100 piores espécies exóticas invasoras do mundo** (IUCN). No Mato Grosso do Sul, a espécie se expandiu de **7 municípios em 2005 para 71 em 2018** (IBAMA/SIMAF), causando prejuízos milionários. Somente em Rio Brilhante, as perdas em milho chegaram a **R$ 1,5 milhão em uma única safra** (FAMASUL, 2014).

O projeto reúne 42 municípios com ocorrência registrada, classifica cada um em 5 níveis de severidade e gera mapas estáticos, um mapa de densidade (KDE) e um mapa interativo.

---

## 📁 Estrutura

```
sus-scrofa-ms/
├── javali_mapa_calor_ms.py       # Mapa de calor, mapa KDE, gráfico de barras e CSV
├── Untitled-1.ipynb              # Mapa interativo com Folium
├── requirements_javali.txt       # Dependências
└── saida_javali/                 # Resultados gerados
    ├── mapa_calor_javali_ms.png
    ├── mapa_kde_javali_ms.png
    ├── grafico_municipios_javali_ms.png
    ├── mapa_interativo_javali_ms.html
    └── municipios_javali_ms.csv
```

---

## 📊 Dados Confirmados

| Indicador | Valor | Fonte |
|-----------|-------|-------|
| Municípios com ocorrência em MS | 71 | IBAMA/SIMAF, 2019 |
| Javalis abatidos em MS (2013–2020) | 12.603–17.248 | IBAMA / Correio do Estado |
| Municípios prioridade extremamente alta | 4 (Rio Brilhante, Douradina, Fátima do Sul, Laguna Carapã) | Plano Javali IBAMA |
| Perda em milho (safrinha) | 10–30% | Embrapa / FAMASUL |
| Prejuízo em Rio Brilhante | R$ 1,5M (uma safra) | Sindicato Rural / FAMASUL, 2014 |
| Expansão territorial | 7 → 46 → 71 municípios (2005–2018) | Fundect/Embrapa / IBAMA |

---

## 🗺️ Visualizações Geradas

- **Mapa de calor** (`mapa_calor_javali_ms.png`): GeoPandas + Matplotlib sobre a malha municipal do IBGE (via `geobr`), com 5 níveis de severidade.
- **Mapa KDE** (`mapa_kde_javali_ms.png`): Kernel Density Estimation com SciPy, mostrando a densidade contínua de ocorrência.
- **Gráfico por município** (`grafico_municipios_javali_ms.png`): municípios ordenados por nível de ocorrência.
- **Mapa interativo** (`mapa_interativo_javali_ms.html`): Folium com marcadores clicáveis por severidade, pop-ups com as informações de cada município, heatmap sobreposto e camadas que podem ser ligadas e desligadas.
- **Tabela** (`municipios_javali_ms.csv`): município, latitude, longitude, nível de ocorrência e observação.

---

## ▶️ Como Rodar

```bash
# Criar ambiente
conda create -n javali python=3.11 -y
conda activate javali

# Instalar dependências
pip install -r requirements_javali.txt
pip install folium

# Gerar mapa de calor, mapa KDE, gráfico e CSV
python javali_mapa_calor_ms.py

# Gerar o mapa interativo: abra e execute o notebook
jupyter notebook Untitled-1.ipynb
```

Os arquivos são salvos em `saida_javali/`. Para ver o mapa interativo sem rodar nada, abra `saida_javali/mapa_interativo_javali_ms.html` no navegador.

---

## 🔗 Projeto Relacionado

A detecção automática de javali em imagens com visão computacional é desenvolvida em um repositório separado:

**[Javali Detech — YOLOv8s](https://github.com/guedesgeorge/javali-detech-yolov8s)**

---

## 📚 Fontes e Referências

Todos os dados utilizados são verificados e rastreáveis:

- **IBAMA/SIMAF**: Sistema de Informação de Manejo de Fauna. Relatório de Gestão do Manejo de Javalis 2013–2016
- **IBAMA**: Plano Nacional de Prevenção, Controle e Monitoramento do Javali (*Sus scrofa*). Portaria Interministerial nº 232/2017
- **Embrapa Agropecuária Oeste**: Levantamento de perdas em milho safrinha 2013 (Showtec 2014)
- **Embrapa Pantanal**: Circular Técnica 124/2022
- **FAMASUL / Sindicato Rural de Rio Brilhante**: Dados de prejuízo em lavouras, safrinha 2013/2014
- **UFMS**: Mapeamento de Javalis em MS (Wagner Fischer, 2019)
- **Fundect / Embrapa Pantanal**: Pesquisador Fernando Ibanez Martins, expansão territorial 2005–2015
- **USP/ESALQ-LOG**: Prof. Paulo Bezerra, estimativa de subnotificação (Brasil 61, dez/2025)

---

## 👨‍🔬 Equipe

| Nome | Função | Contato |
|------|--------|---------|
| **George Emannuel Guedes de Carvalho** | Pesquisador principal | ra196379@ucdb.br |
| **Prof. Alan Rios Bezerra** | Orientador | UCDB |

**Laboratório Inovisão**, Escola de Computação, Universidade Católica Dom Bosco (UCDB)

Campo Grande — MS, Brasil

---

<div align="center">

**🐗 JavaliMS** — Projeto de Pesquisa

Laboratório Inovisão · UCDB · Campo Grande, MS

*Desenvolvido com dados do IBAMA, Embrapa, UFMS e FAMASUL*

</div>
