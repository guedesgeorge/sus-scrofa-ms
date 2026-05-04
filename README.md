<div align="center">

# 🐗 JavaliMS — Monitoramento Inteligente de Javali em Lavouras

### Sistema de IA para detecção, mapeamento e espantamento do javali (*Sus scrofa*) em lavouras do Mato Grosso do Sul

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![YOLO](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF?style=for-the-badge&logo=yolo&logoColor=white)](https://ultralytics.com)
[![License](https://img.shields.io/badge/Licença-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow?style=for-the-badge)]()

<br>

**Laboratório Inovisão — Universidade Católica Dom Bosco (UCDB)**

*Campo Grande, MS — Brasil*

</div>

---

## 📋 Sobre o Projeto

O **JavaliMS** é um projeto de pesquisa que combina **Inteligência Artificial**, **Visão Computacional** e **Análise Geoespacial** para enfrentar um dos maiores problemas do agronegócio sul-mato-grossense: a invasão do javali (*Sus scrofa*) em lavouras de soja, milho e cana-de-açúcar.

O javali é considerado uma das **100 piores espécies exóticas invasoras do mundo** (IUCN). No Mato Grosso do Sul, a espécie se expandiu de **7 municípios em 2005 para 71 em 2018** (IBAMA/SIMAF), causando prejuízos milionários — somente em Rio Brilhante, as perdas em milho chegaram a **R$ 1,5 milhão em uma única safra** (FAMASUL, 2014).

**Não existe atualmente no Brasil um sistema integrado de monitoramento de danos por javali com georreferenciamento e visão computacional.** Este projeto busca preencher essa lacuna.

---

## 🎯 Objetivos

- **Detectar** automaticamente o javali em imagens e vídeos de câmeras de campo utilizando modelos YOLO
- **Identificar e quantificar** danos causados em lavouras a partir de imagens aéreas e terrestres
- **Mapear** as áreas de maior ocorrência e intensidade de ataques no MS via análise geoespacial (KDE)
- **Registrar** ataques em campo com dados georreferenciados (GPS, horário, fotos, tipo de lavoura)
- **Acionar** sistemas autônomos de espantamento (sonoros/luminosos) baseados na detecção em tempo real

---

## 🏗️ Arquitetura do Projeto

```
JavaliMS/
│
├── 📊 analise-geoespacial/          # Mapeamento e heatmaps
│   ├── javali_mapa_calor_ms.py      # Mapa de calor com GeoPandas (42 municípios)
│   ├── javali_mapa_interativo.py    # Mapa interativo Folium (OpenStreetMap/Satélite)
│   └── saida_javali/                # PNGs e CSVs gerados
│
├── 📈 dashboard/                     # Visualização de dados
│   └── dashboard_javali_confirmado.html  # Dashboard com dados verificados (Chart.js)
│
├── 🤖 deteccao-yolo/                # Modelo de detecção (em desenvolvimento)
│   ├── dataset/                     # Imagens anotadas para treinamento
│   │   ├── images/                  # Fotos de javalis + danos em lavouras
│   │   └── labels/                  # Anotações YOLO format (txt)
│   ├── models/                      # Pesos treinados
│   └── train.py                     # Script de treinamento
│
├── 📱 registro-campo/               # Sistema de coleta de dados (em desenvolvimento)
│   └── ...                          # App web para registro georreferenciado
│
├── 📄 docs/                         # Documentação e ofícios
│   ├── Oficio_UCDB_IBAMA_SIMAF.pdf  # Solicitação LAI dos dados SIMAF
│   └── referencias/                 # PDFs das fontes (IBAMA, Embrapa)
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 📊 Módulo 1 — Análise Geoespacial

Mapeamento da ocorrência de javali nos municípios do MS com base em dados oficiais.

### Dados Confirmados

| Indicador | Valor | Fonte |
|-----------|-------|-------|
| Municípios com ocorrência em MS | 71 | IBAMA/SIMAF, 2019 |
| Javalis abatidos em MS (2013–2020) | 12.603–17.248 | IBAMA / Correio do Estado |
| Municípios prioridade extremamente alta | 4 (Rio Brilhante, Douradina, Fátima do Sul, Laguna Carapã) | Plano Javali IBAMA |
| Perda em milho (safrinha) | 10–30% | Embrapa / FAMASUL |
| Prejuízo em Rio Brilhante | R$ 1,5M (uma safra) | Sindicato Rural / FAMASUL, 2014 |
| Expansão territorial | 7 → 46 → 71 municípios (2005–2018) | Fundect/Embrapa / IBAMA |

### Visualizações Geradas

- **Mapa de calor estático** — GeoPandas + Matplotlib, 5 níveis de severidade com buffers coloridos
- **Mapa KDE** — Kernel Density Estimation com estilo heatmap contínuo
- **Mapa interativo** — Folium com camadas OpenStreetMap/Satélite/Topográfico, marcadores clicáveis com pop-ups informativos, heatmap sobreposto e camadas toggleáveis por nível de severidade

### Como Rodar

```bash
# Criar ambiente
conda create -n javali python=3.11 -y
conda activate javali

# Instalar dependências
pip install -r requirements.txt

# Gerar mapas estáticos + KDE
python analise-geoespacial/javali_mapa_calor_ms.py

# Gerar mapa interativo (abre no navegador)
python analise-geoespacial/javali_mapa_interativo.py

# Abrir dashboard de dados confirmados
xdg-open dashboard/dashboard_javali_confirmado.html   # Linux
open dashboard/dashboard_javali_confirmado.html        # macOS
start dashboard/dashboard_javali_confirmado.html       # Windows
```

---

## 🤖 Módulo 2 — Detecção por Visão Computacional (Em Desenvolvimento)

### Classes de Detecção

O modelo YOLO será treinado para detectar:

| Classe | Descrição | Aplicação |
|--------|-----------|-----------|
| `javali` | Javali (*Sus scrofa*) em campo | Acionamento de espantamento autônomo |
| `javaporco` | Híbrido javali × porco doméstico | Classificação de variantes |
| `dano_milho` | Dano em lavoura de milho | Mapeamento de prejuízos |
| `dano_soja` | Dano em lavoura de soja | Mapeamento de prejuízos |
| `dano_cana` | Dano em lavoura de cana | Mapeamento de prejuízos |
| `fucada` | Fuçada / revolvimento de solo | Identificação de presença recente |
| `rastro` | Pegadas e trilhas | Identificação de rotas |

### Fontes de Imagens

- Câmeras trap de caçadores/controladores legalizados
- Registros de produtores rurais (FAMASUL, Aprosoja/MS, Sindicatos Rurais)
- Embrapa Pantanal — acervo de pesquisa
- Coleta própria em campo (sistema de registro)
- Datasets públicos (iNaturalist, GBIF)

---

## 📱 Módulo 3 — Sistema de Registro de Campo (Em Desenvolvimento)

App web para registro georreferenciado de ataques, projetado para uso em campo com celular.

### Dados Coletados por Registro

- Data e horário exato do ataque
- Localização GPS automática (latitude/longitude)
- Município (preenchido automaticamente via geocoding reverso)
- Tipo de lavoura afetada (milho, soja, cana, pastagem, outra)
- Estimativa de área atingida (hectares)
- Tipo de dano (fuçada, destruição de plantas, revolvimento de solo)
- Número estimado de animais
- Fotografias georreferenciadas (dano + animal, se possível)
- Observações livres

---

## 🔬 Relevância Científica

### Lacunas que Este Projeto Preenche

O levantamento das fontes oficiais (IBAMA, Embrapa, UFMS, FAMASUL) revelou lacunas críticas nos dados disponíveis:

| Dado | Disponível? | Quem preenche |
|------|-------------|---------------|
| Horário exato dos ataques | ❌ Não há dados públicos | Este projeto |
| Fotos georreferenciadas de danos | ❌ Não existe banco de imagens | Este projeto |
| Comparativo entre lavouras (soja vs milho vs cana) | ⚠️ Dados escassos | Este projeto |
| Sazonalidade mensal detalhada | ❌ Dados disponíveis são anuais | Este projeto |
| Prejuízo atualizado por município | ❌ Último dado confiável: 2014 | Este projeto |
| Detecção automática por IA | ❌ Não existe no Brasil | Este projeto |

### Potencial de Publicação

- **Sistema de coleta georreferenciado** → Revista Brasileira de Gestão Ambiental / SBSI / WCAMA
- **Análise geoespacial com KDE** → Revista Brasileira de Cartografia / GEOINFO
- **Detecção YOLO de javali** → SIBGRAPI / CVPR Workshop
- **Sistema integrado completo** → Artigo de revista Qualis A

---

## 📚 Fontes e Referências

Todos os dados utilizados são verificados e rastreáveis:

- **IBAMA/SIMAF** — Sistema de Informação de Manejo de Fauna. Relatório de Gestão do Manejo de Javalis 2013–2016
- **IBAMA** — Plano Nacional de Prevenção, Controle e Monitoramento do Javali (*Sus scrofa*). Portaria Interministerial nº 232/2017
- **Embrapa Agropecuária Oeste** — Levantamento de perdas em milho safrinha 2013 (Showtec 2014)
- **Embrapa Pantanal** — Circular Técnica 124/2022
- **FAMASUL / Sindicato Rural de Rio Brilhante** — Dados de prejuízo em lavouras, safrinha 2013/2014
- **UFMS** — Mapeamento de Javalis em MS (Wagner Fischer, 2019)
- **Fundect / Embrapa Pantanal** — Pesquisador Fernando Ibanez Martins, expansão territorial 2005–2015
- **USP/ESALQ-LOG** — Prof. Paulo Bezerra, estimativa de subnotificação (Brasil 61, dez/2025)

---

## ⚙️ Requisitos

```
Python >= 3.11
geopandas >= 0.14
matplotlib >= 3.7
mapclassify >= 2.5
pandas >= 2.0
shapely >= 2.0
folium >= 0.15
geobr >= 0.3
scipy >= 1.11
ultralytics >= 8.0    # para o módulo YOLO (futuro)
```

---

## 👨‍🔬 Equipe

| Nome | Função | Contato |
|------|--------|---------|
| **George Emanuel Guedes de Carvalho** | Pesquisador principal | ra196379@ucdb.br |
| **Prof. Alan Rios Bezerra** | Orientador | UCDB |

**Laboratório Inovisão** — Escola de Computação, Universidade Católica Dom Bosco (UCDB)

Campo Grande — MS, Brasil

---

## 🤝 Como Contribuir

### Enviando Imagens

Se você é **caçador/controlador**, **produtor rural** ou **pesquisador** e possui imagens de javali ou de danos em lavouras, sua contribuição é essencial para treinar a IA:

**📧 E-mail:** ra196379@ucdb.br

**Tipos de imagem que precisamos:**
- 📷 Javali em campo, câmera trap (diurna/noturna), javaporcos, filhotes
- 🌾 Lavouras danificadas (milho, soja, cana), fuçadas, solo revolvido
- 🐾 Rastros, pegadas, trilhas, cercas rompidas

> Todas as imagens são utilizadas exclusivamente para fins acadêmicos.
> Nenhuma informação pessoal será publicada.

### Contribuindo com Código

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">

**🐗 JavaliMS** — Projeto de Pesquisa

Laboratório Inovisão · UCDB · Campo Grande, MS

*Desenvolvido com o apoio de dados do IBAMA, Embrapa, UFMS e FAMASUL*

</div>
