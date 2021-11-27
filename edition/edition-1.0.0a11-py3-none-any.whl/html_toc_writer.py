from typing import IO, List

from comprehemd.outline import Outline, OutlineItem


class HtmlTableOfContentsRenderer:
    def __init__(self, outline: Outline) -> None:
        self._outline = outline

    def _render(self, items: List[OutlineItem], writer: IO[str]) -> None:
        if not items:
            return

        writer.write("<ol>")
        for item in items:
            writer.write('<li><a href="#')
            writer.write(item.block.anchor)
            writer.write('">')
            writer.write(item.block.text)
            writer.write("</a>")
            self._render(items=item.children, writer=writer)
            writer.write("</li>")

        writer.write("</ol>")

    def render(self, writer: IO[str]) -> None:
        writer.write('<nav class="toc">')
        self._render(items=self._outline.root, writer=writer)
        writer.write("</nav>")
