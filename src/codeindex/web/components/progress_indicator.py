"""
Progress indicator component for multi-agent workflows (T092).

This component displays real-time progress for long-running multi-agent workflows:
- Current agent and task
- Progress bar
- Estimated time remaining
- Task status per agent
"""

import streamlit as st
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

from codeindex.web.agents.base import AgentRole

logger = logging.getLogger(__name__)


AGENT_EMOJIS = {
    AgentRole.SENIOR_DEVELOPER: "👨‍💻",
    AgentRole.DATA_ANALYST: "📊",
    AgentRole.FRONTEND_SPECIALIST: "🎨",
    AgentRole.BACKEND_SPECIALIST: "⚙️",
    AgentRole.PRD_WRITER: "📝",
    AgentRole.SPECKIT_WRITER: "📋",
    AgentRole.GHERKIN_TEST_WRITER: "🧪",
    AgentRole.PLAYWRIGHT_TEST_WRITER: "🎭"
}


def render_workflow_progress(
    current_step: int,
    total_steps: int,
    current_agent: Optional[AgentRole] = None,
    estimated_seconds_remaining: Optional[int] = None,
    step_statuses: Optional[List[Dict[str, Any]]] = None
):
    """
    Render workflow progress indicator.

    Args:
        current_step: Current step number (0-indexed)
        total_steps: Total number of steps
        current_agent: Currently executing agent
        estimated_seconds_remaining: Estimated seconds until completion
        step_statuses: List of step status dictionaries
    """
    # Calculate progress
    progress = current_step / total_steps if total_steps > 0 else 0

    # Progress header
    st.markdown(f"### 🔄 Workflow Progress: {current_step}/{total_steps} steps")

    # Progress bar
    st.progress(progress)

    # Current agent
    if current_agent:
        emoji = AGENT_EMOJIS.get(current_agent, "🤖")
        st.info(f"{emoji} **Currently Running**: {current_agent.value}")

    # Estimated time remaining
    if estimated_seconds_remaining is not None:
        time_str = _format_duration(estimated_seconds_remaining)
        st.caption(f"⏱️ **Estimated time remaining**: {time_str}")

    # Step status list
    if step_statuses:
        st.markdown("---")
        st.markdown("**Step Status:**")

        for i, status in enumerate(step_statuses):
            agent_role = status.get("agent_role", "Unknown")
            step_status = status.get("status", "pending")
            duration = status.get("duration_seconds", 0)

            # Status icon
            if step_status == "completed":
                icon = "✅"
            elif step_status == "in_progress":
                icon = "⏳"
            elif step_status == "failed":
                icon = "❌"
            else:
                icon = "⏸️"

            # Duration
            duration_str = f" ({duration:.1f}s)" if duration > 0 else ""

            st.text(f"{icon} {i+1}. {agent_role}{duration_str}")

    st.markdown("---")


def render_workflow_status_badge(
    workflow_status: str,
    start_time: Optional[datetime] = None
):
    """
    Render compact workflow status badge.

    Args:
        workflow_status: Workflow status (running, completed, failed, cancelled)
        start_time: When workflow started
    """
    if workflow_status == "running":
        st.success("🔄 **Workflow Running**")

        if start_time:
            elapsed = datetime.now() - start_time
            elapsed_str = _format_duration(int(elapsed.total_seconds()))
            st.caption(f"Running for: {elapsed_str}")

    elif workflow_status == "completed":
        st.success("✅ **Workflow Completed**")

    elif workflow_status == "failed":
        st.error("❌ **Workflow Failed**")

    elif workflow_status == "cancelled":
        st.warning("⚠️ **Workflow Cancelled**")

    else:
        st.info("⏸️ **Workflow Pending**")


def render_workflow_cancellation_button(
    on_cancel: callable,
    key: str = "cancel_workflow"
) -> bool:
    """
    Render workflow cancellation button.

    Args:
        on_cancel: Callback function to execute on cancellation
        key: Streamlit key for button

    Returns:
        True if button was clicked
    """
    if st.button("🛑 Cancel Workflow", key=key, use_container_width=True):
        if on_cancel:
            on_cancel()
        return True

    return False


def _format_duration(seconds: int) -> str:
    """
    Format duration in human-readable format.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds}s"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        return f"{hours}h {remaining_minutes}m"


def estimate_workflow_time_remaining(
    completed_steps: int,
    total_steps: int,
    elapsed_seconds: int
) -> int:
    """
    Estimate remaining workflow time based on completed steps.

    Args:
        completed_steps: Number of completed steps
        total_steps: Total number of steps
        elapsed_seconds: Elapsed time in seconds

    Returns:
        Estimated seconds remaining
    """
    if completed_steps == 0:
        # No data yet, return default estimate
        return total_steps * 30  # Assume 30 seconds per step

    # Calculate average time per step
    avg_time_per_step = elapsed_seconds / completed_steps

    # Estimate remaining time
    remaining_steps = total_steps - completed_steps
    estimated_remaining = int(remaining_steps * avg_time_per_step)

    return estimated_remaining


def render_workflow_results_summary(
    workflow_result: Dict[str, Any],
    show_details: bool = False
):
    """
    Render workflow results summary.

    Args:
        workflow_result: Workflow result dictionary
        show_details: Whether to show detailed step information
    """
    success = workflow_result.get("success", False)
    error = workflow_result.get("error")
    steps = workflow_result.get("steps", [])

    if success:
        st.success("✅ **Workflow Completed Successfully**")

        # Summary statistics
        total_duration = sum(s.get("duration_seconds", 0) for s in steps)
        st.metric("Total Duration", f"{total_duration:.1f}s")

        if show_details:
            st.markdown("**Step Details:**")

            for step in steps:
                agent_role = step.get("agent_role", "Unknown")
                status = step.get("status", "unknown")
                duration = step.get("duration_seconds", 0)

                with st.expander(f"{agent_role} ({status})"):
                    st.text(f"Status: {status}")
                    st.text(f"Duration: {duration:.1f}s")

                    if step.get("start_time"):
                        st.text(f"Started: {step['start_time']}")
                    if step.get("end_time"):
                        st.text(f"Ended: {step['end_time']}")

    else:
        st.error("❌ **Workflow Failed**")

        if error:
            st.error(f"Error: {error}")

        # Show which step failed
        failed_steps = [s for s in steps if s.get("status") == "failed"]

        if failed_steps:
            st.markdown("**Failed Steps:**")

            for step in failed_steps:
                agent_role = step.get("agent_role", "Unknown")
                st.text(f"• {agent_role}")


__all__ = [
    "render_workflow_progress",
    "render_workflow_status_badge",
    "render_workflow_cancellation_button",
    "render_workflow_results_summary",
    "estimate_workflow_time_remaining"
]
