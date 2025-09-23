import os
from django.utils import timezone

def unique_filename(base_name, ext):
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    return f"{base_name}_{timestamp}.{ext}"

def img_est(instance, filename):
    # Path: estudante/<emis>/img/<filename>
    ext = filename.split('.')[-1]
    emis = instance.emis or "sem_emis"
    return os.path.join("estudante", emis, "img", f"{emis}.{ext}")

def doc_est(instance, filename):
    # Path: estudante/<emis>/docs/<filename>_<doc_type>
    ext = filename.split('.')[-1]
    emis = instance.estudante.emis or "sem_emis"
    doc_type = instance.tipo_dokumentu.lower()
    base_name = f"{emis}_{doc_type}"
    final_name = unique_filename(base_name, ext)
    return os.path.join("estudante", emis, "docs", final_name)
