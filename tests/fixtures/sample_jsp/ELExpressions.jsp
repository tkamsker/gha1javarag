<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<!DOCTYPE html>
<html>
<head>
    <title>EL Expressions</title>
</head>
<body>
    <h1>Expression Language Examples</h1>

    <!-- Simple property access -->
    <p>Username: ${user.username}</p>
    <p>Email: ${user.email}</p>

    <!-- Nested properties -->
    <p>City: ${user.address.city}</p>

    <!-- Collection access -->
    <p>First item: ${items[0]}</p>
    <p>Named item: ${map['key']}</p>

    <!-- Operators -->
    <p>Sum: ${a + b}</p>
    <p>Condition: ${age >= 18 ? 'Adult' : 'Minor'}</p>

    <!-- Null-safe access -->
    <p>Optional: ${empty optionalValue ? 'N/A' : optionalValue}</p>

    <!-- Method calls -->
    <p>Upper: ${user.getName().toUpperCase()}</p>

    <!-- Request parameters -->
    <p>Param: ${param.id}</p>
    <p>Header: ${header['User-Agent']}</p>
</body>
</html>
