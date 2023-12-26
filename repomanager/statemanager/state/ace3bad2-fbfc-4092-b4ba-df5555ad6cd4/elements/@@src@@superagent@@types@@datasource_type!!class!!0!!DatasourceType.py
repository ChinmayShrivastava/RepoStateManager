class DatasourceType(str, enum.Enum):
    """
    An enumeration.
    """

    TXT = "TXT"
    PDF = "PDF"
    CSV = "CSV"
    PPTX = "PPTX"
    XLSX = "XLSX"
    DOCX = "DOCX"
    GOOGLE_DOC = "GOOGLE_DOC"
    YOUTUBE = "YOUTUBE"
    GITHUB_REPOSITORY = "GITHUB_REPOSITORY"
    MARKDOWN = "MARKDOWN"
    WEBPAGE = "WEBPAGE"
    AIRTABLE = "AIRTABLE"
    STRIPE = "STRIPE"
    NOTION = "NOTION"
    SITEMAP = "SITEMAP"
    URL = "URL"
    FUNCTION = "FUNCTION"

    def visit(
        self,
        txt: typing.Callable[[], T_Result],
        pdf: typing.Callable[[], T_Result],
        csv: typing.Callable[[], T_Result],
        pptx: typing.Callable[[], T_Result],
        xlsx: typing.Callable[[], T_Result],
        docx: typing.Callable[[], T_Result],
        google_doc: typing.Callable[[], T_Result],
        youtube: typing.Callable[[], T_Result],
        github_repository: typing.Callable[[], T_Result],
        markdown: typing.Callable[[], T_Result],
        webpage: typing.Callable[[], T_Result],
        airtable: typing.Callable[[], T_Result],
        stripe: typing.Callable[[], T_Result],
        notion: typing.Callable[[], T_Result],
        sitemap: typing.Callable[[], T_Result],
        url: typing.Callable[[], T_Result],
        function: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is DatasourceType.TXT:
            return txt()
        if self is DatasourceType.PDF:
            return pdf()
        if self is DatasourceType.CSV:
            return csv()
        if self is DatasourceType.PPTX:
            return pptx()
        if self is DatasourceType.XLSX:
            return xlsx()
        if self is DatasourceType.DOCX:
            return docx()
        if self is DatasourceType.GOOGLE_DOC:
            return google_doc()
        if self is DatasourceType.YOUTUBE:
            return youtube()
        if self is DatasourceType.GITHUB_REPOSITORY:
            return github_repository()
        if self is DatasourceType.MARKDOWN:
            return markdown()
        if self is DatasourceType.WEBPAGE:
            return webpage()
        if self is DatasourceType.AIRTABLE:
            return airtable()
        if self is DatasourceType.STRIPE:
            return stripe()
        if self is DatasourceType.NOTION:
            return notion()
        if self is DatasourceType.SITEMAP:
            return sitemap()
        if self is DatasourceType.URL:
            return url()
        if self is DatasourceType.FUNCTION:
            return function()
