import { useContext, useState } from "react";
import { Link } from "react-router-dom";

import API from "../api/api";
import { AuthContext } from "../context/AuthContext";

function formatApiError(data) {
  if (!data || typeof data !== "object") return String(data ?? "Request failed");
  const parts = [];
  for (const [key, val] of Object.entries(data)) {
    const msg = Array.isArray(val) ? val.join(" ") : String(val);
    parts.push(`${key}: ${msg}`);
  }
  return parts.join(". ") || "Request failed";
}

export default function Register() {
  const { user, setUser } = useContext(AuthContext);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    try {
      const { data } = await API.post("/auth/register", { email, password });
      setUser(data);
      setSuccess("Account created.");
    } catch (err) {
      const payload = err.response?.data;
      setError(formatApiError(payload ?? err.message));
    }
  }

  return (
    <div>
      <h2>Register</h2>
      {user?.email && (
        <p>
          Signed in as <strong>{user.email}</strong>
        </p>
      )}
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "0.5rem" }}>
          <label htmlFor="email">Email</label>
          <br />
          <input
            id="email"
            type="email"
            autoComplete="email"
            value={email}
            onChange={(ev) => setEmail(ev.target.value)}
            required
          />
        </div>
        <div style={{ marginBottom: "0.5rem" }}>
          <label htmlFor="password">Password</label>
          <br />
          <input
            id="password"
            type="password"
            autoComplete="new-password"
            value={password}
            onChange={(ev) => setPassword(ev.target.value)}
            required
          />
        </div>
        <button type="submit">Create account</button>
      </form>
      {error && (
        <p role="alert" style={{ color: "crimson", marginTop: "1rem" }}>
          {error}
        </p>
      )}
      {success && (
        <p style={{ marginTop: "1rem", color: "green" }}>
          {success}{" "}
          <Link to="/">Home</Link>
        </p>
      )}
      <p style={{ marginTop: "1rem" }}>
        <Link to="/">Back to home</Link>
      </p>
    </div>
  );
}
