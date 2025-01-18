import asyncio
import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv
from retell import AsyncRetell

# Load environment variables
load_dotenv()

# Valid language codes
class LanguageCodes:
    ENGLISH_US = "en-US"
    ENGLISH_UK = "en-GB"
    ENGLISH_INDIA = "en-IN"
    GERMAN = "de-DE"
    SPANISH = "es-ES"
    SPANISH_LATAM = "es-419"
    HINDI = "hi-IN"
    JAPANESE = "ja-JP"
    PORTUGUESE = "pt-PT"
    PORTUGUESE_BR = "pt-BR"
    FRENCH = "fr-FR"
    CHINESE = "zh-CN"
    RUSSIAN = "ru-RU"
    ITALIAN = "it-IT"
    KOREAN = "ko-KR"
    DUTCH = "nl-NL"
    POLISH = "pl-PL"
    ROMANIAN = "ro-RO"
    TURKISH = "tr-TR"
    VIETNAMESE = "vi-VN"
    MULTILINGUAL = "multi"

@dataclass
class VoiceAgentConfig:
    llm_id: str 
    llm_type: str
    voice_id: str
    language: str = LanguageCodes.ENGLISH_US  # Default to US English

class VoiceAgent:
    def __init__(self, api_key: str, config: VoiceAgentConfig):
        self.client = AsyncRetell(api_key=api_key)
        self.config = config
        self.agent_id: Optional[str] = None

    async def create_agent(self) -> str:
        """Create a new voice agent and return its ID."""
        response = await self.client.agent.create(
            response_engine={
                "llm_id": self.config.llm_id,
                "type": self.config.llm_type,
            },
            voice_id=self.config.voice_id,
            language=self.config.language,
        )
        self.agent_id = response.agent_id
        print(f"Agent created with ID: {self.agent_id}")
        return self.agent_id

    async def create_web_call(self) -> None:
        """Create a web call for the agent."""
        if not self.agent_id:
            raise ValueError("Agent ID is not set. Please create the agent first.")

        web_call_response = await self.client.call.create_web_call(
            agent_id=self.agent_id
        )
        print(f"Web call created with Agent ID: {web_call_response.agent_id}")

    async def cleanup(self) -> None:
        """Cleanup resources."""
        if self.agent_id:
            try:
                await self.client.agent.delete(self.agent_id)
                print("Agent deleted successfully")
            except Exception as e:
                print(f"Error deleting agent: {e}")
        await self.client.close()

# Configuration presets
class AgentPresets:
    GPT4_ADRIAN = VoiceAgentConfig(
        llm_id="llm_f1fbe2eefad955e589c03fa8040c",  # Updated to standard GPT-4 identifier
        llm_type="retell-llm",
        voice_id="11labs-Adrian",
        language=LanguageCodes.ENGLISH_US
    )

async def main():
    # Load API key from environment
    api_key = os.getenv("RETELL_API_KEY")
    if not api_key:
        raise ValueError("RETELL_API_KEY not found in environment variables")

    # Create agent with preset configuration
    agent = VoiceAgent(api_key, AgentPresets.GPT4_ADRIAN)
    await agent.create_agent()  # Create a voice agent
    await agent.create_web_call()
    # try:
    #       # Generate a web call for the agent
    # finally:
        # await agent.cleanup()  # Clean up resources

if __name__ == "__main__":
    asyncio.run(main())
