import io
import sys, os

pathname = os.path.dirname(sys.argv[0])
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = pathname+"/Extensions/Sentiment247-4d3b36eedd95.json"

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    for text in texts:
        return text.description
        #print('\n"{}"'.format(text.description))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
