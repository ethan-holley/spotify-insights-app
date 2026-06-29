import { NavLink, useNavigate } from "react-router-dom";
import { auth } from "../lib/auth";

export default function Nav() {
  const navigate = useNavigate();

  const logout = () => {
    auth.clearToken();
    navigate("/");
  };

  return (
    <nav className="nav">
      <NavLink to="/" className="nav-logo">Spotify Insights</NavLink>
      <div className="nav-links">
        <NavLink to="/dashboard" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
          Stats
        </NavLink>
        <NavLink to="/wrapped" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
          Wrapped
        </NavLink>
        <button onClick={logout} className="nav-logout">Log out</button>
      </div>
    </nav>
  );
}
