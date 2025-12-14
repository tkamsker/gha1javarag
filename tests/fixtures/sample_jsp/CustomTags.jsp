<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<%@ taglib uri="http://www.springframework.org/tags" prefix="spring" %>
<%@ taglib uri="/WEB-INF/custom.tld" prefix="custom" %>
<!DOCTYPE html>
<html>
<head>
    <title>Custom Tags</title>
</head>
<body>
    <h1>Custom Tags Example</h1>

    <c:forEach items="${users}" var="user">
        <div class="user">
            <c:out value="${user.name}"/>
            <custom:userBadge user="${user}"/>
        </div>
    </c:forEach>

    <fmt:formatDate value="${now}" pattern="yyyy-MM-dd"/>

    <spring:message code="welcome.message"/>
</body>
</html>
