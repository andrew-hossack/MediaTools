'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2021-03-07 18:31:20
 # @ Description: Text To Speech class
 '''

from google.cloud import texttospeech
import os
from pathlib import Path

class TTSHelper():
    '''
    Text to speech helper class
    https://googleapis.dev/python/texttospeech/latest/index.html
    '''
    def __init__(self, output_directory='dat', outfile_name='audio.mp3', **kwargs):
        '''
        output_directory (str): directory where output audio file will be saved to
            Defaults to /dat
        outfile_name (str): name of audio output file
            Defaults to audio.mp3
        '''
        self.text = None
        self._output_directory = Path(f'{Path(os.path.join(os.path.dirname(__file__))).parent}/{output_directory}')
        self._secrets_filepath = Path(f'{Path(os.path.join(os.path.dirname(__file__)))}/private/google_tts_secrets.json')
        self._outfile_name = outfile_name
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self._secrets_filepath
        self._client = texttospeech.TextToSpeechClient()

    def synthesize_speech(self, text, language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL):
        """Synthesizes speech from the input string of text or ssml.
        Note: ssml must be well-formed according to:
            https://www.w3.org/TR/speech-synthesis/
        """
        self.text = text

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=self.text)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code, ssml_gender=ssml_gender
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self._client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open(f'{self._output_directory}/{self._outfile_name}', "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file "output.mp3"')
