import os
import json
import requests

from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import DetectedFace
from msrest.authentication import CognitiveServicesCredentials

KEY = os.environ["AZURE_FACE_REC_KEY"]
ENDPOINT = os.environ["AZURE_FACE_REC_ENDPOINT"]


def main(url: str) -> dict:
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

    detected_faces = face_client.face.detect_with_url(
        url=url,
        return_face_attributes=["emotion"])

    if detected_faces:
        return [face.face_attributes.emotion.happiness for face in detected_faces]

    return None
