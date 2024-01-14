class News:
    def __init__(self,id, title, description, publish_date, cover_image, link):
        self.id = id
        self.title = title
        self.description = description
        self.publish_date = publish_date
        self.cover_image = cover_image
        self.link = link

    def __str__(self):
        return f"Id: {self.id}\nTitle: {self.title}\nDescription: {self.description}\nPublish Date: {self.publish_date}\nCover Image: {self.cover_image}\nLink: {self.link}"