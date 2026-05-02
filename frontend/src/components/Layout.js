import { useContext } from "react";
import { Link } from "react-router-dom";

import { AuthContext } from "../context/AuthContext";

function Layout({ children }) {
  const { user } = useContext(AuthContext);

  return (
    <div>
      <header style={{ marginBottom: "1rem" }}>
        <h2>CollabAI</h2>
        <nav style={{ fontSize: "0.95rem" }}>
          <Link to="/">Home</Link>
          {" · "}
          <Link to="/register">Register</Link>
          {user?.email && (
            <span style={{ marginLeft: "0.75rem", color: "#444" }}>
              Session: {user.email}
            </span>
          )}
        </nav>
      </header>
      {children}
    </div>
  );
}

export default Layout;
