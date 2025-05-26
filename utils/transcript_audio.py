import os
from speechmatics.models import *
import speechmatics
import threading


def transcribe_with_speechmatics(audio_path, transcription_language="en"):
    """Transcribe audio using Speechmatics WebSocket client"""
    api_key = os.environ.get("SPEECHMATICS_API_KEY")

    if not api_key:
        return "Transcription failed: No API key"

    try:
        # Create transcription client
        sm_client = speechmatics.client.WebsocketClient(api_key)

        # Store transcription results
        transcription_results = []
        transcript_lock = threading.Lock()

        # Handler for processing transcript additions
        def process_transcript(message):
            if "results" in message:
                with transcript_lock:
                    sentence_parts = []

                    for result in message["results"]:
                        if "alternatives" in result:
                            if result["type"] == "word":
                                content = result["alternatives"][0]["content"]
                                # Add space before word if not first word
                                if sentence_parts:
                                    sentence_parts.append(" ")
                                sentence_parts.append(content)
                            elif result["type"] == "punctuation":
                                content = result["alternatives"][0]["content"]
                                sentence_parts.append(content)

                    # Join the sentence parts and add to results
                    if sentence_parts:
                        sentence = "".join(sentence_parts)
                        transcription_results.append(sentence)

        # Add event handler (no partial transcript handler to reduce logs)
        sm_client.add_event_handler(
            event_name=ServerMessageType.AddTranscript,
            event_handler=process_transcript,
        )

        # Configure transcription
        conf = TranscriptionConfig(
            language=transcription_language,
            enable_partials=False,  # Disable partials to reduce logs
            max_delay=5,
        )

        # Check if file exists and has content
        if not os.path.exists(audio_path):
            return f"Audio file not found: {audio_path}"

        file_size = os.path.getsize(audio_path)
        if file_size == 0:
            return "No audio recorded"

        # Run transcription
        with open(audio_path, "rb") as audio_file:
            sm_client.run_synchronously(audio_file, conf)

        # Join all transcript segments
        if transcription_results:
            full_transcript = " ".join(transcription_results)
            print(f"Transcript: {full_transcript}")
            return full_transcript.strip()
        else:
            return "No speech detected in audio"

    except Exception as e:
        return f"Transcription failed: {str(e)}"
