"""
Unit tests for TransactionInfo model (Feature 008 - T001).

Tests the fix for AttributeError: 'TransactionInfo' object has no attribute 'isolation'
Production error from services PRD generation on 2026-01-08.
"""

import pytest
from datetime import datetime
from codeindex.models.prd import TransactionInfo


class TestTransactionInfoIsolationProperty:
    """Test the isolation property alias for backward compatibility."""

    def test_isolation_property_exists(self):
        """
        Test that TransactionInfo has an 'isolation' property.

        This fixes the production error:
        AttributeError: 'TransactionInfo' object has no attribute 'isolation'
        at src/codeindex/cli/prd.py:1345
        """
        tx = TransactionInfo(
            method_name="saveUser",
            transaction_type="REQUIRED",
        )

        # Verify the property exists (doesn't raise AttributeError)
        assert hasattr(tx, 'isolation'), "TransactionInfo should have 'isolation' property"

    def test_isolation_returns_isolation_level(self):
        """
        Test that isolation property returns the value of isolation_level.

        The property is an alias for backward compatibility.
        """
        tx = TransactionInfo(
            method_name="saveUser",
            transaction_type="REQUIRED",
            isolation_level="READ_COMMITTED",
        )

        # isolation property should return isolation_level value
        assert tx.isolation == "READ_COMMITTED"
        assert tx.isolation == tx.isolation_level

    def test_isolation_returns_none_when_not_set(self):
        """
        Test that isolation property returns None when isolation_level is None.

        Production code checks: if tx.isolation: ...
        This should work when isolation_level is None.
        """
        tx = TransactionInfo(
            method_name="getUser",
            transaction_type="SUPPORTS",
            isolation_level=None,
        )

        assert tx.isolation is None
        assert tx.isolation_level is None

    def test_isolation_default_none(self):
        """
        Test that isolation_level defaults to None when not specified.

        This is important for optional transaction attributes.
        """
        tx = TransactionInfo(
            method_name="findAll",
            transaction_type="REQUIRED",
        )

        assert tx.isolation_level is None
        assert tx.isolation is None

    def test_isolation_all_valid_levels(self):
        """
        Test isolation property with all valid isolation levels.

        Valid isolation levels:
        - READ_UNCOMMITTED: Lowest isolation, allows dirty reads
        - READ_COMMITTED: Prevents dirty reads (default in most DBs)
        - REPEATABLE_READ: Prevents non-repeatable reads
        - SERIALIZABLE: Highest isolation, prevents phantom reads
        """
        valid_levels = [
            "READ_UNCOMMITTED",
            "READ_COMMITTED",
            "REPEATABLE_READ",
            "SERIALIZABLE",
        ]

        for level in valid_levels:
            tx = TransactionInfo(
                method_name=f"test_{level}",
                transaction_type="REQUIRED",
                isolation_level=level,
            )

            assert tx.isolation == level, f"isolation should return {level}"
            assert tx.isolation_level == level


class TestTransactionInfoModel:
    """Test TransactionInfo model creation and fields."""

    def test_create_minimal_transaction_info(self):
        """Test creating TransactionInfo with minimal required fields."""
        tx = TransactionInfo(
            method_name="saveOrder",
            transaction_type="REQUIRED",
        )

        assert tx.method_name == "saveOrder"
        assert tx.transaction_type == "REQUIRED"
        assert tx.propagation is None
        assert tx.isolation_level is None
        assert tx.read_only is None

    def test_create_full_transaction_info(self):
        """Test creating TransactionInfo with all fields specified."""
        tx = TransactionInfo(
            method_name="updateInventory",
            transaction_type="REQUIRES_NEW",
            propagation="REQUIRES_NEW",
            isolation_level="SERIALIZABLE",
            read_only=False,
        )

        assert tx.method_name == "updateInventory"
        assert tx.transaction_type == "REQUIRES_NEW"
        assert tx.propagation == "REQUIRES_NEW"
        assert tx.isolation_level == "SERIALIZABLE"
        assert tx.isolation == "SERIALIZABLE"  # Property should also work
        assert tx.read_only is False

    def test_create_read_only_transaction(self):
        """Test creating a read-only transaction (common for queries)."""
        tx = TransactionInfo(
            method_name="findUserById",
            transaction_type="SUPPORTS",
            read_only=True,
        )

        assert tx.method_name == "findUserById"
        assert tx.read_only is True
        assert tx.isolation is None

    def test_transaction_type_variations(self):
        """Test different transaction type values."""
        types = [
            "REQUIRED",
            "REQUIRES_NEW",
            "SUPPORTS",
            "NOT_SUPPORTED",
            "NEVER",
            "MANDATORY",
        ]

        for tx_type in types:
            tx = TransactionInfo(
                method_name=f"test_{tx_type}",
                transaction_type=tx_type,
            )
            assert tx.transaction_type == tx_type


class TestTransactionInfoSerialization:
    """Test TransactionInfo to_dict and from_dict methods."""

    def test_to_dict_all_fields(self):
        """Test serializing TransactionInfo to dictionary."""
        tx = TransactionInfo(
            method_name="processPayment",
            transaction_type="REQUIRES_NEW",
            propagation="REQUIRES_NEW",
            isolation_level="SERIALIZABLE",
            read_only=False,
        )

        tx_dict = tx.to_dict()

        assert tx_dict["method_name"] == "processPayment"
        assert tx_dict["transaction_type"] == "REQUIRES_NEW"
        assert tx_dict["propagation"] == "REQUIRES_NEW"
        assert tx_dict["isolation_level"] == "SERIALIZABLE"
        assert tx_dict["read_only"] is False

    def test_to_dict_minimal_fields(self):
        """Test serializing TransactionInfo with only required fields."""
        tx = TransactionInfo(
            method_name="listProducts",
            transaction_type="SUPPORTS",
        )

        tx_dict = tx.to_dict()

        assert tx_dict["method_name"] == "listProducts"
        assert tx_dict["transaction_type"] == "SUPPORTS"
        assert tx_dict["propagation"] is None
        assert tx_dict["isolation_level"] is None
        assert tx_dict["read_only"] is None

    def test_from_dict_all_fields(self):
        """Test deserializing TransactionInfo from dictionary."""
        data = {
            "method_name": "deleteOrder",
            "transaction_type": "REQUIRED",
            "propagation": "REQUIRED",
            "isolation_level": "READ_COMMITTED",
            "read_only": False,
        }

        tx = TransactionInfo.from_dict(data)

        assert tx.method_name == "deleteOrder"
        assert tx.transaction_type == "REQUIRED"
        assert tx.propagation == "REQUIRED"
        assert tx.isolation_level == "READ_COMMITTED"
        assert tx.isolation == "READ_COMMITTED"  # Property should work
        assert tx.read_only is False

    def test_from_dict_minimal_fields(self):
        """Test deserializing TransactionInfo with minimal fields."""
        data = {
            "method_name": "countUsers",
            "transaction_type": "SUPPORTS",
        }

        tx = TransactionInfo.from_dict(data)

        assert tx.method_name == "countUsers"
        assert tx.transaction_type == "SUPPORTS"
        assert tx.isolation is None

    def test_round_trip_serialization(self):
        """Test that to_dict -> from_dict preserves all data."""
        original = TransactionInfo(
            method_name="archiveData",
            transaction_type="REQUIRES_NEW",
            propagation="REQUIRES_NEW",
            isolation_level="REPEATABLE_READ",
            read_only=False,
        )

        # Serialize and deserialize
        data = original.to_dict()
        restored = TransactionInfo.from_dict(data)

        # Verify all fields match
        assert restored.method_name == original.method_name
        assert restored.transaction_type == original.transaction_type
        assert restored.propagation == original.propagation
        assert restored.isolation_level == original.isolation_level
        assert restored.isolation == original.isolation
        assert restored.read_only == original.read_only


class TestTransactionInfoProductionScenario:
    """Test the exact production error scenario from 2026-01-08."""

    def test_prd_generation_access_pattern(self):
        """
        Simulate the exact code pattern from prd.py:1345 that caused the error.

        Production code:
            for tx in service.transaction_boundaries:
                if tx.isolation:  # ← AttributeError here
                    props.append(f"isolation={tx.isolation}")
        """
        # Simulate transaction_boundaries list
        transaction_boundaries = [
            TransactionInfo(
                method_name="saveUser",
                transaction_type="REQUIRED",
                isolation_level="READ_COMMITTED",
            ),
            TransactionInfo(
                method_name="deleteUser",
                transaction_type="REQUIRES_NEW",
                isolation_level="SERIALIZABLE",
            ),
            TransactionInfo(
                method_name="findUser",
                transaction_type="SUPPORTS",
                # No isolation_level set
            ),
        ]

        # Simulate the production code pattern
        props_list = []
        for tx in transaction_boundaries:
            props = []

            # This should NOT raise AttributeError anymore
            if tx.isolation:
                props.append(f"isolation={tx.isolation}")

            if tx.propagation:
                props.append(f"propagation={tx.propagation}")

            if tx.read_only is not None:
                props.append(f"readOnly={tx.read_only}")

            props_list.append((tx.method_name, props))

        # Verify results
        assert len(props_list) == 3

        # First transaction has isolation
        assert props_list[0][0] == "saveUser"
        assert "isolation=READ_COMMITTED" in props_list[0][1]

        # Second transaction has isolation
        assert props_list[1][0] == "deleteUser"
        assert "isolation=SERIALIZABLE" in props_list[1][1]

        # Third transaction has no isolation (should not crash)
        assert props_list[2][0] == "findUser"
        assert len(props_list[2][1]) == 0  # No properties set

    def test_services_prd_failure_prevented(self):
        """
        Verify that the fix prevents the exact production failure.

        Before fix:
            AttributeError: 'TransactionInfo' object has no attribute 'isolation'
            at src/codeindex/cli/prd.py:1398

        After fix:
            No error, isolation property returns isolation_level value
        """
        # Create a transaction as would be done in production
        tx = TransactionInfo(
            method_name="processOrder",
            transaction_type="REQUIRED",
            isolation_level="READ_COMMITTED",
            propagation="REQUIRED",
            read_only=False,
        )

        # This exact code pattern should now work
        try:
            if tx.isolation:  # Should not raise AttributeError
                result = f"isolation={tx.isolation}"
                assert result == "isolation=READ_COMMITTED"
            success = True
        except AttributeError as e:
            success = False
            pytest.fail(f"AttributeError still occurs: {e}")

        assert success, "Production code pattern should work without AttributeError"


class TestTransactionInfoEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_string_isolation_level(self):
        """Test that empty string isolation_level is handled correctly."""
        tx = TransactionInfo(
            method_name="test",
            transaction_type="REQUIRED",
            isolation_level="",  # Empty string (edge case)
        )

        # Empty string is falsy in Python
        assert tx.isolation == ""
        assert not tx.isolation  # Falsy value

    def test_property_is_read_only(self):
        """
        Test that isolation property is read-only (can't be set directly).

        The isolation property is an alias, not a settable field.
        """
        tx = TransactionInfo(
            method_name="test",
            transaction_type="REQUIRED",
            isolation_level="READ_COMMITTED",
        )

        # Verify we can read it
        assert tx.isolation == "READ_COMMITTED"

        # Verify we can't set it directly (should raise AttributeError)
        with pytest.raises(AttributeError, match="(can't set attribute|has no setter)"):
            tx.isolation = "SERIALIZABLE"  # Should fail

        # Original field should still be settable
        tx.isolation_level = "SERIALIZABLE"
        assert tx.isolation == "SERIALIZABLE"  # Property reflects the change


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
