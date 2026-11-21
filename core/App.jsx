// App.jsx
import { createBrowserRouter, Outlet } from "react-router";
import { RouterProvider } from "react-router/dom";

import HeroSection from "./pages/landing/HeroSection";
import Login from "./pages/authentication/Login";
import Register from "./pages/authentication/Register";

import "./App.css";

function LandingPage() {
  return (
    <HeroSection
      title="DarkOps Security Platform"
      subtitle={{
        regular: "Security for the systems ",
        gradient: "you entrust.",
      }}
      description="Monitor security activity, investigate incidents, and maintain visibility across the applications and systems connected to DarkOps."
      loginHref="/login"
      signupHref="/signup"
      gridOptions={{
        angle: 65,
        opacity: 0.35,
        cellSize: 50,
        lightLineColor: "#8A8580",
        darkLineColor: "#8A8580",
      }}
    />
  );
}

function PlaceholderPage({ title }) {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[#1A1A1A] px-6 text-white">
      <div className="text-center">
        <h1
          className="text-4xl"
          style={{ fontFamily: "Foldit, sans-serif" }}
        >
          {title}
        </h1>

        <p
          className="mt-3 text-sm text-[#8A8580]"
          style={{ fontFamily: "Montserrat Alternates, sans-serif" }}
        >
          This DarkOps page is under construction.
        </p>
      </div>
    </main>
  );
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <Outlet />,
    children: [
      // Landing
      {
        index: true,
        element: <LandingPage />,
      },

      // Authentication
      {
        path: "login",
        element: <Login />,
      },
      {
        path: "signup",
        element: <Register />,
      },
      {
        path: "forgot-question",
        element: <PlaceholderPage title="Forgot Question" />,
      },
      {
        path: "verify",
        element: <PlaceholderPage title="Verify Account" />,
      },
      {
        path: "security-question",
        element: <PlaceholderPage title="Security Question" />,
      },
      {
        path: "forgot-password",
        element: <PlaceholderPage title="Forgot Password" />,
      },
      {
        path: "reset-password",
        element: <PlaceholderPage title="Reset Password" />,
      },
      {
        path: "reset-question",
        element: <PlaceholderPage title="Reset Question" />,
      },

      // Homepage
      {
        path: "dashboard",
        element: <PlaceholderPage title="Command Center" />,
      },
      {
        path: "profile",
        element: <PlaceholderPage title="Profile" />,
      },
      {
        path: "help-center",
        element: <PlaceholderPage title="Help Center" />,
      },
      {
        path: "pwn-test",
        element: <PlaceholderPage title="Pwn Test" />,
      },

      // Applications
      {
        path: "applications",
        element: <PlaceholderPage title="Applications" />,
      },

      // Security
      {
        path: "security/policies",
        element: <PlaceholderPage title="Security Policies" />,
      },
      {
        path: "security/threat-detection",
        element: <PlaceholderPage title="Threat Detection" />,
      },
      {
        path: "security/team",
        element: <PlaceholderPage title="Security Team" />,
      },
      {
        path: "security/settings",
        element: <PlaceholderPage title="Security Settings" />,
      },

      // Events
      {
        path: "events",
        element: <PlaceholderPage title="Events" />,
      },
      {
        path: "events/incidents",
        element: <PlaceholderPage title="Incidents" />,
      },
      {
        path: "events/alerts",
        element: <PlaceholderPage title="Alerts" />,
      },
      {
        path: "events/vulnerabilities",
        element: <PlaceholderPage title="Vulnerabilities" />,
      },
      {
        path: "events/notifications",
        element: <PlaceholderPage title="Notifications" />,
      },

      // Audit Logs
      {
        path: "audit-logs",
        element: <PlaceholderPage title="Audit Logs" />,
      },
      {
        path: "audit-logs/unread",
        element: <PlaceholderPage title="Unread" />,
      },
      {
        path: "audit-logs/recents",
        element: <PlaceholderPage title="Recent Audit Logs" />,
      },
      {
        path: "audit-logs/trash",
        element: <PlaceholderPage title="Trash" />,
      },
      {
        path: "audit-logs/scheduled",
        element: <PlaceholderPage title="Scheduled" />,
      },
      {
        path: "audit-logs/library",
        element: <PlaceholderPage title="Audit Library" />,
      },
      {
        path: "audit-logs/compose",
        element: <PlaceholderPage title="Compose Audit Log" />,
      },

      // Extensions
      {
        path: "extensions",
        element: <PlaceholderPage title="Extensions" />,
      },

      // Demo
      {
        path: "demo",
        element: <PlaceholderPage title="Demo Environment" />,
      },
    ],
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
