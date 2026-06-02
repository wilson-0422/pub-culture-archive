from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from flask_login import login_required
from app.services.report_service import ReportService
from app.services.category_service import CategoryService

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.route("/")
@login_required
def generate():
    categories = CategoryService.get_all()
    return render_template("reports/generate.html", categories=categories)


@reports_bp.route("/export/csv")
@login_required
def export_csv():
    category_id = request.args.get("category_id", type=int)
    status = request.args.get("status", "")
    csv_content = ReportService.generate_archives_csv(category_id=category_id, status=status)
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=archives_report.csv"},
    )


@reports_bp.route("/export/summary")
@login_required
def export_summary():
    summary = ReportService.generate_summary_text()
    return Response(
        summary,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment; filename=summary_report.txt"},
    )
