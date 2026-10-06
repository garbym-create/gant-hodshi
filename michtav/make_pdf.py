"""יצירת PDF למכתב חודשי מתוך דף ה-HTML.

שימוש:  python make_pdf.py cheshvan
מוריד מהדף את כפתור ההורדה, מוסיף את print.css ומדפיס עם Chrome לעמוד A4 אחד.
"""
import re, subprocess, sys, tempfile, pathlib

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
here = pathlib.Path(__file__).parent


def build(src_html: str, out_pdf: pathlib.Path):
    html = re.sub(r'<div style="padding:0 28px 6px;display:flex;justify-content:flex-start">\s*<a href="[^"]+\.pdf"[\s\S]*?</div>\s*', '', src_html)
    css = (here / "print.css").read_text(encoding="utf-8")
    html = html.replace("</head>", f"<style>{css}</style></head>", 1)
    tmp = pathlib.Path(tempfile.gettempdir()) / "michtav_print.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out_pdf}", tmp.as_uri()], check=True, capture_output=True)


if __name__ == "__main__":
    month = sys.argv[1]
    out = here / f"{month}.pdf"
    build((here / f"{month}.html").read_text(encoding="utf-8"), out)
    import pypdf
    n = len(pypdf.PdfReader(out).pages)
    print(f"{out.name}: {n} page(s)")
    if n != 1:
        sys.exit("ERROR: PDF is not a single page")
