FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

COPY model.py model.py
COPY api.py api.py
COPY G_AB.pth G_AB.pth

ENV GPU_USAGE=1

EXPOSE 1707

CMD ["python", "api.py"]