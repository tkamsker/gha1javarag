<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.util.Date" %>
<%@ page import="java.util.List" %>
<!DOCTYPE html>
<html>
<head>
    <title>JSP Scriptlets Example</title>
</head>
<body>
    <h1>Current Time</h1>

    <%-- Declaration --%>
    <%!
        private String formatDate(Date date) {
            return date.toString();
        }

        private int counter = 0;
    %>

    <%-- Scriptlet --%>
    <%
        Date now = new Date();
        String formatted = formatDate(now);
        counter++;
    %>

    <%-- Expression --%>
    <p>Current time: <%= formatted %></p>
    <p>Page views: <%= counter %></p>

    <%-- Java code with logic --%>
    <%
        String message;
        if (counter > 10) {
            message = "Popular page!";
        } else {
            message = "New page.";
        }
    %>

    <p>Status: <%= message %></p>
</body>
</html>
