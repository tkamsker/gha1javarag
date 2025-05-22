from tree_sitter import Language, Parser
import os

def build_grammar():
    # Create build directory if it doesn't exist
    os.makedirs('build', exist_ok=True)
    
    # Build the Java grammar
    Language.build_library(
        'build/java.so',
        ['vendor/tree-sitter-java']
    )
    
    # Test the grammar with a sample Java file
    JAVA_LANGUAGE = Language('build/java.so', 'java')
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    
    # Sample Java code to test
    java_code = """
    public class TestClass {
        private String name;
        
        public TestClass(String name) {
            this.name = name;
        }
        
        public String getName() {
            return name;
        }
    }
    """
    
    # Parse the code
    tree = parser.parse(bytes(java_code, 'utf8'))
    
    # Print the AST
    print("AST Structure:")
    print(tree.root_node.sexp())

if __name__ == "__main__":
    build_grammar() 