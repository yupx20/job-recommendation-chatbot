# Audio Handling in Gemini API - Key Findings

## Upload Methods:
1. **Files API** - For files larger than 20MB or when reusing audio multiple times
2. **Inline data** - For smaller files (total request < 20MB)

## Supported Audio Formats:
- WAV - `audio/wav`
- MP3 - `audio/mp3`
- AIFF - `audio/aiff`
- AAC - `audio/aac`
- OGG Vorbis - `audio/ogg`
- FLAC - `audio/flac`

## Implementation Notes:
- Use `client.files.upload()` for uploading audio files
- Use `types.Part.from_bytes()` for inline audio data
- Maximum audio length: 9.5 hours per prompt
- Audio is represented as 32 tokens per second
- Can request transcripts by including it in the prompt
- Can refer to specific timestamps (MM:SS format)

## Code Examples:

### Upload method:
```python
myfile = client.files.upload(file="path/to/sample.mp3")
response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=["Describe this audio clip", myfile]
)
```

### Inline method:
```python
with open('path/to/small-sample.mp3', 'rb') as f:
    audio_bytes = f.read()

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'Describe this audio clip',
        types.Part.from_bytes(data=audio_bytes, mime_type='audio/mp3')
    ]
)
```
