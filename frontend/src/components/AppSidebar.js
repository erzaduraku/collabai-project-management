import { useCallback, useContext, useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

import { AuthContext } from "../context/AuthContext";
import { useOrganization } from "../context/OrganizationContext";

const STORAGE_KEY = "collabai-sidebar-collapsed";

// Shto pas: import { AuthContext } from "../context/AuthContext";
// (importi ekziston tashmë — shto vetëm komponentin UserChip para export default)

function UserChip() {
  const { user } = useContext(AuthContext);
  if (!user) return null;

  const displayName =
    [user.first_name, user.last_name].filter(Boolean).join(" ") ||
    user.username ||
    user.email ||
    "User";

  const initials = displayName
    .split(" ")
    .map((w) => w[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <div className="sidebar-user-chip">
      <div className="sidebar-user-avatar">{initials}</div>
      <div className="sidebar-user-info">
        <span className="sidebar-user-name">{displayName}</span>
        <span className="sidebar-user-email">{user.email}</span>
      </div>
    </div>
  );
}

function HamburgerIcon() {
  return (
    <span className="dashboard-sidebar-burger" aria-hidden>
      <span className="dashboard-sidebar-burger-line" />
      <span className="dashboard-sidebar-burger-line" />
      <span className="dashboard-sidebar-burger-line" />
    </span>
  );
}

export default function AppSidebar({ onNavigateSection }) {
  const { logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const { pathname } = useLocation();

  const {
    organizations,
    activeOrganization,
    changeOrganization,
    loadingOrganizations,
  } = useOrganization();

  const [collapsed, setCollapsed] = useState(() => {
    try {
      return window.localStorage.getItem(STORAGE_KEY) === "1";
    } catch {
      return false;
    }
  });

  useEffect(() => {
    try {
      window.localStorage.setItem(STORAGE_KEY, collapsed ? "1" : "0");
    } catch {}

    document.documentElement.dataset.sidebarCollapsed = collapsed ? "1" : "0";

    return () => {
      delete document.documentElement.dataset.sidebarCollapsed;
    };
  }, [collapsed]);

  const toggle = useCallback(() => {
    setCollapsed((c) => !c);
  }, []);

  const isDashboard = pathname === "/dashboard";
  const isProjects = pathname === "/projects";
  const isOrganizations = pathname === "/organizations";
  const isInvitations = pathname === "/invitations";
  const isSettings = pathname.startsWith("/settings");
  const isAI = pathname === "/ai";

  const navClass = (active) =>
    `dashboard-nav-item${active ? " dashboard-nav-item--active" : ""}`;

  const linkStyle = { textDecoration: "none", display: "block" };

  const renderSectionLink = (section, label, dataCy) => {
    const className = navClass(false);

    if (isDashboard && typeof onNavigateSection === "function") {
      return (
        <button
          className={className}
          data-cy={dataCy}
          type="button"
          onClick={() => onNavigateSection(section)}
        >
          {label}
        </button>
      );
    }

    return (
      <Link
        className={className}
        data-cy={dataCy}
        to="/dashboard"
        state={{ scrollTo: section }}
        style={linkStyle}
      >
        {label}
      </Link>
    );
  };

  const handleOrganizationChange = (event) => {
    const selected = organizations.find(
      (org) => String(org.id) === String(event.target.value)
    );

    if (selected) {
      changeOrganization(selected);
    }
  };

  return (
    <aside
      className={`dashboard-sidebar${collapsed ? " dashboard-sidebar--collapsed" : ""}`}
      aria-label="Main navigation"
    >
      <div className="dashboard-sidebar-inner">
        <div className="dashboard-sidebar-top">
          <button
            type="button"
            className="dashboard-sidebar-toggle"
            onClick={toggle}
            aria-expanded={!collapsed}
            aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
            title={collapsed ? "Expand menu" : "Collapse menu"}
          >
            <HamburgerIcon />
          </button>

          {!collapsed ? (
            <>
              <div className="dashboard-brand">
                <div className="dashboard-brand-mark">C</div>
                <div>
                  <h1 className="dashboard-brand-title">CollabAI</h1>
                  <p className="dashboard-brand-subtitle">Project intelligence hub</p>
                </div>
              </div>

              <div style={styles.orgSwitcher}>
                <label style={styles.orgLabel}>Organization</label>

                <select
                  style={styles.orgSelect}
                  value={activeOrganization?.id || ""}
                  disabled={loadingOrganizations || organizations.length === 0}
                  onChange={handleOrganizationChange}
                >
                  {organizations.length === 0 ? (
                    <option value="">No organizations</option>
                  ) : (
                    organizations.map((org) => (
                      <option key={org.id} value={org.id}>
                        {org.name}
                      </option>
                    ))
                  )}
                </select>
              </div>

              <nav className="dashboard-nav dashboard-sidebar-nav" aria-label="App sections">
                <Link
                  className={navClass(isDashboard)}
                  data-cy="dashboard-nav-overview"
                  to="/dashboard"
                  style={linkStyle}
                >
                  Overview
                </Link>

                <Link
                  className={navClass(isProjects)}
                  data-cy="dashboard-nav-projects"
                  to="/projects"
                  style={linkStyle}
                >
                  Projects
                </Link>

                <Link
                  className={navClass(isOrganizations)}
                  to="/organizations"
                  style={linkStyle}
                >
                  Organizations
                </Link>

                <Link
                  className={navClass(isInvitations)}
                  to="/invitations"
                  style={linkStyle}
                >
                  Invitations
                </Link>

                <Link
                  className={navClass(isSettings)}
                  to="/settings/profile"
                  style={linkStyle}
                >
                  Settings
                </Link>

                {renderSectionLink("tasks", "Tasks", "dashboard-nav-tasks")}
                {renderSectionLink("activity", "Activity", "dashboard-nav-activity")}

                <Link
                  className={navClass(isAI)}
                  data-cy="dashboard-nav-ai"
                  to="/ai"
                  style={linkStyle}
                >
                  AI Assistant
                </Link>

              </nav>
            </>
          ) : null}
        </div>

        {!collapsed ? (
<div className="dashboard-sidebar-footer">
  <UserChip />
  <button
    className="dashboard-button dashboard-button--ghost"
    data-cy="dashboard-logout"
    type="button"
    onClick={() => {
      logout();
      navigate("/login");
    }}
  >
    Logout
  </button>
</div>
        ) : null}
      </div>
    </aside>
  );
}

const styles = {
  orgSwitcher: {
    margin: "14px 0",
    padding: "10px",
    borderRadius: "12px",
    background: "rgba(255, 255, 255, 0.06)",
  },
  orgLabel: {
    display: "block",
    fontSize: "11px",
    color: "#94a3b8",
    marginBottom: "6px",
    textTransform: "uppercase",
    letterSpacing: "0.04em",
    fontWeight: 700,
  },
  orgSelect: {
    width: "100%",
    border: "1px solid rgba(148, 163, 184, 0.35)",
    borderRadius: "10px",
    padding: "9px 10px",
    background: "#111827",
    color: "#ffffff",
    fontSize: "13px",
    outline: "none",
  },
};
