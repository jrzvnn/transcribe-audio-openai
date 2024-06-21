import openai

# Set your API key, you can use env variables for added security
api_key = "API_KEY"


client = openai.Client(api_key=api_key)

# Define the path to your large audio file
audio_path = 'audio.mp3'


def transcribe_audio(audio_file):
    try:
        # Call the transcriptions.create() method on the client object
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return response
    except openai.OpenAIError as e:
        print(f"OpenAIError: {e}")
        return None

# Split the audio file into manageable chunks (example splitting by 10 MB chunks)
chunk_size = 10 * 1024 * 1024  # 10 MB in bytes
with open(audio_path, "rb") as audio_file:
    audio_data = audio_file.read()
    file_size = len(audio_data)
    chunks = []

    # Split into chunks
    for i in range(0, file_size, chunk_size):
        chunk = audio_data[i:i + chunk_size]
        chunks.append(chunk)

    # Transcribe each chunk
    for i, chunk in enumerate(chunks):
        with open(f"chunk_{i+1}.mp3", "wb") as chunk_file:
            chunk_file.write(chunk)
        
        with open(f"chunk_{i+1}.mp3", "rb") as chunk_file:
            response = transcribe_audio(chunk_file)
            if response:
                print(f"Transcription for chunk {i+1}: {response}")

# Note: This is a basic example. Adjust the chunk size and handling based on your specific requirements.
