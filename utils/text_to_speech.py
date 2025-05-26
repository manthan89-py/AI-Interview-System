import asyncio
import edge_tts
import pygame
import tempfile
import os


async def speak_edge_tts(text, voice="en-US-AriaNeural", rate="+0%", pitch="+0Hz"):
    """
    High-quality TTS using Microsoft Edge voices

    Popular voices:
    - en-US-AriaNeural (female)
    - en-US-GuyNeural (male)
    - en-GB-SoniaNeural (British female)
    - en-AU-NatashaNeural (Australian female)
    """
    try:
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            await communicate.save(tmp_file.name)

            # Play using pygame
            pygame.mixer.init()
            pygame.mixer.music.load(tmp_file.name)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)

            pygame.mixer.quit()

        os.unlink(tmp_file.name)

    except Exception as e:
        print(f"Edge-TTS Error: {e}")
        print("Text:", text)


def speak_text(text, voice="en-US-GuyNeural", rate="+0%", pitch="+0Hz"):
    """Synchronous wrapper for Edge-TTS"""
    asyncio.run(speak_edge_tts(text, voice, rate, pitch))
