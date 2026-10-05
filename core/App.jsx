import { createBrowserRouter, Outlet } from "react-router";
import { RouterProvider } from "react-router/dom";

import HeroSection from "./components/HeroSection";
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
    <main className="min-h-screen bg-[#1A1A1A] text-white p-10">
      <h1 className="text-4xl font-semibold">{title}</h1>
      <p className="mt-4 text-[#8A8580]">
        This DarkOps module is under construction.
      </p>
    </main>
  );
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <Outlet />,
    children: [
      {
        index: true,
        element: <LandingPage />,
      },

      {
        path: "login",
        element: <PlaceholderPage title="Log In" />,
      },
      {
        path: "signup",
        element: <PlaceholderPage title="Sign Up" />,
      },

      // Core DarkOps modules
      {
        path: "dashboard",
        element: <PlaceholderPage title="Command Center" />,
      },
      {
        path: "security-posture",
        element: <PlaceholderPage title="Security Posture" />,
      },
      {
        path: "applications",
        element: <PlaceholderPage title="Applications" />,
      },
      {
        path: "assets",
        element: <PlaceholderPage title="Assets" />,
      },
      {
        path: "events",
        element: <PlaceholderPage title="Events" />,
      },
      {
        path: "alerts",
        element: <PlaceholderPage title="Alerts" />,
      },
      {
        path: "incidents",
        element: <PlaceholderPage title="Incidents" />,
      },
      {
        path: "vulnerabilities",
        element: <PlaceholderPage title="Vulnerabilities" />,
      },
      {
        path: "intelligence",
        element: <PlaceholderPage title="Threat Intelligence" />,
      },
      {
        path: "audit-logs",
        element: <PlaceholderPage title="Audit Logs" />,
      },
      {
        path: "organization",
        element: <PlaceholderPage title="Organization" />,
      },
      {
        path: "team",
        element: <PlaceholderPage title="Team & Roles" />,
      },
      {
        path: "integrations",
        element: <PlaceholderPage title="Integrations" />,
      },
      {
        path: "settings",
        element: <PlaceholderPage title="Settings" />,
      },
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