import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { auth } from "./lib/auth";
import Nav from "./components/Nav";
import Home from "./pages/Home";
import Callback from "./pages/Callback";
import Dashboard from "./pages/Dashboard";
import Wrapped from "./pages/Wrapped";
import "./styles.css";

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  if (!auth.isLoggedIn()) return <Navigate to="/" replace />;
  return <>{children}</>;
}

export default function App() {
  return (
    <BrowserRouter>
      <Nav />
      <main className="main">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/callback" element={<Callback />} />

          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          <Route
            path="/wrapped"
            element={
              <ProtectedRoute>
                <Wrapped />
              </ProtectedRoute>
            }
          />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}