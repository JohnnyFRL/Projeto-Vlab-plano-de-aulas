import { Outlet, NavLink, useNavigate } from "react-router-dom";
import styles from "./Layout.module.css";

export default function Layout() {
  const navigate = useNavigate();

  return (
    <div className={styles.root}>
      <aside className={styles.sidebar}>
        <div className={styles.brand}>
          <span className={styles.brandIcon}>◈</span>
          <span className={styles.brandName}>Vlab</span>
        </div>

        <nav className={styles.nav}>
          <NavLink
            to="/planos"
            className={({ isActive }) =>
              `${styles.navItem} ${isActive ? styles.active : ""}`
            }
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="3" width="7" height="7" rx="1" />
              <rect x="14" y="3" width="7" height="7" rx="1" />
              <rect x="3" y="14" width="7" height="7" rx="1" />
              <rect x="14" y="14" width="7" height="7" rx="1" />
            </svg>
            Planos de Aula
          </NavLink>
        </nav>

        <button
          className={styles.newBtn}
          onClick={() => navigate("/planos/novo")}
        >
          + Novo Plano
        </button>
      </aside>

      <main className={styles.main}>
        <Outlet />
      </main>
    </div>
  );
}
