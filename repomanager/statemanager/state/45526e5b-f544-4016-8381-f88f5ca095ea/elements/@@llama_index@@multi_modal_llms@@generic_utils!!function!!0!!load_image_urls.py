def load_image_urls(image_urls: List[str]) -> List[ImageDocument]:
    # load remote image urls into image documents
    image_documents = []
    for i in range(len(image_urls)):
        new_image_document = ImageDocument(image_url=image_urls[i])
        image_documents.append(new_image_document)
    return image_documents
