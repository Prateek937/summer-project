import boto3
import subprocess

def text_to_speech(text):
    # Initialize the Amazon Polly client
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'  # Example voice ID, you can replace it with a desired voice
    )

    # Save the audio file
    with open('./output.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())

def process_file(file_path):
    # Read the file
    with open(file_path, 'r') as file:
        file_contents = file.read()

    # Call Polly to convert the contents to speech
    text_to_speech(file_contents)

    # Play the audio file
    subprocess.run(['mpg123', './output.mp3'])
