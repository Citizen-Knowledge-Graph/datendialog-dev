import json
import requests

with open("by-leistung.txt", "r", encoding='utf-8') as file:
    lines = file.readlines()

for i in range(len(lines)):
    line = lines[i].strip()
    if line.startswith(">"):
        # antragUrl = "https://sozialplattform.de/leistung/" + line[1:]
        infoId = lines[i - 1].strip().split(":")[0].strip()
        infoUrl = "https://sozialplattform.de/inhalt/" + infoId
        leikaId = lines[i + 1].strip()

        print(leikaId)

        response = requests.get(infoUrl)
        with open("data/1/" + infoId + ".html", "wb") as file:
            file.write(response.content)

        leikaServiceUrl = "https://sozialplattform.de/content/de/api/v1/node/leika_service?filter%5Bfield_leika_service_id.id%5D=" + leikaId + "&include=field_stage.field_media.field_media_image_1%2Cfield_teaser_media.field_media_image_1%2Cfield_paragraph.field_downloads_files.field_media_file%2Cfield_paragraph.field_faq_list_inner_paragraphs%2Cfield_paragraph.field_media.field_media_image_1%2Cfield_paragraph.field_media_reference_media.field_media_image_1%2Cfield_paragraph.field_media_reference_media.field_media_video_file%2Cfield_paragraph.field_media.field_media_image_1%2Cfield_paragraph.field_media.field_media_video_file%2Cfield_paragraph.field_slideshow_slides.field_media_image_1%2Cfield_paragraph.field_label_node_reference_nodes.field_image.field_media_image_1%2Cfield_paragraph.field_label_node_reference_nodes.field_teaser_media.field_media_image_1%2Cfield_paragraph.field_label_node_reference_nodes.field_teaser_media.field_media_image_1%2Cfield_paragraph.field_media%2Cfield_paragraph.field_gallery_images.field_media.field_media_image_1%2Cfield_paragraph.field_image_links%2Cfield_paragraph.field_image_links.field_media.field_media_image_1"
        response = requests.get(leikaServiceUrl)
        with open("data/1/" + leikaId + ".json", "wb") as file:
            file.write(response.content)

        pvogUrl = "https://public.demo.pvog.cloud-bdc.dataport.de/suchdienst/api/v3/servicedescriptions/leikaid"
        ars = "00"
        response = requests.get(pvogUrl, params={"leikaIds": leikaId, "ars": ars})
        content = response.json()["content"]
        if len(content) > 0:
            with open("data/1/" + leikaId + "_pvog.json", "w") as file:
                file.write(json.dumps(content[0], indent=4))
        else:
            print("No PVOG json for LeikaId " + leikaId + " and ARS " + ars)
