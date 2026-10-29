"""יצירת PDF למכתב חודשי מתוך דף ה-HTML.

שימוש:  python make_pdf.py <חודש> [a|b]
  a = עיצוב א' (ברירת מחדל, נבחר בכסלו): print-a.css
  b = עיצוב ב' (המקורי של חשוון): print.css
מוריד מהדף את כפתור ההורדה, מוסיף את הגדרות ההדפסה ומדפיס עם Chrome לעמוד A4 אחד.
"""
import re, subprocess, sys, tempfile, pathlib

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
here = pathlib.Path(__file__).parent
STYLES = {"a": "print-a.css", "b": "print.css"}


def build(src_html: str, out_pdf: pathlib.Path, style: str = "a"):
    html = re.sub(r'<div style="padding:0 28px 6px;display:flex;justify-content:flex-start">\s*<a href="[^"]+\.pdf"[\s\S]*?</div>\s*', '', src_html)
    css = (here / STYLES[style]).read_text(encoding="utf-8")
    html = html.replace("</head>", f"<style>{css}</style></head>", 1)
    tmp = pathlib.Path(tempfile.gettempdir()) / "michtav_print.html"
    tmp.write_text(html, encoding="utf-8")
    # Chrome לא כותב לנתיב עם עברית, אז מדפיסים לנתיב זמני ומעתיקים
    tmp_pdf = pathlib.Path(tempfile.gettempdir()) / "michtav_print.pdf"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={tmp_pdf}", tmp.as_uri()], check=True, capture_output=True)
    out_pdf.write_bytes(tmp_pdf.read_bytes())


def check(pdf: pathlib.Path):
    """עמוד אחד, הפוטר בתוך העמוד, והטקסט לא נוגע בו."""
    import fitz
    doc = fitz.open(pdf)
    print(f"{pdf.name}: {len(doc)} page(s)")
    if len(doc) != 1:
        sys.exit("ERROR: PDF is not a single page")
    page = doc[0]
    hits = page.search_for("המחלקה לחינוך לחיים בחברה")
    if not hits or hits[-1].y1 > page.rect.height - 5:
        sys.exit("ERROR: footer is cut off, letter too long")
    footer_top = min(h.y0 for h in page.search_for("משרד החינוך")) - 12
    bottom = max(b[3] for b in page.get_text("blocks") if b[3] < footer_top + 5)
    print(f"text ends at {bottom:.0f}pt, footer starts at {footer_top:.0f}pt")
    if bottom > footer_top - 6:
        sys.exit("ERROR: letter too long, text reaches the footer")


if __name__ == "__main__":
    month = sys.argv[1]
    style = sys.argv[2] if len(sys.argv) > 2 else "a"
    out = here / f"{month}.pdf"
    build((here / f"{month}.html").read_text(encoding="utf-8"), out, style)
    check(out)
