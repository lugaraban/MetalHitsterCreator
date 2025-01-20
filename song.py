import qrcode

class Song:
    id = None
    title = None
    artist = None
    year = None
    link = None
    qr_filename = None

    def __init__(self, rowNumber, title, artist, year, link):
        self.id = rowNumber
        self.title = title
        self.artist = artist
        self.year = year
        self.link = link
        self.qr_filename = "qrs/qr-"+str(rowNumber)+".png"

    def generate_qr(self):
        if (self.link):
            qr = qrcode.QRCode(version=1, box_size=10, border=1)
            qr.add_data(self.link)
            qr.make(fit=True)
            image = qr.make_image(fill_color="black", back_color="white")
            image.save(self.qr_filename)
    
    def is_empty(self):
        return self.title == None and self.artist == None and self.year == None and self.link == None