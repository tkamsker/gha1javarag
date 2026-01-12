"""
Integration tests for Feature 008 production error fixes.

Tests the three critical fixes:
- T001: TransactionInfo.isolation property
- T002: Adaptive timeout calculation
- T003: XML parser null safety

These tests verify the fixes work in realistic scenarios.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from tempfile import TemporaryDirectory

from codeindex.models.prd import TransactionInfo
from codeindex.parsers.xml_parser import XMLParser
from codeindex.services.ollama_client import OllamaClient
from codeindex.utils.timeout_calculator import TimeoutCalculator


@pytest.mark.integration
class TestTransactionInfoIntegration:
    """Integration tests for TransactionInfo.isolation fix (T001).

    Production issue: AttributeError when PRD generation accessed tx.isolation
    Fix: Added @property isolation() that returns isolation_level
    """

    def test_prd_generation_with_transaction_info(self):
        """Test PRD generation code pattern with TransactionInfo."""
        # Create transaction as done in production PRD generation
        tx = TransactionInfo(
            method_name='saveUser',
            transaction_type='REQUIRED',
            isolation_level='READ_COMMITTED',
            propagation='REQUIRED',
            read_only=False
        )

        # Simulate PRD generation code from prd.py:1345
        props = []

        # This exact pattern caused production failure before fix
        if tx.propagation:
            props.append(f'propagation={tx.propagation}')

        # ✅ This should work with the isolation property
        if tx.isolation:
            props.append(f'isolation={tx.isolation}')

        if tx.read_only is not None:
            props.append(f'readOnly={tx.read_only}')

        # Verify properties were extracted correctly
        assert len(props) == 3
        assert 'propagation=REQUIRED' in props
        assert 'isolation=READ_COMMITTED' in props
        assert 'readOnly=False' in props

    def test_prd_generation_with_multiple_transactions(self):
        """Test PRD generation with list of transactions (production pattern)."""
        # Simulate transaction_boundaries list from production
        transaction_boundaries = [
            TransactionInfo(
                method_name='saveOrder',
                transaction_type='REQUIRED',
                isolation_level='SERIALIZABLE',
                propagation='REQUIRED',
            ),
            TransactionInfo(
                method_name='findOrders',
                transaction_type='SUPPORTS',
                read_only=True,
            ),
            TransactionInfo(
                method_name='deleteOrder',
                transaction_type='REQUIRES_NEW',
                isolation_level='READ_COMMITTED',
            ),
        ]

        # Process all transactions (production pattern)
        all_props = []
        for tx in transaction_boundaries:
            props = []

            if tx.propagation:
                props.append(f'propagation={tx.propagation}')

            # Should not raise AttributeError
            if tx.isolation:
                props.append(f'isolation={tx.isolation}')

            if tx.read_only is not None:
                props.append(f'readOnly={tx.read_only}')

            all_props.append((tx.method_name, props))

        # Verify all transactions processed
        assert len(all_props) == 3

        # First transaction has isolation and propagation
        assert all_props[0][0] == 'saveOrder'
        assert 'isolation=SERIALIZABLE' in all_props[0][1]
        assert 'propagation=REQUIRED' in all_props[0][1]

        # Second transaction has only read_only
        assert all_props[1][0] == 'findOrders'
        assert 'readOnly=True' in all_props[1][1]

        # Third transaction has isolation
        assert all_props[2][0] == 'deleteOrder'
        assert 'isolation=READ_COMMITTED' in all_props[2][1]

    def test_transaction_info_serialization_roundtrip(self):
        """Test that isolation property works with serialization."""
        # Create transaction with isolation_level
        original = TransactionInfo(
            method_name='processPayment',
            transaction_type='REQUIRES_NEW',
            isolation_level='REPEATABLE_READ',
            propagation='REQUIRES_NEW',
            read_only=False,
        )

        # Serialize to dict
        data = original.to_dict()

        # Verify isolation_level in serialized data (not isolation)
        assert 'isolation_level' in data
        assert data['isolation_level'] == 'REPEATABLE_READ'

        # Deserialize from dict
        restored = TransactionInfo.from_dict(data)

        # Verify isolation property works on restored object
        assert restored.isolation == 'REPEATABLE_READ'
        assert restored.isolation_level == 'REPEATABLE_READ'


@pytest.mark.integration
class TestAdaptiveTimeoutIntegration:
    """Integration tests for adaptive timeout calculation (T002).

    Production issue: 11.5% timeout rate with fixed 240s timeout
    Fix: Dynamic timeouts based on file size
    """

    def test_ollama_client_uses_adaptive_timeout(self):
        """Test that OllamaClient uses TimeoutCalculator for adaptive timeouts."""
        # Create OllamaClient
        client = OllamaClient(read_timeout=240)

        # Verify TimeoutCalculator is initialized
        assert hasattr(client, 'timeout_calculator')
        assert isinstance(client.timeout_calculator, TimeoutCalculator)

        # Verify timeout calculator configuration
        config = client.timeout_calculator.get_config()
        assert config['base'] == 240
        assert config['scale'] == 10
        assert config['min_timeout'] == 60
        assert config['max_timeout'] == 600

    def test_timeout_calculation_for_small_file(self):
        """Test timeout for small file (should be fast)."""
        client = OllamaClient(read_timeout=240)

        # Small file (100 lines) should get minimal extra time
        timeout = client._calculate_timeout(100)

        # Expected: 240 + (100/100)*10 = 250s
        assert timeout == 250.0
        assert timeout < 300  # Keep it fast for small files

    def test_timeout_calculation_for_large_file(self):
        """Test timeout for large file (production scenario)."""
        client = OllamaClient(read_timeout=240)

        # Large file (3000 lines) - like SolrPartyRepository.java
        timeout = client._calculate_timeout(3000)

        # Expected: 240 + (3000/100)*10 = 540s
        assert timeout == 540.0
        assert timeout > 240  # More than old fixed timeout
        assert timeout < 600  # But capped at max_timeout

    def test_timeout_calculation_for_very_large_file(self):
        """Test timeout for very large file (capped at max)."""
        client = OllamaClient(read_timeout=240)

        # Very large file (10000 lines)
        timeout = client._calculate_timeout(10000)

        # Should be capped at max_timeout (600s)
        assert timeout == 600.0

    def test_concurrent_worker_limit_reduced(self):
        """Test that MAX_CONCURRENT_AI_CALLS is reduced to 5 (from 10)."""
        from codeindex.services.ollama_client import MAX_CONCURRENT_AI_CALLS

        # Verify reduced parallelism
        assert MAX_CONCURRENT_AI_CALLS == 5, \
            "MAX_CONCURRENT_AI_CALLS should be 5 to prevent Ollama overload"

    def test_adaptive_timeout_production_scenarios(self):
        """Test timeout calculation matches production requirements."""
        calc = TimeoutCalculator(base=240, scale=10, max_timeout=600)

        # Scenario 1: Small service (~200 lines) - should stay fast
        small_timeout = calc.calculate_for_lines(200)
        assert small_timeout == 260  # 240 + 20
        assert small_timeout < 300

        # Scenario 2: Medium service (~1000 lines)
        medium_timeout = calc.calculate_for_lines(1000)
        assert medium_timeout == 340  # 240 + 100

        # Scenario 3: Large service (~3000 lines) - production timeout case
        large_timeout = calc.calculate_for_lines(3000)
        assert large_timeout == 540  # 240 + 300
        assert large_timeout > 240  # More than old fixed timeout

        # Scenario 4: Very large file - should cap at 600s
        huge_timeout = calc.calculate_for_lines(10000)
        assert huge_timeout == 600  # Capped at max


@pytest.mark.integration
class TestXMLParserNullSafetyIntegration:
    """Integration tests for XML parser null safety (T003).

    Production issue: AttributeError on malformed ProductPortletView.ui.xml
    Fix: Added null check before accessing root.tag
    """

    def test_parse_malformed_gwt_uibinder(self, tmp_path):
        """Test parsing malformed GWT UiBinder (production scenario)."""
        # Create malformed UiBinder file (like ProductPortletView.ui.xml)
        malformed_file = tmp_path / "MalformedView.ui.xml"
        malformed_file.write_text("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ui:UiBinder SYSTEM "http://example.com/UiBinder.dtd">
<!-- Malformed: missing actual root element -->
""")

        parser = XMLParser()

        # Should not raise AttributeError
        try:
            result = parser.parse_file(malformed_file)

            # If parsing succeeds with recover=True, should return dict
            assert isinstance(result, dict)

            # May have empty root_element due to malformed XML
            assert 'root_element' in result
            assert 'root_attributes' in result
            assert 'namespaces' in result
            assert 'elements' in result

        except Exception as e:
            # XMLSyntaxError is acceptable
            from lxml import etree
            assert isinstance(e, etree.XMLSyntaxError), \
                f"Should raise XMLSyntaxError, not {type(e).__name__}: {e}"

    def test_parse_empty_xml_file(self, tmp_path):
        """Test parsing XML file with only declaration."""
        empty_file = tmp_path / "empty.xml"
        empty_file.write_text("<?xml version='1.0' encoding='UTF-8'?>")

        parser = XMLParser()

        # Should not raise AttributeError about NoneType
        try:
            result = parser.parse_file(empty_file)
            assert isinstance(result, dict)
        except Exception as e:
            from lxml import etree
            # XMLSyntaxError is acceptable, AttributeError is not
            assert not isinstance(e, AttributeError), \
                f"AttributeError should not occur: {e}"

    def test_parse_multiple_malformed_files(self, tmp_path):
        """Test parsing multiple malformed files (pipeline resilience)."""
        # Create multiple malformed files
        files = []
        for i in range(5):
            malformed = tmp_path / f"malformed_{i}.xml"
            malformed.write_text(f"<?xml version='1.0'?>\n<!-- File {i} -->")
            files.append(malformed)

        parser = XMLParser()
        results = []
        errors = []

        # Parse all files (simulating extraction pipeline)
        for file in files:
            try:
                result = parser.parse_file(file)
                results.append(result)
            except Exception as e:
                from lxml import etree
                # Should only be XMLSyntaxError, not AttributeError
                if isinstance(e, AttributeError):
                    errors.append((file, e))
                elif isinstance(e, etree.XMLSyntaxError):
                    # Expected error - malformed XML
                    results.append({'root_element': None, 'error': str(e)})

        # Verify no AttributeErrors occurred
        assert len(errors) == 0, \
            f"AttributeError occurred on files: {errors}"

    def test_xml_parser_with_valid_and_invalid_mix(self, tmp_path):
        """Test parser handles mix of valid and invalid XML files."""
        # Create valid XML
        valid_file = tmp_path / "valid.xml"
        valid_file.write_text("""<?xml version="1.0"?>
<root>
    <element>value</element>
</root>
""")

        # Create malformed XML
        malformed_file = tmp_path / "malformed.xml"
        malformed_file.write_text("<?xml version='1.0'?>")

        parser = XMLParser()

        # Parse valid file - should work
        valid_result = parser.parse_file(valid_file)
        assert valid_result['root_element'] == 'root'

        # Parse malformed file - should not crash
        try:
            malformed_result = parser.parse_file(malformed_file)
            # If it succeeds, should return dict
            assert isinstance(malformed_result, dict)
        except Exception as e:
            from lxml import etree
            # Only XMLSyntaxError is acceptable
            assert isinstance(e, etree.XMLSyntaxError)
            assert not isinstance(e, AttributeError)


@pytest.mark.integration
class TestProductionErrorFixesEndToEnd:
    """End-to-end integration tests for all three fixes together.

    Verifies that T001, T002, T003 work together in production scenarios.
    """

    def test_full_prd_generation_workflow(self, tmp_path):
        """Test full PRD generation workflow with all fixes."""
        # T001: Create transaction info with isolation
        transactions = [
            TransactionInfo(
                method_name='saveData',
                transaction_type='REQUIRED',
                isolation_level='READ_COMMITTED',
                propagation='REQUIRED',
            )
        ]

        # T002: Calculate timeout for service file
        calc = TimeoutCalculator(base=240, scale=10)
        timeout = calc.calculate_for_lines(500)
        assert timeout > 240  # Adaptive timeout applied

        # T003: Parse XML configuration
        config_file = tmp_path / "spring-config.xml"
        config_file.write_text("""<?xml version="1.0"?>
<beans xmlns="http://www.springframework.org/schema/beans">
    <bean id="dataSource" class="org.apache.commons.dbcp.BasicDataSource"/>
</beans>
""")

        parser = XMLParser()
        config_result = parser.parse_file(config_file)
        assert config_result['root_element'] == 'beans'

        # All three fixes working together
        # T001: Access transaction.isolation (no AttributeError)
        for tx in transactions:
            if tx.isolation:
                assert tx.isolation == 'READ_COMMITTED'

        # T002: Adaptive timeout calculated
        assert timeout == 290  # 240 + (500/100)*10

        # T003: XML parsed successfully
        assert len(config_result['elements']) > 0

    def test_extraction_pipeline_resilience(self, tmp_path):
        """Test extraction pipeline handles all error scenarios."""
        # Create test files
        files_to_process = []

        # 1. Java file with transactions
        java_file = tmp_path / "UserService.java"
        java_file.write_text("""
public class UserService {
    @Transactional(propagation = Propagation.REQUIRED,
                   isolation = Isolation.READ_COMMITTED)
    public void saveUser(User user) {
        // code
    }
}
""")
        files_to_process.append(('java', java_file))

        # 2. Large Java file (needs adaptive timeout)
        large_file = tmp_path / "LargeService.java"
        large_content = "public class LargeService {\n"
        large_content += "\n".join([f"    // Line {i}" for i in range(3000)])
        large_content += "\n}"
        large_file.write_text(large_content)
        files_to_process.append(('java', large_file))

        # 3. Valid XML config
        valid_xml = tmp_path / "valid-config.xml"
        valid_xml.write_text("""<?xml version="1.0"?>
<beans>
    <bean id="test" class="Test"/>
</beans>
""")
        files_to_process.append(('xml', valid_xml))

        # 4. Malformed XML (should not crash pipeline)
        malformed_xml = tmp_path / "malformed.xml"
        malformed_xml.write_text("<?xml version='1.0'?>")
        files_to_process.append(('xml', malformed_xml))

        # Process all files (simulating extraction)
        parser = XMLParser()
        calc = TimeoutCalculator()

        processed = 0
        errors = []

        for file_type, file_path in files_to_process:
            try:
                if file_type == 'xml':
                    # T003: Parse XML with null safety
                    result = parser.parse_file(file_path)
                    assert isinstance(result, dict)
                    processed += 1
                elif file_type == 'java':
                    # T002: Calculate adaptive timeout
                    lines = len(file_path.read_text().split('\n'))
                    timeout = calc.calculate_for_lines(lines)
                    assert timeout >= 60  # min_timeout
                    processed += 1
            except Exception as e:
                from lxml import etree
                # Only XMLSyntaxError is acceptable for malformed XML
                if isinstance(e, AttributeError):
                    errors.append((file_path, e))
                elif isinstance(e, etree.XMLSyntaxError):
                    # Expected for malformed XML - count as processed
                    processed += 1

        # Verify pipeline processed all files without AttributeError
        assert len(errors) == 0, f"Unexpected errors: {errors}"
        assert processed == len(files_to_process), \
            f"Expected {len(files_to_process)} files processed, got {processed}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
