import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children, allowedRoles }) => {
  const loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));

  if (!loggedInUser) {
    // Not logged in, redirect to login page
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(loggedInUser.role)) {
    // Logged in but unauthorized role, redirect to a suitable page (e.g., user dashboard for admin trying to access user, or vice versa)
    // For simplicity, let's redirect to login for now, or a generic unauthorized page
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;