from PIL import Image, ImageFilter
import climage
import requests
from io import BytesIO

##----------------png aus URL in relativ glates Terminal Bild verwandeln--------------###
def smooth_image(
    URL
    ="https://upload.wikimedia.org/wikipedia/commons"
    +"/thumb/c/c4/Flag_of_Dominica.svg/320px-Flag_of_Dominica.svg.png"
    ):
    """
    Funktion die ein Image aus einer URL erzeugt und dann ausgibt
    """
    # Bild aus einer URL laden
    flag_url =   URL
    response = requests.get(flag_url)
    img = Image.open(BytesIO(response.content))

    # Konvertieren zu CMYK (Richer colors)
    img = img.convert("CMYK").convert("RGB")

    # Gauschscher unschaerfe Filter
    img = img.filter(ImageFilter.GaussianBlur(0.1))  # Wenn noetig kann die unschaerfe angepasst werden

    # Hochaufloesende verkleinerung LANCZOS (high-quality downscaling)
    new_width = 5230 # breite anpassen um optimale qualitaet zu finden
    aspect_ratio = img.height / img.width
    new_height = int(new_width * aspect_ratio)
    img = img.resize((new_width, new_height), Image.LANCZOS)

    # in Terminal freundliches Format umwandeln
    output = climage.convert_pil(img, is_unicode=True, width=76)
    print(output)


class FileHandler:
    def __init__(self, file_path=None):
        '''
        standardconstructor to create FileHandler object
        from FileHandler class
        '''
        self.file_path = file_path


    def txt_file_to_str(self):
        '''
        method to create string from txt file content
        return: file_content as str
        '''
        with open(self.file_path, 'r') as file:
            file_content = file.read()
        file.close()
        return file_content


def main():
    '''
    main function as usage example and for testing
    '''
    print(FileHandler("rules.txt").txt_file_to_str())

#dunder main for testing
if __name__ == "__main__":
    main()
    smooth_image()
