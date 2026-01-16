"""
Settings preview component for agent configuration (US2.4).

Shows example agent responses with different settings combinations.
"""

import streamlit as st
from typing import Dict, Any, List


def get_default_preview_query() -> str:
    """Get default example query for preview."""
    return "Explain how the authentication flow works in this application"


def get_example_queries() -> List[str]:
    """Get list of example queries for preview."""
    return [
        "Explain how the authentication flow works in this application",
        "What are the main components of the payment processing system?",
        "How is the user registration process implemented?",
        "Describe the database schema for orders and customers"
    ]


def generate_preview_response(query: str, settings: Dict[str, Any]) -> str:
    """
    Generate preview response based on settings.

    This function generates mock responses that demonstrate how different
    settings affect agent output. It does NOT call actual LLM.

    Args:
        query: Preview query
        settings: Settings dictionary

    Returns:
        Mock response text showing settings effect
    """
    verbosity = settings.get("verbosity", "standard")
    technical_level = settings.get("technical_level", "senior")
    citation_style = settings.get("citation_style", "inline")
    output_format = settings.get("output_format", "markdown")

    # Generate response based on verbosity
    if verbosity == "concise":
        response = _generate_concise_response(query, technical_level)
    elif verbosity == "verbose":
        response = _generate_verbose_response(query, technical_level)
    else:  # standard
        response = _generate_standard_response(query, technical_level)

    # Add citations based on style
    if citation_style == "inline":
        response += "\n\nThe authentication is implemented in AuthenticationService.java [1] and validated by TokenValidator.java [2]."
    elif citation_style == "footnotes":
        response += "\n\n**References:**\n1. AuthenticationService.java (BackendDoc)\n2. TokenValidator.java (BackendDoc)"
    # none - no citations added

    # Format output
    if output_format == "text":
        # Remove markdown formatting for text mode
        import re
        response = re.sub(r'\*\*([^\*]+)\*\*', r'\1', response)
        response = re.sub(r'\*([^\*]+)\*', r'\1', response)
        response = re.sub(r'`([^`]+)`', r'\1', response)
        response = re.sub(r'^#+\s+', '', response, flags=re.MULTILINE)

    return response


def _generate_concise_response(query: str, technical_level: str) -> str:
    """Generate concise response (brief)."""
    if technical_level == "junior":
        return "The authentication flow uses JWT tokens. Users log in with credentials, get a token, and use it for requests. Simple and secure."
    elif technical_level == "mid":
        return "JWT-based authentication. Login endpoint validates credentials, generates token with claims, client includes token in Authorization header. Token validated on each request."
    else:  # senior
        return "Implements OAuth 2.0 with JWT bearer tokens. HMAC-SHA256 signing, 24h expiration, refresh token flow. See AuthenticationService:42."


def _generate_standard_response(query: str, technical_level: str) -> str:
    """Generate standard response (moderate detail)."""
    if technical_level == "junior":
        return """The authentication system works in a few simple steps:

1. **Login**: User sends username and password to the server
2. **Verification**: Server checks if credentials are correct
3. **Token Creation**: If correct, server creates a special token (like a digital key)
4. **Using the Token**: User includes this token with each request to prove they're logged in

The token expires after 24 hours for security. Think of it like a day pass at an amusement park - it proves you paid to get in and is only good for that day."""
    elif technical_level == "mid":
        return """The authentication flow implements a token-based approach:

**Flow Steps:**
1. Client submits credentials to `/api/auth/login`
2. Server validates credentials against database
3. Upon success, generates JWT containing user claims
4. Client stores token and includes in Authorization header
5. Server validates token on protected endpoints

**Key Components:**
- `AuthenticationService` - Handles login logic
- `TokenValidator` - Verifies token signatures
- JWT tokens with 24-hour expiration

This pattern provides stateless authentication suitable for REST APIs."""
    else:  # senior
        return """## Authentication Architecture

**Implementation Pattern**: OAuth 2.0 with JWT bearer tokens

**Authentication Flow**:
1. POST `/api/auth/login` → Credentials validation
2. Generate JWT (HMAC-SHA256) with claims: userId, roles, exp
3. Return access token (24h) + refresh token (7d)
4. Client: `Authorization: Bearer <token>` on protected endpoints
5. Middleware validates signature, expiration, blacklist

**Components**:
- `AuthenticationService.java` - Token generation, credential validation
- `JwtTokenProvider.java` - Signing/verification with secret key rotation
- `SecurityFilter.java` - Request interceptor

**Security Considerations**: Token revocation via Redis blacklist, rate limiting on auth endpoints, secure HttpOnly cookies for web clients."""


def _generate_verbose_response(query: str, technical_level: str) -> str:
    """Generate verbose response (detailed)."""
    if technical_level == "junior":
        return """Let me explain the authentication system in detail, step by step.

**What is Authentication?**
Authentication is basically the process of verifying who you are. It's like showing your ID card before entering a building.

**How It Works in This Application:**

**Step 1: Login**
When you want to log in, you type your username and password into a form. The application sends this information to a special place on the server called an "endpoint" (think of it as a specific address like "/login").

**Step 2: Checking Credentials**
The server receives your username and password and checks them against what's stored in the database. If they match, great! If not, you get an error message.

**Step 3: Creating a Token**
If your credentials are correct, the server creates something called a JWT token. Think of this like a special badge that proves you're who you say you are. This token contains information about you (like your username and what permissions you have).

**Step 4: Using the Token**
From now on, whenever you want to do something in the application (like view your profile or make a purchase), you send this token along with your request. It's like showing your badge each time you want to enter a restricted area.

**Step 5: Token Expiration**
For security reasons, this token doesn't last forever. After 24 hours, it expires and you need to log in again to get a new one. This prevents someone from using an old stolen token.

**Why This Approach?**
This method is very popular because:
- It's secure (tokens are encrypted)
- It's efficient (server doesn't need to remember every logged-in user)
- It works great for mobile apps and websites

The actual code that handles all this is in files like `AuthenticationService.java` and `TokenValidator.java`."""
    elif technical_level == "mid":
        return """## Comprehensive Authentication Flow Analysis

Let me walk you through the complete authentication implementation in this application.

### Overview
The system implements a JWT (JSON Web Token) based authentication pattern, which provides stateless, scalable authentication suitable for modern REST APIs and single-page applications.

### Detailed Flow

**1. User Initiates Login**
- User submits credentials via POST request to `/api/auth/login`
- Request body: `{ "username": "...", "password": "..." }`
- Frontend typically handles this via login form submission

**2. Server-Side Credential Validation**
- `AuthenticationController` receives the request
- Calls `AuthenticationService.validateCredentials()`
- Service queries `UserRepository` to find user by username
- Compares submitted password hash with stored hash (bcrypt algorithm)
- If invalid: Returns 401 Unauthorized with error message
- If valid: Proceeds to token generation

**3. JWT Token Generation**
- `TokenProvider.generateToken()` creates JWT with:
  - **Header**: Algorithm (HS256) and token type
  - **Payload**: User ID, username, roles, issued time, expiration time
  - **Signature**: HMAC-SHA256 signed with secret key
- Token expires in 24 hours (configurable)
- Additionally generates refresh token valid for 7 days

**4. Token Response**
- Server returns JSON response:
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIs...",
  "refreshToken": "dGhpcyBpcyByZWZyZXNo...",
  "expiresIn": 86400
}
```

**5. Client Token Storage**
- Client stores tokens (typically in localStorage or secure cookies)
- Includes access token in Authorization header: `Bearer <token>`

**6. Protected Endpoint Access**
- User makes request to protected endpoint
- `SecurityFilter` intercepts request
- Extracts token from Authorization header
- `TokenValidator.validateToken()` verifies:
  - Signature is valid (hasn't been tampered)
  - Token hasn't expired
  - Token isn't in blacklist (for logout functionality)
- If valid: Request proceeds with user context
- If invalid: Returns 401 Unauthorized

**7. Token Refresh**
- Before access token expires, client can use refresh token
- POST to `/api/auth/refresh` with refresh token
- Returns new access token without requiring login

### Security Considerations
- Passwords stored as bcrypt hashes (not plaintext)
- Tokens signed with secret key (environment variable)
- Token expiration prevents indefinite access
- HTTPS required for production (prevents token interception)
- Rate limiting on login endpoint (prevents brute force)

### Key Classes
- `AuthenticationService.java` - Core authentication logic
- `TokenProvider.java` - JWT generation and validation
- `SecurityFilter.java` - Request interception
- `UserRepository.java` - Database access

This implementation follows industry best practices and provides a secure, scalable authentication solution."""
    else:  # senior
        return """## Authentication Architecture: Deep Technical Analysis

### System Overview
Implements OAuth 2.0 Resource Owner Password Credentials Grant with JWT bearer tokens. Architecture designed for stateless, horizontally-scalable REST API authentication.

### Component Architecture

**Authentication Service Layer**
```
AuthenticationController → AuthenticationService → [UserRepository, TokenProvider]
                       ↓
                 SecurityFilter (Interceptor)
                       ↓
                 TokenValidator → [JwtParser, BlacklistCache]
```

### Implementation Details

**1. Token Generation (AuthenticationService:42-89)**
```java
public AuthToken authenticate(LoginRequest request) {
    User user = userRepository.findByUsername(request.getUsername())
        .orElseThrow(() -> new AuthenticationException("Invalid credentials"));

    if (!passwordEncoder.matches(request.getPassword(), user.getPasswordHash())) {
        throw new AuthenticationException("Invalid credentials");
    }

    Claims claims = Claims.builder()
        .subject(user.getId().toString())
        .claim("username", user.getUsername())
        .claim("roles", user.getRoles().stream()
            .map(Role::getName)
            .collect(Collectors.toList()))
        .issuedAt(new Date())
        .expiration(Date.from(Instant.now().plus(24, ChronoUnit.HOURS)))
        .build();

    String accessToken = jwtProvider.generateToken(claims);
    String refreshToken = jwtProvider.generateRefreshToken(user.getId());

    return new AuthToken(accessToken, refreshToken, 86400);
}
```

**2. JWT Structure**
- **Algorithm**: HMAC-SHA256 (symmetric signing)
- **Claims**: sub (userId), username, roles[], iat, exp
- **Secret Key**: 256-bit key from environment (key rotation every 90 days)
- **Expiration**: Access token 24h, refresh token 7d

**3. Token Validation Pipeline (SecurityFilter:31-58)**
```java
protected void doFilter(HttpServletRequest request, HttpServletResponse response, FilterChain chain) {
    String token = extractToken(request);

    if (token != null && tokenValidator.validate(token)) {
        Claims claims = jwtParser.parseClaimsJws(token).getBody();

        if (!blacklistCache.contains(token)) {
            Authentication auth = new UsernamePasswordAuthenticationToken(
                claims.getSubject(),
                null,
                extractAuthorities(claims)
            );
            SecurityContextHolder.getContext().setAuthentication(auth);
        }
    }

    chain.doFilter(request, response);
}
```

**4. Security Mechanisms**

**Token Revocation**:
- Redis-backed blacklist for logged-out tokens
- TTL matches token expiration
- O(1) lookup performance

**Rate Limiting**:
```
/api/auth/login: 5 requests/minute/IP (bucket4j)
/api/auth/refresh: 10 requests/minute/user
```

**Refresh Token Flow**:
- Opaque token (not JWT) stored in database with user association
- Single-use pattern: New refresh token issued with each access token refresh
- Automatic revocation on password change

**Key Rotation**:
- Secret key rotation every 90 days (automated via cron)
- Graceful transition with dual-key validation during rotation window
- Old tokens remain valid until expiration

### Performance Characteristics
- Token validation: <1ms (no database lookup)
- Stateless design: Horizontal scaling without session persistence
- Redis blacklist: <5ms P99 latency
- Concurrent auth throughput: 10k RPS (measured)

### Attack Mitigation
- **Brute Force**: Rate limiting + account lockout after 5 failed attempts
- **Token Theft**: Short expiration, HTTPS-only, secure cookie flags
- **Replay Attacks**: Jti (JWT ID) claim + blacklist for sensitive operations
- **CSRF**: SameSite cookie attribute + double-submit cookie pattern

### Future Enhancements
- [ ] MFA support (TOTP via authenticator apps)
- [ ] Biometric authentication for mobile
- [ ] OAuth 2.0 Authorization Code flow for third-party integrations
- [ ] WebAuthn/FIDO2 for password less authentication

### Related Components
- `JwtProvider.java:42` - Token generation
- `SecurityFilter.java:31` - Request interception
- `TokenValidator.java:18` - Signature verification
- `BlacklistService.java:27` - Token revocation
- `application.yml:security.jwt.*` - Configuration

This implementation provides enterprise-grade security while maintaining high performance and scalability."""


def render_settings_preview(settings: Dict[str, Any], query: str = None):
    """
    Render settings preview component.

    Args:
        settings: Current settings
        query: Optional custom query (uses default if not provided)
    """
    with st.expander("👁️ Preview Agent Response", expanded=False):
        # Settings summary
        st.caption(
            f"**Preview with:** {settings.get('verbosity', 'standard')} verbosity, "
            f"{settings.get('technical_level', 'senior')} level, "
            f"{settings.get('citation_style', 'inline')} citations, "
            f"{settings.get('output_format', 'markdown')} format"
        )

        # Query selector if no custom query
        if not query:
            query = st.selectbox(
                "Example Query",
                options=get_example_queries(),
                index=0,
                key="preview_query_selector"
            )

        # Generate and display preview
        preview_response = generate_preview_response(query, settings)

        st.markdown("**Example Agent Response:**")
        st.markdown(preview_response)

        st.caption("💡 This is a mock response showing how settings affect output. Actual agent responses will vary based on codebase content.")


def render_preview_query_selector() -> str:
    """
    Render preview query selector.

    Returns:
        Selected query
    """
    return st.selectbox(
        "Preview Query",
        options=get_example_queries(),
        index=0
    )
