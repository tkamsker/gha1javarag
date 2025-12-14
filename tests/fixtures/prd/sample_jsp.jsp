<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>User Registration</title>
    <style>
        .error { color: red; font-size: 0.9em; }
        .required { color: red; }
    </style>
</head>
<body>
    <h1>Create New User Account</h1>

    <c:if test="${not empty error}">
        <div class="error">${error}</div>
    </c:if>

    <form id="registrationForm" action="/api/users" method="POST" onsubmit="return validateForm()">

        <!-- Email Field -->
        <div class="form-group">
            <label for="email">Email Address: <span class="required">*</span></label>
            <input type="email"
                   id="email"
                   name="email"
                   required
                   maxlength="255"
                   pattern="^[A-Za-z0-9+_.-]+@(.+)$"
                   placeholder="user@example.com" />
            <span class="error" id="emailError"></span>
        </div>

        <!-- Password Field -->
        <div class="form-group">
            <label for="password">Password: <span class="required">*</span></label>
            <input type="password"
                   id="password"
                   name="password"
                   required
                   minlength="8"
                   maxlength="255"
                   placeholder="At least 8 characters" />
            <span class="error" id="passwordError"></span>
        </div>

        <!-- Confirm Password Field -->
        <div class="form-group">
            <label for="confirmPassword">Confirm Password: <span class="required">*</span></label>
            <input type="password"
                   id="confirmPassword"
                   name="confirmPassword"
                   required
                   minlength="8"
                   maxlength="255" />
            <span class="error" id="confirmPasswordError"></span>
        </div>

        <!-- First Name Field -->
        <div class="form-group">
            <label for="firstName">First Name:</label>
            <input type="text"
                   id="firstName"
                   name="firstName"
                   maxlength="100"
                   placeholder="John" />
        </div>

        <!-- Last Name Field -->
        <div class="form-group">
            <label for="lastName">Last Name:</label>
            <input type="text"
                   id="lastName"
                   name="lastName"
                   maxlength="100"
                   placeholder="Doe" />
        </div>

        <!-- Terms and Conditions -->
        <div class="form-group">
            <label>
                <input type="checkbox"
                       id="agreeTerms"
                       name="agreeTerms"
                       required />
                I agree to the Terms and Conditions <span class="required">*</span>
            </label>
        </div>

        <!-- Submit Buttons -->
        <div class="form-actions">
            <button type="submit">Create Account</button>
            <button type="button" onclick="window.location.href='/login'">Cancel</button>
        </div>

        <!-- CSRF Token -->
        <input type="hidden" name="csrfToken" value="${csrfToken}" />
    </form>

    <script>
        function validateForm() {
            let isValid = true;

            // Clear previous errors
            document.querySelectorAll('.error').forEach(el => el.textContent = '');

            // Validate email
            const email = document.getElementById('email').value;
            if (!email.match(/^[A-Za-z0-9+_.-]+@(.+)$/)) {
                document.getElementById('emailError').textContent = 'Invalid email format';
                isValid = false;
            }

            // Validate password
            const password = document.getElementById('password').value;
            if (password.length < 8) {
                document.getElementById('passwordError').textContent = 'Password must be at least 8 characters';
                isValid = false;
            }

            // Validate password confirmation
            const confirmPassword = document.getElementById('confirmPassword').value;
            if (password !== confirmPassword) {
                document.getElementById('confirmPasswordError').textContent = 'Passwords do not match';
                isValid = false;
            }

            return isValid;
        }

        // Real-time validation
        document.getElementById('confirmPassword').addEventListener('blur', function() {
            const password = document.getElementById('password').value;
            const confirmPassword = this.value;
            if (password && confirmPassword && password !== confirmPassword) {
                document.getElementById('confirmPasswordError').textContent = 'Passwords do not match';
            }
        });
    </script>
</body>
</html>
