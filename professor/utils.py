import os
import re
from django.utils import timezone

def unique_filename(base_name, ext):
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    return f"{base_name}_{timestamp}.{ext}"

def normalize_name(name: str) -> str:
    return re.sub(r"\s+", "_", name.strip().lower()) if name else "sem_nome"

def img_prof(instance, filename):
    ext = filename.split('.')[-1]
    prof_name = normalize_name(getattr(instance, "nome", None))
    return os.path.join("professor", prof_name, "img", f"{prof_name}.{ext}")

def docs_prof(instance, filename):
    ext = filename.split('.')[-1]
    prof_name = normalize_name(getattr(instance, "nome", None))
    doc_type = instance.tipo_dokumentu.lower()
    base_name = f"{prof_name}_{doc_type}"
    final_name = unique_filename(base_name, ext)
    return os.path.join("professor", prof_name, "docs", final_name)