def parse_items(data_source, row_extractor, entry_extractor):
    articles = ()
    rows = row_extractor(data_source)
    for row in reversed(rows):
        entry = entry_extractor(row)
        if entry and getattr(entry, 'item_guid', '') != "":
            articles += (entry,)
    return articles
