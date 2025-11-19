"""
Main entry point for the AI Agent Collective.

This script initializes and runs the agent collective.
"""

import asyncio
import logging
from pathlib import Path

from core.config import settings
from core.agent_framework import AgentManager, agent_manager


# Set up logging
def setup_logging():
    """Configure logging for the application."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(settings.log_file),
            logging.StreamHandler()
        ]
    )


logger = logging.getLogger(__name__)


async def main():
    """Main application entry point."""
    setup_logging()

    logger.info("=" * 60)
    logger.info("AI Agent Collective - Starting Up")
    logger.info("=" * 60)
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Default Model: {settings.default_model}")
    logger.info(f"Content Moderation: {'Enabled' if settings.enable_content_moderation else 'Disabled'}")
    logger.info(f"Human Approval Required: {'Yes' if settings.require_human_approval else 'No'}")
    logger.info("=" * 60)

    # TODO: Initialize agents
    # from agents.jordanthejet import JordanTheJetAgent
    # from agents.pixelphantom import PixelPhantomAgent
    # from agents.luxeai import LuxeAIAgent

    # jordan = JordanTheJetAgent(...)
    # pixel = PixelPhantomAgent(...)
    # luxe = LuxeAIAgent(...)

    # agent_manager.register_agent(jordan)
    # agent_manager.register_agent(pixel)
    # agent_manager.register_agent(luxe)

    # Start all agents
    # await agent_manager.start_all()

    logger.info("No agents configured yet. See docs/roadmap.md to begin development.")
    logger.info("Next steps:")
    logger.info("1. Review docs/SETUP.md for environment setup")
    logger.info("2. Follow docs/roadmap.md Phase 1 to build JordanTheJet augmentation")
    logger.info("3. Implement first agent in agents/jordanthejet/")

    # Keep running
    # try:
    #     while True:
    #         status = agent_manager.get_collective_status()
    #         logger.info(f"Collective Status: {status}")
    #         await asyncio.sleep(60)
    # except KeyboardInterrupt:
    #     logger.info("Shutting down...")
    #     await agent_manager.stop_all()


if __name__ == "__main__":
    asyncio.run(main())
