"""
Unit tests for progress indicator component (T085).

Tests agent status display, progress bar, time estimation, and workflow results.
"""

import pytest
from unittest.mock import Mock, patch, call
from datetime import datetime, timedelta
from typing import List, Dict, Any


class TestProgressIndicator:
    """Test suite for progress indicator component."""

    @pytest.fixture
    def sample_step_statuses(self) -> List[Dict[str, Any]]:
        """Create sample step statuses."""
        return [
            {
                "agent_role": "Backend Specialist",
                "status": "completed",
                "duration_seconds": 5.2
            },
            {
                "agent_role": "Frontend Specialist",
                "status": "in_progress",
                "duration_seconds": 0
            },
            {
                "agent_role": "Data Analyst",
                "status": "pending",
                "duration_seconds": 0
            },
            {
                "agent_role": "PRD Writer",
                "status": "pending",
                "duration_seconds": 0
            }
        ]

    @pytest.fixture
    def workflow_result_success(self) -> Dict[str, Any]:
        """Create successful workflow result."""
        return {
            "success": True,
            "prd_content": "# PRD\n\nTest content",
            "steps": [
                {
                    "agent_role": "Backend Specialist",
                    "status": "completed",
                    "start_time": "2024-01-01T00:00:00",
                    "end_time": "2024-01-01T00:00:05",
                    "duration_seconds": 5.0
                },
                {
                    "agent_role": "Frontend Specialist",
                    "status": "completed",
                    "start_time": "2024-01-01T00:00:05",
                    "end_time": "2024-01-01T00:00:12",
                    "duration_seconds": 7.0
                }
            ],
            "error": None
        }

    @pytest.fixture
    def workflow_result_failure(self) -> Dict[str, Any]:
        """Create failed workflow result."""
        return {
            "success": False,
            "prd_content": "",
            "steps": [
                {
                    "agent_role": "Backend Specialist",
                    "status": "completed",
                    "duration_seconds": 5.0
                },
                {
                    "agent_role": "Frontend Specialist",
                    "status": "failed",
                    "duration_seconds": 2.0
                },
                {
                    "agent_role": "Data Analyst",
                    "status": "pending",
                    "duration_seconds": 0
                }
            ],
            "error": "Frontend Specialist failed: Connection timeout"
        }

    @patch('streamlit.markdown')
    @patch('streamlit.progress')
    @patch('streamlit.info')
    @patch('streamlit.caption')
    def test_render_workflow_progress_basic(
        self,
        mock_caption,
        mock_info,
        mock_progress,
        mock_markdown
    ):
        """Test basic workflow progress rendering."""
        from codeindex.web.components.progress_indicator import render_workflow_progress
        from codeindex.web.agents.base import AgentRole

        render_workflow_progress(
            current_step=2,
            total_steps=4,
            current_agent=AgentRole.FRONTEND_SPECIALIST
        )

        # Verify progress bar called with 0.5 (2/4)
        mock_progress.assert_called_once_with(0.5)

        # Verify markdown header called
        assert mock_markdown.call_count >= 1
        header_call = [call for call in mock_markdown.call_args_list if "2/4" in str(call)]
        assert len(header_call) > 0

        # Verify agent info displayed
        mock_info.assert_called_once()
        info_text = str(mock_info.call_args)
        assert "Frontend Specialist" in info_text

    @patch('streamlit.markdown')
    @patch('streamlit.progress')
    def test_render_workflow_progress_no_agent(
        self,
        mock_progress,
        mock_markdown
    ):
        """Test workflow progress without current agent."""
        from codeindex.web.components.progress_indicator import render_workflow_progress

        render_workflow_progress(
            current_step=0,
            total_steps=4,
            current_agent=None
        )

        # Verify progress bar called with 0
        mock_progress.assert_called_once_with(0.0)

    @patch('streamlit.markdown')
    @patch('streamlit.progress')
    @patch('streamlit.caption')
    def test_render_workflow_progress_with_time_estimate(
        self,
        mock_caption,
        mock_progress,
        mock_markdown
    ):
        """Test workflow progress with time estimation."""
        from codeindex.web.components.progress_indicator import render_workflow_progress

        render_workflow_progress(
            current_step=1,
            total_steps=4,
            estimated_seconds_remaining=120
        )

        # Verify caption called with time estimate
        mock_caption.assert_called_once()
        caption_text = str(mock_caption.call_args)
        assert "2m" in caption_text or "120" in caption_text

    @patch('streamlit.markdown')
    @patch('streamlit.progress')
    @patch('streamlit.text')
    def test_render_workflow_progress_with_step_statuses(
        self,
        mock_text,
        mock_progress,
        mock_markdown,
        sample_step_statuses
    ):
        """Test workflow progress with step statuses."""
        from codeindex.web.components.progress_indicator import render_workflow_progress

        render_workflow_progress(
            current_step=2,
            total_steps=4,
            step_statuses=sample_step_statuses
        )

        # Verify step statuses displayed
        # Should have 4 text calls for 4 steps
        assert mock_text.call_count == 4

        # Verify status icons
        text_calls = [str(call) for call in mock_text.call_args_list]
        assert any("✅" in call for call in text_calls)  # Completed
        assert any("⏳" in call for call in text_calls)  # In progress
        assert any("⏸️" in call for call in text_calls)  # Pending

    @patch('streamlit.success')
    @patch('streamlit.caption')
    def test_render_workflow_status_badge_running(
        self,
        mock_caption,
        mock_success
    ):
        """Test workflow status badge for running workflow."""
        from codeindex.web.components.progress_indicator import render_workflow_status_badge

        start_time = datetime.now() - timedelta(seconds=30)

        render_workflow_status_badge("running", start_time=start_time)

        # Verify success badge shown
        mock_success.assert_called_once()
        success_text = str(mock_success.call_args)
        assert "Running" in success_text

        # Verify elapsed time caption
        mock_caption.assert_called_once()

    @patch('streamlit.success')
    def test_render_workflow_status_badge_completed(self, mock_success):
        """Test workflow status badge for completed workflow."""
        from codeindex.web.components.progress_indicator import render_workflow_status_badge

        render_workflow_status_badge("completed")

        # Verify success badge shown
        mock_success.assert_called_once()
        success_text = str(mock_success.call_args)
        assert "Completed" in success_text

    @patch('streamlit.error')
    def test_render_workflow_status_badge_failed(self, mock_error):
        """Test workflow status badge for failed workflow."""
        from codeindex.web.components.progress_indicator import render_workflow_status_badge

        render_workflow_status_badge("failed")

        # Verify error badge shown
        mock_error.assert_called_once()
        error_text = str(mock_error.call_args)
        assert "Failed" in error_text

    @patch('streamlit.warning')
    def test_render_workflow_status_badge_cancelled(self, mock_warning):
        """Test workflow status badge for cancelled workflow."""
        from codeindex.web.components.progress_indicator import render_workflow_status_badge

        render_workflow_status_badge("cancelled")

        # Verify warning badge shown
        mock_warning.assert_called_once()
        warning_text = str(mock_warning.call_args)
        assert "Cancelled" in warning_text

    @patch('streamlit.button')
    def test_render_workflow_cancellation_button_not_clicked(self, mock_button):
        """Test cancellation button when not clicked."""
        from codeindex.web.components.progress_indicator import render_workflow_cancellation_button

        mock_button.return_value = False
        callback = Mock()

        clicked = render_workflow_cancellation_button(callback)

        assert clicked == False
        callback.assert_not_called()

    @patch('streamlit.button')
    def test_render_workflow_cancellation_button_clicked(self, mock_button):
        """Test cancellation button when clicked."""
        from codeindex.web.components.progress_indicator import render_workflow_cancellation_button

        mock_button.return_value = True
        callback = Mock()

        clicked = render_workflow_cancellation_button(callback)

        assert clicked == True
        callback.assert_called_once()

    def test_format_duration_seconds(self):
        """Test duration formatting for seconds."""
        from codeindex.web.components.progress_indicator import _format_duration

        assert _format_duration(30) == "30s"
        assert _format_duration(45) == "45s"

    def test_format_duration_minutes(self):
        """Test duration formatting for minutes."""
        from codeindex.web.components.progress_indicator import _format_duration

        assert _format_duration(60) == "1m 0s"
        assert _format_duration(90) == "1m 30s"
        assert _format_duration(125) == "2m 5s"

    def test_format_duration_hours(self):
        """Test duration formatting for hours."""
        from codeindex.web.components.progress_indicator import _format_duration

        assert _format_duration(3600) == "1h 0m"
        assert _format_duration(3660) == "1h 1m"
        assert _format_duration(7200) == "2h 0m"

    def test_estimate_workflow_time_no_completed_steps(self):
        """Test time estimation with no completed steps."""
        from codeindex.web.components.progress_indicator import estimate_workflow_time_remaining

        estimated = estimate_workflow_time_remaining(
            completed_steps=0,
            total_steps=4,
            elapsed_seconds=0
        )

        # Default estimate: 30 seconds per step
        assert estimated == 120  # 4 * 30

    def test_estimate_workflow_time_with_completed_steps(self):
        """Test time estimation based on completed steps."""
        from codeindex.web.components.progress_indicator import estimate_workflow_time_remaining

        estimated = estimate_workflow_time_remaining(
            completed_steps=2,
            total_steps=4,
            elapsed_seconds=60
        )

        # Average time: 60 / 2 = 30 seconds per step
        # Remaining: 2 steps * 30 = 60 seconds
        assert estimated == 60

    def test_estimate_workflow_time_almost_complete(self):
        """Test time estimation when almost complete."""
        from codeindex.web.components.progress_indicator import estimate_workflow_time_remaining

        estimated = estimate_workflow_time_remaining(
            completed_steps=3,
            total_steps=4,
            elapsed_seconds=90
        )

        # Average time: 90 / 3 = 30 seconds per step
        # Remaining: 1 step * 30 = 30 seconds
        assert estimated == 30

    @patch('streamlit.success')
    @patch('streamlit.metric')
    def test_render_workflow_results_summary_success(
        self,
        mock_metric,
        mock_success,
        workflow_result_success
    ):
        """Test rendering successful workflow results."""
        from codeindex.web.components.progress_indicator import render_workflow_results_summary

        render_workflow_results_summary(workflow_result_success)

        # Verify success message
        mock_success.assert_called_once()
        success_text = str(mock_success.call_args)
        assert "Completed Successfully" in success_text

        # Verify duration metric
        mock_metric.assert_called_once()

    @patch('streamlit.error')
    @patch('streamlit.text')
    def test_render_workflow_results_summary_failure(
        self,
        mock_text,
        mock_error,
        workflow_result_failure
    ):
        """Test rendering failed workflow results."""
        from codeindex.web.components.progress_indicator import render_workflow_results_summary

        render_workflow_results_summary(workflow_result_failure)

        # Verify error message
        assert mock_error.call_count >= 1

        # Verify error details shown
        error_calls = [str(call) for call in mock_error.call_args_list]
        assert any("Failed" in call for call in error_calls)
        assert any("Connection timeout" in call for call in error_calls)

    @patch('streamlit.success')
    @patch('streamlit.expander')
    @patch('streamlit.markdown')
    @patch('streamlit.metric')
    def test_render_workflow_results_summary_with_details(
        self,
        mock_metric,
        mock_markdown,
        mock_expander,
        mock_success,
        workflow_result_success
    ):
        """Test rendering workflow results with detailed step information."""
        from codeindex.web.components.progress_indicator import render_workflow_results_summary

        # Mock expander context manager
        mock_expander.return_value.__enter__ = Mock()
        mock_expander.return_value.__exit__ = Mock()

        render_workflow_results_summary(workflow_result_success, show_details=True)

        # Verify expanders created for each step
        assert mock_expander.call_count == 2  # 2 steps

    def test_agent_emojis_mapping(self):
        """Test agent emoji mapping exists for all roles."""
        from codeindex.web.components.progress_indicator import AGENT_EMOJIS
        from codeindex.web.agents.base import AgentRole

        # Verify emojis exist for common agent roles
        assert AgentRole.BACKEND_SPECIALIST in AGENT_EMOJIS
        assert AgentRole.FRONTEND_SPECIALIST in AGENT_EMOJIS
        assert AgentRole.DATA_ANALYST in AGENT_EMOJIS
        assert AgentRole.PRD_WRITER in AGENT_EMOJIS

    @patch('streamlit.progress')
    def test_render_workflow_progress_handles_zero_steps(
        self,
        mock_progress
    ):
        """Test workflow progress handles edge case of zero total steps."""
        from codeindex.web.components.progress_indicator import render_workflow_progress

        render_workflow_progress(
            current_step=0,
            total_steps=0
        )

        # Should not crash, progress should be 0
        mock_progress.assert_called_once_with(0.0)

    def test_estimate_workflow_time_handles_edge_cases(self):
        """Test time estimation handles edge cases."""
        from codeindex.web.components.progress_indicator import estimate_workflow_time_remaining

        # All steps completed
        estimated = estimate_workflow_time_remaining(
            completed_steps=4,
            total_steps=4,
            elapsed_seconds=120
        )
        assert estimated == 0  # No steps remaining

        # Faster than expected
        estimated = estimate_workflow_time_remaining(
            completed_steps=2,
            total_steps=4,
            elapsed_seconds=10
        )
        # Average: 5 seconds per step, remaining: 2 * 5 = 10
        assert estimated == 10
