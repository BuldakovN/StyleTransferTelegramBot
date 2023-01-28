FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

COPY model.py model.py
COPY api.py api.py
COPY starry_night.jpg starry_night.jpg
COPY 21styles.model 21styles.model

ENV GPU_USAGE=1

EXPOSE 1202

CMD ["python", "api.py"]