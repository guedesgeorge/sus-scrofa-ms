# 🤖 Detecção de javali — Javali Detech YOLOv8s

Detector de objeto de classe única (`Javali`) para javali e javaporco (*Sus scrofa*) em fotos e imagens de armadilha fotográfica.

🤗 **Modelo no Hugging Face:** [Georgeemannuel007/javali-detech-yolov8s](https://huggingface.co/Georgeemannuel007/javali-detech-yolov8s)

## Como usar

```bash
pip install -r requirements.txt
python predict.py foto.jpg                 # uma imagem
python predict.py pasta_de_fotos/          # várias imagens
python predict.py video.mp4 --conf 0.4     # vídeo, com confiança mínima de 0,4
```

Os pesos (`best.pt`, 22 MB) são baixados do Hugging Face na primeira execução. As imagens com as caixas desenhadas ficam em `runs/detect/`.

No seu próprio código:

```python
from huggingface_hub import hf_hub_download
from ultralytics import YOLO

modelo = YOLO(hf_hub_download("Georgeemannuel007/javali-detech-yolov8s", "best.pt"))
resultado = modelo.predict("foto.jpg", conf=0.25)[0]
print("javalis detectados:", len(resultado.boxes))
```

## Treinamento

| Parâmetro | Valor |
|---|---|
| Arquitetura | YOLOv8s pré-treinado no COCO (transfer learning) |
| Imagem / batch | 640 px / 8 |
| Otimizador | AdamW, lr0 = 1e-4, cosine LR |
| Épocas | até 1000, early stopping com paciência 100 (convergiu entre 152 e 251) |
| Aumento de dados | mosaic, flip horizontal, HSV, translação/escala, RandAugment, random erasing |
| Validação | 5-fold cross-validation, ~50 imagens de teste por fold |
| Base | 252 imagens, 481 javalis anotados |

## Resultados

Média ± desvio padrão no conjunto de **teste** dos 5 folds. As três arquiteturas foram treinadas e avaliadas nos mesmos folds.

| Modelo | mAP@50-95 | mAP@50 | mAP@75 | Precisão | Revocação | F1 | MAE contagem | r contagem |
|---|---|---|---|---|---|---|---|---|
| **YOLOv8s** | 0.396 ± 0.035 | 0.579 ± 0.048 | **0.462** ± 0.053 | 0.794 ± 0.041 | 0.726 ± 0.035 | 0.758 ± 0.032 | 0.53 ± 0.18 | **0.942** ± 0.009 |
| DETR | **0.405** ± 0.054 | **0.641** ± 0.043 | 0.444 ± 0.072 | **0.800** ± 0.026 | **0.765** ± 0.044 | **0.782** ± 0.025 | **0.52** ± 0.16 | 0.926 ± 0.020 |
| Faster R-CNN | 0.152 ± 0.029 | 0.413 ± 0.039 | 0.044 ± 0.028 | 0.160 ± 0.046 | 0.772 ± 0.052 | 0.262 ± 0.064 | 7.69 ± 3.04 | 0.797 ± 0.072 |

- **MAE contagem:** erro absoluto médio no número de javalis por imagem.
- **r contagem:** correlação de Pearson entre a contagem real e a predita.

Os resultados por fold estão em [`resultados/cv_metrics.csv`](resultados/cv_metrics.csv), e a contagem imagem a imagem está em [`resultados/counting.csv`](resultados/counting.csv).

O mAP@50 de 0,89–0,95 que aparece nas curvas de treino é do conjunto de *validação* usado no early stopping. Os números citáveis são os da tabela acima, do conjunto de *teste* separado.

## Limitações

- **Base pequena (252 imagens).** O desempenho pode cair em armadilhas fotográficas noturnas (IR), em outros biomas ou com animais parcialmente ocultos.
- **Espécies nativas.** O modelo ainda não foi avaliado contra **cateto** (*Pecari tajacu*) e **queixada** (*Tayassu pecari*), espécies nativas protegidas. A próxima versão vai incluir imagens dessas espécies como fundo negativo e medir a taxa de falso positivo.
- **Uso com revisão humana.** Não use as detecções como única base para abate ou outra ação irreversível.

## Dados

As imagens vêm de registros do GBIF/iNaturalist sob licenças Creative Commons, de fotos de campo e de parceiros institucionais. Por causa das licenças diferentes, o dataset não é distribuído neste repositório.

## Licença

Os scripts desta pasta seguem a licença MIT do repositório. Os pesos do modelo seguem a AGPL-3.0, herdada do Ultralytics YOLOv8.
