#!/usr/bin/env python3
"""
Test script for Enhanced Component Classification
Tests the new LLM-based content analysis system
"""

import sys
import json
import tempfile
from pathlib import Path
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def setup_test_environment():
    """Set up test environment with sample files"""
    test_dir = Path(tempfile.mkdtemp())
    
    # Create sample Java files
    samples = {
        # DAO Example
        'UserRepository.java': '''package com.example.dao;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import com.example.entity.User;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    User findByEmail(String email);
    List<User> findByActiveTrue();
}''',

        # DTO Example  
        'UserDto.java': '''package com.example.dto;

import javax.persistence.Entity;
import javax.persistence.Table;
import javax.persistence.Id;
import javax.persistence.GeneratedValue;

@Entity
@Table(name = "users")
public class UserDto {
    @Id
    @GeneratedValue
    private Long id;
    
    private String email;
    private String name;
    
    // Getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}''',

        # Service Example
        'UserService.java': '''package com.example.service;

import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;
import com.example.dao.UserRepository;

@Service
@Transactional
public class UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    public User createUser(UserDto userDto) {
        // Business logic for user creation
        if (userDto.getEmail() == null) {
            throw new IllegalArgumentException("Email cannot be null");
        }
        
        User user = new User();
        user.setEmail(userDto.getEmail());
        user.setName(userDto.getName());
        
        return userRepository.save(user);
    }
    
    @Transactional(readOnly = true)
    public List<User> getActiveUsers() {
        return userRepository.findByActiveTrue();
    }
}''',

        # Controller Example
        'UserController.java': '''package com.example.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;
import com.example.service.UserService;

@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @Autowired
    private UserService userService;
    
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody UserDto userDto) {
        User user = userService.createUser(userDto);
        return ResponseEntity.ok(user);
    }
    
    @GetMapping("/active")
    public ResponseEntity<List<User>> getActiveUsers() {
        List<User> users = userService.getActiveUsers();
        return ResponseEntity.ok(users);
    }
}''',

        # Configuration file (should be classified as config, not DAO)
        'application.properties': '''spring.datasource.url=jdbc:mysql://localhost:3306/testdb
spring.datasource.username=root
spring.datasource.password=password
spring.jpa.hibernate.ddl-auto=update''',

        # Build file (should be excluded or classified as build)
        'pom.xml': '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>test-project</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
</project>''',

        # JSP Frontend
        'user-form.jsp': '''<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>User Registration</title>
</head>
<body>
    <form action="/users" method="post" id="userForm">
        <div>
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>
        <div>
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
        </div>
        <button type="submit">Register</button>
    </form>
    
    <script>
        document.getElementById('userForm').addEventListener('submit', function(e) {
            // Basic validation
            const email = document.getElementById('email').value;
            if (!email.includes('@')) {
                alert('Please enter a valid email');
                e.preventDefault();
            }
        });
    </script>
</body>
</html>''',

        # JavaScript
        'user-validation.js': '''// User form validation and AJAX handling
class UserValidator {
    static validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    static validateForm(formData) {
        const errors = [];
        
        if (!this.validateEmail(formData.email)) {
            errors.push('Invalid email format');
        }
        
        if (!formData.name || formData.name.trim().length < 2) {
            errors.push('Name must be at least 2 characters');
        }
        
        return errors;
    }
    
    static async submitUser(userData) {
        try {
            const response = await fetch('/api/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });
            
            if (response.ok) {
                return await response.json();
            } else {
                throw new Error('Failed to create user');
            }
        } catch (error) {
            console.error('Error creating user:', error);
            throw error;
        }
    }
}'''
    }
    
    # Write sample files
    for filename, content in samples.items():
        file_path = test_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return test_dir, samples

def create_mock_config(test_dir):
    """Create mock configuration for testing"""
    class MockConfig:
        def __init__(self, test_dir):
            self.java_source_dir = str(test_dir)
            self.output_dir = str(test_dir / 'output')
            self.parallel_processing = False
            self.ai_provider = 'openai'  # Assuming OpenAI for testing
            self.openai_api_key = 'test-key'
            self.openai_model_name = 'gpt-3.5-turbo'
    
    return MockConfig(test_dir)

def create_mock_project_data(test_dir, samples):
    """Create mock project data structure"""
    file_list = []
    
    for filename in samples.keys():
        file_info = {
            'path': filename,
            'language': 'java' if filename.endswith('.java') else 'other',
            'size_bytes': len(samples[filename]),
            'enhanced_ai_analysis': {}  # Empty for testing
        }
        file_list.append(file_info)
    
    return {
        'file_list': file_list,
        'project_name': 'test-project'
    }

def test_content_analyzer():
    """Test the ContentAnalyzer class"""
    print("🧪 Testing ContentAnalyzer...")
    
    # Set up test environment
    test_dir, samples = setup_test_environment()
    config = create_mock_config(test_dir)
    
    # Mock LLM client
    class MockLLMClient:
        def generate_text(self, prompt, max_tokens=500):
            # Mock responses based on content analysis
            # Check what type of file content is in the prompt
            
            if 'UserController' in prompt:
                return '''```json
{
  "component_type": "controller",
  "confidence": 0.96,
  "purpose": "REST API controller for user operations",
  "business_logic": "HTTP request handling and response formatting",
  "api_endpoints": ["/api/users POST", "/api/users/active GET"],
  "dependencies": ["UserService"],
  "annotations": ["@RestController", "@RequestMapping", "@PostMapping", "@GetMapping"],
  "key_methods": ["createUser", "getActiveUsers"]
}
```'''
            elif 'UserService' in prompt:
                return '''```json
{
  "component_type": "service",
  "confidence": 0.97,
  "purpose": "User business logic service layer",
  "business_logic": "User creation, validation, and active user retrieval",
  "api_endpoints": [],
  "dependencies": ["UserRepository"],
  "annotations": ["@Service", "@Transactional", "@Autowired"],
  "key_methods": ["createUser", "getActiveUsers"]
}
```'''
            elif 'UserRepository' in prompt:
                return '''```json
{
  "component_type": "dao",
  "confidence": 0.95,
  "purpose": "User data access repository with JPA methods",
  "business_logic": "User data persistence and retrieval",
  "api_endpoints": [],
  "dependencies": ["JpaRepository", "User entity"],
  "annotations": ["@Repository"],
  "key_methods": ["findByEmail", "findByActiveTrue"]
}
```'''
            elif 'UserDto' in prompt:
                return '''```json
{
  "component_type": "dto",
  "confidence": 0.93,
  "purpose": "User entity data transfer object",
  "business_logic": "none",
  "api_endpoints": [],
  "dependencies": [],
  "annotations": ["@Entity", "@Table"],
  "key_methods": ["getId", "setId", "getEmail", "setEmail"]
}
```'''
            elif 'pom.xml' in prompt:
                return '''```json
{
  "component_type": "build_script",
  "confidence": 0.98,
  "purpose": "Maven build configuration file",
  "business_logic": "",
  "api_endpoints": [],
  "dependencies": [],
  "annotations": [],
  "key_methods": []
}
```'''
            elif 'user-form.jsp' in prompt:
                return '''```json
{
  "component_type": "frontend_view",
  "confidence": 0.88,
  "purpose": "User registration form page",
  "business_logic": "Form validation and submission",
  "api_endpoints": ["/users POST"],
  "dependencies": ["user-validation.js"],
  "annotations": [],
  "key_methods": ["form validation", "submit handler"]
}
```'''
            elif 'user-validation.js' in prompt:
                return '''```json
{
  "component_type": "frontend_script",
  "confidence": 0.91,
  "purpose": "User form validation and API communication",
  "business_logic": "Client-side validation and AJAX user creation",
  "api_endpoints": ["/api/users POST"],
  "dependencies": ["fetch API"],
  "annotations": [],
  "key_methods": ["validateEmail", "validateForm", "submitUser"]
}
```'''
            elif 'application.properties' in prompt:
                return '''```json
{
  "component_type": "configuration",
  "confidence": 0.90,
  "purpose": "Application configuration properties",
  "business_logic": "",
  "api_endpoints": [],
  "dependencies": [],
  "annotations": [],
  "key_methods": []
}
```'''
            else:
                return '''```json
{
  "component_type": "unknown",
  "confidence": 0.5,
  "purpose": "Unknown file type",
  "business_logic": "",
  "api_endpoints": [],
  "dependencies": [],
  "annotations": [],
  "key_methods": []
}
```'''
    
    # Test ContentAnalyzer
    try:
        from src.content_analyzer import ContentAnalyzer
        analyzer = ContentAnalyzer(MockLLMClient(), logging.getLogger())
    except ImportError as e:
        print(f"  ❌ Could not import ContentAnalyzer: {e}")
        return False
    
    test_results = {}
    
    # Test each sample file
    for filename, content in samples.items():
        file_path = str(test_dir / filename)
        analysis = analyzer.analyze_file_content(file_path, content)
        
        test_results[filename] = {
            'component_type': analysis.component_type.value,
            'confidence': analysis.confidence,
            'purpose': analysis.purpose
        }
        
        print(f"  📄 {filename}: {analysis.component_type.value} (confidence: {analysis.confidence:.2f})")
    
    # Validate results
    expected_classifications = {
        'UserRepository.java': 'dao',
        'UserDto.java': 'dto', 
        'UserService.java': 'service',
        'UserController.java': 'controller',
        'pom.xml': 'build_script',
        'application.properties': 'configuration',
        'user-form.jsp': 'frontend_view',
        'user-validation.js': 'frontend_script'
    }
    
    correct_classifications = 0
    for filename, expected_type in expected_classifications.items():
        actual_type = test_results.get(filename, {}).get('component_type')
        if actual_type == expected_type:
            correct_classifications += 1
            print(f"  ✅ {filename}: Correctly classified as {expected_type}")
        else:
            print(f"  ❌ {filename}: Expected {expected_type}, got {actual_type}")
    
    accuracy = correct_classifications / len(expected_classifications)
    print(f"\n📊 Classification Accuracy: {accuracy:.1%} ({correct_classifications}/{len(expected_classifications)})")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    
    return accuracy >= 0.8  # 80% accuracy threshold

def test_enhanced_classifier():
    """Test the EnhancedComponentClassifier"""
    print("\n🧪 Testing EnhancedComponentClassifier...")
    
    # Set up test environment
    test_dir, samples = setup_test_environment()
    config = create_mock_config(test_dir)
    project_data = create_mock_project_data(test_dir, samples)
    
    # Mock LLM client (same as above)
    class MockLLMClient:
        def generate_text(self, prompt, max_tokens=500):
            # Simplified mock - return DAO for Repository, Service for Service, etc.
            if '@Repository' in prompt or 'Repository' in prompt:
                return '{"component_type": "dao", "confidence": 0.95, "purpose": "Data access", "business_logic": "", "api_endpoints": [], "dependencies": [], "annotations": ["@Repository"], "key_methods": []}'
            elif '@Service' in prompt or 'Service' in prompt:
                return '{"component_type": "service", "confidence": 0.95, "purpose": "Business logic", "business_logic": "User operations", "api_endpoints": [], "dependencies": [], "annotations": ["@Service"], "key_methods": []}'
            elif '@RestController' in prompt or 'Controller' in prompt:
                return '{"component_type": "controller", "confidence": 0.95, "purpose": "REST API", "business_logic": "", "api_endpoints": ["/api/users"], "dependencies": [], "annotations": ["@RestController"], "key_methods": []}'
            elif '@Entity' in prompt or 'Dto' in prompt:
                return '{"component_type": "dto", "confidence": 0.90, "purpose": "Data transfer", "business_logic": "", "api_endpoints": [], "dependencies": [], "annotations": ["@Entity"], "key_methods": []}'
            elif 'pom.xml' in prompt:
                return '{"component_type": "build_script", "confidence": 0.98, "purpose": "Build config", "business_logic": "", "api_endpoints": [], "dependencies": [], "annotations": [], "key_methods": []}'
            elif '.jsp' in prompt:
                return '{"component_type": "frontend_view", "confidence": 0.85, "purpose": "User form", "business_logic": "", "api_endpoints": [], "dependencies": [], "annotations": [], "key_methods": []}'
            elif '.js' in prompt:
                return '{"component_type": "frontend_script", "confidence": 0.88, "purpose": "Form validation", "business_logic": "Client validation", "api_endpoints": [], "dependencies": [], "annotations": [], "key_methods": []}'
            else:
                return '{"component_type": "configuration", "confidence": 0.80, "purpose": "Configuration", "business_logic": "", "api_endpoints": [], "dependencies": [], "annotations": [], "key_methods": []}'
    
    try:
        from src.enhanced_component_classifier import EnhancedComponentClassifier
        
        classifier = EnhancedComponentClassifier(
            config=config,
            llm_client=MockLLMClient(),
            logger=logging.getLogger()
        )
        
        # Test classification
        result = classifier.classify_project_components(project_data)
        
        # Print results
        print("  📊 Classification Results:")
        for component_type, components in result.items():
            if component_type != 'statistics' and components:
                print(f"    {component_type.upper()}: {len(components)} components")
                for comp in components[:3]:  # Show first 3
                    print(f"      - {comp['file_path']} (confidence: {comp['confidence']:.2f})")
        
        # Validate no XML files classified as DAO
        dao_components = result.get('dao', [])
        xml_in_dao = [comp for comp in dao_components if comp['file_path'].endswith('.xml')]
        
        if xml_in_dao:
            print(f"  ❌ Found {len(xml_in_dao)} XML files incorrectly classified as DAO")
            return False
        else:
            print("  ✅ No XML files incorrectly classified as DAO")
        
        # Check quality metrics
        stats = result.get('statistics', {})
        total_components = stats.get('files_analyzed', 0)
        avg_confidence = 0.0
        
        # Calculate average confidence
        all_components = []
        for comp_type, components in result.items():
            if comp_type != 'statistics':
                all_components.extend(components)
        
        if all_components:
            avg_confidence = sum(comp['confidence'] for comp in all_components) / len(all_components)
        
        print(f"  📈 Quality Metrics:")
        print(f"    Total components: {total_components}")
        print(f"    Average confidence: {avg_confidence:.2f}")
        
        # Cleanup
        import shutil
        shutil.rmtree(test_dir)
        
        return avg_confidence >= 0.8
        
    except ImportError as e:
        print(f"  ❌ Could not import enhanced classifier: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Enhanced Component Classification System")
    print("=" * 60)
    
    # Set up logging
    logging.basicConfig(level=logging.ERROR)  # Suppress most logs during testing
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: Content Analyzer
    try:
        if test_content_analyzer():
            tests_passed += 1
            print("✅ ContentAnalyzer test passed")
        else:
            print("❌ ContentAnalyzer test failed")
    except Exception as e:
        print(f"❌ ContentAnalyzer test error: {e}")
    
    # Test 2: Enhanced Classifier
    try:
        if test_enhanced_classifier():
            tests_passed += 1
            print("✅ EnhancedComponentClassifier test passed")
        else:
            print("❌ EnhancedComponentClassifier test failed")
    except Exception as e:
        print(f"❌ EnhancedComponentClassifier test error: {e}")
    
    print("\n" + "=" * 60)
    print(f"🎯 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Enhanced classification system is ready.")
        print("\n📋 Next Steps:")
        print("1. Run: ./step3-pgm.sh --enhanced --parallel")
        print("2. Compare results with: ./step3-pgm.sh --pattern-based")
        print("3. Review quality reports in output directory")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the implementation.")
        return 1

if __name__ == '__main__':
    sys.exit(main())