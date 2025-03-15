import pandas as pd

from scraper import scrape_law


def extract_text_diff(new_text: str, old_text: str) -> tuple[str, str]:
    """Extracts the text difference between two texts and removes common prefixes and suffixes."""
    old_words = old_text.split()
    new_words = new_text.split()

    # Find the common prefix
    start = 0
    while start < len(old_words) and start < len(new_words) and old_words[start] == new_words[start]:
        start += 1

    # Find the common suffix
    end_old, end_new = len(old_words), len(new_words)
    while end_old > start and end_new > start and old_words[end_old - 1] == new_words[end_new - 1]:
        end_old -= 1
        end_new -= 1

    # Extract differences
    diff_old = " ".join(old_words[start:end_old])
    diff_new = " ".join(new_words[start:end_new])

    return diff_new, diff_old


def compare_law_versions(df_new: pd.DataFrame, df_old: pd.DataFrame, only_output_diff: bool = True) -> None:
    """Compare two law versions and print the differences on a paragraph level."""
    paragraphs_new = set(df_new.paragraph_id.tolist())
    paragraphs_old = set(df_old.paragraph_id.tolist())

    print("Die folgenden Paragraphen wurden hinzugefügt:")
    new_paragraphs = paragraphs_new - paragraphs_old
    for p in new_paragraphs:
        print(f'{p}: {df_new.loc[df.paragraph_id == p, "text_content"].iloc[0]}')

    print("\n\nDie folgenden Paragraphen sind nicht mehr vorhanden:")
    removed_paragraphs = paragraphs_old - paragraphs_new
    for p in removed_paragraphs:
        print(f'{p}: {df_old.loc[df_old.paragraph_id == p, "text_content"].iloc[0]}')

    print("\n\nBei den folgenden Paragraphen hat sich der Text verändert:")
    common_paragraphs = paragraphs_new & paragraphs_old
    for p in common_paragraphs:
        if df_new.loc[df_new.paragraph_id == p, "text_content"].iloc[0] != df_old.loc[df.paragraph_id == p, "text_content"].iloc[0]:
            old_text = df_old.loc[df_old.paragraph_id == p, "text_content"].iloc[0]
            new_text = df_new.loc[df_new.paragraph_id == p, "text_content"].iloc[0]

            if only_output_diff:
                new_text, old_text = extract_text_diff(new_text=new_text, old_text=old_text)
            print(f"{p}:")
            print(f'Alter Text: {old_text}')
            print(f'\nNeuer Text: {new_text}')


if __name__ == "__main__":
    law_url = "https://www.gesetze-im-internet.de/asylblg/xml.zip"

    df, metadata = scrape_law(url=law_url)

    # Create mock previous version, with one paragraph removed, one added, and one changed
    df_modified = df.copy()
    ind_to_delete = 28
    new_paragraph = pd.Series({
        "paragraph_id": "§ 21",
        "paragraph_title": "Datendialog",
        "text_content": "Lorem Ipsum Dolor Sit Amet",
    })
    df_modified = pd.concat([df_modified, new_paragraph.to_frame().T])
    df_modified.drop(ind_to_delete, inplace=True)
    start_index = df_modified.iloc[0, -1].find("(4) Leistungsberechtigte nach Absatz 1 Nummer 5")
    df_modified.iloc[0, -1] = df_modified.iloc[0, -1][:start_index] + "(4) Leistungsberechtigte nach Absatz 1 Nummer 5, denen bereits von einem anderen Mitgliedstaat der Europäischen Union oder von einem am Verteilmechanismus teilnehmenden Drittstaat im Sinne von § 1a Absatz 4 Satz 1 internationaler Schutz gewährt worden ist, haben keinen Anspruch auf Leistungen nach diesem Gesetz, wenn der internationale Schutz fortbesteht. 2 Hilfebedürftigen Ausländern, die Satz 1 unterfallen, werden bis zur Ausreise, längstens jedoch für einen Zeitraum von zwei Wochen, einmalig innerhalb von zwei Jahren nur eingeschränkte Hilfen gewährt, um den Zeitraum bis zur Ausreise zu überbrücken (Überbrückungsleistungen); die Zweijahresfrist beginnt mit dem Erhalt der Überbrückungsleistungen nach Satz 2. 3 Hierüber und über die Möglichkeit der Leistungen nach Satz 6 sind die Leistungsberechtigten zu unterrichten. 4 Die Überbrückungsleistungen umfassen die Leistungen nach § 1a Absatz 1 und nach § 4 Absatz 1 Satz 1 und Absatz 2. 5 Sie sollen als Sachleistung erbracht werden. 6 Soweit dies im Einzelfall besondere Umstände erfordern, werden Leistungsberechtigten nach Satz 2 zur Überwindung einer besonderen Härte andere Leistungen nach den §§ 3, 4 und 6 gewährt; ebenso sind Leistungen über einen Zeitraum von zwei Wochen hinaus zu erbringen, soweit dies im Einzelfall auf Grund besonderer Umstände zur Überwindung einer besonderen Härte und zur Deckung einer zeitlich befristeten Bedarfslage geboten ist. 7 Neben den Überbrückungsleistungen werden auf Antrag auch die angemessenen Kosten der Rückreise übernommen. 8 Satz 7 gilt entsprechend, soweit die Personen allein durch die angemessenen Kosten der Rückreise die in Satz 4 genannten Bedarfe nicht aus eigenen Mitteln oder mit Hilfe Dritter decken können. 9 Die Leistung ist als Darlehen zu erbringen."

    compare_law_versions(df_new=df, df_old=df_modified, only_output_diff=True)
