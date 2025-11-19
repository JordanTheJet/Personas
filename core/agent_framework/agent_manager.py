"""Manager for coordinating multiple agents."""

import logging
from typing import Dict, List, Optional
from datetime import datetime

from .base_agent import BaseAgent, AgentState


logger = logging.getLogger(__name__)


class AgentManager:
    """
    Manages multiple agents in the collective.

    Handles agent lifecycle, coordination, and resource allocation.
    """

    def __init__(self):
        """Initialize the agent manager."""
        self.agents: Dict[str, BaseAgent] = {}
        self.start_time = datetime.now()
        logger.info("AgentManager initialized")

    def register_agent(self, agent: BaseAgent) -> None:
        """
        Register an agent with the manager.

        Args:
            agent: The agent to register
        """
        agent_id = agent.config.agent_id
        if agent_id in self.agents:
            logger.warning(f"Agent {agent_id} already registered, replacing")

        self.agents[agent_id] = agent
        logger.info(f"Registered agent: {agent.config.agent_name} ({agent_id})")

    def unregister_agent(self, agent_id: str) -> None:
        """
        Unregister an agent.

        Args:
            agent_id: ID of the agent to unregister
        """
        if agent_id in self.agents:
            del self.agents[agent_id]
            logger.info(f"Unregistered agent: {agent_id}")
        else:
            logger.warning(f"Agent {agent_id} not found")

    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """
        Get an agent by ID.

        Args:
            agent_id: ID of the agent

        Returns:
            The agent if found, None otherwise
        """
        return self.agents.get(agent_id)

    def list_agents(self) -> List[Dict]:
        """
        List all registered agents.

        Returns:
            List of agent status dictionaries
        """
        return [agent.get_status() for agent in self.agents.values()]

    async def start_agent(self, agent_id: str) -> None:
        """
        Start an agent.

        Args:
            agent_id: ID of the agent to start
        """
        agent = self.get_agent(agent_id)
        if agent:
            await agent.start()
        else:
            logger.error(f"Agent {agent_id} not found")

    async def stop_agent(self, agent_id: str) -> None:
        """
        Stop an agent.

        Args:
            agent_id: ID of the agent to stop
        """
        agent = self.get_agent(agent_id)
        if agent:
            await agent.stop()
        else:
            logger.error(f"Agent {agent_id} not found")

    async def start_all(self) -> None:
        """Start all registered agents."""
        logger.info("Starting all agents")
        for agent in self.agents.values():
            await agent.start()

    async def stop_all(self) -> None:
        """Stop all registered agents."""
        logger.info("Stopping all agents")
        for agent in self.agents.values():
            await agent.stop()

    def get_collective_status(self) -> Dict:
        """
        Get status of the entire collective.

        Returns:
            Dictionary with collective-wide metrics and status
        """
        total_agents = len(self.agents)
        active_agents = sum(1 for a in self.agents.values() if a.state == AgentState.ACTIVE)
        idle_agents = sum(1 for a in self.agents.values() if a.state == AgentState.IDLE)

        total_actions = sum(a.metrics.total_actions for a in self.agents.values())
        total_cost = sum(a.metrics.cost_usd for a in self.agents.values())

        return {
            "total_agents": total_agents,
            "active_agents": active_agents,
            "idle_agents": idle_agents,
            "total_actions": total_actions,
            "total_cost_usd": total_cost,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "agents": self.list_agents()
        }


# Global agent manager instance
agent_manager = AgentManager()
