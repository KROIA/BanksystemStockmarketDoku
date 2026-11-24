# Fails the build when a page's front matter can't be read. MkDocs would otherwise
# show the raw "title: ... description: ..." block as page text without a warning.
from mkdocs.exceptions import PluginError


def on_page_markdown(markdown, page, **kwargs):
    if "title" not in page.meta or "description" not in page.meta:
        raise PluginError(
            f"{page.file.src_uri}: front matter is missing or invalid YAML. "
            'Put title and description in double quotes.'
        )
    return markdown
