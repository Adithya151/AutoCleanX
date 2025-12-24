import pandas as pd
import chardet
from django.shortcuts import render, redirect
from django.http import FileResponse
from .cleaning_engine import clean_data
from .profiler import profile_data
from .visualizer import missingness_heatmap, before_after_hist
import os

import os
from django.conf import settings

UPLOAD_DIR = os.path.join(settings.MEDIA_ROOT, "uploads")
CLEANED_DIR = os.path.join(settings.MEDIA_ROOT, "cleaned")
PLOTS_DIR = os.path.join(settings.MEDIA_ROOT, "plots")

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CLEANED_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)


def upload_file(request):
    if request.method == "POST":
        uploaded_file = request.FILES["file"]

        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

        with open(file_path, "wb+") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        request.session["file_path"] = file_path
        return redirect("options")

    return render(request, "cleaner/upload.html")



def cleaning_options(request):
    if request.method == "POST":
        request.session["options"] = {
            "missing_strategy": request.POST.get("missing"),
            "handle_outliers": request.POST.get("outliers") == "on",
            "exclude_columns": request.POST.getlist("exclude")
        }
        return redirect("report")

    df = pd.read_csv(request.session["file_path"])
    return render(request, "cleaner/options.html", {"columns": df.columns})

def cleaning_report(request):
    path = request.session["file_path"]

    # Detect encoding safely
    with open(path, "rb") as f:
        encoding = chardet.detect(f.read())["encoding"] or "utf-8"

    # Load data
    df_before = pd.read_csv(path, encoding=encoding)
    before_profile = profile_data(df_before)

    # Clean data
    df_after, clean_report = clean_data(
        df_before.copy(),
        request.session["options"]
    )
    after_profile = profile_data(df_after)

    # Save cleaned CSV (filesystem path)
    cleaned_file_path = os.path.join(CLEANED_DIR, "cleaned.csv")
    df_after.to_csv(cleaned_file_path, index=False)

    # -------- PLOTS (IMPORTANT FIX) --------

    # Filesystem paths (for saving)
    heatmap_fs_path = os.path.join(PLOTS_DIR, "missing.png")
    hist_fs_path = os.path.join(PLOTS_DIR, "hist.png")

    # Generate plots
    missingness_heatmap(df_before, heatmap_fs_path)

    numeric_cols = df_before.select_dtypes(
        include=["int64", "float64"]
    ).columns

    hist_url_path = None
    if len(numeric_cols) > 0:
        before_after_hist(
            df_before,
            df_after,
            numeric_cols[0],
            hist_fs_path
        )
        hist_url_path = "plots/hist.png"

    # URL paths (for template rendering)
    heatmap_url_path = "plots/missing.png"

    # Store cleaned file path in session (for download)
    request.session["cleaned_file"] = cleaned_file_path

    return render(
        request,
        "cleaner/report.html",
        {
            "before": before_profile,
            "after": after_profile,
            "clean_report": clean_report,
            "heatmap": heatmap_url_path,   # 👈 URL path
            "hist": hist_url_path,         # 👈 URL path
            "MEDIA_URL": settings.MEDIA_URL,
        },
    )

def download_cleaned_file(request):
    return FileResponse(
        open(request.session["cleaned_file"], "rb"),
        as_attachment=True
    )
