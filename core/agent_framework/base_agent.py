"""Base agent class that all persona agents inherit from."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

from pydantic import BaseModel, Field


logger = logging.getLogger(__name__)


class AgentState(str, Enum):
    """Agent operational states."""
    IDLE = "idle"
    ACTIVE = "active"
    PAUSED = "paused"
    ERROR = "error"
    STOPPED = "stopped"


class AgentMode(str, Enum):
    """Agent operational modes."""
    SHADOW = "shadow"        # Observe only, no actions
    COPILOT = "copilot"      # Suggest, human approves
    AUTOPILOT = "autopilot"  # Act autonomously within bounds


class AgentConfig(BaseModel):
    """Configuration for an agent instance."""
    agent_id: str
    agent_name: str
    agent_type: str
    model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 4096
    temperature: float = 0.7
    mode: AgentMode = AgentMode.COPILOT
    require_approval: bool = True
    daily_budget_usd: float = 10.0


class AgentMetrics(BaseModel):
    """Metrics for tracking agent performance."""
    total_actions: int = 0
    successful_actions: int = 0
    failed_actions: int = 0
    api_calls: int = 0
    tokens_used: int = 0
    cost_usd: float = 0.0
    uptime_seconds: float = 0.0
    last_active: Optional[datetime] = None


class BaseAgent(ABC):
    """
    Base class for all AI agents in the collective.

    All persona agents (JordanTheJet, PixelPhantom, LuxeAI) inherit from this.
    Provides core functionality for state management, memory, and actions.
    """

    def __init__(self, config: AgentConfig):
        """Initialize the agent with configuration."""
        self.config = config
        self.state = AgentState.IDLE
        self.metrics = AgentMetrics()
        self.start_time = datetime.now()

        logger.info(f"Initialized agent: {self.config.agent_name}")

    @abstractmethod
    async def initialize(self) -> None:
        """
        Initialize agent-specific resources.

        Must be implemented by each persona agent.
        Called once when agent is first started.
        """
        pass

    @abstractmethod
    async def perceive(self) -> Dict[str, Any]:
        """
        Gather context and information from the environment.

        Returns:
            Dictionary containing current context and observations
        """
        pass

    @abstractmethod
    async def reason(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process context and determine next actions.

        Args:
            context: Current context from perceive()

        Returns:
            Dictionary containing decisions and planned actions
        """
        pass

    @abstractmethod
    async def act(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the decided action.

        Args:
            decision: Decision from reason()

        Returns:
            Result of the action
        """
        pass

    @abstractmethod
    async def reflect(self, result: Dict[str, Any]) -> None:
        """
        Learn from the outcome of an action.

        Args:
            result: Result from act()
        """
        pass

    async def run_cycle(self) -> None:
        """
        Execute one complete agent decision cycle.

        This is the main loop: perceive -> reason -> act -> reflect
        """
        try:
            self.state = AgentState.ACTIVE

            # Perceive: Gather context
            context = await self.perceive()
            logger.debug(f"{self.config.agent_name}: Perceived context")

            # Reason: Decide what to do
            decision = await self.reason(context)
            logger.debug(f"{self.config.agent_name}: Made decision")

            # Check if approval needed
            if self.config.require_approval and self.config.mode == AgentMode.COPILOT:
                approved = await self.request_approval(decision)
                if not approved:
                    logger.info(f"{self.config.agent_name}: Action not approved")
                    return

            # Act: Execute decision
            result = await self.act(decision)
            logger.debug(f"{self.config.agent_name}: Executed action")

            # Reflect: Learn from result
            await self.reflect(result)
            logger.debug(f"{self.config.agent_name}: Reflected on outcome")

            # Update metrics
            self.metrics.successful_actions += 1
            self.metrics.last_active = datetime.now()

            self.state = AgentState.IDLE

        except Exception as e:
            logger.error(f"{self.config.agent_name}: Error in cycle: {e}")
            self.state = AgentState.ERROR
            self.metrics.failed_actions += 1
            raise

    async def request_approval(self, decision: Dict[str, Any]) -> bool:
        """
        Request human approval for an action.

        Args:
            decision: The decision requiring approval

        Returns:
            True if approved, False otherwise
        """
        # TODO: Implement approval mechanism (webhook, UI, etc.)
        logger.info(f"{self.config.agent_name}: Approval requested for: {decision}")
        return True  # Default to approved for now

    async def start(self) -> None:
        """Start the agent."""
        logger.info(f"Starting agent: {self.config.agent_name}")
        await self.initialize()
        self.state = AgentState.IDLE

    async def stop(self) -> None:
        """Stop the agent."""
        logger.info(f"Stopping agent: {self.config.agent_name}")
        self.state = AgentState.STOPPED

    async def pause(self) -> None:
        """Pause the agent."""
        logger.info(f"Pausing agent: {self.config.agent_name}")
        self.state = AgentState.PAUSED

    async def resume(self) -> None:
        """Resume the agent."""
        logger.info(f"Resuming agent: {self.config.agent_name}")
        self.state = AgentState.IDLE

    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "agent_id": self.config.agent_id,
            "agent_name": self.config.agent_name,
            "state": self.state.value,
            "mode": self.config.mode.value,
            "metrics": self.metrics.model_dump(),
            "uptime": (datetime.now() - self.start_time).total_seconds()
        }
