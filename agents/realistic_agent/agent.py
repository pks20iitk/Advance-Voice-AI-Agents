import asyncio
import json
import logging
from datetime import datetime
from typing import List, Optional

from dotenv import load_dotenv

from livekit.agents import (
    Agent,
    AgentSession,
    AudioConfig,
    BackgroundAudioPlayer,
    BuiltinAudioClip,
    JobContext,
    RunContext,
    WorkerOptions,
    cli,
    function_tool,
)
from livekit.plugins import deepgram, google, silero

logger = logging.getLogger("realistic-office-agent")

load_dotenv()

class OfficeCallerAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions=(
                "You are a professional office assistant named Alex from Tech Solutions. "
                "You speak in a clear, friendly, and professional tone. "
                "You are helpful, attentive, and efficient when assisting callers. "
                "You work at a modern tech company and have access to general information "
                "about schedules, meeting coordination, and basic office tasks. "
                "When you don't know something specific, you'll offer to take a message "
                "or suggest alternative ways to help. "
                "You should avoid making up specific company details that you don't know. Tech Solutions is a professional services company that helps businesses with their technology needs. "
                "Always maintain a professional demeanor while being personable."
                "You must ask one question at a time to make sure its more conversational."
                "Use Backchanneling response like 'umm' or 'hmm', 'I see', 'thats right', 'wow', 'thats crazy' etc to make it more conversational"
                "When you need to think or process information, use verbal cues like 'let me check', 'just a moment', 'I need to look that up', 'let me see if I can find that for you' etc to make it more conversational."
            )
        )
        self._meetings = []
        self._notes = {}
        
    async def on_enter(self):
        # When the agent is added to the session, generate an initial greeting
        self.session.generate_reply(instructions="Introduce yourself and ask how you can help.")
    
    @function_tool
    async def schedule_meeting(
        self, 
        context: RunContext,
        name: str, 
        date: str, 
        time: str, 
        topic: Optional[str] = None,
        participants: Optional[List[str]] = None
    ) -> str:
        """
        Schedule a meeting in the calendar.
        
        Args:
            name: The name of the person scheduling the meeting
            date: The date of the meeting in YYYY-MM-DD format
            time: The time of the meeting in HH:MM format
            topic: Optional topic for the meeting
            participants: Optional list of participant names
        """
        # Simulate scheduling process
        logger.info(f"Scheduling meeting for {name} on {date} at {time}")
        
        # Add meeting to internal tracking
        meeting_id = len(self._meetings) + 1
        meeting = {
            "id": meeting_id,
            "name": name,
            "date": date,
            "time": time,
            "topic": topic or "Unspecified",
            "participants": participants or []
        }
        self._meetings.append(meeting)
        
        # Simulate thinking time
        await asyncio.sleep(2)
        
        return (
            f"Meeting scheduled successfully. "
            f"Meeting ID: {meeting_id}, "
            f"Date: {date}, "
            f"Time: {time}, "
            f"Topic: {topic or 'Unspecified'}"
        )

    @function_tool
    async def check_availability(
        self, 
        context: RunContext,
        date: str, 
        time_range: str
    ) -> str:
        """
        Check availability for a specific date and time range.
        
        Args:
            date: The date to check in YYYY-MM-DD format
            time_range: The time range to check (e.g., "10:00-11:00")
        """
        logger.info(f"Checking availability for {date} at {time_range}")
        
        # Simulate database lookup
        await asyncio.sleep(2)
        
        # Simulate random availability
        # In a real implementation, this would check against an actual calendar
        is_available = not any(
            meeting["date"] == date and time_range in meeting["time"] 
            for meeting in self._meetings
        )
        
        if is_available:
            return f"The requested time slot ({date}, {time_range}) is available."
        else:
            return f"Sorry, the requested time slot ({date}, {time_range}) is already booked."

    @function_tool
    async def take_message(
        self, 
        context: RunContext,
        from_name: str, 
        to_name: str, 
        message: str, 
        urgency: Optional[str] = "normal"
    ) -> str:
        """
        Take a message for someone in the office.
        
        Args:
            from_name: The name of the person leaving the message
            to_name: The name of the person the message is for
            message: The content of the message
            urgency: The urgency level (low, normal, high)
        """
        logger.info(f"Taking message from {from_name} for {to_name}")
        
        # Store the message
        if to_name not in self._notes:
            self._notes[to_name] = []
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._notes[to_name].append({
            "from": from_name,
            "message": message,
            "urgency": urgency,
            "timestamp": timestamp
        })
        
        # Simulate processing time
        await asyncio.sleep(1.5)
        
        return (
            f"Message from {from_name} to {to_name} saved successfully. "
            f"Urgency: {urgency}. I'll make sure {to_name} receives your message."
        )

    @function_tool
    async def provide_company_info(
        self, 
        context: RunContext,
        topic: str
    ) -> str:
        """
        Provide general information about the company based on the requested topic.
        
        Args:
            topic: The topic to provide information about (e.g., "hours", "location", "website")
        """
        logger.info(f"Providing company info about: {topic}")
        
        # Simulate thinking/lookup
        await asyncio.sleep(3)
        
        # Basic company information
        company_info = {
            "hours": "Our office hours are Monday through Friday, 9:00 AM to 5:00 PM Eastern Time.",
            "location": "Our main office is located in the downtown business district. For specific address details, please visit our website.",
            "website": "You can find more information on our website at techsolutions.com",
            "contact": "You can reach our general office line at 555-TECH-SOL or email us at info@techsolutions.com."
        }
        
        # Default response for unknown topics
        default_response = "I don't have specific information about that topic. For more details, I'd recommend checking our website at techsolutions.com or contacting our main office."
        
        return company_info.get(topic.lower(), default_response)

    @function_tool
    async def find_person(
        self, 
        context: RunContext,
        name: str
    ) -> str:
        """
        Check if a person is available in the office.
        
        Args:
            name: The name of the person to find
        """
        logger.info(f"Checking if {name} is available")
        
        # Simulate database lookup
        await asyncio.sleep(2)
        
        # Simulate random availability
        import random
        statuses = [
            f"{name} is currently in a meeting and will be available in about an hour.",
            f"{name} is out of the office today. Would you like to leave a message?",
            f"{name} is currently available. Would you like me to transfer your call?",
            f"I don't see {name} in our directory. Could you provide their department or job title?"
        ]
        
        return random.choice(statuses)


def prewarm(proc):
    # Preload VAD model during worker startup
    proc.userdata["vad"] = silero.VAD.load()


async def send_transcription_data(room, text):
    """Send transcription data to the frontend"""
    try:
        data = json.dumps({
            "type": "transcription",
            "text": text,
            "timestamp": datetime.now().isoformat()
        }).encode('utf-8')

        logger.info(f"Sending transcription data: {text}")
        logger.info(f"Room: {room.name if hasattr(room, 'name') else 'unknown'}")
        logger.info(f"Local participant: {room.local_participant.identity if room.local_participant else 'none'}")

        await room.local_participant.publish_data(data)
        logger.info(f"Successfully sent transcription: {text}")
    except Exception as e:
        logger.error(f"Failed to send transcription data: {e}")
        logger.error(f"Room state: {getattr(room, 'connection_state', 'unknown')}")
        logger.error(f"Local participant exists: {room.local_participant is not None}")


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    # Create agent session with Google Gemini LLM and Deepgram STT/TTS
    session = AgentSession(
        vad=ctx.proc.userdata["vad"],
        llm=google.LLM(),  # Using Google Gemini (default model)
        stt=deepgram.STT(),  # Using Deepgram for speech-to-text
        tts=deepgram.TTS(),  # Using Deepgram for text-to-speech
    )

    # Add transcription listener for TTS synthesis
    def on_tts_text(text):
        if text:
            try:
                # Send the TTS text as transcription data
                import asyncio
                asyncio.create_task(send_transcription_data(session.room, text))
                logger.info(f"TTS text: {text}")
            except Exception as e:
                logger.error(f"Failed to send transcription data: {e}")

    # Hook into agent responses by overriding the generate_reply method
    original_generate_reply = session.generate_reply
    async def intercepted_generate_reply(*args, **kwargs):
        logger.info("🎯 generate_reply called with args:", args, "kwargs:", kwargs)

        # Call original method
        result = await original_generate_reply(*args, **kwargs)
        logger.info("🎯 generate_reply result:", result)
        logger.info("🎯 result type:", type(result))

        # Try to extract text from the result
        if result and hasattr(result, 'text') and result.text:
            logger.info("📝 Sending transcription from result.text:", result.text)
            await send_transcription_data(session.room, result.text)
        elif isinstance(result, str):
            logger.info("📝 Sending transcription from string result:", result)
            await send_transcription_data(session.room, result)
        elif hasattr(result, 'content') and result.content:
            logger.info("📝 Sending transcription from result.content:", result.content)
            await send_transcription_data(session.room, result.content)
        else:
            logger.warning("⚠️ No text found in result to send as transcription")

        print("🎯 result:", result)
        return result

    session.generate_reply = intercepted_generate_reply

    # Start the agent session
    await session.start(OfficeCallerAgent(), room=ctx.room)
    
    # Configure background audio for a realistic office environment
    try:
        background_audio = BackgroundAudioPlayer(
            # Play office ambience sound looping in the background
            ambient_sound=AudioConfig(BuiltinAudioClip.OFFICE_AMBIENCE, volume=0.3),  # Reduced volume
        )

        # Start background audio
        await background_audio.start(room=ctx.room, agent_session=session)
        logger.info("Background audio started successfully")
    except Exception as e:
        logger.warning(f"Failed to start background audio: {e}. Continuing without background audio.")


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))