"""Detecta javalis (Sus scrofa) em imagens com o modelo Javali Detech YOLOv8s.

Os pesos são baixados automaticamente do Hugging Face na primeira execução.

Uso:
    python predict.py foto.jpg
    python predict.py pasta_de_fotos/ --conf 0.4
    python predict.py video.mp4

As imagens com as caixas desenhadas são salvas em runs/detect/.
"""
import argparse

from huggingface_hub import hf_hub_download
from ultralytics import YOLO

REPO_HF = "Georgeemannuel007/javali-detech-yolov8s"


def main():
    parser = argparse.ArgumentParser(description="Detecção de javali com YOLOv8s")
    parser.add_argument("fonte", help="Imagem, pasta de imagens ou vídeo")
    parser.add_argument("--conf", type=float, default=0.25, help="Confiança mínima (padrão: 0.25)")
    args = parser.parse_args()

    pesos = hf_hub_download(REPO_HF, "best.pt")
    modelo = YOLO(pesos)

    for resultado in modelo.predict(args.fonte, conf=args.conf, save=True, stream=True, verbose=False):
        confs = ", ".join(f"{c:.2f}" for c in resultado.boxes.conf.tolist())
        print(f"{resultado.path}: {len(resultado.boxes)} javali(s) [{confs}]")

    print(f"Imagens anotadas salvas em: {resultado.save_dir}")


if __name__ == "__main__":
    main()
