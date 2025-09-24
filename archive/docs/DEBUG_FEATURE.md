# Debug Feature Documentation

## Overview

The debug feature allows you to process specific files instead of entire directories, making it ideal for:
- Testing the analysis pipeline with a small set of files
- Debugging issues with specific files
- Processing only relevant files for faster iteration
- Enhanced metadata extraction with pom.xml analysis

## Features

### 🔍 Selective File Processing
- Process only files listed in a debug file
- Skip entire directory scanning
- Faster processing for targeted analysis

### 📦 Enhanced pom.xml Analysis
- Automatically find and analyze pom.xml files in each directory
- Extract project information, dependencies, and build configuration
- AI-powered analysis of project architecture and technology stack

### 🎯 Improved Metadata
- Enhanced file statistics and debug information
- Priority-based processing (files with pom.xml analysis first)
- More detailed AI analysis with debug insights

### 🔧 Debug Mode Enhancements
- Smaller batch sizes for more detailed processing
- More permissive file filtering
- Enhanced logging and error reporting
- Debug-specific output files

## Configuration

### 1. Environment Variable Setup

Add the `DEBUGFILE` variable to your `.env` file:

```bash
# Debug Configuration
# Set to full path of file containing list of files to process in debug mode
# One file path per line, empty or commented out to disable debug mode
DEBUGFILE=/path/to/your/debug_files.txt
```

### 2. Debug File Format

Create a text file with the following format:

```txt
# Debug Files List
# One file path per line, full absolute paths
# Lines starting with # are comments and will be ignored

/path/to/your/project/src/main/java/com/example/Controller.java
/path/to/your/project/src/main/java/com/example/Service.java
/path/to/your/project/src/main/webapp/index.jsp
/path/to/your/project/src/main/resources/application.properties
```

### 3. File Path Requirements

- Use **absolute paths** for all files
- One file path per line
- Supported file types: `.java`, `.jsp`, `.xml`, `.html`, `.js`, `.sql`
- Files must exist and be readable

## Usage

### Step 1: File Processing and AI Analysis

```bash
# Debug mode will be automatically detected
./Step1.sh test
```

**What happens:**
- Reads files from `DEBUGFILE`
- Finds and analyzes pom.xml files in each directory
- Processes files with enhanced metadata
- Saves results to `debug_metadata.json`

### Step 2: Requirements Generation

```bash
# Debug mode will be automatically detected
./Step2.sh test
```

**What happens:**
- Loads debug metadata from Step 1
- Generates enhanced requirements documentation
- Creates `step2_debug_index.md` with debug information
- Includes pom.xml analysis in requirements

### Step 3: Modern Requirements

```bash
# Debug mode will be automatically detected
./Step3.sh test
```

**What happens:**
- Processes requirements with debug enhancements
- Generates `modern_requirements_debug.md` (production) or `modern_requirements_debug_test.md` (test)
- Includes debug insights and recommendations
- Uses test mode optimizations when `./Step3.sh test` is used

## Output Files

### Debug Mode Outputs

| File | Description |
|------|-------------|
| `debug_metadata.json` | Enhanced metadata with pom.xml analysis |
| `step2_debug_index.md` | Requirements index with debug information |
| `modern_requirements_debug.md` | Modern requirements with debug insights (production) |
| `modern_requirements_debug_test.md` | Modern requirements with debug insights (test mode) |

### pom.xml Analysis

Each processed file includes pom.xml analysis with:

```json
{
  "pom_analysis": {
    "pom_path": "/path/to/pom.xml",
    "project_info": {
      "groupId": "com.example",
      "artifactId": "my-project",
      "version": "1.0.0"
    },
    "dependencies": [...],
    "build_info": {...},
    "properties": {...},
    "ai_analysis": {
      "project_type": "web application",
      "technology_stack": ["Spring Boot", "Hibernate"],
      "architecture_patterns": ["MVC", "Repository"],
      "deployment_target": "application server",
      "key_features": [...],
      "integration_points": [...],
      "security_considerations": [...],
      "performance_characteristics": "...",
      "scalability_aspects": "..."
    }
  }
}
```

## Enhanced AI Analysis

Debug mode provides more detailed AI analysis including:

### File Analysis
- **Purpose and Overview**: Detailed description of file purpose
- **Key Components**: Enhanced component analysis with complexity ratings
- **Data Structures**: Usage patterns and relationships
- **Business Rules**: Priority-based business logic extraction
- **Integration Points**: Detailed integration analysis
- **Security Considerations**: Security-focused analysis
- **Performance Notes**: Performance optimization insights
- **Debug Insights**: Code quality and improvement suggestions

### Debug Insights
- Code quality assessment
- Potential issues identification
- Improvement suggestions
- Architecture recommendations
- Debug and monitoring considerations

## Rate Limiting

Debug mode uses more conservative rate limiting:
- **Smaller batch sizes**: 2 files per batch (vs 3 in normal mode)
- **Longer delays**: 6 seconds between requests (vs 4-5 in normal mode)
- **Fewer requests per hour**: 600 (vs 800 in normal mode)

## Error Handling

### Debug File Issues
- Missing debug file: Falls back to normal processing
- Invalid file paths: Logged as warnings, processing continues
- Unsupported file types: Logged as warnings, skipped

### pom.xml Analysis Issues
- Missing pom.xml: Processing continues without pom analysis
- Invalid XML: Error logged, basic metadata extracted
- AI analysis failure: Basic pom.xml parsing continues

## Examples

### Example 1: Basic Debug Setup

1. Create debug file:
```txt
/Users/me/project/src/main/java/com/example/UserController.java
/Users/me/project/src/main/java/com/example/UserService.java
```

2. Set environment variable:
```bash
DEBUGFILE=/Users/me/debug_files.txt
```

3. Run processing:
```bash
./Step1.sh test
./Step2.sh test
./Step3.sh test
```

### Example 2: With pom.xml Analysis

The system will automatically:
1. Find pom.xml in `/Users/me/project/`
2. Analyze project structure and dependencies
3. Include AI-powered architecture analysis
4. Enhance metadata with project context

### Example 3: Debug Output

Generated requirements will include:
```markdown
# Requirements Analysis: UserController.java

**File Path:** `src/main/java/com/example/UserController.java`
**Debug Mode:** Enabled
**Debug Source:** /Users/me/debug_files.txt

## POM.xml Analysis

**Project Type:** Web Application
**Technology Stack:** Spring Boot, Spring MVC, Hibernate
**Architecture Patterns:** MVC, REST API

## Key Components

1. **UserController** (Complexity: Medium)
   - REST API endpoints for user management
   - Input validation and error handling
   - Integration with UserService

## Debug Insights

- **Code Quality:** Good, follows Spring conventions
- **Potential Issues:** Missing input validation for some endpoints
- **Improvement Suggestions:** Add comprehensive error handling
```

## Troubleshooting

### Common Issues

1. **Debug mode not detected**
   - Check `DEBUGFILE` path in `.env`
   - Ensure debug file exists and is readable
   - Verify file paths in debug file are absolute

2. **Files not found**
   - Verify absolute paths in debug file
   - Check file permissions
   - Ensure files are in supported formats

3. **pom.xml not found**
   - System searches parent directories automatically
   - Check if pom.xml exists in project root
   - Verify XML syntax in pom.xml

4. **AI analysis failures**
   - Check API key configuration
   - Verify rate limiting settings
   - Review error logs for specific issues

### Debug Logs

Enable detailed logging by setting:
```bash
LOG_LEVEL=DEBUG
```

Debug logs will show:
- File processing progress
- pom.xml discovery and analysis
- AI analysis attempts and results
- Error details and fallback behavior

## Best Practices

1. **Start Small**: Begin with 2-3 files for testing
2. **Use Absolute Paths**: Ensure all paths are complete and correct
3. **Include pom.xml**: Place files in directories with pom.xml for enhanced analysis
4. **Monitor Logs**: Check logs for processing status and errors
5. **Iterate**: Use debug mode for rapid iteration and testing

## Migration from Normal Mode

To migrate from normal processing to debug mode:

1. **Identify Key Files**: Select the most important files for analysis
2. **Create Debug File**: List selected files with absolute paths
3. **Set Environment**: Add `DEBUGFILE` to `.env`
4. **Test**: Run with debug mode to verify processing
5. **Scale**: Gradually add more files as needed

## Performance Considerations

- **Faster Processing**: Debug mode processes fewer files, so it's faster
- **Enhanced Analysis**: More detailed analysis per file
- **Memory Usage**: Lower memory usage due to smaller file sets
- **API Costs**: Potentially higher per-file costs due to enhanced analysis 