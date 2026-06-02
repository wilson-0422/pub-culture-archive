import csv
import io
from app.models.archive import Archive
from app.models.category import Category
from app import db


class ReportService:
    @staticmethod
    def generate_archives_csv(category_id=None, status=None):
        query = Archive.query
        if category_id:
            query = query.filter_by(category_id=category_id)
        if status:
            query = query.filter_by(status=status)
        archives = query.order_by(Archive.created_at.desc()).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "标题", "描述", "分类", "年代", "地点", "状态", "创建时间"])
        for a in archives:
            cat_name = a.category.name if a.category else ""
            writer.writerow([
                a.id,
                a.title,
                a.description[:200] if a.description else "",
                cat_name,
                a.era,
                a.location,
                a.status,
                a.created_at.strftime("%Y-%m-%d %H:%M") if a.created_at else "",
            ])
        return output.getvalue()

    @staticmethod
    def generate_summary_text():
        total_archives = Archive.query.count()
        total_categories = Category.query.count()
        status_counts = ArchiveService.count_by_status()

        lines = [
            "文化遗产档案系统 - 统计报告",
            "=" * 40,
            f"档案总数: {total_archives}",
            f"分类总数: {total_categories}",
            "",
            "各状态档案数量:",
        ]
        for status, count in status_counts.items():
            status_label = {"draft": "草稿", "published": "已发布", "archived": "已归档"}.get(status, status)
            lines.append(f"  {status_label}: {count}")

        lines.append("")
        lines.append("各分类档案数量:")
        categories = Category.query.all()
        for cat in categories:
            count = Archive.query.filter_by(category_id=cat.id).count()
            lines.append(f"  {cat.name}: {count}")

        return "\n".join(lines)


from app.services.archive_service import ArchiveService
