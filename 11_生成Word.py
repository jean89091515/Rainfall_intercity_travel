"""把 论文初稿/manuscript_en.md、manuscript_zh.md 转成 Word（pandoc + 自制参考模板）。

模板：A4、2.54 cm 页边距、1.5 倍行距、页脚居中页码；英文 Times New Roman，中文正文宋体、标题黑体；
标题黑色；表格为三线表；图题、表注 10.5 pt。英文稿加连续行号（Elsevier 投稿要求）。
公式由 pandoc 转成 Word 原生公式，可直接编辑。

用法：python3 11_生成Word.py            # 两种语言都生成
      python3 11_生成Word.py en         # 只生成英文
"""
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DRAFT = ROOT / "论文初稿"
OUTPUTS = {"en": ("manuscript_en.md", "Rainfall_intercity_travel_manuscript_EN.docx"),
           "zh": ("manuscript_zh.md", "降雨与城际出行_论文初稿_中文.docx")}

FOOTER = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
          '<w:p><w:pPr><w:suppressLineNumbers/><w:jc w:val="center"/></w:pPr>'
          '<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
          '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r>'
          '</w:p></w:ftr>')


def fonts(east_asia):
    return (f'<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="{east_asia}" '
            f'w:cs="Times New Roman" />')


def style_block(styles, sid):
    m = re.search(r'<w:style [^>]*w:styleId="%s".*?</w:style>' % sid, styles, re.S)
    return m.group(0)


def set_rpr(block, rpr_inner):
    """Replace a style's run properties wholesale (or add them)."""
    block = re.sub(r"<w:rPr>.*?</w:rPr>", "", block, flags=re.S)
    return block.replace("</w:style>", f"<w:rPr>{rpr_inner}</w:rPr></w:style>")


def set_ppr(block, ppr_inner):
    block = re.sub(r"<w:pPr>.*?</w:pPr>", "", block, flags=re.S)
    return block.replace("</w:style>", f"<w:pPr>{ppr_inner}</w:pPr></w:style>")


def build_reference(lang, out):
    base = Path(tempfile.mkdtemp())
    raw = base / "base.docx"
    with open(raw, "wb") as fh:
        fh.write(subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"],
                                capture_output=True, check=True).stdout)
    unz = base / "x"
    with zipfile.ZipFile(raw) as z:
        z.extractall(unz)

    zh = lang == "zh"
    body_ea, head_ea = ("宋体", "黑体") if zh else ("宋体", "宋体")
    st = (unz / "word/styles.xml").read_text(encoding="utf-8")
    st = re.sub(r"/>\s*(>|&gt;)", "/>", st)                     # pandoc 3.1 默认模板 AbstractTitle 里多余的“>”
    # 默认字体、字号、行距
    st = re.sub(r"<w:rPrDefault>.*?</w:rPrDefault>",
                f'<w:rPrDefault><w:rPr>{fonts(body_ea)}<w:sz w:val="24" /><w:szCs w:val="24" />'
                f'<w:lang w:val="en-US" w:eastAsia="{"zh-CN" if zh else "en-US"}" /></w:rPr></w:rPrDefault>', st, flags=re.S)
    st = re.sub(r"<w:pPrDefault>.*?</w:pPrDefault>",
                '<w:pPrDefault><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="auto" /></w:pPr></w:pPrDefault>',
                st, flags=re.S)
    indent = '<w:ind w:firstLine="480" />' if zh else ""
    edits = {
        "BodyText": lambda b: set_ppr(b, f'<w:spacing w:before="0" w:after="120" />{indent}<w:jc w:val="both" />'),
        "FirstParagraph": lambda b: set_ppr(b, f'<w:spacing w:before="0" w:after="120" />{indent}<w:jc w:val="both" />'),
        "Compact": lambda b: set_rpr(set_ppr(b, '<w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto" />'
                                                    '<w:ind w:firstLine="0" />'),
                                     f'{fonts(body_ea)}<w:sz w:val="20" /><w:szCs w:val="20" />'),
        "Title": lambda b: set_rpr(b, f'{fonts(head_ea)}<w:b /><w:bCs /><w:sz w:val="32" /><w:szCs w:val="32" />'),
        "Heading1": lambda b: set_rpr(b, f'{fonts(head_ea)}<w:b /><w:bCs /><w:sz w:val="28" /><w:szCs w:val="28" />'),
        "Heading2": lambda b: set_rpr(b, f'{fonts(head_ea)}<w:b /><w:bCs /><w:sz w:val="24" /><w:szCs w:val="24" />'),
        "Heading3": lambda b: set_rpr(b, f'{fonts(head_ea)}<w:b /><w:bCs />{"" if zh else "<w:i />"}'
                                         '<w:sz w:val="24" /><w:szCs w:val="24" />'),
        "Caption": lambda b: set_rpr(b, f'{fonts(body_ea)}{"" if zh else "<w:i />"}<w:sz w:val="21" /><w:szCs w:val="21" />'),
        "ImageCaption": lambda b: set_ppr(b, '<w:spacing w:before="60" w:after="240" w:line="240" w:lineRule="auto" />'
                                             '<w:jc w:val="center" />'),
        "Author": lambda b: set_ppr(b, '<w:keepNext /><w:spacing w:before="0" w:after="60" /><w:jc w:val="center" />'),
    }
    for sid, fn in edits.items():
        old = style_block(st, sid)
        st = st.replace(old, fn(old))
    # 自定义段落样式：表题（居中、与表同页）、表注（小字、无缩进）；正文中用 ::: {custom-style="..."} 引用
    st = st.replace("</w:styles>",
                    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="TableTitle"><w:name w:val="Table Title" />'
                    '<w:basedOn w:val="Normal" /><w:qFormat /><w:pPr><w:keepNext /><w:spacing w:before="240" w:after="120" />'
                    '<w:jc w:val="center" /></w:pPr><w:rPr><w:sz w:val="21" /><w:szCs w:val="21" /></w:rPr></w:style>'
                    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="TableNote"><w:name w:val="Table Note" />'
                    '<w:basedOn w:val="Normal" /><w:qFormat /><w:pPr><w:spacing w:before="60" w:after="240" w:line="276" '
                    'w:lineRule="auto" /><w:jc w:val="both" /></w:pPr><w:rPr><w:sz w:val="20" /><w:szCs w:val="20" />'
                    '</w:rPr></w:style>'
                    f'<w:style w:type="paragraph" w:customStyle="1" w:styleId="Declarations"><w:name w:val="Declarations" />'
                    f'<w:basedOn w:val="BodyText" /><w:qFormat /><w:pPr><w:jc w:val="left" /></w:pPr></w:style>'
                    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="ReferenceList"><w:name w:val="Reference List" />'
                    '<w:basedOn w:val="Normal" /><w:qFormat /><w:pPr><w:spacing w:before="0" w:after="80" w:line="264" '
                    'w:lineRule="auto" /><w:ind w:left="360" w:hanging="360" /><w:jc w:val="left" /></w:pPr>'
                    '<w:rPr><w:sz w:val="21" /><w:szCs w:val="21" /></w:rPr></w:style></w:styles>')
    for sid in ("Heading1", "Heading2", "Heading3"):              # 标题前后间距
        old = style_block(st, sid)
        st = st.replace(old, re.sub(r'<w:spacing [^>]*/>', '<w:spacing w:before="240" w:after="120" />', old))
    # 三线表：表格上下粗线，表头下细线
    old = style_block(st, "Table")
    new = old.replace('<w:tblInd w:w="0" w:type="dxa" />',
                      '<w:tblInd w:w="0" w:type="dxa" /><w:tblBorders>'
                      '<w:top w:val="single" w:sz="12" w:space="0" w:color="000000" />'
                      '<w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000" /></w:tblBorders>', 1)
    new = re.sub(r'(<w:tblStylePr w:type="firstRow">.*?)<w:tcPr>.*?</w:tcPr>',      # 表头下细线（子元素按 schema 顺序）
                 r'\1<w:tcPr><w:tcBorders><w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000" /></w:tcBorders>'
                 r'<w:vAlign w:val="bottom" /></w:tcPr>', new, count=1, flags=re.S)
    st = st.replace(old, new)
    old = style_block(st, "AbstractTitle")                      # pandoc 模板里 jc 在 spacing 之前，按 schema 调整
    jc = re.search(r"<w:jc [^>]*/>", old)
    if jc:
        st = st.replace(old, old.replace(jc.group(0), "").replace("</w:pPr>", jc.group(0) + "</w:pPr>", 1))
    (unz / "word/styles.xml").write_text(st, encoding="utf-8")

    # 页面：A4、页边距、页脚页码；英文稿加连续行号
    (unz / "word/footer1.xml").write_text(FOOTER, encoding="utf-8")
    rels = (unz / "word/_rels/document.xml.rels").read_text(encoding="utf-8")
    rels = rels.replace("</Relationships>",
                        '<Relationship Id="rIdFooterPg" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                        'relationships/footer" Target="footer1.xml"/></Relationships>')
    (unz / "word/_rels/document.xml.rels").write_text(rels, encoding="utf-8")
    ct = (unz / "[Content_Types].xml").read_text(encoding="utf-8")
    ct = ct.replace("</Types>", '<Override PartName="/word/footer1.xml" ContentType="application/'
                                'vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/></Types>')
    (unz / "[Content_Types].xml").write_text(ct, encoding="utf-8")

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(unz.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(unz).as_posix())
    shutil.rmtree(base)


def set_page(docx, lang):
    """pandoc 不保留模板的节属性：生成后写入 A4、页边距、页脚页码，英文稿加连续行号。"""
    tmp = docx.with_suffix(".tmp")
    with zipfile.ZipFile(docx) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        rels = zin.read("word/_rels/document.xml.rels").decode("utf-8")
        rid = re.search(r'Id="([^"]+)"[^>]*Target="footer1.xml"|Target="footer1.xml"[^>]*Id="([^"]+)"', rels)
        rid = rid.group(1) or rid.group(2)
        lnnum = "" if lang == "zh" else '<w:lnNumType w:countBy="1" w:distance="360" w:restart="continuous" />'
        sect = (f'<w:sectPr><w:footerReference w:type="default" r:id="{rid}" />'
                '<w:pgSz w:w="11906" w:h="16838" />'
                '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" '
                f'w:gutter="0" />{lnnum}</w:sectPr>')
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "[Content_Types].xml" and b'Extension="png"' not in data:   # 补声明 png 类型
                data = data.replace(b"<Default ", b'<Default Extension="png" ContentType="image/png" /><Default ', 1)
            if item.filename == "word/document.xml":
                doc = re.sub(r"<w:sectPr\s*/>|<w:sectPr.*?</w:sectPr>", "", data.decode("utf-8"), flags=re.S)
                if 'xmlns:r=' not in doc[:2000]:
                    doc = doc.replace("<w:document ", '<w:document xmlns:r="http://schemas.openxmlformats.org/'
                                      'officeDocument/2006/relationships" ', 1)
                data = doc.replace("</w:body>", sect + "</w:body>").encode("utf-8")
            zout.writestr(item, data)
    tmp.replace(docx)


def convert(lang):
    src, dst = OUTPUTS[lang]
    ref = DRAFT / f"_reference_{lang}.docx"
    build_reference(lang, ref)
    cmd = ["pandoc", src, "-o", dst, f"--reference-doc={ref.name}",
           "-f", "markdown+pipe_tables+tex_math_dollars+implicit_figures+fenced_divs+superscript",
           "--resource-path=."]
    subprocess.run(cmd, cwd=DRAFT, check=True)
    set_page(DRAFT / dst, lang)
    print("已生成", DRAFT / dst)


if __name__ == "__main__":
    for lang in (sys.argv[1:] or ["en", "zh"]):
        if (DRAFT / OUTPUTS[lang][0]).exists():
            convert(lang)
        else:
            print("缺少源文件：", OUTPUTS[lang][0])
