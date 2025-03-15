import io
import zipfile

import pandas as pd
import requests
from lxml import etree


def scrape_law(url: str) -> tuple[pd.DataFrame, dict]:
    """Scrape law paragraphs from a given XML URL of gesetze-im-internet.de."""
    # Download and parse XML
    r = requests.get(url, stream=True)
    with zipfile.ZipFile(io.BytesIO(r.content)) as zip_file:
        for name in zip_file.namelist():
            with zip_file.open(name) as f:
                tree = etree.parse(f)

    root = tree.getroot()

    # Extract paragraph data
    paragraphs = []
    metadata = {}
    if build_date := root.attrib["builddate"]:
        metadata["build_date"] = build_date
    if document_number := root.attrib["doknr"]:
        metadata["document_number"] = document_number
    for child in root:
        if (law_abbreviation := child.find(".//jurabk")) is not None:
            metadata["law_abbreviation"] = law_abbreviation.text

        paragraph_id = child.find(".//enbez")
        if paragraph_id is None:  # Header row with no paragraph_id
            if (document_title := child.find(".//langue")) is not None:
                metadata["document_title"] = document_title.text
            if (
                new_state_comment := child.find(
                    ".//standangabe[standtyp='Neuf']/standkommentar"
                )
            ) is not None:
                metadata["new_state_comment"] = new_state_comment.text
            if (
                current_state_comment := child.find(
                    ".//standangabe[standtyp='Stand']/standkommentar"
                )
            ) is not None:
                metadata["current_state_comment"] = current_state_comment.text
            continue
        paragraph_id = paragraph_id.text
        paragraph_title = child.find(".//titel").text
        try:
            text_content = "\n".join(
                " ".join(p.itertext()) for p in child.findall(".//text/Content/P")
            )
        except TypeError:  # Occurs when there is no text
            text_content = ""
        paragraphs.append(
            {
                "paragraph_id": paragraph_id,
                "paragraph_title": paragraph_title,
                "text_content": text_content,
            }
        )

    return pd.DataFrame(paragraphs), metadata


if __name__ == "__main__":
    law_url = "https://www.gesetze-im-internet.de/asylblg/xml.zip"

    df, metadata = scrape_law(url=law_url)
    print(df)
    print(metadata)
