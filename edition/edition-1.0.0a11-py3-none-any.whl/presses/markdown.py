from io import StringIO
from typing import IO

from comprehemd import MarkdownParser
from dinject.enums import Content, Host
from dinject.types import ParserOptions

from edition.html_renderer import EditionHtmlRenderer
from edition.presses.press import Press


class MarkdownPress(Press):
    @property
    def injection_options(self) -> ParserOptions:
        return ParserOptions(force_content=Content.MARKDOWN, force_host=Host.SHELL)

    def _press(self, writer: IO[str]) -> None:
        reader = StringIO(self._markdown_body)
        toc = self._metadata.get("toc", None)

        for block in MarkdownParser().read(reader):
            if not block.source.startswith("<edition "):
                writer.write(block.source)
                writer.write("\n")
                continue

            renderer = EditionHtmlRenderer(
                metadata=self._metadata,
                toc_writer=toc.render if toc else None,
            )

            renderer.render(
                reader=block.source,
                writer=writer,
            )
            writer.write("\n")
