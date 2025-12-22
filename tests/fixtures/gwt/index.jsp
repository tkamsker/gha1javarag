<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.util.Date" %>
<%@ page import="com.example.service.ConfigService" %>
<%@ include file="/WEB-INF/includes/header.jsp" %>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>GWT Application - JSP Entry Point</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <%-- GWT module declarations --%>
    <script type="text/javascript" language="javascript">
        var contextPath = '<%= request.getContextPath() %>';
        var serverTime = '<%= new Date() %>';
    </script>

    <%-- Main GWT application module --%>
    <script type="text/javascript" language="javascript"
            src="<%= request.getContextPath() %>/app/app.nocache.js"></script>

    <%-- Admin GWT module (conditional loading) --%>
    <%
        String userRole = (String) session.getAttribute("userRole");
        if ("ADMIN".equals(userRole)) {
    %>
        <script type="text/javascript" language="javascript"
                src="<%= request.getContextPath() %>/admin/admin.nocache.js"></script>
    <%
        }
    %>

    <%-- Reports module --%>
    <script type="text/javascript" language="javascript"
            src="${pageContext.request.contextPath}/reports/reports.nocache.js"></script>

    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        #loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <noscript>
        <div style="color: red; padding: 20px; text-align: center;">
            Your web browser must have JavaScript enabled in order for this application to display correctly.
        </div>
    </noscript>

    <div id="loading">
        <div class="spinner"></div>
        <p>Loading application...</p>
    </div>

    <%-- GWT history frame --%>
    <iframe src="javascript:''" id="__gwt_historyFrame" tabIndex='-1'
            style="position:absolute;width:0;height:0;border:0"></iframe>

    <%-- Main application container --%>
    <div id="gwtAppContainer"></div>

    <%-- Additional module loaded via JSP variable --%>
    <%
        String customModule = ConfigService.getCustomModule();
        if (customModule != null) {
            out.println("<script type='text/javascript' language='javascript' src='" +
                       request.getContextPath() + "/" + customModule + "/" + customModule + ".nocache.js'></script>");
        }
    %>

    <%@ include file="/WEB-INF/includes/footer.jsp" %>
</body>
</html>
