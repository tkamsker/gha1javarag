import os

# Test directories
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(TEST_DIR, 'data')
TEST_XML_DIR = os.path.join(TEST_DATA_DIR, 'xml')
TEST_DB_DIR = os.path.join(TEST_DATA_DIR, 'chroma_db')

# Test data
SAMPLE_XML = """
<doxygen>
    <compounddef kind="class" id="classTest">
        <compoundname>Test</compoundname>
        <memberdef kind="function" id="test_1">
            <name>testFunction</name>
            <definition>void testFunction()</definition>
            <argsstring>()</argsstring>
            <detaileddescription>Test function</detaileddescription>
        </memberdef>
    </compounddef>
</doxygen>
"""

# Test artifacts
SAMPLE_ARTIFACT = {
    'id': 'test1',
    'name': 'testFunction',
    'definition': 'void testFunction()',
    'doc': 'Test function',
    'description': 'Test function',
    'class': 'Test'
}

# Test cluster
SAMPLE_CLUSTER = [
    {
        'name': 'calculateTotal',
        'definition': 'double calculateTotal(double price, int quantity)',
        'doc': 'Calculates total price',
        'description': 'Calculates total price'
    },
    {
        'name': 'calculateDiscount',
        'definition': 'double calculateDiscount(double total, double rate)',
        'doc': 'Calculates discount amount',
        'description': 'Calculates discount amount'
    }
]

# Test settings
TEST_SETTINGS = {
    'n_clusters': 2,
    'embedding_dim': 384,  # all-MiniLM-L6-v2 dimension
    'collection_name': 'test_collection'
}

def setup_test_environment():
    """Create necessary test directories"""
    os.makedirs(TEST_XML_DIR, exist_ok=True)
    os.makedirs(TEST_DB_DIR, exist_ok=True)

def cleanup_test_environment():
    """Remove test directories"""
    import shutil
    shutil.rmtree(TEST_DATA_DIR, ignore_errors=True) 