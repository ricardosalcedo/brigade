"""Unit tests for core configuration"""

import os

import pytest

from core.config import Config


class TestConfig:

    def test_default_config(self):
        """Test default configuration values"""
        config = Config()
        assert config.aws_region == "us-west-2"
        assert config.quality_threshold == 6
        assert config.max_issues_to_fix == 10
        assert ".py" in config.supported_extensions

    def test_from_env(self):
        """Test configuration from environment variables"""
        os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
        os.environ["QUALITY_THRESHOLD"] = "8"

        config = Config.from_env()
        assert config.aws_region == "us-east-1"
        assert config.quality_threshold == 8

        # Cleanup
        del os.environ["AWS_DEFAULT_REGION"]
        del os.environ["QUALITY_THRESHOLD"]

    def test_from_dict(self):
        """Test configuration from dictionary"""
        config_dict = {
            "aws_region": "eu-west-1",
            "quality_threshold": 7,
            "max_issues_to_fix": 5,
        }

        config = Config.from_dict(config_dict)
        assert config.aws_region == "eu-west-1"
        assert config.quality_threshold == 7
        assert config.max_issues_to_fix == 5

    def test_to_dict(self):
        """Test configuration to dictionary conversion"""
        config = Config()
        config_dict = config.to_dict()

        assert isinstance(config_dict, dict)
        assert "aws_region" in config_dict
        assert "quality_threshold" in config_dict
        assert config_dict["aws_region"] == config.aws_region
